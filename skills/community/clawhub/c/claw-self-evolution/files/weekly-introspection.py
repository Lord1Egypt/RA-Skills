#!/usr/bin/env python3
"""
每周自省反思
自动总结一周工作，找出当前可以优化改进的点，生成反思报告
真正做到：每周复盘，持续进化
"""

import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional

REPORT_DIR = "/app/working/logs/introspection/"
MEMORY_DIR = "/app/working/memory/"

def get_recent_changes(days: int = 7) -> List[Dict]:
    """获取最近几天修改的文件，分析做了什么"""
    print("🔍 分析最近一周修改记录...")
    changes = []
    cutoff = datetime.now() - timedelta(days=days)
    
    # 关键目录扫描
    scan_dirs = [
        ("/app/working/scripts/", "脚本修改"),
        ("/app/working/skills/", "技能修改"),
        ("/app/working/memory/", "记忆文档修改"),
        ("/app/working/", "根目录配置修改"),
    ]
    
    for root_dir, category in scan_dirs:
        for root, dirs, files in os.walk(root_dir):
            # 跳过git和缓存
            if ".git" in root or "__pycache__" in root or "node_modules" in root:
                continue
            for f in files:
                filepath = os.path.join(root, f)
                try:
                    mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if mtime > cutoff:
                        rel_path = filepath.replace("/app/working/", "")
                        changes.append({
                            "path": rel_path,
                            "mtime": mtime,
                            "category": category,
                            "ext": os.path.splitext(f)[1]
                        })
                except:
                    continue
    
    # 按时间排序
    changes.sort(key=lambda x: x["mtime"], reverse=True)
    print(f"📊 最近一周发现 {len(changes)} 个文件修改")
    return changes

def analyze_work_topics(changes: List[Dict]) -> Dict:
    """分析最近工作主题"""
    topics = {
        "底座优化": 0,
        "安全加固": 0,
        "技能开发": 0,
        "文件规范": 0,
        "定时任务": 0,
        "业务功能": 0,
        "其他": 0
    }
    
    keywords = {
        "底座优化": ["base", "permission", "cache", "规范", "目录", "权限", "节能", "clean", "整理"],
        "安全加固": ["security", "audit", "scan", "安全", "检查", "baseline"],
        "技能开发": ["skill", "intention", "syncer", "predict", "开发", "创建"],
        "文件规范": ["index", "structure", "archive", "清理", "冗余"],
        "定时任务": ["cron", "job", "schedule", "定时", "task", "daily", "weekly"],
        "业务功能": ["fund", "monitor", "api", "finance", "push", "播报"],
    }
    
    for change in changes:
        path = change["path"].lower()
        matched = False
        for topic, keys in keywords.items():
            for key in keys:
                if key.lower() in path:
                    topics[topic] += 1
                    matched = True
                    break
            if matched:
                break
        if not matched:
            topics["其他"] += 1
    
    # 找出主要话题
    main_topics = sorted([(v, k) for k, v in topics.items() if v > 0], reverse=True)
    return {
        "topic_counts": topics,
        "main_topics": main_topics
    }

def find_improvement_points(changes: List[Dict], topic_analysis: Dict) -> List[str]:
    """基于最近工作，找出可以改进的点"""
    improvements = []
    
    # 检查是否还有冗余文件
    if any("archive" in c["path"] or "clean" in c["path"] for c in changes):
        improvements.append("✅ 根目录已经清理干净，但可以再检查一遍是否还有冗余文件可以归档")
    
    # 检查权限问题
    if any("permission" in c["path"] or "chown" in c["path"] for c in changes):
        improvements.append("🔍 权限问题刚修复过，下周可以再抽查几个关键缓存文件确认权限仍然正确")
    
    # 检查技能合并
    if any("merge" in c["path"] or "delete" in c["path"] and "skill" in c["path"] for c in changes):
        improvements.append("🧹 刚清理合并了技能，可以再检查一下索引是否都同步正确")
    
    # 检查自我进化相关
    if any("introspect" in c["path"] or "evolution" in c["path"] or "self" in c["path"] for c in changes):
        improvements.append("🚀 新增了自省反思能力，可以观察运行一个礼拜看看效果，根据体验调整频率")
    
    # 检查智能意图预判
    if any("intention" in c["path"] or "predict" in c["path"] for c in changes):
        improvements.append("🎯 新增了智能意图预判，可以多测试几次，看看预判准确率，不准可以再训练")
    
    # 检查基金监控
    if any("fund" in c["path"] for c in changes):
        improvements.append("📊 基金监控已经配置完成，明天开始第一次推送，观察推送格式是否符合预期")
    
    # 检查token节能
    improvements.append("🔋 检查最近一周token平均用量，看看缓存机制生效了没有，有没有可以再优化的地方")
    
    # 检查自动化
    improvements.append("🤖 看看还有哪些手动操作可以改成自动，减少人工干预")
    
    # 检查备份
    improvements.append("💾 确认核心备份机制正常运行，恢复测试没问题")
    
    return improvements

