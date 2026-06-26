"""
监控主入口 - 编排采集→去重→输出的流程
"""

import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
CONFIG_DIR = SKILL_DIR / "config"

sys.path.insert(0, str(SCRIPT_DIR))

from fetcher import fetch_all, Article
from dedup import filter_new, check_quota, load_state


DEFAULT_CONFIG = CONFIG_DIR / "sources.json"
TEMPLATE_CONFIG = CONFIG_DIR / "sources_template.json"


def load_sources():
    """加载用户配置的信息源"""
    if DEFAULT_CONFIG.exists():
        with open(DEFAULT_CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)
    
    if TEMPLATE_CONFIG.exists():
        with open(TEMPLATE_CONFIG, "r", encoding="utf-8") as f:
            sources = json.load(f)
        enabled = [s for s in sources if s.get("enabled", True)]
        print("[INFO] 使用默认模板，已启用 {} 个信息源".format(len(enabled)))
        return enabled
    
    print("[ERROR] 未找到配置文件，请先运行 python setup.py")
    return []


def get_proxy():
    """从环境变量获取代理设置"""
    return os.environ.get("INFO_MONITOR_PROXY", "")


def run_monitor(keywords=None, dry_run=False):
    """执行一次完整的监控循环
    
    Args:
        keywords: list of str, 关键词过滤（可选）
        dry_run: bool, 是否只采集不输出摘要
    
    Returns:
        dict: 统计结果
    """
    quota = check_quota()
    if not quota["allowed"]:
        print("""
⚠️ 免费次数已用完（今日已用 {used}/3 次）

需要更多次数？
💎 专业版：¥29.9 一次性 → 无限次使用 + 无限信息源

获取授权码请联系作者，或运行：
  python scripts/license.py activate YOUR-KEY
""".format(**quota))
        return {"status": "quota_exceeded", **quota}
    
    print("=" * 50)
    print("📡 信息源监控助手 — 开始执行")
    print("套餐: {} | 剩余次数: {}".format(quota["plan"].upper(), quota["remaining"]))
    print("=" * 50)
    
    sources = load_sources()
    if not sources:
        return {"status": "no_sources", "articles": []}
    
    proxy = get_proxy()
    articles = fetch_all(sources, proxy=proxy)
    
    new_articles, filtered_count = filter_new(articles)
    
    if keywords:
        kw_lower = [k.lower() for k in keywords]
        new_articles = [
            a for a in new_articles
            if any(k in a.title.lower() or k in a.content.lower() for k in kw_lower)
        ]
    
    result = {
        "status": "ok",
        "total_fetched": len(articles),
        "new_articles": len(new_articles),
        "filtered_duplicates": filtered_count,
        "filtered_keywords": len(articles) - len(new_articles) - filtered_count if keywords else 0,
        "articles": [a.to_dict() for a in new_articles],
        "plan": quota["plan"],
        "remaining": quota["remaining"]
    }
    
    print("\n--- 结果 ---")
    print("共采集: {} 篇 | 新文章: {} 篇 | 去重: {} 篇".format(
        result["total_fetched"],
        result["new_articles"],
        result["filtered_duplicates"]
    ))
    
    for i, a in enumerate(new_articles[:10], 1):
        print("  {}. [{}] {}".format(i, a.source_name, a.title))
    
    if len(new_articles) > 10:
        print("  ... 还有 {} 篇".format(len(new_articles) - 10))
    
    return result


if __name__ == "__main__":
    keywords = sys.argv[1:] if len(sys.argv) > 1 else None
    result = run_monitor(keywords=keywords)
    
    if result.get("status") == "ok" and result["new_articles"] > 0:
        print("\n✅ 发现 {} 篇新文章！可继续用 summarizer.py 生成AI摘要".format(result["new_articles"]))
