#!/usr/bin/env python3
"""
解释cron表达式的脚本
将cron表达式转换为自然语言描述
"""

import argparse
import sys

def parse_cron_field(field: str, field_name: str, ranges: dict) -> str:
    """
    解析单个cron字段并返回自然语言描述
    """
    if field == "*":
        return f"任何{field_name}"
    
    # 处理步长
    if "/" in field:
        base, step = field.split("/", 1)
        if base == "*":
            return f"每{step}个{field_name}"
        else:
            base_desc = parse_cron_field(base, field_name, ranges)
            return f"{base_desc}开始，每{step}个{field_name}"
    
    # 处理列表
    if "," in field:
        items = field.split(",")
        descriptions = [parse_cron_field(item, field_name, ranges) for item in items]
        return f"{field_name}为 {'、'.join(descriptions)}"
    
    # 处理范围
    if "-" in field:
        start, end = field.split("-", 1)
        
        # 尝试转换为名称（对于月份和星期）
        if field_name == "月" and ranges.get("month_names"):
            try:
                start_name = ranges["month_names"].get(int(start), start)
                end_name = ranges["month_names"].get(int(end), end)
                return f"从{start_name}到{end_name}"
            except:
                pass
        
        if field_name == "星期" and ranges.get("weekday_names"):
            try:
                start_name = ranges["weekday_names"].get(int(start), start)
                end_name = ranges["weekday_names"].get(int(end), end)
                return f"从{start_name}到{end_name}"
            except:
                pass
        
        return f"从{start}到{end}"
    
    # 单个值
    if field_name == "月" and ranges.get("month_names"):
        try:
            return ranges["month_names"].get(int(field), field)
        except:
            pass
    
    if field_name == "星期" and ranges.get("weekday_names"):
        try:
            return ranges["weekday_names"].get(int(field), field)
        except:
            pass
    
    return field

def explain_cron_expression(cron_expr: str) -> str:
    """
    将cron表达式转换为自然语言描述
    """
    parts = cron_expr.strip().split()
    if len(parts) != 5:
        return "无效的cron表达式：必须是5个字段"
    
    minute, hour, day, month, weekday = parts
    
    # 定义字段名称和范围
    field_defs = [
        {
            "field": minute,
            "name": "分钟",
            "ranges": {}
        },
        {
            "field": hour,
            "name": "小时",
            "ranges": {}
        },
        {
            "field": day,
            "name": "日",
            "ranges": {}
        },
        {
            "field": month,
            "name": "月",
            "ranges": {
                "month_names": {
                    1: "一月", 2: "二月", 3: "三月", 4: "四月",
                    5: "五月", 6: "六月", 7: "七月", 8: "八月",
                    9: "九月", 10: "十月", 11: "十一月", 12: "十二月"
                }
            }
        },
        {
            "field": weekday,
            "name": "星期",
            "ranges": {
                "weekday_names": {
                    0: "周日", 1: "周一", 2: "周二", 3: "周三",
                    4: "周四", 5: "周五", 6: "周六", 7: "周日"
                }
            }
        }
    ]
    
    # 解析每个字段
    descriptions = []
    for field_def in field_defs:
        desc = parse_cron_field(field_def["field"], field_def["name"], field_def["ranges"])
        descriptions.append(desc)
    
    # 构建完整的描述
    minute_desc, hour_desc, day_desc, month_desc, weekday_desc = descriptions
    
    # 特殊情况处理
    result_parts = []
    
    # 处理分钟
    if minute == "0":
        result_parts.append("整点")
    elif minute == "*":
        result_parts.append("每分钟")
    elif "/" in minute and minute.split("/")[0] == "*":
        step = minute.split("/")[1]
        result_parts.append(f"每{step}分钟")
    else:
        result_parts.append(f"在分钟{minute_desc}")
    
    # 处理小时
    if hour == "*":
        result_parts.append("每小时")
    elif hour == "0":
        result_parts.append("午夜")
    else:
        result_parts.append(f"在{hour_desc}点")
    
    # 处理日
    if day == "*":
        result_parts.append("每天")
    else:
        result_parts.append(f"在{day_desc}号")
    
    # 处理月
    if month == "*":
        result_parts.append("每月")
    else:
        result_parts.append(f"在{month_desc}")
    
    # 处理星期
    if weekday == "*":
        result_parts.append("任何星期")
    else:
        result_parts.append(f"在{weekday_desc}")
    
    # 构建最终描述
    description = "，".join(result_parts) + "执行"
    
    # 简化常见模式
    if cron_expr == "0 0 * * *":
        return "每天午夜执行"
    elif cron_expr == "0 * * * *":
        return "每小时整点执行"
    elif cron_expr == "* * * * *":
        return "每分钟执行"
    elif cron_expr == "0 0 * * 0":
        return "每周日午夜执行"
    elif cron_expr == "0 9 * * 1-5":
        return "工作日（周一到周五）上午9点执行"
    elif cron_expr == "*/5 * * * *":
        return "每5分钟执行"
    elif cron_expr == "0 */2 * * *":
        return "每2小时整点执行"
    
    return description

