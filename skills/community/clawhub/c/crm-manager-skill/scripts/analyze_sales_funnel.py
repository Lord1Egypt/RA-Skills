#!/usr/bin/env python3
"""
销售漏斗分析

用法:
    python analyze_sales_funnel.py [--days DAYS] [--stage STAGE]

示例:
    python analyze_sales_funnel.py
    python analyze_sales_funnel.py --days 30
    python analyze_sales_funnel.py --stage "报价"
"""

import os
import sys
import yaml
import argparse
from datetime import datetime, timedelta
from collections import defaultdict


# 销售阶段顺序（用于漏斗计算）
STAGE_ORDER = ["潜在客户", "需求确认", "报价", "谈判", "成交", "售后"]

# 销售阶段权重（用于计算整体进展）
STAGE_WEIGHTS = {
    "潜在客户": 0.1,
    "需求确认": 0.25,
    "报价": 0.4,
    "谈判": 0.6,
    "成交": 0.8,
    "售后": 1.0
}


def load_all_customers():
    """加载所有客户数据"""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'customers')
    
    if not os.path.exists(data_dir):
        return []
    
    customers = []
    for filename in os.listdir(data_dir):
        if filename.endswith('.yaml'):
            file_path = os.path.join(data_dir, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    record = yaml.safe_load(f)
                    if record:
                        record['file_name'] = filename
                        customers.append(record)
            except Exception as e:
                print(f"警告: 无法读取文件 {filename}: {e}")
    
    return customers


def analyze_sales_funnel(days=None, stage=None):
    """
    分析销售漏斗
    
    Args:
        days: 分析最近N天的数据（None表示所有时间）
        stage: 按特定阶段筛选（None表示所有阶段）
    
    Returns:
        dict: 分析结果
    """
    customers = load_all_customers()
    
    if not customers:
        return {
            "success": False,
            "message": "没有找到客户数据"
        }
    
    # 计算起始日期
    start_date = None
    if days:
        start_date = datetime.now() - timedelta(days=days)
    
    # 统计变量
    stage_counts = defaultdict(int)  # 各阶段客户数
    type_counts = defaultdict(int)   # 各类型记录数
    outcome_counts = defaultdict(int) # 结果状态计数
    total_amount = 0.0               # 总金额
    activity_count = 0               # 活动总数
    active_customers = set()         # 活跃客户数
    customer_stage_map = {}          # 客户最新阶段映射
    
    for customer in customers:
        customer_name = customer.get('name', '未知')
        # 兼容旧数据sales_activities和新数据service_records
        activities = customer.get('service_records', customer.get('sales_activities', []))
        
        for activity in activities:
            activity_date = activity.get('date')
            
            # 日期过滤
            if start_date and activity_date:
                try:
                    act_dt = datetime.strptime(activity_date, "%Y-%m-%d")
                    if act_dt < start_date:
                        continue
                except:
                    pass
            
            activity_stage = activity.get('stage', '')
            activity_type = activity.get('type', '')
            outcome = activity.get('outcome', '')
            amount = activity.get('amount', 0)
            
            # 阶段过滤
            if stage and activity_stage != stage:
                continue
            
            # 统计
            stage_counts[activity_stage] += 1
            type_counts[activity_type] += 1
            outcome_counts[outcome] += 1
            
            if amount:
                total_amount += amount
            
            activity_count += 1
            active_customers.add(customer_name)
            
            # 记录客户的最新阶段（用于漏斗分析）
            if customer_name not in customer_stage_map:
                customer_stage_map[customer_name] = activity_stage
            else:
                # 比较阶段顺序，保留更靠后的阶段
                current_stage_idx = STAGE_ORDER.index(customer_stage_map[customer_name]) if customer_stage_map[customer_name] in STAGE_ORDER else -1
                new_stage_idx = STAGE_ORDER.index(activity_stage) if activity_stage in STAGE_ORDER else -1
                if new_stage_idx > current_stage_idx:
                    customer_stage_map[customer_name] = activity_stage
    
    # 计算漏斗转化率
    funnel_data = {}
    prev_count = 0
    for s in STAGE_ORDER:
        count = stage_counts.get(s, 0)
        funnel_data[s] = {
            "count": count,
            "percentage": (count / activity_count * 100) if activity_count > 0 else 0
        }
        if prev_count > 0:
            funnel_data[s]["conversion_rate"] = (count / prev_count * 100)
        prev_count = count if count > 0 else prev_count
    
    # 构建结果
    result = {
        "success": True,
        "message": "销售漏斗分析完成",
        "summary": {
            "total_customers": len(customers),
            "active_customers": len(active_customers),
            "total_activities": activity_count,
            "total_amount": total_amount,
            "analysis_period": f"最近{days}天" if days else "全部时间",
            "stage_filter": stage or "全部阶段"
        },
        "stage_distribution": dict(stage_counts),
        "type_distribution": dict(type_counts),
        "outcome_distribution": dict(outcome_counts),
        "funnel_analysis": funnel_data,
        "customer_stage_map": customer_stage_map
    }
    
    return result


def format_analysis_report(result):
    """格式化分析报告"""
    if not result["success"]:
        return result["message"]
    
    lines = []
    lines.append("=" * 60)
    lines.append("销售漏斗分析报告")
    lines.append("=" * 60)
    
    summary = result["summary"]
    lines.append(f"\n📊 分析概况")
    lines.append(f"  分析周期: {summary['analysis_period']}")
    lines.append(f"  阶段筛选: {summary['stage_filter']}")
    lines.append(f"  总客户数: {summary['total_customers']}")
    lines.append(f"  活跃客户: {summary['active_customers']}")
    lines.append(f"  销售活动: {summary['total_activities']} 次")
    lines.append(f"  涉及金额: ¥{summary['total_amount']:,.2f}")
    
    lines.append(f"\n📈 销售漏斗分布")
    funnel = result["funnel_analysis"]
    for stage in STAGE_ORDER:
        data = funnel.get(stage, {"count": 0, "percentage": 0})
        lines.append(f"  {stage:10s}: {data['count']:3d} 次 ({data['percentage']:5.1f}%)")
    
    lines.append(f"\n🏷️ 销售类型分布")
    for type_name, count in sorted(result["type_distribution"].items(), key=lambda x: x[1], reverse=True):
        lines.append(f"  {type_name:10s}: {count} 次")
    
    lines.append(f"\n✅ 结果状态分布")
    for outcome, count in sorted(result["outcome_distribution"].items(), key=lambda x: x[1], reverse=True):
        lines.append(f"  {outcome:10s}: {count} 次")
    
    lines.append(f"\n🎯 转化率分析")
    lines.append(f"  活跃客户占比: {(summary['active_customers']/summary['total_customers']*100) if summary['total_customers'] > 0 else 0:.1f}%")
    
    # 计算成交率
    if "成交" in result["stage_distribution"] and summary["total_activities"] > 0:
        lines.append(f"  成交转化率: {result['stage_distribution']['成交']/summary['total_activities']*100:.1f}%")
    
    lines.append("\n" + "=" * 60)
    
    return "\n".join(lines)


def main():
    # 修复 Windows 控制台输出编码问题
    import sys
    import io
    if sys.platform == 'win32' and sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    parser = argparse.ArgumentParser(description="销售漏斗分析")
    parser.add_argument("--days", type=int, help="分析最近N天的数据")
    parser.add_argument("--stage", help="按特定阶段筛选")
    
    args = parser.parse_args()
    
    result = analyze_sales_funnel(
        days=args.days,
        stage=args.stage
    )
    
    if result["success"]:
        print(format_analysis_report(result))
        return 0
    else:
        print(result["message"])
        return 1


if __name__ == "__main__":
    sys.exit(main())
