"""
sync_skills_to_memory.py — 将 skills.json 同步到 self-improving/memory.md

每次 classify/promote 后运行，以及 heartbeat 定期运行。
"""
import json, os
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
SKILLS_FILE = WORKSPACE / "data" / "skills.json"
SKILLS_MEM_FILE = WORKSPACE / "data" / "skills.memory.md"
MEMORY_FILE = Path(os.environ["USERPROFILE"]) / "self-improving" / "memory.md"


def sync():
    if not SKILLS_FILE.exists():
        # 创建空骨架，让 memory_search 有索引目标
        SKILLS_FILE.parent.mkdir(parents=True, exist_ok=True)
        SKILLS_FILE.write_text("[]", encoding="utf-8")
        print("skills.json 不存在，已创建空骨架")

    with open(SKILLS_FILE, "r", encoding="utf-8") as f:
        skills = json.load(f)

    if not skills:
        print("skills.json 为空，跳过同步（skills.memory.md 清空）")
        # 仍然写入空 skills.memory.md，防止过期数据残留
        SKILLS_MEM_FILE.parent.mkdir(parents=True, exist_ok=True)
        SKILLS_MEM_FILE.write_text("## 积累的经验与操作规则\n\n（暂无积累的技能条目）\n", encoding="utf-8")
        return
    
    # 构建技能区块
    lines = ["## 积累的经验与操作规则"]
    lines.append("")
    for i, s in enumerate(skills, 1):
        if not s.get("is_active", True):
            continue
        lines.append(f"### {i}. {s['content']}")
        lines.append(f"- **适用场景:** {s['when']}")
        lines.append(f"- **可信度:** {s['confidence']}/1.0")
        lines.append(f"- **层级:** {s['level']}")
        if s.get("keywords"):
            lines.append(f"- **关键词:** {'、'.join(s['keywords'][:3])}")
        lines.append("")
    
    skills_block = "\n".join(lines)
    
    # 写入 data/skills.memory.md（被 memory_search 索引，不占上下文）
    SKILLS_MEM_FILE.parent.mkdir(parents=True, exist_ok=True)
    SKILLS_MEM_FILE.write_text(skills_block, encoding="utf-8")
    
    # 从 memory.md 中移除旧的技能区块（如果存在）
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    if MEMORY_FILE.exists():
        existing = MEMORY_FILE.read_text(encoding="utf-8", errors="replace")
        start_marker = "## 积累的经验与操作规则"
        if start_marker in existing:
            start = existing.index(start_marker)
            next_heading = existing.find("\n## ", start + 2)
            if next_heading >= 0:
                new_content = existing[:start] + existing[next_heading:]
            else:
                new_content = existing[:start]
            MEMORY_FILE.write_text(new_content.strip() + "\n", encoding="utf-8", errors="replace")
            print("  已从 memory.md 中移除旧技能区块")
    
    print(f"同步完成: {len(skills)} 条技能 → skills.memory.md")

# ── Health report ──
try:
    from system_health import task_report
    task_report("sync_skills_to_memory", status="ok")
except Exception:
    pass


if __name__ == "__main__":
    sync()