def generate_report(changes: List[Dict], topic_analysis: Dict, improvements: List[str]) -> str:
    """生成自省报告Markdown"""
    now = datetime.now()
    start = now - timedelta(days=7)
    
    main_topics = topic_analysis["main_topics"]
    topic_counts = topic_analysis["topic_counts"]
    
    report = f"# 🧠 每周自省反思报告 - {start.strftime('%Y-%m-%d')} ~ {now.strftime('%Y-%m-%d')}\n\n"
    
    # 总体统计
    report += "## 📊 一周工作统计\n\n"
    report += f"- **修改文件总数**: {len(changes)} 个\n"
    report += "- **主要工作主题**:\n"
    for count, topic in main_topics[:5]:
        if count > 0:
            report += f"  - {topic}: {count} 个文件修改\n"
    report += "\n"
    
    # 工作总结
    report += "## 📝 工作总结\n\n"
    if "底座优化" in [t[1] for t in main_topics[:3]]:
        report += "这一周主要在 **夯实底层底座**，做了:\n"
        report += "- 目录规范整理\n"
        report += "- 权限问题修复\n"
        report += "- 清理冗余技能\n"
        report += "- 合并重复功能\n"
        report += "- 构建自我进化能力\n"
        report += "\n底座越来越稳固，为上层业务打下坚实基础 ✅\n\n"
    
    if "技能开发" in [t[1] for t in main_topics[:3]]:
        report += "这一周新增/优化了这些技能:\n"
        report += "- ✅ `intention-prediction` - 智能意图预判\n"
        report += "- ✅ `memory-syncer` - 合并自动同步功能\n"
        report += "- ✅ `service-health-check` - 服务健康监控自动恢复\n"
        report += "- ✅ `auto-user-profile` - 自动用户画像学习\n"
        report += "\n"
    
    if "业务功能" in [t[1] for t in main_topics[:3]]:
        report += "这一周主要开发业务功能:\n"
        report += "- ✅ 基金监控每日飞书播报\n"
        report += "- ✅ 免费金融API对接\n"
        report += "\n"
    
    # 🧠 整合 self-improving-agent 学习记录
    report += "## 📚 本周学习记录汇总\n\n"
    learning_dir = "/app/working/memory/learnings/"
    
    # 读取各文件记录
    have_learning = False
    for fname, title in [
        ("ERRORS.md", "❌ 错误记录"),
        ("LEARNINGS.md", "🧠 经验教训"), 
        ("FEATURE_REQUESTS.md", "🚀 功能需求")
    ]:
        fpath = os.path.join(learning_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
                entries = content.count('## ')
                if entries > 0:
                    report += f"- **{title}**: {entries} 条记录\n"
                    have_learning = True
    
    if not have_learning:
        report += "- 暂无学习记录\n"
    report += "\n"
    
    # 从功能需求提取改进点
    from collections import defaultdict
    feature_path = os.path.join(learning_dir, "FEATURE_REQUESTS.md")
    if os.path.exists(feature_path):
        with open(feature_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 找出未实现的需求
            lines = content.split('\n')
            for line in lines:
                if '[ ]' in line and '优先级' not in line:
                    # 提取需求标题
                    if line.startswith('## '):
                        improvements.append(line[3:].strip() + " (用户需求)")
    
    # 改进点
    report += "## 🔍 发现可优化改进点\n\n"
    if not improvements:
        report += "- ✅ 暂无需要改进的地方，一切正常\n"
    else:
        for i, imp in enumerate(improvements, 1):
            report += f"{i}. {imp}\n"
    report += "\n"
    
    # 下一步计划
    report += "## 🚀 下周计划\n\n"
    report += "1. 持续验证自我进化闭环，观察自动化运行效果\n"
    report += "2. 根据本周体验，调整优化频率和策略\n"
    report += "3. 如果发现问题，立即改进\n"
    report += "\n"
    
    report += "---\n"
    report += f"*自动生成 - {now.strftime('%Y-%m-%d %H:%M')}*\n"
    report += "*持续进化，每天进步一点点*\n"
    
    return report

def main():
    print("🧠 开始每周自省反思...")
    
    changes = get_recent_changes(7)
    topic_analysis = analyze_work_topics(changes)
    improvements = find_improvement_points(changes, topic_analysis)
    report = generate_report(changes, topic_analysis, improvements)
    
    # 保存报告
    os.makedirs(REPORT_DIR, exist_ok=True)
    filename = f"introspection-{datetime.now().strftime('%Y%m%d')}.md"
    filepath = os.path.join(REPORT_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📝 报告已保存: {filepath}")
    print("\n" + "="*60)
    print(report)
    print("="*60)
    
    # 如果有改进点，退出码1触发推送
    if improvements:
        print(f"\n🔍 发现 {len(improvements)} 个改进点，推送报告请求审阅")
        sys.exit(1)
    else:
        print("\n✅ 没有需要改进的地方，一切正常")
        sys.exit(0)

if __name__ == "__main__":
    main()
