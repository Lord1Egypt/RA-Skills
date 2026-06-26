#!/usr/bin/env python3
"""
自动化标签生成器

用法:
    python auto_tagger.py <name>

功能:
根据客户的服务记录、跟进记录和时间维度，自动生成智能标签
"""

import os
import sys
import yaml
import argparse
from datetime import datetime, timedelta
from collections import Counter


def load_customer(name):
    """加载客户数据"""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'customers')
    file_path = os.path.join(data_dir, f"{name}.yaml")
    
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def generate_auto_tags(customer_data):
    """
    基于客户数据自动生成标签
    
    标签类型:
    1. 服务频率标签
    2. 进度状态标签
    3. 财务状态标签
    4. 活跃度标签
    5. 流失风险标签
    """
    tags = []
    today = datetime.now()
    
    # 获取服务记录（兼容新旧字段名）
    service_records = customer_data.get('service_records', 
                                       customer_data.get('sales_activities', []))
    notes = customer_data.get('notes', [])
    
    # 1. 服务频率标签
    if service_records:
        recent_records = [
            r for r in service_records 
            if datetime.strptime(r['date'], "%Y-%m-%d") > today - timedelta(days=30)
        ]
        
        service_count = len(recent_records)
        if service_count >= 8:
            tags.append("高频客户")
        elif service_count >= 4:
            tags.append("活跃客户")
        elif service_count <= 1:
            tags.append("低频客户")
    
    # 2. 出勤率标签
    if service_records:
        attendance_list = [r.get('attendance') for r in service_records if r.get('attendance')]
        if attendance_list:
            attendance_counter = Counter(attendance_list)
            total = len(attendance_list)
            present_count = attendance_counter.get('出席', 0)
            absent_count = attendance_counter.get('缺席', 0)
            
            if present_count / total >= 0.9:
                tags.append("出勤优秀")
            elif absent_count / total >= 0.3:
                tags.append("出勤不佳")
    
    # 3. 进度标签
    progress_keywords = {
        "积极进展": ["进步明显", "进步很大", "表现优秀", "出色", "优秀"],
        "需重点关注": ["需要加强", "跟不上", "不太理想", "需改进"],
        "稳定保持": ["稳定", "正常", "良好"]
    }
    
    all_text = " ".join([r.get('description', '') for r in service_records])
    all_text += " ".join(notes)
    
    for tag, keywords in progress_keywords.items():
        if any(kw in all_text for kw in keywords):
            tags.append(tag)
            break  # 只添加最匹配的一个进度标签
    
    # 4. 财务状态标签
    payments = [r for r in service_records if r.get('type') in ['课程购买', '续费'] and r.get('outcome') == '成功']
    if payments:
        last_payment = max(payments, key=lambda x: x['date'])
        last_payment_date = datetime.strptime(last_payment['date'], "%Y-%m-%d")
        days_since_payment = (today - last_payment_date).days
        
        if days_since_payment > 60:
            tags.append("可能流失")
        elif days_since_payment > 45:
            tags.append("续费提醒期")
        elif days_since_payment <= 7:
            tags.append("新付费客户")
    
    # 5. 活跃度标签
    last_contact = customer_data.get('last_contact')
    if last_contact:
        last_contact_date = datetime.strptime(last_contact, "%Y-%m-%d")
        days_since_contact = (today - last_contact_date).days
        
        if days_since_contact > 30:
            tags.append("沉睡客户")
        elif days_since_contact > 14:
            tags.append("需跟进")
    
    # 6. 特殊事件标签
    trial_records = [r for r in service_records if r.get('type') == '体验课']
    if trial_records and not payments:
        tags.append("体验未转化")
    
    return list(set(tags))  # 去重


