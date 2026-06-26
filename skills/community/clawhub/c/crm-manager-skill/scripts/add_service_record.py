#!/usr/bin/env python3
"""
添加服务记录

用法:
    python add_service_record.py <name> --type <type> --description <description> [options]

示例:
    python add_service_record.py "李雷" --type "单次服务" --description "健身课，深蹲从50kg进步到60kg" --attendance "出席" --duration 60 --progress "良好"
    python add_service_record.py "王芳" --type "课程购买" --description "购买10次心理咨询课程" --amount 3000 --outcome "成功"
"""

import os
import sys
import yaml
import argparse
from datetime import datetime

# 服务类型枚举
SERVICE_TYPES = ["课程购买", "单次服务", "体验课", "续费", "课程调整", "进度评估", "反馈沟通"]

# 出勤状态枚举
ATTENDANCE_STATUS = ["出席", "缺席", "请假", "补课"]

# 进度评级枚举
PROGRESS_RATINGS = ["优秀", "良好", "一般", "需加强"]

# 结果状态枚举
OUTCOME_STATUS = ["成功", "失败", "进行中"]


def generate_record_id(service_records):
    """生成新的服务记录ID"""
    if not service_records:
        return "SR001"
    
    # 找到最大的ID号
    max_num = 0
    for record in service_records:
        record_id = record.get('id', '')
        if record_id.startswith('SR'):
            try:
                num = int(record_id[2:])
                max_num = max(max_num, num)
            except ValueError:
                pass
    
    return f"SR{str(max_num + 1).zfill(3)}"


def add_service_record(name, type, description, attendance=None, duration=None, 
                       progress=None, amount=None, outcome=None, related_note_id=None, date=None):
    """
    为客户添加服务记录
    
    Args:
        name: 客户姓名
        type: 服务类型（课程购买/单次服务/体验课/续费/课程调整/进度评估/反馈沟通）
        description: 描述说明
        attendance: 出勤状态（可选）
        duration: 服务时长（分钟，可选）
        progress: 进度评级（可选）
        amount: 涉及金额（可选）
        outcome: 结果状态（可选）
        related_note_id: 关联的跟进记录ID（可选）
        date: 发生日期（可选，默认今天）
    
    Returns:
        dict: 操作结果
    """
    # 验证服务类型
    if type not in SERVICE_TYPES:
        return {
            "success": False,
            "message": f"无效的服务类型: {type}。有效类型: {', '.join(SERVICE_TYPES)}"
        }
    
    # 验证出勤状态（如果提供）
    if attendance and attendance not in ATTENDANCE_STATUS:
        return {
            "success": False,
            "message": f"无效的出勤状态: {attendance}。有效状态: {', '.join(ATTENDANCE_STATUS)}"
        }
    
    # 验证进度评级（如果提供）
    if progress and progress not in PROGRESS_RATINGS:
        return {
            "success": False,
            "message": f"无效的进度评级: {progress}。有效评级: {', '.join(PROGRESS_RATINGS)}"
        }
    
    # 验证结果状态（如果提供）
    if outcome and outcome not in OUTCOME_STATUS:
        return {
            "success": False,
            "message": f"无效的结果状态: {outcome}。有效状态: {', '.join(OUTCOME_STATUS)}"
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
    
    # 获取现有服务记录列表（兼容旧数据sales_activities）
    if "service_records" not in record or record["service_records"] is None:
        # 尝试读取旧字段名
        if "sales_activities" in record and record["sales_activities"]:
            record["service_records"] = record["sales_activities"]
        else:
            record["service_records"] = []
    
    # 生成记录ID
    record_id = generate_record_id(record["service_records"])
    
    # 设置日期（默认今天）
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # 如果未提供结果，默认"进行中"
    if not outcome:
        outcome = "进行中"
    
    # 构建服务记录
    service_record = {
        "id": record_id,
        "date": date,
        "type": type,
        "description": description,
        "outcome": outcome
    }
    
    # 添加可选字段
    if attendance:
        service_record["attendance"] = attendance
    if duration:
        service_record["duration"] = duration
    if progress:
        service_record["progress"] = progress
    if amount:
        service_record["amount"] = amount
    if related_note_id:
        service_record["related_note_id"] = related_note_id
    
    # 添加到列表
    record["service_records"].append(service_record)
    
    # 更新最后联系时间
    record["last_contact"] = date
    
    # 根据结果更新客户状态
    if outcome == "成功" and type in ["课程购买", "续费"]:
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
        "message": f"已为 {name} 添加服务记录 [{record_id}]",
        "data": {
            "record": service_record,
            "total_records": len(record["service_records"])
        }
    }


def main():
    # 修复 Windows 控制台输出编码问题
    import sys
    import io
    if sys.platform == 'win32' and sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    parser = argparse.ArgumentParser(description="添加服务记录")
    parser.add_argument("name", help="客户姓名")
    parser.add_argument("--type", required=True, help="服务类型（课程购买/单次服务/体验课/续费/课程调整/进度评估/反馈沟通）")
    parser.add_argument("--description", required=True, help="描述说明")
    parser.add_argument("--attendance", help="出勤状态（出席/缺席/请假/补课）")
    parser.add_argument("--duration", type=int, help="服务时长（分钟）")
    parser.add_argument("--progress", help="进度评级（优秀/良好/一般/需加强）")
    parser.add_argument("--amount", type=float, help="涉及金额")
    parser.add_argument("--outcome", help="结果状态（成功/失败/进行中）")
    parser.add_argument("--related-note-id", help="关联的跟进记录ID")
    parser.add_argument("--date", help="发生日期（格式：YYYY-MM-DD，默认为今天）")
    
    args = parser.parse_args()
    
    result = add_service_record(
        name=args.name,
        type=args.type,
        description=args.description,
        attendance=args.attendance,
        duration=args.duration,
        progress=args.progress,
        amount=args.amount,
        outcome=args.outcome,
        related_note_id=args.related_note_id,
        date=args.date
    )
    
    print(result["message"])
    if result["success"]:
        print(f"当前共有 {result['data']['total_records']} 条服务记录")
        print(f"记录详情: {result['data']['record']['id']} - {result['data']['record']['type']}")
    
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
