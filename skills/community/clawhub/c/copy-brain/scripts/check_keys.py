"""检测三个数据源的 API Key 配置情况（读取系统环境变量，不发起任何网络请求）。

用法：python scripts/check_keys.py
输出每个服务是否已配置，并给出未配置项的申请地址。
"""
from __future__ import annotations

import os

# 触发 common.py 的 UTF-8 控制台修复
import common  # noqa: F401

SERVICES = [
    ("TAVILY_API_KEY", "Tavily（搜索海外/英文内容）", "https://app.tavily.com"),
    ("SCRAPEBADGER_API_KEY", "ScrapeBadger（X/Twitter 内容）", "https://scrapebadger.com/dashboard"),
    ("REDFOX_API_KEY", "RedFox（小红书 / 公众号文章）", "https://redfox.hk/dashboard/keys"),
]


def main() -> None:
    configured = 0
    print("API Key 配置检测：\n")
    for env_name, label, url in SERVICES:
        ok = bool(os.environ.get(env_name, "").strip())
        configured += ok
        mark = "[已配置]" if ok else "[未配置]"
        print(f"  {mark}  {label}  [{env_name}]")
        if not ok:
            print(f"           申请：{url}")
    print(f"\n共 {configured}/{len(SERVICES)} 个服务已配置。")
    if configured == 0:
        print("提示：可仅用 Cursor 内置联网搜索继续，但覆盖面较窄；推荐至少配置 Tavily。")


if __name__ == "__main__":
    main()
