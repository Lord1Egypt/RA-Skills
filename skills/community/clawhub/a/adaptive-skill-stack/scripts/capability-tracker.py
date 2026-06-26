# -*- coding: utf-8 -*-
"""
⚠️ 结构锁定文件：此脚本为自适应技能叠加技能的结构性代码。
⚠️ 与 references/capability-registry.md 的格式强耦合（正则匹配依赖特定标记）。
⚠️ 未经用户明确授权，本技能在使用过程中不得修改此文件。
⚠️ 擅自修改可能导致自动化追踪链静默崩溃。

自适应技能叠加 - 能力追踪脚本
用于记录和管理能力注册表的自动化工具。

用法：
    python capability_tracker.py register --name "能力名称" --domain "领域" --trigger "触发场景" --method "核心方法" --tools "依赖工具" --related "关联能力"
    python capability_tracker.py increment --name "能力名称"
    python capability_tracker.py stats
    python capability_tracker.py log --message "日志信息"
"""

import argparse
import os
import re
from datetime import datetime

# 技能根目录
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY_PATH = os.path.join(SKILL_ROOT, "references", "capability-registry.md")


def get_today():
    return datetime.now().strftime("%Y-%m-%d")


def read_registry():
    if not os.path.exists(REGISTRY_PATH):
        return ""
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return f.read()


def write_registry(content):
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        f.write(content)


def register_capability(name, domain, trigger, method, tools, related):
    """注册新能力到能力注册表"""
    content = read_registry()
    today = get_today()

    # 检查是否已存在
    if f"#### {name}" in content:
        print(f"⚠️ 能力「{name}」已存在于注册表中")
        return False

    # 确定能力类别
    category = "🟣 领域能力"
    meta_keywords = ["元能力", "核心架构", "协议"]
    if any(kw in domain for kw in meta_keywords):
        category = "🟢 基础能力"
    elif "通用" in domain or "工具" in domain:
        category = "🔵 通用能力"

    # 构建新能力条目
    entry = f"""
#### {name}
- **领域**：{domain}
- **触发场景**：{trigger}
- **核心方法**：{method}
- **依赖工具**：{tools}
- **获得日期**：{today}
- **使用次数**：0
- **关联能力**：{related}
- **状态**：🟢 活跃
"""

    # 找到对应类别区域插入
    section_header = f"### {category}（初始注入）" if category == "🟢 基础能力" else f"### {category}"
    
    if section_header in content:
        # 在对应类别下插入（找到下一个 ### 或 ## 之前）
        pattern = re.compile(rf"({re.escape(section_header)}.*?)(\n###|\n##|\Z)", re.DOTALL)
        match = pattern.search(content)
        if match:
            insert_pos = match.start(2)
            content = content[:insert_pos] + entry + "\n" + content[insert_pos:]
        else:
            content += entry
    else:
        # 在统计表之前插入新类别
        stats_marker = "## 📊 能力统计"
        new_section = f"\n### 🟢 基础能力（初始注入）{entry}\n" if category == "🟢 基础能力" else f"\n### {category}{entry}\n"
        if stats_marker in content:
            content = content.replace(stats_marker, new_section + stats_marker)
        else:
            content += new_section

    # 更新统计
    content = update_stats(content)

    # 更新增长日志
    content = add_log_entry(content, today, f"**新能力注册**：{name}（{domain}）")

    write_registry(content)
    print(f"✅ 能力「{name}」已成功注册到 {category}")
    return True


def increment_usage(name):
    """递增能力使用次数"""
    content = read_registry()

    # 查找能力条目
    pattern = rf"(#### {name}.*?- \*\*使用次数\*\*：)(\d+)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        old_count = int(match.group(2))
        new_count = old_count + 1
        content = content[:match.start(2)] + str(new_count) + content[match.end(2):]
        write_registry(content)
        print(f"✅ 能力「{name}」使用次数：{old_count} → {new_count}")
        return True
    else:
        print(f"⚠️ 未找到能力「{name}」")
        return False


