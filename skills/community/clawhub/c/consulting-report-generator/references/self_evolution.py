#!/usr/bin/env python3
"""
通用报告生成器 — 自进化系统 v1
====================================
功能：
1. 技能发现引擎 — 扫描 ~/.workbuddy/skills/ 发现新技能
2. 使用追踪引擎 — 记录布局模式使用频率与效果
3. 错误学习引擎 — 记录错误与修复方案
4. 模板优化引擎 — 基于使用数据优化模板推荐

用法：
    python self_evolution.py scan       # 技能发现扫描
    python self_evolution.py status     # 查看进化状态
    python self_evolution.py log        # 查看使用日志摘要
    
数据目录：
    self_evolution/
    ├── known_skills.json
    ├── usage_log.json
    ├── error_log.json
    ├── improvements.json
    ├── template_stats.json
    └── evolution_summary.md
"""

import os, sys, json, glob
from datetime import datetime

# ═══════════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════════

SKILLS_DIR = os.path.expanduser("~/.workbuddy/skills")
EVO_DIR = "self_evolution"

# 已知的相关技能关键词（用于相关性评估）
RELEVANCE_KEYWORDS = [
    "ppt", "报告", "presentation", "slide", "pptx",
    "精益", "制造", "数字化", "咨询",
    "数据", "chart", "图表", "分析", "analysis",
    "expert", "专家", "库存", "计划", "物控",
    "design", "设计", "字体", "font", "排版",
    "humanizer", "润色", "writing",
    "六西格玛", "sixsigma", "kaizen",
    "search", "搜索", "research", "研究",
]

# 标准技能生态（已知集成的技能）
STANDARD_SKILLS = {
    "设计引擎": ["mck-ppt-design"],
    "分析诊断": ["ie-expert", "rohoon-6sigma", "kaizen", "sixsigma"],
    "库存分析": ["inventory-eye", "inventory-demand-planning"],
    "计划物控": ["planning-mc-assistant", "supply-chain-bom-analyzer"],
    "精益工具": ["lean-production-toolkit", "manufacturing-consulting-toolkit"],
    "通用分析": ["chart-visualization", "data-analysis-report", "academic-deep-research"],
    "战略规划": ["cio", "afrexai-change-management-plan"],
    "进化辅助": ["self-improving-agent", "self-reflection", "proactive-agent"],
    "润色输出": ["humanizer-zh", "humanizer", "manufacturing-expert"],
}


# ═══════════════════════════════════════════════════════════
# 数据管理
# ═══════════════════════════════════════════════════════════

def ensure_evo_dir():
    """确保进化数据目录存在"""
    try:
        os.makedirs(EVO_DIR, exist_ok=True)
        for fname, default in [
            ("known_skills.json", "[]"),
            ("usage_log.json", "[]"),
            ("error_log.json", "[]"),
            ("improvements.json", "[]"),
            ("template_stats.json", "{}"),
        ]:
            fpath = os.path.join(EVO_DIR, fname)
            if not os.path.exists(fpath):
                with open(fpath, 'w') as f:
                    f.write(default)
    except (OSError, PermissionError) as e:
        print(f"⚠️ 进化数据目录创建失败: {e}")
        print("  将使用内存模式运行，数据不会被持久化")


def load_json(fname):
    """加载 JSON 数据"""
    fpath = os.path.join(EVO_DIR, fname)
    if os.path.exists(fpath):
        with open(fpath, 'r') as f:
            return json.load(f)
    return []


