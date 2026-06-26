#!/usr/bin/env python3
"""
GEO Monitor - 完整报告生成模块
整合搜索+评分+分析，生成完整GEO报告
"""

import asyncio
import sys
import json
import time
import subprocess
from pathlib import Path
import importlib.util

# 动态导入geo_quota模块
import geo_quota

# 动态导入geo_searcher模块（因为文件名有连字符）
spec = importlib.util.spec_from_file_location(
    "geo_searcher",
    Path(__file__).parent / "geo_searcher.py"
)
geo_searcher_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(geo_searcher_module)
GeoSearcher = geo_searcher_module.GeoSearcher

# 动态导入geo_analyzer模块
spec2 = importlib.util.spec_from_file_location(
    "geo_analyzer",
    Path(__file__).parent / "geo_analyzer.py"
)
geo_analyzer_module = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(geo_analyzer_module)
GeoAnalyzer = geo_analyzer_module.GeoAnalyzer


def push_to_feishu(content: str, webhook_url: str = None) -> bool:
    """推送报告到飞书"""
    if not webhook_url:
        config_path = Path(__file__).parent.parent / "config.json"
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
                webhook_url = config.get("report", {}).get("feishu_webhook")

    if not webhook_url:
        print("未配置飞书Webhook，跳过推送")
        return False

    try:
        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {"tag": "plain_text", "content": "GEO可见性检测报告"},
                    "template": "purple"
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {"tag": "lark_md", "content": content[:4000]}
                    },
                    {
                        "tag": "note",
                        "elements": [
                            {"tag": "plain_text", "content": "生成时间: " + time.strftime("%Y-%m-%d %H:%M:%S")}
                        ]
                    }
                ]
            }
        }

        cmd = [
            "curl", "-s", "-X", "POST",
            webhook_url,
            "-H", "Content-Type: application/json",
            "-d", json.dumps(payload)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        resp = json.loads(result.stdout)

        if resp.get("code") == 0 or resp.get("StatusCode") == 0:
            print("报告已推送到飞书")
            return True
        else:
            print("推送失败: " + str(resp))
            return False

    except Exception as e:
        print("推送异常: " + str(e))
        return False


async def run_full_scan(keywords: list, config_path: str = None, push: bool = True) -> dict:
    """运行完整GEO检测流程"""
    # 默认使用skill目录下的config.json
    if config_path is None:
        config_path = str(Path(__file__).parent.parent / "config.json")

    # Step 0: 配额检查（免费版限制）
    allowed, err_msg, enabled_platforms = geo_quota.check_quota(keywords)
    if not allowed:
        print("\n" + "=" * 50)
        print("❌ 配额不足")
        print("=" * 50)
        print(err_msg)
        return {"error": err_msg}

    print("=" * 50)
    print("GEO Monitor - 完整检测流程")
    print("=" * 50)
    print(f"配置: {config_path}")
    geo_quota.show_quota_status()

    # Step 1: 搜索
    print("\n[1/4] 正在搜索AI平台...")
    searcher = GeoSearcher(keywords, config_path, enabled_platforms=enabled_platforms)
    results = await searcher.search_all()

    # Step 2: 评分
    print("\n[2/4] 正在计算GEM评分...")
    score_data = searcher.calculate_gem_score()

    # Step 3: 生成报告
    print("\n[3/4] 正在生成报告...")
    report = searcher.format_report()

    # Step 4: AI分析（仅对第一个品牌）
    print("\n[4/4] 正在AI分析...")
    analyzer = GeoAnalyzer(keywords[0], results, score_data["score"])
    ai_analysis = analyzer.analyze()

    # 合并报告
    full_report = report + "\n\n" + ai_analysis

    # 保存报告
    timestamp = int(time.time())
    report_file = "/tmp/geo_report_full_%d.md" % timestamp
    with open(report_file, "w") as f:
        f.write(full_report)

    print("\n报告已保存: " + report_file)
    print("GEM评分: %d/100 %s" % (score_data["score"], score_data["grade"]))

    # 推送到飞书
    if push:
        push_to_feishu(full_report)

    # Step 5: 记录配额使用（免费版）
    geo_quota.record_usage(keywords, enabled_platforms or [])

    return {
        "keywords": keywords,
        "score": score_data,
        "results": results,
        "report": full_report,
        "report_file": report_file,
    }


def main():
    """命令行入口"""
    keywords = [kw for kw in sys.argv[1:] if not kw.startswith("--")]
    push = "--no-push" not in sys.argv

    if "--status" in sys.argv:
        geo_quota.show_quota_status()
        return

    if "--upgrade-pro" in sys.argv:
        geo_quota.upgrade_to_pro()
        return

    if "--upgrade-ent" in sys.argv:
        geo_quota.upgrade_to_enterprise()
        return

    if not keywords:
        print("""
GEO Monitor - 品牌AI可见性检测

用法:
  python geo_report.py <品牌名> [品牌B] [品牌C] [--no-push]
  python geo_report.py --status        # 查看配额状态
  python geo_report.py --upgrade-pro   # 升级到专业版
  python geo_report.py --upgrade-ent   # 升级到企业版

示例:
  python geo_report.py 提分引擎AI
  python geo_report.py 提分引擎AI 药常记 --no-push
        """)
        sys.exit(1)

    asyncio.run(run_full_scan(keywords, push=push))


if __name__ == "__main__":
    main()
