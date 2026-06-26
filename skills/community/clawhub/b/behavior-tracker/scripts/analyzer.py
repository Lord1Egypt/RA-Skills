#!/usr/bin/env python3
"""
行为分析器 - behavior-tracker 核心
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter

# 配置 - 跨平台路径
OPENCLAW_DIR = Path(os.environ.get("OPENCLAW_DIR", str(Path.home() / ".openclaw")))
WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", str(OPENCLAW_DIR / "workspace")))
MEMORY_DIR = WORKSPACE / "memory"
BEHAVIOR_FILE = MEMORY_DIR / "behavior-patterns.json"
SKILL_DIR = Path(__file__).parent.parent

# 关键词库
KEYWORDS = {
    "topics": [
        "AI Agent", "Python", "C语言", "MiroFish", "OASIS", 
        "N8n", "Moltbook", "EvoMap", "OpenClaw", "Tool", 
        "Memory", "Decorator", "LangChain", "Git", "API"
    ],
    "projects": [
        "N8n", "Moltbook", "EvoMap", "The Machine", 
        "Hostinger", "rapidwebwork", "OpenClaw"
    ],
    "skills": [
        "browser", "search", "memory", "feishu", "imessage"
    ]
}

def load_behavior_data():
    """加载行为数据"""
    if BEHAVIOR_FILE.exists():
        with open(BEHAVIOR_FILE, 'r') as f:
            return json.load(f)
    return {
        "topics": {},
        "projects": {},
        "skills": {},
        "active_hours": {},
        "communication_styles": [],
        "learning_modes": [],
        "total_conversations": 0,
        "last_updated": None
    }

def save_behavior_data(data):
    """保存行为数据"""
    data["last_updated"] = datetime.now().isoformat()
    BEHAVIOR_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(BEHAVIOR_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def extract_from_memory(date_str=None):
    """从记忆文件提取信息"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    memory_file = MEMORY_DIR / f"{date_str}.md"
    if not memory_file.exists():
        return None
    
    with open(memory_file, 'r') as f:
        content = f.read().lower()
    
    found = {"topics": [], "projects": [], "skills": []}
    
    for kw in KEYWORDS["topics"]:
        if kw.lower() in content:
            found["topics"].append(kw)
    
    for kw in KEYWORDS["projects"]:
        if kw.lower() in content:
            found["projects"].append(kw)
    
    for kw in KEYWORDS["skills"]:
        if kw.lower() in content:
            found["skills"].append(kw)
    
    return found

def analyze(days=7):
    """分析最近N天的行为"""
    results = {
        "topics": [],
        "projects": [],
        "skills": [],
        "dates": []
    }
    
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        
        found = extract_from_memory(date_str)
        if found:
            results["topics"].extend(found["topics"])
            results["projects"].extend(found["projects"])
            results["skills"].extend(found["skills"])
            results["dates"].append(date_str)
    
    return results

def update_patterns(analysis):
    """更新行为模式"""
    data = load_behavior_data()
    
    # 确保keys存在
    if "skills" not in data:
        data["skills"] = {}
    if "active_hours" not in data:
        data["active_hours"] = {}
    
    # 更新话题
    for topic in analysis["topics"]:
        data["topics"][topic] = data["topics"].get(topic, 0) + 1
    
    # 更新项目
    for project in analysis["projects"]:
        data["projects"][project] = data["projects"].get(project, 0) + 1
    
    # 更新技能
    for skill in analysis["skills"]:
        data["skills"][skill] = data["skills"].get(skill, 0) + 1
    
    # 更新活跃时间
    hour = datetime.now().hour
    data["active_hours"][str(hour)] = data["active_hours"].get(str(hour), 0) + 1
    
    # 更新总数
    data["total_conversations"] = data.get("total_conversations", 0) + 1
    
    save_behavior_data(data)
    return data

def generate_report(analysis, data):
    """生成报告"""
    from collections import Counter
    
    topic_counts = Counter(analysis["topics"])
    project_counts = Counter(analysis["projects"])
    skill_counts = Counter(analysis["skills"])
    
    report = f"""# 行为分析报告 - {datetime.now().strftime("%Y-%m-%d")}

## 📊 话题统计 (最近7天)
"""
    for topic, count in topic_counts.most_common(10):
        report += f"- **{topic}**: {count}次\n"
    
    report += f"""
## 🛠️ 项目关注 (最近7天)
"""
    for project, count in project_counts.most_common():
        report += f"- **{project}**: {count}次\n"
    
    report += f"""
## 🔧 技能使用 (最近7天)
"""
    for skill, count in skill_counts.most_common():
        report += f"- **{skill}**: {count}次\n"
    
    report += f"""
## 📅 活跃日期
{', '.join(analysis["dates"])}

## 📈 累计统计
- 总对话数: {data.get("total_conversations", 0)}
- 活跃话题数: {len(data.get("topics", {}))}
- 关注项目数: {len(data.get("projects", {}))}

---
生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    return report

def main():
    """主函数"""
    print(f"[{datetime.now()}] 🔍 开始行为分析...")
    
    # 1. 分析最近记忆
    analysis = analyze(days=7)
    print(f"   找到 {len(analysis['topics'])} 个话题, {len(analysis['projects'])} 个项目")
    
    # 2. 更新模式
    data = update_patterns(analysis)
    
    # 3. 生成报告
    report = generate_report(analysis, data)
    report_file = MEMORY_DIR / "behavior-report.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"[{datetime.now()}] ✅ 分析完成!")
    print(f"   话题: {Counter(analysis['topics']).most_common(3)}")
    print(f"   报告: {report_file}")

if __name__ == "__main__":
    main()
