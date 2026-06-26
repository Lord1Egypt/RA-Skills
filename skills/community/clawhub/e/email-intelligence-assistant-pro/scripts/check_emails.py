#!/usr/bin/env python3
"""
邮件客服助手 - 检查新邮件主脚本
功能：IMAP读取 → AI分类 → 回复建议 → 飞书推送
"""

import sys
import json
import argparse
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from typing import Optional

# 导入本地模块
sys.path.insert(0, __file__.rsplit('/', 1)[0] if '/' in __file__ else '.')
from imap_client import IMAPClient
from classifier import EmailClassifier
from reply_generator import ReplyGenerator
from feishu_pusher import FeishuPusher


# ── 91Skillhub Token Verification ─────────────────────────────────────────────
#
# 重要：已迁移到 skills-developer/shared/token_validator.py
# 本地保留此模块以确保独立运行能力
#
VERIFY_URL = "https://geo-api.yk-global.com/validate"  # 修正：正确的验证接口

# Tier 映射（与 yk global 前缀规范一致）
TIER_MAP = {
    "FREE":  "FREE",
    "BSC":   "BASIC",
    "STD":   "STANDARD",
    "PRO":   "PRO",
    "ENT":   "ENTERPRISE",
    "MAX":   "MAX",
}

# 已知 91Skillhub 前缀
VALID_PREFIXES = {
    "GEO", "PROFIT", "INV", "DATA", "MON",
    "PDF", "BANK", "CONTRACT", "EMAIL", "CONV",
    "RPT", "SENTIMENT",
}

def _get_cached(key: str) -> dict:
    """读取本地缓存（5分钟TTL）"""
    import time
    cache_dir = Path.home() / ".email_assistant_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"{key[:8].replace('/', '_')}.json"
    if not cache_file.exists():
        return None
    try:
        with open(cache_file) as f:
            data = json.load(f)
        if time.time() - data.get("_ts", 0) > 300:
            return None
        return data
    except Exception:
        return None


def _set_cached(key: str, data: dict) -> None:
    """写入本地缓存"""
    import time
    cache_dir = Path.home() / ".email_assistant_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"{key[:8].replace('/', '_')}.json"
    try:
        data["_ts"] = time.time()
        with open(cache_file, "w") as f:
            json.dump(data, f)
    except Exception:
        pass


def _map_prefix_to_tier(api_key: str) -> str:
    """根据 API key 前缀推断套餐级别。"""
    if not api_key:
        return "FREE"
    upper = api_key.upper()
    if "ENT" in upper:
        return "ENTERPRISE"
    if "MAX" in upper:
        return "MAX"
    if "PRO" in upper:
        return "PRO"
    if "STD" in upper:
        return "STANDARD"
    if "BSC" in upper:
        return "BASIC"
    if "FREE" in upper:
        return "FREE"
    return "FREE"