def add_log_entry(content, date, message):
    """在增长日志中追加条目"""
    log_section = "## 📝 能力增长日志"
    
    if date in content:
        # 日期已存在，追加到该日期下
        pattern = rf"(### {date}\n)(.*?)(\n### |\n## 📝|$)"
        match = re.search(pattern, content, re.DOTALL)
        if match:
            insert_pos = match.start(3)
            content = content[:insert_pos] + f"\n- {message}" + content[insert_pos:]
    else:
        # 新日期
        if log_section in content:
            content = content.replace(log_section, f"{log_section}\n\n### {date}\n- {message}")
        else:
            content += f"\n\n## 📝 能力增长日志\n\n### {date}\n- {message}"
    
    return content


def update_stats(content):
    """更新能力统计表"""
    categories = {
        "🟢 基础能力": 0,
        "🔵 通用能力": 0,
        "🟣 领域能力": 0,
        "🟡 复合能力": 0,
    }
    
    for cat in categories:
        # 统计该类别下的 #### 数量
        pattern = rf"### {re.escape(cat)}(.*?)(?:\n### |\n## |\Z)"
        match = re.search(pattern, content, re.DOTALL)
        if match:
            section = match.group(1)
            categories[cat] = len(re.findall(r"#### ", section))
    
    total = sum(categories.values())
    
    stats_table = """## 📊 能力统计

| 类别 | 数量 |
|------|------|
| 🟢 基础能力 | {basic} |
| 🔵 通用能力 | {general} |
| 🟣 领域能力 | {domain} |
| 🟡 复合能力 | {compound} |
| **总计** | **{total}** |""".format(
        basic=categories["🟢 基础能力"],
        general=categories["🔵 通用能力"],
        domain=categories["🟣 领域能力"],
        compound=categories["🟡 复合能力"],
        total=total,
    )
    
    # 替换旧的统计表
    old_pattern = r"## 📊 能力统计.*?(?=\n## |\n### |\Z)"
    content = re.sub(old_pattern, stats_table, content, flags=re.DOTALL)
    
    return content


def show_stats():
    """显示能力统计"""
    content = read_registry()
    stats_pattern = r"## 📊 能力统计\n\n(.+?)(?:\n---|\n## |\Z)"
    match = re.search(stats_pattern, content, re.DOTALL)
    if match:
        print(f"\n📊 能力统计\n\n{match.group(1).strip()}")
    else:
        print("⚠️ 无法读取能力统计")


def log_message(message):
    """添加自定义日志"""
    content = read_registry()
    today = get_today()
    content = add_log_entry(content, today, message)
    write_registry(content)
    print(f"📝 日志已记录：{message}")


def main():
    parser = argparse.ArgumentParser(description="自适应技能叠加 - 能力追踪工具")
    subparsers = parser.add_subparsers(dest="command")

    # register 命令
    reg_parser = subparsers.add_parser("register", help="注册新能力")
    reg_parser.add_argument("--name", required=True, help="能力名称")
    reg_parser.add_argument("--domain", required=True, help="所属领域")
    reg_parser.add_argument("--trigger", required=True, help="触发场景")
    reg_parser.add_argument("--method", required=True, help="核心方法")
    reg_parser.add_argument("--tools", default="无", help="依赖工具")
    reg_parser.add_argument("--related", default="无", help="关联能力")

    # increment 命令
    inc_parser = subparsers.add_parser("increment", help="递增使用次数")
    inc_parser.add_argument("--name", required=True, help="能力名称")

    # stats 命令
    subparsers.add_parser("stats", help="显示能力统计")

    # log 命令
    log_parser = subparsers.add_parser("log", help="添加日志")
    log_parser.add_argument("--message", required=True, help="日志信息")

    args = parser.parse_args()

    if args.command == "register":
        register_capability(args.name, args.domain, args.trigger, args.method, args.tools, args.related)
    elif args.command == "increment":
        increment_usage(args.name)
    elif args.command == "stats":
        show_stats()
    elif args.command == "log":
        log_message(args.message)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