def save_json(fname, data):
    """保存 JSON 数据"""
    with open(os.path.join(EVO_DIR, fname), 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════
# 1. 技能发现引擎
# ═══════════════════════════════════════════════════════════

def assess_relevance(skill_name, description=""):
    """评估技能与报告生成的相关性"""
    text = f"{skill_name} {description}".lower()
    score = 0
    for kw in RELEVANCE_KEYWORDS:
        if kw.lower() in text:
            score += 1
    return score


def scan_new_skills():
    """扫描 ~/.workbuddy/skills/ 发现新技能"""
    ensure_evo_dir()
    known = load_json("known_skills.json")
    known_names = {s.get("name", "") for s in known}
    
    new_skills = []
    
    if not os.path.exists(SKILLS_DIR):
        print(f"⚠️ 技能目录不存在: {SKILLS_DIR}")
        return new_skills
    
    for skill_dir in sorted(os.listdir(SKILLS_DIR)):
        skill_path = os.path.join(SKILLS_DIR, skill_dir)
        if not os.path.isdir(skill_path):
            continue
        
        # 读取 SKILL.md 获取描述
        description = ""
        skill_md = os.path.join(skill_path, "SKILL.md")
        if os.path.exists(skill_md):
            with open(skill_md, 'r', errors='ignore') as f:
                for line in f:
                    if 'description:' in line:
                        description = line.split('description:')[-1].strip().strip('>| ')
                        break
        
        # 判断是否已知
        if skill_dir not in known_names:
            relevance = assess_relevance(skill_dir, description)
            if relevance >= 2:  # 相关性阈值
                new_skills.append({
                    "name": skill_dir,
                    "description": description[:100],
                    "relevance_score": relevance,
                    "discovered_at": datetime.now().isoformat(),
                    "status": "new",
                })
                print(f"  🔍 发现新技能: {skill_dir} (相关度:{relevance})")
        else:
            # 检查版本变更
            for known_skill in known:
                if known_skill.get("name") == skill_dir:
                    # 已有记录，检查新增的属性
                    pass
    
    # 更新已知列表
    for ns in new_skills:
        known.append(ns)
    save_json("known_skills.json", known)
    
    return new_skills


# ═══════════════════════════════════════════════════════════
# 2. 使用追踪引擎
# ═══════════════════════════════════════════════════════════

def log_usage(content_type, template_used, modes_used, success=True):
    """记录一次使用"""
    ensure_evo_dir()
    usage = load_json("usage_log.json")
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "content_type": content_type,
        "template": template_used,
        "modes_used": modes_used,
        "success": success,
        "graphics_count": 0,
    }
    usage.append(entry)
    
    # 只保留最近100条
    if len(usage) > 100:
        usage = usage[-100:]
    
    save_json("usage_log.json", usage)
    
    # 更新模板统计
    stats = load_json("template_stats.json")
    if template_used not in stats:
        stats[template_used] = {"count": 0, "success": 0}
    stats[template_used]["count"] += 1
    if success:
        stats[template_used]["success"] += 1
    save_json("template_stats.json", stats)


# ═══════════════════════════════════════════════════════════
# 3. 错误学习引擎
# ═══════════════════════════════════════════════════════════

def log_error(error_type, description, resolution=""):
    """记录一次错误"""
    ensure_evo_dir()
    errors = load_json("error_log.json")
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "type": error_type,
        "description": description,
        "resolution": resolution,
        "fixed": bool(resolution),
    }
    errors.append(entry)
    
    # 只保留最近50条
    if len(errors) > 50:
        errors = errors[-50:]
    
    save_json("error_log.json", errors)


# ═══════════════════════════════════════════════════════════
# 4. 模板优化引擎
# ═══════════════════════════════════════════════════════════

def get_template_recommendation(content_type):
    """根据使用统计推荐最佳模板"""
    stats = load_json("template_stats.json")
    
    # 找到该内容类型下成功率最高的模板
    best_template = None
    best_score = -1
    
    for tmpl, data in stats.items():
        if tmpl.startswith(content_type) or content_type in tmpl:
            score = data["success"] / max(data["count"], 1)
            if score > best_score:
                best_score = score
                best_template = tmpl
    
    return best_template


# ═══════════════════════════════════════════════════════════
# 5. 进化摘要生成
# ═══════════════════════════════════════════════════════════

