#!/usr/bin/env python3
import os
import json
import time
import uuid
import argparse
from pathlib import Path

PROPOSAL_DIR = os.path.expanduser("~/.openclaw/skill-proposals/")

def generate_proposal(skill_name, demand, version):
    """生成技能优化方案"""
    proposal_id = str(uuid.uuid4())[:8]
    timestamp = int(time.time())
    
    proposal = {
        "proposal_id": proposal_id,
        "skill_name": skill_name,
        "demand": demand,
        "version": version,
        "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp)),
        "timestamp": timestamp,
        "status": "pending",  # pending/approved/rejected/executed
        "change_list": [],
        "risk_assessment": "低风险",
        "expected_effect": "",
        "test_cases": []
    }

    # 保存方案
    os.makedirs(PROPOSAL_DIR, exist_ok=True)
    proposal_path = os.path.join(PROPOSAL_DIR, f"{proposal_id}.json")
    with open(proposal_path, "w", encoding="utf-8") as f:
        json.dump(proposal, f, ensure_ascii=False, indent=2)

    # 生成Markdown格式方案
    md_content = f"""# 技能优化方案 - {proposal_id}

## 基本信息
- **技能名称**: {skill_name}
- **目标版本**: {version}
- **需求背景**: {demand}
- **创建时间**: {proposal['create_time']}
- **方案ID**: {proposal_id}

## 变更内容清单
1. [ ] 待填充具体修改内容

## 影响范围评估
- **风险等级**: {proposal['risk_assessment']}
- 影响范围: 待评估

## 预期效果
{proposal['expected_effect']}

## 测试用例
1. [ ] 待补充测试用例

---
### 确认操作
- 同意方案请回复: `approve {proposal_id}`
- 拒绝方案请回复: `reject {proposal_id} [原因]`
"""

    md_path = os.path.join(PROPOSAL_DIR, f"{proposal_id}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"✅ 方案已生成: {proposal_id}")
    print(f"方案详情路径: {md_path}")
    print("\n" + md_content)
    return proposal_id

def list_proposals(skill_name=None):
    """列出所有方案"""
    if not os.path.exists(PROPOSAL_DIR):
        print("❌ 没有找到任何方案")
        return
    
    proposals = []
    for file in os.listdir(PROPOSAL_DIR):
        if file.endswith(".json"):
            with open(os.path.join(PROPOSAL_DIR, file), "r", encoding="utf-8") as f:
                p = json.load(f)
            if skill_name and p["skill_name"] != skill_name:
                continue
            proposals.append(p)
    
    proposals.sort(key=lambda x: x["timestamp"], reverse=True)
    print(f"📋 技能优化方案列表 (共{len(proposals)}个):")
    print("-" * 100)
    print(f"{'方案ID':<10} {'技能名称':<18} {'目标版本':<8} {'状态':<10} {'创建时间':<20} {'需求'}")
    print("-" * 100)
    for p in proposals:
        demand = p["demand"][:30] + "..." if len(p["demand"]) > 30 else p["demand"]
        print(f"{p['proposal_id']:<10} {p['skill_name']:<18} {p['version']:<8} {p['status']:<10} {p['create_time']:<20} {demand}")

def approve_proposal(proposal_id):
    """审批通过方案"""
    proposal_path = os.path.join(PROPOSAL_DIR, f"{proposal_id}.json")
    if not os.path.exists(proposal_path):
        print(f"❌ 方案 {proposal_id} 不存在")
        exit(1)
    with open(proposal_path, "r", encoding="utf-8") as f:
        proposal = json.load(f)
    proposal["status"] = "approved"
    proposal["approve_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(proposal_path, "w", encoding="utf-8") as f:
        json.dump(proposal, f, ensure_ascii=False, indent=2)
    print(f"✅ 方案 {proposal_id} 已审批通过，可以开始执行修改")

def reject_proposal(proposal_id, reason=""):
    """拒绝方案"""
    proposal_path = os.path.join(PROPOSAL_DIR, f"{proposal_id}.json")
    if not os.path.exists(proposal_path):
        print(f"❌ 方案 {proposal_id} 不存在")
        exit(1)
    with open(proposal_path, "r", encoding="utf-8") as f:
        proposal = json.load(f)
    proposal["status"] = "rejected"
    proposal["reject_reason"] = reason
    proposal["reject_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(proposal_path, "w", encoding="utf-8") as f:
        json.dump(proposal, f, ensure_ascii=False, indent=2)
    print(f"❌ 方案 {proposal_id} 已拒绝")
    if reason:
        print(f"拒绝原因: {reason}")

def main():
    parser = argparse.ArgumentParser(description="技能优化方案管理")
    subparsers = parser.add_subparsers(dest="action", required=True)
    
    # 生成方案
    generate_parser = subparsers.add_parser("generate", help="生成优化方案")
    generate_parser.add_argument("skill_name", help="技能名称")
    generate_parser.add_argument("demand", help="优化需求描述")
    generate_parser.add_argument("--version", default="v1.0.0", help="目标版本号")
    
    # 列出方案
    list_parser = subparsers.add_parser("list", help="列出所有方案")
    list_parser.add_argument("--skill", help="指定技能名称，只查看该技能的方案")
    
    # 审批通过方案
    approve_parser = subparsers.add_parser("approve", help="审批通过方案")
    approve_parser.add_argument("proposal_id", help="方案ID")
    
    # 拒绝方案
    reject_parser = subparsers.add_parser("reject", help="拒绝方案")
    reject_parser.add_argument("proposal_id", help="方案ID")
    reject_parser.add_argument("--reason", default="", help="拒绝原因")
    
    args = parser.parse_args()
    
    if args.action == "generate":
        generate_proposal(args.skill_name, args.demand, args.version)
    elif args.action == "list":
        list_proposals(args.skill)
    elif args.action == "approve":
        approve_proposal(args.proposal_id)
    elif args.action == "reject":
        reject_proposal(args.proposal_id, args.reason)

if __name__ == "__main__":
    main()
