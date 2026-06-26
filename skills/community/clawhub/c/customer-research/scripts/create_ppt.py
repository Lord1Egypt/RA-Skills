#!/usr/bin/env python3
"""
⚠️ 此脚本已废弃 - 请使用 create_scenario_ppt.py

旧版 PPT 生成脚本，使用通用模板，不基于调研结果。
新版脚本（create_scenario_ppt.py）会根据实际调研结果选择和定制场景，
符合 ASI09（Human-Agent Trust Exploitation）安全要求。

如果你仍需使用此脚本，请确保：
1. 已完成 4 轮搜索（12 个关键词）
2. 已生成 research_results.json
3. 使用 create_scenario_ppt.py 生成 PPT
"""

import sys

def main():
    print("⚠️  此脚本已废弃，请使用 create_scenario_ppt.py")
    print("")
    print("新版脚本会根据实际调研结果生成场景化 PPT，")
    print("确保 PPT 内容基于真实搜索发现，而非通用模板。")
    print("")
    print("用法：python create_scenario_ppt.py <客户名称> <输出路径> [research_results.json]")
    print("")
    print("执行流程：")
    print("  1. 完成 4 轮搜索（12 个关键词）")
    print("  2. 生成 research_results.json（调研结果）")
    print("  3. 调用 create_scenario_ppt.py 生成 PPT")
    sys.exit(1)

if __name__ == "__main__":
    main()