def validate_cron_expression(cron_expr: str) -> bool:
    """
    简单的cron表达式验证
    """
    parts = cron_expr.strip().split()
    if len(parts) != 5:
        return False
    
    # 检查是否包含有效字符
    valid_chars = set("0123456789*,-/")
    for part in parts:
        if not all(c in valid_chars for c in part):
            return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description="解释cron表达式")
    parser.add_argument("cron_expr", nargs="?", help="cron表达式 (例如: '*/5 9-17 * * 1-5')")
    parser.add_argument("--examples", action="store_true", help="显示示例")
    
    args = parser.parse_args()
    
    # 显示示例
    if args.examples:
        print("Cron表达式示例:")
        print("=" * 50)
        examples = [
            ("* * * * *", "每分钟执行"),
            ("0 * * * *", "每小时整点执行"),
            ("0 0 * * *", "每天午夜执行"),
            ("0 9 * * 1-5", "工作日（周一到周五）上午9点执行"),
            ("0 0 * * 0", "每周日午夜执行"),
            ("*/5 * * * *", "每5分钟执行"),
            ("0 */2 * * *", "每2小时整点执行"),
            ("0 0 1 * *", "每月1号午夜执行"),
            ("0 12 * * 6", "每周六中午12点执行"),
            ("0 9-17 * * 1-5", "工作日每小时整点执行，从9点到17点"),
        ]
        
        for expr, desc in examples:
            print(f"{expr:20} → {desc}")
        
        print("=" * 50)
        return
    
    # 如果没有提供cron表达式，则提示输入
    if not args.cron_expr:
        args.cron_expr = input("请输入cron表达式: ").strip()
    
    print("=" * 50)
    print(f"Cron表达式: {args.cron_expr}")
    print("=" * 50)
    
    # 验证cron表达式
    if not validate_cron_expression(args.cron_expr):
        print("❌ 无效的cron表达式!")
        print("请检查表达式格式:")
        print("  格式: 分钟 小时 日 月 星期")
        print("  示例: */5 9-17 * * 1-5")
        sys.exit(1)
    
    # 解释cron表达式
    explanation = explain_cron_expression(args.cron_expr)
    
    print("表达式解释:")
    print(f"  {explanation}")
    print()
    
    # 显示字段详情
    parts = args.cron_expr.strip().split()
    minute, hour, day, month, weekday = parts
    
    print("字段详情:")
    print(f"  分钟 ({minute}): 控制任务在每小时的第几分钟执行 (0-59)")
    print(f"  小时 ({hour}): 控制任务在一天中的第几小时执行 (0-23)")
    print(f"  日 ({day}): 控制任务在每月的第几天执行 (1-31)")
    print(f"  月 ({month}): 控制任务在每年的第几月执行 (1-12)")
    print(f"  星期 ({weekday}): 控制任务在每周的第几天执行 (0-6, 0=周日)")
    print()
    
    print("提示:")
    print("  * 使用 '*' 表示任何值")
    print("  * 使用 ',' 分隔多个值 (例如: '1,3,5')")
    print("  * 使用 '-' 表示范围 (例如: '1-5')")
    print("  * 使用 '/' 表示步长 (例如: '*/5' 每5个单位)")
    print("  * 使用 '?' 仅在日和星期字段，表示无特定值")
    print("=" * 50)

if __name__ == "__main__":
    main()