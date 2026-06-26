#!/usr/bin/env python3
"""
查询客户详情

用法:
    python query_customer.py <name>

示例:
    python query_customer.py "李雷"
"""

import os
import sys
import yaml
import argparse


def query_customer(name):
    """
    查询客户详细信息
    
    Args:
        name: 客户姓名
    
    Returns:
        dict: 操作结果
    """
    # 数据目录
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'customers')
    file_path = os.path.join(data_dir, f"{name}.yaml")
    
    # 检查客户是否存在
    if not os.path.exists(file_path):
        return {
            "success": False,
            "message": f"客户 {name} 不存在"
        }
    
    # 读取记录
    with open(file_path, "r", encoding="utf-8") as f:
        record = yaml.safe_load(f)
    
    return {
        "success": True,
        "message": f"找到客户 {name}",
        "data": record
    }


def format_customer_info(record):
    """格式化客户信息输出"""
    lines = []
    lines.append(f"客户姓名: {record.get('name', 'N/A')}")
    lines.append(f"联系电话: {record.get('phone', 'N/A')}")
    lines.append(f"邮箱地址: {record.get('email', 'N/A')}")
    lines.append(f"性别年龄: {record.get('gender', '未知')} / {record.get('age', '未设置')}岁")
    lines.append(f"客户等级: {record.get('level', '普通')}")
    lines.append(f"客户来源: {record.get('source', '未设置') or '未设置'}")
    lines.append(f"标签: {', '.join(record.get('tags', [])) or '无'}")
    lines.append(f"当前状态: {record.get('status', '新增')}")
    lines.append(f"最后联系: {record.get('last_contact') or '无'}")
    
    # 服务记录
    service_records = record.get('service_records', record.get('sales_activities', []))
    if service_records:
        lines.append(f"\n服务记录（共{len(service_records)}条）:")
        for i, record_item in enumerate(service_records, 1):
            # 处理旧数据（sales_activities）和新数据（service_records）的字段差异
            record_type = record_item.get('type', 'N/A')
            stage = record_item.get('stage', '')
            amount = record_item.get('amount')
            product = record_item.get('product', '')
            attendance = record_item.get('attendance', '')
            duration = record_item.get('duration')
            progress = record_item.get('progress', '')
            
            lines.append(f"  {i}. [{record_item.get('id', 'N/A')}] {record_item.get('date', 'N/A')}")
            
            # 构建类型/阶段/出勤信息
            type_info = f"类型: {record_type}"
            if stage:
                type_info += f" | 阶段: {stage}"
            if attendance:
                type_info += f" | 出勤: {attendance}"
            type_info += f" | 结果: {record_item.get('outcome', 'N/A')}"
            lines.append(f"     {type_info}")
            
            # 显示进度和时长（如果存在）
            if duration or progress:
                extra_info = []
                if duration:
                    extra_info.append(f"时长: {duration}分钟")
                if progress:
                    extra_info.append(f"进度: {progress}")
                if extra_info:
                    lines.append(f"     {' | '.join(extra_info)}")
            
            # 显示金额和产品（兼容旧数据）
            if amount or product:
                financial_info = []
                if product:
                    financial_info.append(f"产品: {product}")
                if amount:
                    financial_info.append(f"金额: {amount}元")
                if financial_info:
                    lines.append(f"     {' | '.join(financial_info)}")
            
            lines.append(f"     描述: {record_item.get('description', 'N/A')}")
    else:
        lines.append("\n服务记录: 暂无")
    
    # 跟进记录
    notes = record.get('notes', [])
    if notes:
        lines.append(f"\n跟进记录（共{len(notes)}条）:")
        for i, note in enumerate(notes, 1):
            lines.append(f"  {i}. {note}")
    else:
        lines.append("\n跟进记录: 暂无")
    
    return "\n".join(lines)


def main():
    # 修复 Windows 控制台输出编码问题
    import sys
    import io
    if sys.platform == 'win32' and sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    parser = argparse.ArgumentParser(description="查询客户详情")
    parser.add_argument("name", help="客户姓名")
    
    args = parser.parse_args()
    
    result = query_customer(args.name)
    
    if result["success"]:
        print(format_customer_info(result["data"]))
        return 0
    else:
        print(result["message"])
        return 1


if __name__ == "__main__":
    sys.exit(main())