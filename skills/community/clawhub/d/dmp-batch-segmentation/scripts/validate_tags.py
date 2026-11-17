#!/usr/bin/env python3
"""
标签校验模块
功能：校验标签列表格式，计算拆分方案
"""

import sys
import json
import math
from pathlib import Path

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

MAX_TAGS_PER_GROUP = 50  # 每组最多50个标签

def parse_tags_input(tags_input):
    """
    解析标签输入
    
    Args:
        tags_input: 标签输入（可以是逗号分隔的字符串、文件路径）
        
    Returns:
        list: 标签ID列表
    """
    tags = []
    
    # 检查是否是文件路径
    if Path(tags_input).exists():
        file_path = Path(tags_input)
        suffix = file_path.suffix.lower()
        
        if not PANDAS_AVAILABLE:
            raise ValueError("pandas库未安装，无法读取Excel文件")
        
        if suffix == '.csv':
            df = pd.read_csv(file_path)
        elif suffix in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {suffix}")
        
        # 取第一列作为标签ID
        tags = df.iloc[:, 0].dropna().astype(str).tolist()
    else:
        # 逗号分隔的字符串
        tags = [t.strip() for t in tags_input.split(',') if t.strip()]
    
    # 转换为整数
    tag_ids = []
    for tag in tags:
        try:
            tag_ids.append(int(tag))
        except ValueError:
            raise ValueError(f"无效的标签ID: {tag}")
    
    return tag_ids

def validate_tags(tag_ids):
    """
    校验标签列表
    
    Args:
        tag_ids: 标签ID列表
        
    Returns:
        dict: 校验结果
    """
    result = {
        "is_valid": True,
        "error_msg": "",
        "tag_count": len(tag_ids),
        "needs_split": len(tag_ids) > MAX_TAGS_PER_GROUP,
        "group_count": math.ceil(len(tag_ids) / MAX_TAGS_PER_GROUP) if len(tag_ids) > MAX_TAGS_PER_GROUP else 1
    }
    
    # 检查是否有重复
    unique_tags = set(tag_ids)
    if len(unique_tags) < len(tag_ids):
        result["warning"] = f"发现{len(tag_ids) - len(unique_tags)}个重复标签，已自动去重"
        tag_ids = list(unique_tags)
        result["tag_count"] = len(tag_ids)
    
    return result

def calculate_split_plan(tag_count, strategy, params=None):
    """
    计算拆分方案
    
    Args:
        tag_count: 标签数量
        strategy: 拆分策略 (fixed_per_group / fixed_group_count / custom)
        params: 策略参数
        
    Returns:
        dict: 拆分方案
    """
    if params is None:
        params = {}
    
    plan = {
        "tag_count": tag_count,
        "strategy": strategy,
        "group_count": 0,
        "tags_per_group": 0,
        "groups": []
    }
    
    if strategy == "fixed_per_group":
        per_group = min(params.get("tags_per_group", MAX_TAGS_PER_GROUP), MAX_TAGS_PER_GROUP)
        group_count = math.ceil(tag_count / per_group)
        
        plan["group_count"] = group_count
        plan["tags_per_group"] = per_group
        
        for i in range(group_count):
            start = i * per_group
            end = min((i + 1) * per_group, tag_count)
            plan["groups"].append({
                "group_no": i + 1,
                "start_index": start,
                "end_index": end,
                "tag_count": end - start
            })
    
    elif strategy == "fixed_group_count":
        group_count = params.get("group_count", 1)
        per_group = math.ceil(tag_count / group_count)
        
        if per_group > MAX_TAGS_PER_GROUP:
            return {
                "is_valid": False,
                "error_msg": f"每组{per_group}个标签，超过{MAX_TAGS_PER_GROUP}个限制"
            }
        
        plan["group_count"] = group_count
        plan["tags_per_group"] = per_group
        
        for i in range(group_count):
            start = i * per_group
            end = min((i + 1) * per_group, tag_count)
            plan["groups"].append({
                "group_no": i + 1,
                "start_index": start,
                "end_index": end,
                "tag_count": end - start
            })
    
    return plan

def determine_split_mode(a_tag_count, b_tag_count):
    """
    确定拆分模式
    
    Args:
        a_tag_count: A规则标签数量
        b_tag_count: B规则标签数量
        
    Returns:
        str: 拆分模式 (many_to_one / one_to_many / many_to_many)
    """
    a_needs_split = a_tag_count > MAX_TAGS_PER_GROUP
    b_needs_split = b_tag_count > MAX_TAGS_PER_GROUP
    
    if a_needs_split and not b_needs_split:
        return "many_to_one"  # 多对一：A拆分，B固定
    elif not a_needs_split and b_needs_split:
        return "one_to_many"  # 一对多：A固定，B拆分
    elif a_needs_split and b_needs_split:
        return "many_to_many"  # 多对多：A拆分，B拆分
    else:
        return "one_to_one"  # 一对一：都不需要拆分

def print_split_plan(plan, mode_name=""):
    """打印拆分方案"""
    print("\n" + "="*50)
    print(f"标签拆分方案 {mode_name}")
    print("="*50)
    
    print(f"标签总数: {plan['tag_count']}个")
    print(f"拆分策略: {plan['strategy']}")
    print(f"拆分组数: {plan['group_count']}组")
    print(f"每组标签数: {plan['tags_per_group']}个")
    print()
    print("分组详情:")
    for group in plan["groups"]:
        print(f"  组{group['group_no']}: 标签{group['start_index']+1}-{group['end_index']} ({group['tag_count']}个)")
    
    print("="*50)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python validate_tags.py <标签输入>")
        print("  标签输入可以是：")
        print("    - 逗号分隔的标签ID: 15688,15689,15690")
        print("    - 文件路径: tags.csv 或 tags.xlsx")
        sys.exit(1)
    
    tags_input = sys.argv[1]
    
    try:
        tag_ids = parse_tags_input(tags_input)
        result = validate_tags(tag_ids)
        
        print("\n" + "="*50)
        print("标签校验结果")
        print("="*50)
        print(f"标签数量: {result['tag_count']}个")
        print(f"是否需要拆分: {'是' if result['needs_split'] else '否'}")
        if result['needs_split']:
            print(f"预计拆分组数: {result['group_count']}组（每组最多{MAX_TAGS_PER_GROUP}个）")
        if result.get("warning"):
            print(f"⚠️ 警告: {result['warning']}")
        print("="*50)
        
        # 输出JSON结果
        print("\n---JSON_RESULT---")
        output = {
            "tag_ids": tag_ids,
            "validation": result
        }
        print(json.dumps(output, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)
