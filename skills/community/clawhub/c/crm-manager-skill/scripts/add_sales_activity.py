#!/usr/bin/env python3
"""
添加销售行为记录

用法:
    python add_sales_activity.py <name> --type <type> --description <description> [options]

示例:
    python add_sales_activity.py "李雷" --type "询价" --description "客户咨询产品价格" --stage "需求确认" --amount 50000 --product "A产品" --outcome "进行中"
    python add_sales_activity.py "王芳" --type "购买" --description "客户决定购买" --stage "成交" --amount 100000 --product "B产品" --outcome "成功"
"""

import os
import sys
import yaml
import argparse
from datetime import datetime

# 销售类型枚举
VALID_TYPES = ["购买", "询价", "演示", "报价", "合同", "售后"]

# 销售阶段枚举
VALID_STAGES = ["潜在客户", "需求确认", "报价", "谈判", "成交", "售后"]

# 结果状态枚举
VALID_OUTCOMES = ["成功", "失败", "进行中"]


def generate_activity_id(sales_activities):
    """生成新的销售记录ID"""
    if not sales_activities:
        return "SA001"
    
    # 找到最大的ID号
    max_num = 0
    for activity in sales_activities:
        activity_id = activity.get('id', '')
        if activity_id.startswith('SA'):
            try:
                num = int(activity_id[2:])
                max_num = max(max_num, num)
            except ValueError:
                pass
    
    return f"SA{str(max_num + 1).zfill(3)}"


def add_sales_activity(name, type, description, stage=None, amount=None, product=None, 
                       outcome=None, related_note_id=None, date=None):
    """
    为客户添加销售行为记录
    
    Args:
        name: 客户姓名
        type: 销售类型（购买/询价/演示/报价/合同/售后）
        description: 描述说明
        stage: 销售阶段（可选）
        amount: 涉及金额（可选）
        product: 相关产品（可选）
        outcome: 结果状态（可选）
        related_note_id: 关联的跟进记录ID（可选）
        date: 发生日期（可选，默认今天）
    
    Returns:
        dict: 操作结果
    """
    # 验证销售类型
    if type not in VALID_TYPES:
        return {
            "success": False,
            "message": f"无效的销售类型: {type}。有效类型: {', '.join(VALID_TYPES)}"
        }
    
    # 验证销售阶段（如果提供）
    if stage and stage not in VALID_STAGES:
        return {
            "success": False,
            "message": f"无效的销售阶段: {stage}。有效阶段: {', '.join(VALID_STAGES)}"
        }
    
    # 验证结果状态（如果提供）
    if outcome and outcome not in VALID_OUTCOMES:
        return {
            "success": False,
            "message": f"无效的结果状态: {outcome}。有效状态: {', '.join(VALID_OUTCOMES)}"
        }
    
    # 数据目录
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'customers')
    file_path = os.path.join(data_dir, f"{name}.yaml")
    
    # 检查客户是否存在
    if not os.path.exists(file_path):
        return {
            "success": False,
            "message": f"客户 {name} 不存在"
        }
    
    # 读取现有记录
    with open(file_path, "r", encoding="utf-8") as f:
        record = yaml.safe_load(f)
    
    # 获取现有销售活动列表
    if "sales_activities" not in record or record["sales_activities"] is None:
        record["sales_activities"] = []
    
    # 生成活动ID
    activity_id = generate_activity_id(record["sales_activities"])
    
    # 设置日期（默认今天）
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # 如果未提供阶段，根据类型默认设置
    if not stage:
        stage_map = {
            "购买": "成交",
            "询价": "需求确认",
            "演示": "报价",
            "报价": "谈判",
            "合同": "成交",
            "售后": "售后"
        }
        stage = stage_map.get(type, "潜在客户")
    
    # 如果未提供结果，默认"进行中"
    if not outcome:
        outcome = "进行中"
    
    # 构建销售行为记录
    activity = {
        "id": activity_id,
        "date": date,
        "type": type,
        "stage": stage,
        "description": description,
        "outcome": outcome
    }
    
    # 添加可选字段
    if amount is not None:
        activity["amount"] = amount
    if product:
        activity["product"] = product
    if related_note_id:
        activity["related_note_id"] = related_note_id
    
    # 添加到列表
    record["sales_activities"].append(activity)
    
    # 更新客户状态和最后联系时间
    record["last_contact"] = date
    if outcome == "成功" and type in ["购买", "合同"]:
        record["status"] = "已成交"
    elif record["status"] == "新增":
        record["status"] = "跟进中"
    
    # 更新时间戳
    record["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 保存文件
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(record, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    return {
        "success": True,
        "message": f"已为 {name} 添加销售行为记录 [{activity_id}]",
        "data": {
            "activity": activity,
            "total_activities": len(record["sales_activities"])
        }
    }


def main():
    # 修复 Windows 控制台输出编码问题
    import sys
    import io
    if sys.platform == 'win32' and sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    parser = argparse.ArgumentParser(description="添加销售行为记录")
    parser.add_argument("name", help="客户姓名")
    parser.add_argument("--type", required=True, help="销售类型（购买/询价/演示/报价/合同/售后）")
    parser.add_argument("--description", required=True, help="描述说明")
    parser.add_argument("--stage", help="销售阶段（潜在客户/需求确认/报价/谈判/成交/售后）")
    parser.add_argument("--amount", type=float, help="涉及金额")
    parser.add_argument("--product", help="相关产品")
    parser.add_argument("--outcome", help="结果状态（成功/失败/进行中）")
    parser.add_argument("--related-note-id", help="关联的跟进记录ID")
    parser.add_argument("--date", help="发生日期（格式：YYYY-MM-DD，默认为今天）")
    
    args = parser.parse_args()
    
    result = add_sales_activity(
        name=args.name,
        type=args.type,
        description=args.description,
        stage=args.stage,
        amount=args.amount,
        product=args.product,
        outcome=args.outcome,
        related_note_id=args.related_note_id,
        date=args.date
    )
    
    print(result["message"])
    if result["success"]:
        print(f"当前共有 {result['data']['total_activities']} 条销售行为记录")
        print(f"记录详情: {result['data']['activity']['id']} - {result['data']['activity']['type']} - {result['data']['activity']['stage']}")
    
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
