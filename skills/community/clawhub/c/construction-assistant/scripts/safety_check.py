#!/usr/bin/env python3
"""
安全检查记录脚本
生成安全检查报告和整改通知单
"""

import argparse
import json
from datetime import datetime

# 安全检查清单模板
SAFETY_CHECKLIST = {
    "daily": [
        "安全帽佩戴情况",
        "临边防护是否完好",
        "脚手架稳定性",
        "用电安全",
        "消防设施",
        "材料堆放"
    ],
    "special": [
        "深基坑支护",
        "高支模体系",
        "起重机械",
        "临时用电系统",
        "危险化学品管理"
    ],
    "holiday": [
        "值班人员安排",
        "现场封闭管理",
        "断电断水情况",
        "防火防盗措施",
        "应急联系方式"
    ]
}

def create_check_record(check_type, project_name, items, recorder):
    """创建安全检查记录"""
    checklist = SAFETY_CHECKLIST.get(check_type, SAFETY_CHECKLIST["daily"])
    
    record = {
        "project_name": project_name,
        "check_type": check_type,
        "check_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "recorder": recorder,
        "checklist": []
    }
    
    for i, item in enumerate(checklist):
        status = items.get(i, {"status": "待检查", "note": ""})
        record["checklist"].append({
            "item": item,
            "status": status.get("status", "待检查"),
            "note": status.get("note", "")
        })
    
    # 统计
    total = len(record["checklist"])
    passed = sum(1 for c in record["checklist"] if c["status"] == "合格")
    issues = total - passed
    
    record["summary"] = {
        "total": total,
        "passed": passed,
        "issues": issues,
        "pass_rate": f"{passed/total*100:.1f}%" if total > 0 else "0%"
    }
    
    return record

def generate_rectification_notice(project_name, issues, deadline):
    """生成整改通知单"""
    notice = {
        "title": "安全隐患整改通知单",
        "project_name": project_name,
        "issue_date": datetime.now().strftime("%Y-%m-%d"),
        "deadline": deadline,
        "issues": issues,
        "requirements": [
            "按期完成整改",
            "整改完成后报验",
            "举一反三，全面排查"
        ]
    }
    return notice

def main():
    parser = argparse.ArgumentParser(description="安全检查记录工具")
    parser.add_argument("--type", "-t", default="daily", help="检查类型")
    parser.add_argument("--project", "-p", required=True, help="项目名称")
    parser.add_argument("--recorder", "-r", default="安全员", help="记录人")
    parser.add_argument("--output", "-o", help="输出文件")
    
    args = parser.parse_args()
    
    # 示例检查项（实际使用时可通过交互或文件输入）
    items = {
        0: {"status": "合格", "note": ""},
        1: {"status": "合格", "note": ""},
        2: {"status": "整改中", "note": "局部防护松动"},
        3: {"status": "合格", "note": ""},
        4: {"status": "合格", "note": ""},
        5: {"status": "合格", "note": ""}
    }
    
    record = create_check_record(args.type, args.project, items, args.recorder)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        print(f"检查记录已保存到：{args.output}")
    else:
        print(json.dumps(record, ensure_ascii=False, indent=2))
    
    # 如果有问题，生成整改通知
    if record["summary"]["issues"] > 0:
        notice = generate_rectification_notice(
            args.project,
            [c for c in record["checklist"] if c["status"] != "合格"],
            datetime.now().strftime("%Y-%m-%d")
        )
        print("\n--- 整改通知单 ---")
        print(json.dumps(notice, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
