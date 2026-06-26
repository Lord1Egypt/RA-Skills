#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大恩营销策划七步法 - 方案生成器
根据项目信息自动生成营销策划方案框架
"""

import json
import os
from datetime import datetime
from pathlib import Path

STATE_DIR = Path(__file__).parent.parent / "state"
PROJECTS_DIR = STATE_DIR / "projects"

def ensure_dirs():
    """确保目录存在"""
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

def create_project(project_name, basic_info):
    """创建新项目"""
    ensure_dirs()
    
    project = {
        "name": project_name,
        "created_at": datetime.now().isoformat(),
        "status": "draft",
        "steps": {
            "step1": {"title": "核心营销课题", "content": "", "completed": False},
            "step2": {"title": "核心操盘思路", "content": "", "completed": False},
            "step3": {"title": "市场分析", "content": "", "completed": False},
            "step4": {"title": "产品优劣势", "content": "", "completed": False},
            "step5": {"title": "项目定位", "content": "", "completed": False},
            "step6": {"title": "故事线", "content": "", "completed": False},
            "step7": {"title": "传播计划", "content": "", "completed": False}
        },
        "basic_info": basic_info
    }
    
    project_file = PROJECTS_DIR / f"{project_name}.json"
    project_file.write_text(json.dumps(project, ensure_ascii=False, indent=2))
    
    return project

def load_project(project_name):
    """加载项目"""
    project_file = PROJECTS_DIR / f"{project_name}.json"
    if project_file.exists():
        return json.loads(project_file.read_text())
    return None

def save_project(project):
    """保存项目"""
    project_file = PROJECTS_DIR / f"{project['name']}.json"
    project_file.write_text(json.dumps(project, ensure_ascii=False, indent=2))

def update_step(project_name, step_num, content):
    """更新某个步骤的内容"""
    project = load_project(project_name)
    if not project:
        return {"error": f"项目 {project_name} 不存在"}
    
    step_key = f"step{step_num}"
    if step_key in project["steps"]:
        project["steps"][step_key]["content"] = content
        project["steps"][step_key]["completed"] = bool(content.strip())
        project["updated_at"] = datetime.now().isoformat()
        save_project(project)
        return {"success": True, "step": step_key}
    
    return {"error": f"无效的步骤编号: {step_num}"}

def generate_report(project_name):
    """生成完整报告"""
    project = load_project(project_name)
    if not project:
        return {"error": f"项目 {project_name} 不存在"}
    
    report = f"""# {project['name']} 营销策划方案

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

---

"""
    
    for i in range(1, 8):
        step_key = f"step{i}"
        step = project["steps"][step_key]
        status = "✅" if step["completed"] else "⏳"
        report += f"## {step['title']} {status}\n\n"
        if step["content"]:
            report += step["content"] + "\n\n"
        else:
            report += "*待填写*\n\n"
        report += "---\n\n"
    
    return {"report": report}

def list_projects():
    """列出所有项目"""
    ensure_dirs()
    projects = []
    for f in PROJECTS_DIR.glob("*.json"):
        project = json.loads(f.read_text())
        completed_steps = sum(1 for s in project["steps"].values() if s["completed"])
        projects.append({
            "name": project["name"],
            "created_at": project["created_at"],
            "progress": f"{completed_steps}/7"
        })
    return projects

# 七步法模板
STEP_TEMPLATES = {
    1: """【课题界定】

本项目面临的核心营销挑战，可归纳为以下课题：

课题一：[课题名称]
• [挑战描述]
• [解决方向]

课题二：[课题名称]
• [挑战描述]
• [解决方向]
""",
    2: """【核心策略】

总体策略方向：______

执行路径：

第一步：[阶段目标]
• [具体动作]
• [具体动作]

第二步：[阶段目标]
• [具体动作]
• [具体动作]

【传播调性】
关键词：______、______、______
""",
    3: """【地段价值】
宏观层面：______
中观层面：______
微观层面：______

【竞品格局】
竞品A：______，本案优势：______
竞品B：______，本案优势：______

【目标客户】
基础画像：______
购买理由：______
购买障碍：______
需求痛点：______
""",
    4: """【核心卖点】

核心卖点一：[卖点名称]
• [支撑点1]
• [支撑点2]

核心卖点二：[卖点名称]
• [支撑点1]
• [支撑点2]

【SWOT分析】
优势：______
劣势：______
机会：______
威胁：______
""",
    5: """【项目定位】
______

【SLOGAN】
______

【SLOGAN释义】
______
""",
    6: """【叙事主题】

第一幕：[层面]——[主题]
______

第二幕：[层面]——[主题]
______

第三幕：[层面]——[主题]
______
""",
    7: """【传播节奏】

阶段一：[阶段名称]（__月-__月）
目标：______
动作：______

阶段二：[阶段名称]（__月-__月）
目标：______
动作：______

阶段三：[阶段名称]（__月-__月）
目标：______
动作：______
"""
}

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python seven_steps.py <命令> [参数]")
        print("命令:")
        print("  new <项目名>           创建新项目")
        print("  list                   列出所有项目")
        print("  template <步骤号>      获取步骤模板")
        print("  update <项目> <步骤>   更新步骤内容")
        print("  report <项目>          生成报告")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "new":
        if len(sys.argv) < 3:
            print("请指定项目名")
        else:
            project = create_project(sys.argv[2], {})
            print(f"✅ 项目已创建: {sys.argv[2]}")
    
    elif cmd == "list":
        projects = list_projects()
        if projects:
            print("项目列表:")
            for p in projects:
                print(f"  • {p['name']} ({p['progress']})")
        else:
            print("暂无项目")
    
    elif cmd == "template":
        if len(sys.argv) < 3:
            print("请指定步骤号 (1-7)")
        else:
            step_num = int(sys.argv[2])
            if step_num in STEP_TEMPLATES:
                print(f"\n=== Step {step_num} 模板 ===\n")
                print(STEP_TEMPLATES[step_num])
    
    elif cmd == "report":
        if len(sys.argv) < 3:
            print("请指定项目名")
        else:
            result = generate_report(sys.argv[2])
            if "report" in result:
                print(result["report"])
            else:
                print(result.get("error", "未知错误"))
    
    else:
        print(f"未知命令: {cmd}")