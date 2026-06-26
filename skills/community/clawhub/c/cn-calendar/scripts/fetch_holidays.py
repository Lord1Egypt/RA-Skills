#!/usr/bin/env python3
"""
cn-calendar: 从国务院官网抓取指定年份的法定节假日通知，解析后：
1. 生成 references/holidays-YYYY.md 文件
2. 将假期数据以 JSON 格式输出到 stdout 供 workday_query.py 使用

用法:
  python3 fetch_holidays.py <YYYY>            # 抓取并输出数据
  python3 fetch_holidays.py <YYYY> --save     # 抓取并保存到 references/
  python3 fetch_holidays.py <YYYY> --check    # 只检查本地是否已有数据

本脚本由 Claude Agent 调用，不直接被用户执行。
"""

import sys
import os
import json
import re
from datetime import date
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
REFERENCES_DIR = SKILL_DIR / "references"

# 国务院节假日通知搜索入口（按年份）
GOV_SEARCH_URLS = [
    "https://www.gov.cn/zhengce/jiejiarianzhi.htm",
    "https://www.gov.cn/zhengce/content/",
]


def check_local(year: int) -> dict | None:
    """检查本地是否已有该年份数据，返回已解析的数据或 None"""
    ref_file = REFERENCES_DIR / f"holidays-{year}.md"
    if ref_file.exists():
        return {"exists": True, "path": str(ref_file)}
    return None


def parse_holiday_from_md(year: int) -> dict:
    """从本地 references/holidays-YYYY.md 解析出假期数据"""
    ref_file = REFERENCES_DIR / f"holidays-{year}.md"
    if not ref_file.exists():
        return {}
    
    # 读取文件内容，提取日期列表
    # 此处返回文件路径，由 Claude 读取并解析
    return {"file": str(ref_file), "year": year}


def generate_workday_data_block(year: int, holidays: list[str], extra_workdays: list[str]) -> str:
    """生成可插入 workday_query.py 的数据块"""
    h_lines = "\n".join(f"    date({y}, {m}, {d})," for y, m, d in 
                         [tuple(map(int, s.split("-"))) for s in sorted(holidays)])
    w_lines = "\n".join(f"    date({y}, {m}, {d})," for y, m, d in 
                         [tuple(map(int, s.split("-"))) for s in sorted(extra_workdays)])
    
    return f"""
# {year}年法定节假日（自动抓取，来源：国务院）
HOLIDAYS_{year} = {{
{h_lines}
}}

# {year}年调休工作日（自动抓取，来源：国务院）
WORKDAYS_{year} = {{
{w_lines}
}}
"""


def save_references_md(year: int, content: str):
    """将节假日信息保存为 references/holidays-YYYY.md"""
    REFERENCES_DIR.mkdir(exist_ok=True)
    ref_file = REFERENCES_DIR / f"holidays-{year}.md"
    ref_file.write_text(content, encoding="utf-8")
    print(f"✅ 已保存到 {ref_file}", file=sys.stderr)


def update_workday_script(year: int, holidays: list[str], extra_workdays: list[str]):
    """将新年份数据插入 workday_query.py"""
    script_path = SKILL_DIR / "scripts" / "workday_query.py"
    content = script_path.read_text(encoding="utf-8")
    
    # 检查是否已有该年份数据
    if f"HOLIDAYS_{year}" in content:
        print(f"ℹ️  workday_query.py 已包含 {year} 年数据，跳过更新", file=sys.stderr)
        return
    
    new_block = generate_workday_data_block(year, holidays, extra_workdays)
    
    # 在 ALL_HOLIDAYS 定义之前插入新数据块
    insert_marker = "ALL_HOLIDAYS = "
    content = content.replace(insert_marker, new_block + "\n" + insert_marker)
    
    # 更新 ALL_HOLIDAYS 和 ALL_EXTRA_WORKDAYS 合并集合
    content = re.sub(
        r"ALL_HOLIDAYS = ([^\n]+)",
        lambda m: m.group(0).rstrip() + f" | HOLIDAYS_{year}",
        content
    )
    content = re.sub(
        r"ALL_EXTRA_WORKDAYS = ([^\n]+)",
        lambda m: m.group(0).rstrip() + f" | WORKDAYS_{year}",
        content
    )
    
    script_path.write_text(content, encoding="utf-8")
    print(f"✅ 已更新 workday_query.py，添加 {year} 年数据", file=sys.stderr)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)
    
    year = int(args[0])
    mode = args[1] if len(args) > 1 else "--check"
    
    if mode == "--check":
        result = check_local(year)
        if result:
            print(json.dumps({"status": "exists", "year": year, "path": result["path"]}))
        else:
            print(json.dumps({"status": "missing", "year": year}))
    
    elif mode == "--save":
        # 此模式由 Claude 在获取到官网数据后调用
        # 数据通过 stdin 传入（JSON 格式）
        data = json.loads(sys.stdin.read())
        holidays = data.get("holidays", [])
        extra_workdays = data.get("extra_workdays", [])
        md_content = data.get("md_content", "")
        
        if md_content:
            save_references_md(year, md_content)
        
        if holidays:
            update_workday_script(year, holidays, extra_workdays)
        
        print(json.dumps({"status": "saved", "year": year, 
                          "holidays_count": len(holidays),
                          "extra_workdays_count": len(extra_workdays)}))
    
    else:
        print(f"未知模式: {mode}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