def generate_summary():
    """生成进化摘要"""
    ensure_evo_dir()
    
    known = load_json("known_skills.json")
    usage = load_json("usage_log.json")
    errors = load_json("error_log.json")
    stats = load_json("template_stats.json")
    
    lines = []
    lines.append("# 技能进化摘要")
    lines.append(f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    
    # 技能统计
    lines.append("## 技能生态")
    lines.append(f"- 已知技能：{len(known)} 个")
    lines.append(f"- 待发现：扫描 ~/.workbuddy/skills/ 获取最新")
    lines.append("")
    
    # 使用统计
    lines.append("## 使用统计")
    lines.append(f"- 总使用次数：{len(usage)}")
    if usage:
        last = usage[-1]
        lines.append(f"- 最近使用：{last.get('content_type', '未知')} ({last['timestamp'][:10]})")
    lines.append("")
    
    # 模板统计
    lines.append("## 模板使用排名")
    sorted_stats = sorted(stats.items(), key=lambda x: x[1]["count"], reverse=True)
    for tmpl, data in sorted_stats[:5]:
        rate = data["success"] / max(data["count"], 1) * 100
        lines.append(f"- {tmpl}: {data['count']}次 (成功率{rate:.0f}%)")
    lines.append("")
    
    # 错误分析
    lines.append("## 错误分析")
    if errors:
        error_types = {}
        for e in errors:
            et = e.get("type", "unknown")
            error_types[et] = error_types.get(et, 0) + 1
        for et, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True)[:5]:
            lines.append(f"- {et}: {count}次")
    else:
        lines.append("- 暂无错误记录")
    
    summary = "\n".join(lines)
    
    with open(os.path.join(EVO_DIR, "evolution_summary.md"), 'w') as f:
        f.write(summary)
    
    return summary


# ═══════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("用法: python self_evolution.py <命令>")
        print("命令:")
        print("  scan    扫描 ~/.workbuddy/skills/ 发现新技能")
        print("  status  查看进化状态摘要")
        print("  log     查看使用日志摘要")
        print("  summary 生成进化摘要")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "scan":
        print("🔍 正在扫描技能目录...")
        print(f"   目标: {SKILLS_DIR}")
        new_skills = scan_new_skills()
        if new_skills:
            print(f"\n✅ 发现 {len(new_skills)} 个新技能:")
            for s in new_skills:
                print(f"   - {s['name']} (相关度:{s['relevance_score']})")
        else:
            print("\n✅ 未发现新技能")
    
    elif cmd == "status":
        known = load_json("known_skills.json")
        usage = load_json("usage_log.json")
        errors = load_json("error_log.json")
        
        print("📊 技能自进化系统 — 状态")
        print(f"{'='*40}")
        print(f"  已知技能:     {len(known)}")
        print(f"  使用记录:     {len(usage)}")
        print(f"  错误记录:     {len(errors)}")
        print(f"  新技能待查:   {sum(1 for s in known if s.get('status') == 'new')}")
        print(f"{'='*40}")
        print("  技能领域分布:")
        for domain, skills in STANDARD_SKILLS.items():
            print(f"    {domain}: {', '.join(skills)}")
    
    elif cmd == "log":
        usage = load_json("usage_log.json")
        if not usage:
            print("📝 暂无使用记录")
            return
        print(f"📝 使用日志 (最近{len(usage)}条):")
        for i, entry in enumerate(usage[-10:]):
            status = "✅" if entry.get("success") else "❌"
            ct = entry.get("content_type", "未知")
            tmpl = entry.get("template", "未知")
            ts = entry["timestamp"][:19]
            print(f"  {status} [{ts}] {ct} → {tmpl}")
    
    elif cmd == "summary":
        summary = generate_summary()
        print("📋 进化摘要已生成:")
        print(summary)
    
    else:
        print(f"❌ 未知命令: {cmd}")


if __name__ == '__main__':
    main()
