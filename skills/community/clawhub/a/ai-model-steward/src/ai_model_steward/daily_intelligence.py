"""
AI Model Steward - 每日情报搜集模块

功能:
1. 从各数据源抓取最新模型资讯
2. 提取免费 tokens 领取信息
3. 存储到本地缓存和飞书多维表格
"""

import json
import time
import re
from datetime import datetime, timezone
from typing import Optional, List, Dict
from pathlib import Path

try:
    import requests
except ImportError:
    print("错误: 需要 requests 库。安装命令: pip install requests")
    import sys
    sys.exit(1)

# 缓存目录
CACHE_DIR = Path.home() / ".openclaw" / ".ai-model-steward"
CACHE_DIR.mkdir(exist_ok=True)
DAILY_CACHE_FILE = CACHE_DIR / "daily_intelligence.json"


class DataSource:
    """数据源基类"""
    def __init__(self, name: str, url: str, source_type: str):
        self.name = name
        self.url = url
        self.source_type = source_type  # 'api', 'webpage', 'rss'
    
    def fetch(self) -> list:
        raise NotImplementedError


class OpenRouterAPI(DataSource):
    """OpenRouter 模型列表 API"""
    
    def __init__(self, api_key: str):
        super().__init__(
            name="OpenRouter Models",
            url="https://openrouter.ai/api/v1/models",
            source_type="api"
        )
        self.api_key = api_key
    
    def fetch(self) -> list:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ai-model-steward.local",
            "X-Title": "AI Model Steward"
        }
        try:
            resp = requests.get(self.url, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            models = data.get("data", [])
            results = []
            for m in models:
                pricing = m.get("pricing", {})
                is_free = all(float(v) == 0 for v in pricing.values()) if pricing else False
                results.append({
                    "source": self.name,
                    "type": "new_model" if is_free else "model_info",
                    "title": m.get("name", "Unknown"),
                    "model_id": m.get("id", ""),
                    "description": m.get("description", "")[:300],
                    "context_length": m.get("context_length", 0),
                    "pricing": pricing,
                    "is_free": is_free,
                    "url": self.url,
                    "fetched_at": datetime.now(timezone.utc).isoformat(),
                })
            return results
        except Exception as e:
            return [{"source": self.name, "error": str(e), "fetched_at": datetime.now().isoformat()}]


class ModelNewsScraper(DataSource):
    """AI 模型新闻抓取"""
    
    def __init__(self, name: str, url: str):
        super().__init__(name, url, "webpage")
    
    def fetch(self) -> list:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.4 Safari/605.1.15"
            }
            resp = requests.get(self.url, headers=headers, timeout=30)
            resp.raise_for_status()
            
            # 简单关键词提取
            content = resp.text[:50000]
            model_keywords = [
                'qwen3', 'gpt', 'claude', 'gemini', 
                'deepseek', 'llama', 'minimax', 'moonshot',
                'kimi', '通义', '文心', '混元',
                'glm', 'stepfun', 'nvidia', 'nemotron'
            ]
            free_keywords = ['免费', '免费额度', 'free', '免费tokens', '0.00', '限时免费']
            
            findings = []
            for kw in model_keywords:
                if kw.lower() in content.lower():
                    context = self._extract_context(content.lower(), kw.lower())
                    is_free = any(fk in content.lower() for fk in free_keywords)
                    findings.append({
                        "source": self.name,
                        "type": "free_tokens" if is_free else "model_news",
                        "title": f"发现 {kw} 相关资讯",
                        "model_keywords": [kw],
                        "context_preview": context,
                        "is_free_related": is_free,
                        "url": self.url,
                        "fetched_at": datetime.now().isoformat(),
                    })
            return findings
        except Exception as e:
            return [{"source": self.name, "error": str(e), "fetched_at": datetime.now().isoformat()}]
    
    def _extract_context(self, text: str, keyword: str, length: int = 200) -> str:
        idx = text.find(keyword)
        if idx == -1:
            return ""
        start = max(0, idx - 100)
        end = min(len(text), idx + length)
        return text[start:end]


def get_api_key_from_config():
    """从 OpenClaw 配置获取 OpenRouter API Key"""
    config_path = Path.home() / ".openclaw" / "openclaw.json"
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text())
            key = config.get("env", {}).get("OPENROUTER_API_KEY", "")
            return key or None
        except Exception:
            pass
    return None


def daily_intelligence() -> dict:
    """
    执行每日情报搜集
    返回: { status, items_count, items }
    """
    print("=" * 50)
    print("🔍 AI 模型智能管家 - 每日情报搜集")
    print(f"⏰ 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    api_key = get_api_key_from_config()
    if not api_key:
        api_key = input("请输入 OpenRouter API Key (回车跳过): ").strip() or None
    
    sources = [
        OpenRouterAPI(api_key) if api_key else None,
        ModelNewsScraper("机器之心", "https://www.jiqizhixin.com/"),
        ModelNewsScraper("量子位", "https://www.qbitai.com/"),
        ModelNewsScraper("HuggingFace Blog", "https://huggingface.co/blog"),
        ModelNewsScraper("36Kr AI", "https://36kr.com/information/AI/"),
    ]
    sources = [s for s in sources if s is not None]
    
    all_items = []
    for source in sources:
        print(f"\n📡 抓取 {source.name} ...")
        items = source.fetch() if source else []
        print(f"   找到 {len(items)} 条信息")
        all_items.extend(items)
        time.sleep(1)  # 礼貌延迟
    
    # 加载历史数据并去重
    history = []
    if DAILY_CACHE_FILE.exists():
        try:
            history = json.loads(DAILY_CACHE_FILE.read_text())
        except Exception:
            pass
    
    # 去重：基于 model_id + title 组合
    seen = {f"{h.get('model_id', '')}_{h.get('title', '')}" for h in history if h.get("title")}
    new_items = []
    for item in all_items:
        key = f"{item.get('model_id', '')}_{item.get('title', '')}"
        if key not in seen:
            new_items.append(item)
            seen.add(key)
    
    merged = history[-500:] + new_items  # 保留最近 500 条
    DAILY_CACHE_FILE.write_text(json.dumps(merged, indent=2, ensure_ascii=False))
    
    print(f"\n{'='*50}")
    print(f"✅ 今日新增 {len(new_items)} 条情报")
    print(f"📊 历史总计 {len(merged)} 条情报")
    print(f"{'='*50}")
    
    # 打印摘要
    free_count = sum(1 for i in new_items if i.get("is_free") or i.get("is_free_related"))
    news_count = sum(1 for i in new_items if i.get("type") == "model_news")
    if free_count:
        print(f"\n🎁 发现 {free_count} 条免费/free tokens 相关消息")
    if news_count:
        print(f"📰 发现 {news_count} 条新模型新闻")
    
    return {
        "status": "success",
        "new_items": len(new_items),
        "total_items": len(merged),
        "free_related": free_count,
        "news_count": news_count,
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AI 模型智能管家 - 每日情报")
    parser.add_argument("--save-bitable", action="store_true", help="保存到飞书多维表格")
    parser.add_argument("--app-token", help="飞书多维表格 token")
    parser.add_argument("--table-id", help="飞书多维表格 table_id")
    args = parser.parse_args()
    
    result = daily_intelligence()
    
    if args.save_bitable and args.app_token and args.table_id:
        print("\n📋 正在保存到飞书多维表格...")
        # 延迟导入，避免依赖
        from ai_model_steward.bitable_writer import save_to_bitable
        save_to_bitable(result, args.app_token, args.table_id)
