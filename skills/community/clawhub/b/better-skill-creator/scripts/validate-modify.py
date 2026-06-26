#!/usr/bin/env python3
import os
import json
import sys
from config import *

def has_approved_proposal(skill_name):
    """检查是否有已审批的方案"""
    if not REQUIRE_PROPOSAL_APPROVAL:
        return True, "未开启方案强制审批"
    
    if not os.path.exists(PROPOSAL_DIR):
        return False, "未找到任何已审批的优化方案，请先创建并审批方案"
    
    for file in os.listdir(PROPOSAL_DIR):
        if not file.endswith(".json"):
            continue
        with open(os.path.join(PROPOSAL_DIR, file), "r", encoding="utf-8") as f:
            proposal = json.load(f)
        if proposal.get("skill_name") == skill_name and proposal.get("status") == "approved":
            return True, f"找到已审批方案: {proposal['proposal_id']} - {proposal['demand']}"
    
    return False, f"技能 {skill_name} 没有已审批的优化方案，请先执行：\npython scripts/proposal.py generate <需求描述>\npython scripts/proposal.py approve <方案ID>"

def check_risk(skill_path):
    """评估修改风险"""
    if not ENABLE_RISK_CONFIRM:
        return True, "未开启风险确认"
    
    # 简单风险评估逻辑
    risk_level = "低风险"
    risk_desc = []
    
    # 检查是否修改SKILL.md的description
    skill_md = os.path.join(skill_path, "SKILL.md")
    if os.path.exists(skill_md):
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()
        if "description:" in content:
            risk_level = "中风险"
            risk_desc.append("修改了技能触发描述，可能影响技能触发逻辑")
    
    # 检查是否修改scripts目录下的文件
    scripts_dir = os.path.join(skill_path, "scripts")
    if os.path.exists(scripts_dir):
        script_files = [f for f in os.listdir(scripts_dir) if f.endswith(".py")]
        if script_files:
            risk_level = "高风险"
            risk_desc.append("修改了核心脚本代码，可能影响技能功能")
    
    # 判断是否需要确认
    threshold_order = {"低风险": 1, "中风险": 2, "高风险": 3}
    if threshold_order[risk_level] >= threshold_order[RISK_CONFIRM_THRESHOLD]:
        return False, f"本次修改风险等级: {risk_level}\n风险点: {'; '.join(risk_desc)}\n是否继续执行修改？"
    
    return True, f"本次修改风险等级: {risk_level}"

def main():
    if len(sys.argv) < 2:
        print("用法: python validate-modify.py <skill-path>")
        exit(1)
    
    skill_path = sys.argv[1]
    skill_name = os.path.basename(os.path.normpath(skill_path))
    
    # 检查方案审批
    proposal_ok, proposal_msg = has_approved_proposal(skill_name)
    if not proposal_ok:
        print(f"❌ 方案校验失败: {proposal_msg}")
        exit(1)
    print(f"✅ {proposal_msg}")
    
    # 检查风险
    risk_ok, risk_msg = check_risk(skill_path)
    if not risk_ok:
        print(f"⚠️  风险提示: {risk_msg}")
        confirm = input("请输入y确认继续，其他键取消: ")
        if confirm.lower() != "y":
            print("❌ 修改已取消")
            exit(1)
    print(f"✅ {risk_msg}")
    
    print("\n✅ 校验通过，可以执行修改")
    exit(0)

if __name__ == "__main__":
    main()