def add_auto_tags(name, dry_run=False):
    """
    为客户添加自动生成的标签
    
    Args:
        name: 客户姓名
        dry_run: 如果为True，只显示建议的标签，不实际添加
    
    Returns:
        dict: 操作结果
    """
    customer_data = load_customer(name)
    
    if not customer_data:
        return {
            "success": False,
            "message": f"客户 {name} 不存在"
        }
    
    # 生成标签
    auto_tags = generate_auto_tags(customer_data)
    
    if not auto_tags:
        return {
            "success": True,
            "message": f"客户 {name} 暂无建议的自动标签",
            "suggested_tags": []
        }
    
    if dry_run:
        return {
            "success": True,
            "message": f"客户 {name} 建议添加以下标签",
            "suggested_tags": auto_tags,
            "dry_run": True
        }
    
    # 合并现有标签和新标签
    existing_tags = set(customer_data.get('tags', []))
    new_tags = existing_tags.union(set(auto_tags))
    
    # 更新客户数据
    customer_data['tags'] = list(new_tags)
    customer_data['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 保存文件
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'customers')
    file_path = os.path.join(data_dir, f"{name}.yaml")
    
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(customer_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    added_tags = list(set(auto_tags) - existing_tags)
    
    return {
        "success": True,
        "message": f"已为 {name} 自动添加标签",
        "added_tags": added_tags,
        "all_tags": list(new_tags)
    }


def analyze_all_customers():
    """分析所有客户并生成标签建议报告"""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'customers')
    
    if not os.path.exists(data_dir):
        return {
            "success": False,
            "message": "数据目录不存在"
        }
    
    report = {
        "total_customers": 0,
        "tagged_customers": 0,
        "tag_distribution": {},
        "recommendations": []
    }
    
    for filename in os.listdir(data_dir):
        if filename.endswith('.yaml'):
            name = filename[:-5]  # 去掉.yaml
            result = add_auto_tags(name, dry_run=True)
            
            if result["success"]:
                report["total_customers"] += 1
                
                if result.get("suggested_tags"):
                    report["tagged_customers"] += 1
                    
                    for tag in result["suggested_tags"]:
                        report["tag_distribution"][tag] = report["tag_distribution"].get(tag, 0) + 1
                    
                    report["recommendations"].append({
                        "customer": name,
                        "suggested_tags": result["suggested_tags"]
                    })
    
    return {
        "success": True,
        "message": "分析完成",
        "report": report
    }


def main():
    # 修复 Windows 控制台输出编码问题
    import sys
    import io
    if sys.platform == 'win32' and sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    parser = argparse.ArgumentParser(description="自动化标签生成器")
    parser.add_argument("name", nargs="?", help="客户姓名（不提供则分析所有客户）")
    parser.add_argument("--dry-run", action="store_true", help="仅预览建议标签，不实际添加")
    parser.add_argument("--all", action="store_true", help="分析所有客户")
    
    args = parser.parse_args()
    
    if args.all or not args.name:
        # 分析所有客户
        result = analyze_all_customers()
        
        if result["success"]:
            report = result["report"]
            print("=" * 60)
            print("自动化标签分析报告")
            print("=" * 60)
            print(f"\n总客户数: {report['total_customers']}")
            print(f"建议打标签的客户: {report['tagged_customers']}")
            
            if report['tag_distribution']:
                print("\n建议标签分布:")
                for tag, count in sorted(report['tag_distribution'].items(), key=lambda x: x[1], reverse=True):
                    print(f"  {tag}: {count}人")
            
            if report['recommendations']:
                print("\n详细建议:")
                for rec in report['recommendations'][:10]:  # 只显示前10个
                    print(f"  {rec['customer']}: {', '.join(rec['suggested_tags'])}")
                
                if len(report['recommendations']) > 10:
                    print(f"  ... 还有 {len(report['recommendations']) - 10} 个客户")
            
            print("\n" + "=" * 60)
            return 0
        else:
            print(result["message"])
            return 1
    else:
        # 处理单个客户
        result = add_auto_tags(args.name, dry_run=args.dry_run)
        
        print(result["message"])
        
        if result["success"] and result.get("suggested_tags"):
            print(f"\n建议标签: {', '.join(result['suggested_tags'])}")
            
            if result.get("added_tags"):
                print(f"新添加标签: {', '.join(result['added_tags'])}")
            
            if result.get("all_tags"):
                print(f"\n当前所有标签: {', '.join(result['all_tags'])}")
        
        return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