def verify_token(api_key: str) -> dict:
    """
    验证 API key via geo-api.yk-global.com。

    降级策略：
    1. 无 key → FREE
    2. key 不属于 91Skillhub 体系 → FREE
    3. 网络错误 → FREE（不阻断使用）
    4. 验证失败 → FREE
    5. 验证成功 → 对应 tier

    缓存：结果缓存 5 分钟。
    """
    if not api_key:
        return {"valid": False, "tier": "FREE", "error": "No API key"}

    # 快速判断：不在已知前缀列表 = 外部 key，跳过验证
    prefix = api_key.split("-")[0].upper() if "-" in api_key else api_key[:4].upper()
    if prefix not in VALID_PREFIXES:
        return {"valid": False, "tier": "FREE", "error": "Not a 91Skillhub key"}

    # 缓存查询
    cached = _get_cached(api_key)
    if cached:
        return cached

    try:
        req = urllib.request.Request(
            VERIFY_URL,
            method="POST",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            data=b"{}",  # POST body required
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            # 修正：使用 valid 字段
            if data.get("valid", False):
                tier = _map_prefix_to_tier(api_key)
                result = {"valid": True, "tier": tier, "prefix": data.get("prefix", ""),
                           "plan_id": data.get("plan_id"), "quota_remaining": data.get("quota_remaining")}
            else:
                result = {"valid": False, "tier": "FREE",
                           "error": data.get("error", "Invalid or expired key")}
            _set_cached(api_key, result)
            return result
    except urllib.error.HTTPError as e:
        try:
            err_body = json.loads(e.read().decode("utf-8"))
            err_msg = err_body.get("error", f"HTTP {e.code}")
        except Exception:
            err_msg = f"HTTP {e.code}"
        result = {"valid": False, "tier": "FREE", "error": err_msg}
        _set_cached(api_key, result)
        return result
    except Exception as e:
        # 网络异常 → FREE，不阻断使用
        return {"valid": False, "tier": "FREE", "error": f"Network error: {e}"}


class EmailAssistant:
    """邮件客服助手主类"""

    def __init__(self, config: dict, api_key: str = ""):
        self.config = config
        # ── Tier 推断优先级 ──────────────────────────────────────────
        # 1. 优先用显式传入的 key 进行验证
        # 2. 其次用 OPENAI_API_KEY 环境变量
        # 3. 最终降级到 config 里的 tier
        import os
        key = api_key or os.environ.get("OPENAI_API_KEY", "")
        if key:
            result = verify_token(key)
            if result["valid"]:
                self.tier = result["tier"]
                print(f"[INFO] Token verified: valid=True, tier={self.tier}")
            else:
                self.tier = "FREE"
                print(f"[WARN] Token invalid ({result['error']}), using FREE tier")
        else:
            self.tier = config.get("tier", "FREE")
            print(f"[INFO] No API key, using tier={self.tier}")
        self.imap_client = IMAPClient(config.get('imap', {}))
        self.classifier = EmailClassifier(config.get('ai', {}))
        self.reply_gen = ReplyGenerator(config.get('ai', {}))
        self.pusher = FeishuPusher(config.get('feishu', {}))

    def process_emails(self, limit: int = 10) -> list:
        """
        检查并处理邮件

        Args:
            limit: 最多处理邮件数

        Returns:
            处理结果列表
        """
        # 连接邮箱
        if not self.imap_client.connect():
            return [{'error': '连接邮箱失败'}]

        try:
            # 获取最新邮件
            emails = self.imap_client.fetch_unread(limit=limit)
            if not emails:
                return []

            results = []
            for email in emails:
                # AI分类
                category = self.classifier.classify(email)
                email['category'] = category

                # 生成回复建议
                reply_suggestion = self.reply_gen.generate(email)
                email['reply_suggestion'] = reply_suggestion

                results.append(email)

            # 推送飞书
            if results and self.config.get('feishu', {}).get('enabled'):
                self.pusher.push_summary(results)

            return results

        finally:
            self.imap_client.disconnect()

    def generate_report(self, results: list) -> str:
        """生成处理报告"""
        if not results:
            return "✅ 没有新邮件"

        report = ["📧 邮件处理报告", "=" * 30, ""]

        categories = {}
        for r in results:
            cat = r.get('category', '🟢 可延后')
            categories[cat] = categories.get(cat, 0) + 1

        report.append(f"总计: {len(results)} 封")
        report.append("")
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            report.append(f"  {cat}: {count} 封")

        report.append("")
        report.append("-" * 30)

        for i, r in enumerate(results, 1):
            cat = r.get('category', '🟢 可延后')
            subject = r.get('subject', '(无主题)')[:50]
            from_ = r.get('from', '未知发件人')
            snippet = r.get('snippet', '')[:100]

            report.append(f"\n{i}. {cat}")
            report.append(f"   主题: {subject}")
            report.append(f"   发件人: {from_}")
            if snippet:
                report.append(f"   摘要: {snippet}...")

        return "\n".join(report)


def load_config(config_path: str = 'config/config.yaml') -> dict:
    """加载配置文件"""
    try:
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except ImportError:
        # 如果没有yaml，使用json配置
        json_path = config_path.replace('.yaml', '.json').replace('config/', 'config/')
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}


def main():
    parser = argparse.ArgumentParser(description='邮件客服助手')
    parser.add_argument('--config', '-c', default='config/config.yaml', help='配置文件路径')
    parser.add_argument('--limit', '-l', type=int, default=10, help='处理邮件数量上限')
    parser.add_argument('--api-key', default='', help='91Skillhub API key for automatic tier verification')
    parser.add_argument('--json', '-j', action='store_true', help='JSON格式输出')
    parser.add_argument('--dry-run', action='store_true', help='仅检查不推送')

    args = parser.parse_args()

    config = load_config(args.config)
    assistant = EmailAssistant(config, api_key=args.api_key)

    results = assistant.process_emails(limit=args.limit)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(assistant.generate_report(results))

    # 如果是紧急邮件，打印回复建议
    urgent = [r for r in results if '🔴' in r.get('category', '')]
    if urgent:
        print("\n" + "=" * 30)
        print("⚠️  紧急邮件回复建议")
        print("=" * 30)
        for r in urgent:
            print(f"\n主题: {r.get('subject')}")
            print(f"建议回复:\n{r.get('reply_suggestion', '暂无建议')}")
            print("-" * 20)


if __name__ == '__main__':
    main()
