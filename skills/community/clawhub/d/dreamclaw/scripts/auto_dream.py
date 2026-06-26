#!/usr/bin/env python3
"""
OpenClaw Auto Dream - 记忆整合系统 v3

参考 Claude Code Auto Dream 架构：
1. Append-only 日志：logs/YYYY/MM/YYYY-MM-DD.md
2. 定时蒸馏：dream 命令用 AI 分析日志，更新记忆文件 + MEMORY.md
3. MEMORY.md 只做索引，记忆内容在独立文件里
4. 4 阶段 Prompt：Orient → Gather → Consolidate → Prune

Usage:
    python3 auto_dream.py append "用户想每周读完一本书" --type project
    python3 auto_dream.py dream
    python3 auto_dream.py dream --days 7
    python3 auto_dream.py list
    python3 auto_dream.py check
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# 路径配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
AUTO_DREAM_DIR = WORKSPACE / ".auto-dream"
MEMORY_MD = WORKSPACE / "MEMORY.md"
MEMORIES_DIR = AUTO_DREAM_DIR / "memories"
SESSIONS_DIR = Path.home() / ".openclaw" / "agents" / "main" / "sessions"

# 子目录
MEMORY_TYPES = ["user", "feedback", "project", "reference"]

# 常量
MAX_MEMORY_LINES = 200
MAX_ENTRYPOINT_CHARS = 25_000
MAX_MEMORY_FILES = 200

# ============================================================================
# 记忆文件 Frontmatter 模板
# ============================================================================

FRONTMATTER_TEMPLATE = """---
name: {name}
type: {memory_type}
description: {description}
mtime: {mtime}
---

{content}
"""


# ============================================================================
# 数据结构
# ============================================================================

@dataclass
class MemoryHeader:
    """记忆文件头部信息"""
    filename: str
    file_path: str
    mtime: datetime
    description: str | None
    memory_type: str | None


@dataclass
class SessionMessage:
    """会话消息"""
    role: str
    text: str
    timestamp: datetime
    session_id: str


# ============================================================================
# 目录和文件操作
# ============================================================================

def ensure_directories():
    """确保必要的目录存在"""
    AUTO_DREAM_DIR.mkdir(parents=True, exist_ok=True)
    MEMORIES_DIR.mkdir(parents=True, exist_ok=True)
    for mtype in MEMORY_TYPES:
        (MEMORIES_DIR / mtype).mkdir(exist_ok=True)


def get_daily_log_path(date: datetime = None) -> Path:
    """获取每日日志路径"""
    if date is None:
        date = datetime.now()
    log_dir = AUTO_DREAM_DIR / "logs" / date.strftime("%Y") / date.strftime("%m")
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / f"{date.strftime('%Y-%m-%d')}.md"


def read_daily_logs(days_back: int = 7) -> dict[str, str]:
    """读取过去 N 天的日志"""
    logs = {}
    now = datetime.now()
    
    for i in range(days_back):
        date = now - timedelta(days=i)
        log_path = get_daily_log_path(date)
        if log_path.exists():
            logs[date.strftime("%Y-%m-%d")] = log_path.read_text(encoding="utf-8")
    
    return logs


def append_to_daily_log(entry: str, date: datetime = None):
    """追加条目到每日日志（append-only）"""
    log_path = get_daily_log_path(date)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry_line = f"- [{timestamp}] {entry}\n"
    
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry_line)
    
    print(f"  ✅ 已追加到 {log_path}")
    return log_path


def scan_memory_files() -> list[MemoryHeader]:
    """扫描记忆目录，返回所有记忆文件的头部信息"""
    headers = []
    
    for mtype in MEMORY_TYPES:
        type_dir = MEMORIES_DIR / mtype
        if not type_dir.exists():
            continue
        
        for md_file in type_dir.glob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
                mtime = datetime.fromtimestamp(md_file.stat().st_mtime)
                
                # 解析 frontmatter
                name, description = parse_frontmatter(content)
                
                headers.append(MemoryHeader(
                    filename=md_file.name,
                    file_path=str(md_file),
                    mtime=mtime,
                    description=description,
                    memory_type=mtype
                ))
            except Exception as e:
                print(f"  ⚠️  读取 {md_file} 失败: {e}")
                continue
    
    # 按 mtime 排序（最新优先）
    headers.sort(key=lambda h: h.mtime, reverse=True)
    return headers[:MAX_MEMORY_FILES]


def parse_frontmatter(content: str) -> tuple[str | None, str | None]:
    """解析 frontmatter，提取 name 和 description"""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            name = None
            description = None
            for line in frontmatter.split("\n"):
                if line.startswith("name:"):
                    name = line.split(":", 1)[1].strip().strip('"\'')
                elif line.startswith("description:"):
                    description = line.split(":", 1)[1].strip().strip('"\'')
            return name, description
    return None, None


def format_memory_manifest(headers: list[MemoryHeader]) -> str:
    """格式化记忆文件清单（用于 AI prompt）"""
    lines = []
    for h in headers:
        tag = f"[{h.memory_type}]" if h.memory_type else ""
        ts = h.mtime.strftime("%Y-%m-%d")
        desc = f": {h.description}" if h.description else ""
        lines.append(f"- {tag} {h.filename} ({ts}){desc}")
    return "\n".join(lines)


def build_consolidation_prompt(transcript_snippets: str = "", extra: str = "") -> str:
    """
    构建 4 阶段蒸馏 prompt（参考 Claude Code consolidationPrompt.ts）
    """
    memory_root = str(AUTO_DREAM_DIR)
    memory_manifest = format_memory_manifest(scan_memory_files())
    daily_logs = read_daily_logs(days_back=7)
    logs_content = "\n\n".join([
        f"## {date}\n{content}" 
        for date, content in sorted(daily_logs.items(), reverse=True)
    ])
    
    prompt = f"""# Dream: Memory Consolidation

You are performing a dream — a reflective pass over your memory files. Synthesize what you've learned recently into durable, well-organized memories so that future sessions can orient quickly.

Memory directory: `{memory_root}`
This directory already exists — write to it directly (do not run mkdir or check for its existence).

---

## Phase 1 — Orient

- `ls` the memory directory to see what already exists
- Read `MEMORY.md` to understand the current index
- Skim existing topic files so you improve them rather than creating duplicates
- Check `logs/` subdirectory for recent append-only log entries

## Phase 2 — Gather recent signal

Look for new information worth persisting. Sources in rough priority order:

1. **Daily logs** (`logs/YYYY/MM/YYYY-MM-DD.md`) — these are the append-only stream:

```
{logs_content}
```

2. **Existing memories that drifted** — facts that contradict something you see in the current state
3. **Session transcript snippets** — if you need specific context, grep the transcripts for narrow terms

{logs_content if transcript_snippets else "(No transcript snippets provided — rely on daily logs and existing memories)"}

## Phase 3 — Consolidate

For each thing worth remembering, write or update a memory file in the appropriate subdirectory of `memories/`. Use the frontmatter format:

```
---
name: <简短标题，50字以内>
type: <user|feedback|project|reference>
description: <一句话描述>
mtime: <ISO格式时间>
---

<可选的详细正文>
```

**Memory types:**
- `user`: 用户角色、目标、偏好、知识
- `feedback`: 用户的指导/纠正（什么该做、什么不该做）
- `project`: 项目上下文、决定、截止日期
- `reference`: 外部系统指针（如飞书文档、项目地址等）

**Focus on:**
- Merging new signal into existing topic files rather than creating near-duplicates
- Converting relative dates ("yesterday", "last week") to absolute dates so they remain interpretable
- **Deleting contradicted facts** — if today's investigation disproves an old memory, remove it at the source
- If an old memory has wrong/outdated information, update or delete it

## Phase 4 — Prune and index

Update `MEMORY.md` so it stays under {MAX_MEMORY_LINES} lines AND under ~{MAX_ENTRYPOINT_CHARS} chars. It's an **index**, not a dump — each entry should be one line under ~150 characters:

```
- [Title](memories/<type>/file.md) — one-line hook
```

**Index rules:**
- Remove pointers to memories that are now stale, wrong, or superseded
- Demote verbose entries — if an index line is over ~200 chars, move the detail to the topic file and shorten the line
- Add pointers to newly important memories
- Resolve contradictions — if two files disagree, fix the wrong one

---

Return a brief summary of what you consolidated, updated, or pruned. If nothing changed (memories are already tight), say so.

{extra if extra else ""}
"""
    return prompt


# ============================================================================
# 会话读取
# ============================================================================

def read_sessions_index() -> dict:
    """读取 sessions.json 索引"""
    sessions_file = SESSIONS_DIR / "sessions.json"
    if not sessions_file.exists():
        return {}
    
    with open(sessions_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_recent_session_snippets(days_back: int = 7, max_chars: int = 5000) -> str:
    """获取最近会话的关键片段（用于 AI 分析）"""
    sessions = read_sessions_index()
    snippets = []
    cutoff = datetime.now() - timedelta(days=days_back)
    
    for key, info in sessions.items():
        session_file = info.get('sessionFile')
        if not session_file or not Path(session_file).exists():
            continue
        
        # 跳过飞书会话（太多噪音），只取 main/cron
        # if 'feishu' in key:
        #     continue
        
        try:
            messages = []
            with open(session_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    obj = json.loads(line)
                    if obj.get('type') != 'message':
                        continue
                    
                    msg = obj.get('message', {})
                    role = msg.get('role')
                    if role in ('system', 'tool'):
                        continue
                    
                    # 解析时间戳
                    ts = obj.get('timestamp', 0)
                    if isinstance(ts, str):
                        try:
                            from datetime import timezone
                            ts_dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                            msg_time = ts_dt.astimezone().replace(tzinfo=None)
                        except:
                            msg_time = datetime.now()
                    elif isinstance(ts, (int, float)):
                        msg_time = datetime.fromtimestamp(ts / 1000)
                    else:
                        continue
                    
                    if msg_time < cutoff:
                        continue
                    
                    # 提取文本
                    content = msg.get('content', '')
                    text = ''
                    if isinstance(content, list):
                        for c in content:
                            if isinstance(c, dict) and c.get('type') == 'text':
                                text += c.get('text', '')
                    elif isinstance(content, str):
                        text = content
                    
                    text = text.strip()
                    if text and len(text) > 5:
                        # 截断太长的消息
                        if len(text) > 300:
                            text = text[:300] + "..."
                        messages.append(f"[{msg_time.strftime('%m-%d %H:%M')}] {text}")
            
            if messages:
                snippets.append(f"\n## Session: {key[:50]}...\n")
                snippets.append("\n".join(messages[-10:]))  # 每个会话最多10条
                
        except Exception as e:
            continue
    
    result = "\n".join(snippets)
    # 截断总长度
    if len(result) > max_chars:
        result = result[:max_chars] + "\n... (truncated)"
    
    return result


# ============================================================================
# MEMORY.md 操作
# ============================================================================

def read_memory_md() -> str:
    """读取 MEMORY.md"""
    if not MEMORY_MD.exists():
        return ""
    return MEMORY_MD.read_text(encoding="utf-8")


def write_memory_md(content: str):
    """写入 MEMORY.md"""
    MEMORY_MD.write_text(content, encoding="utf-8")


def build_memory_md_from_headers(headers: list[MemoryHeader]) -> str:
    """从记忆文件头部构建 MEMORY.md 索引"""
    lines = ["# MEMORY.md - Long-term Memory", "", f"**最后更新**: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]
    
    # 按类型分组
    by_type = {mtype: [] for mtype in MEMORY_TYPES}
    for h in headers:
        if h.memory_type:
            by_type[h.memory_type].append(h)
    
    for mtype in MEMORY_TYPES:
        if by_type[mtype]:
            lines.append(f"## {mtype.upper()}")
            for h in by_type[mtype]:
                desc = h.description or ""
                lines.append(f"- [{h.filename}](memories/{mtype}/{h.filename}) — {desc}")
            lines.append("")
    
    content = "\n".join(lines)
    
    # 截断
    if len(content) > MAX_ENTRYPOINT_CHARS:
        content = content[:MAX_ENTRYPOINT_CHARS] + "\n> ... (truncated)"
    
    return content


# ============================================================================
# 记忆文件操作
# ============================================================================

def create_memory_file(
    name: str,
    memory_type: str,
    description: str,
    content: str = "",
    mtime: datetime = None
) -> Path:
    """创建或更新记忆文件"""
    if memory_type not in MEMORY_TYPES:
        raise ValueError(f"Invalid memory type: {memory_type}")
    
    if mtime is None:
        mtime = datetime.now()
    
    # 生成文件名
    safe_name = re.sub(r'[^\w\-_.]', '_', name)[:50]
    filename = f"{mtime.strftime('%Y%m%d')}_{safe_name}.md"
    file_path = MEMORIES_DIR / memory_type / filename
    
    frontmatter = FRONTMATTER_TEMPLATE.format(
        name=name,
        memory_type=memory_type,
        description=description,
        mtime=mtime.isoformat(),
        content=content
    )
    
    file_path.write_text(frontmatter, encoding="utf-8")
    return file_path


def delete_memory_file(file_path: Path):
    """删除记忆文件"""
    if file_path.exists() and str(file_path).startswith(str(MEMORIES_DIR)):
        file_path.unlink()
        print(f"  🗑️  Deleted: {file_path}")


def update_memory_file(file_path: Path, **updates):
    """更新记忆文件的 frontmatter"""
    if not file_path.exists():
        return
    
    content = file_path.read_text(encoding="utf-8")
    
    if not content.startswith("---"):
        return
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return
    
    frontmatter = parts[1]
    body = parts[2]
    
    for key, value in updates.items():
        if key in ('name', 'description', 'mtime'):
            # 更新 frontmatter
            pattern = rf"^{key}:.*$"
            replacement = f"{key}: {value}"
            frontmatter = re.sub(pattern, replacement, frontmatter, flags=re.MULTILINE)
    
    new_content = f"---\n{frontmatter}---\n{body}"
    file_path.write_text(new_content, encoding="utf-8")


# ============================================================================
# AI 蒸馏（通过 sub-agent）
# ============================================================================

def run_dream_consolidation(days_back: int = 7):
    """
    运行 Dream 蒸馏：通过 sub-agent 执行 4 阶段 prompt
    """
    print("\n" + "🌙" * 30)
    print("🌙 OpenClaw Auto Dream v3 - 记忆蒸馏 🌙")
    print("🌙" * 30)
    
    ensure_directories()
    
    # Phase 1-2: 收集信息
    print("\n📡 Phase 1-2: Gather Signal")
    print("-" * 40)
    
    headers = scan_memory_files()
    print(f"  发现 {len(headers)} 个已有记忆文件")
    
    logs = read_daily_logs(days_back)
    print(f"  发现 {len(logs)} 天的日志")
    
    session_snippets = get_recent_session_snippets(days_back)
    print(f"  会话片段: {len(session_snippets)} 字符")
    
    # 构建 prompt
    prompt = build_consolidation_prompt(
        transcript_snippets=session_snippets,
        extra=f"\n\n## Sessions since last consolidation ({days_back} days):\nUse the session snippets above to find new information worth remembering."
    )
    
    # 写入临时 prompt 文件
    prompt_file = AUTO_DREAM_DIR / ".dream_prompt.md"
    prompt_file.write_text(prompt, encoding="utf-8")
    
    print(f"\n  📝 Prompt 已写入: {prompt_file}")
    print(f"  📋 记忆文件: {MEMORIES_DIR}")
    print(f"  📋 索引文件: {MEMORY_MD}")
    
    print("\n" + "=" * 40)
    print("⚠️  AI 蒸馏需要通过 sub-agent 执行")
    print("=" * 40)
    print("""
请在 OpenClaw 主会话中执行以下命令：

    /dream

或者手动调用：

    python3 -c "
    from auto_dream import run_dream_consolidation
    run_dream_consolidation()
    "

建议通过 sessions_spawn 启动 sub-agent 来执行。
""")
    
    return prompt


# ============================================================================
# 命令行接口
# ============================================================================

def cmd_append(args):
    """追加记忆条目到每日日志"""
    ensure_directories()
    append_to_daily_log(args.text, args.date)
    
    if args.type:
        print(f"\n💡 提示: --type 参数仅用于日志，不影响记忆分类")
        print(f"   日后 dream 时会根据内容自动分类到 user/feedback/project/reference")


def cmd_dream(args):
    """运行记忆蒸馏"""
    ensure_directories()
    run_dream_consolidation(days_back=args.days)


def cmd_list(args):
    """列出所有记忆"""
    ensure_directories()
    headers = scan_memory_files()
    
    print(f"\n📚 记忆文件 ({len(headers)} 个)")
    print("=" * 60)
    
    if not headers:
        print("  暂无记忆")
        return
    
    by_type = {mtype: [] for mtype in MEMORY_TYPES}
    for h in headers:
        if h.memory_type:
            by_type[h.memory_type].append(h)
    
    for mtype in MEMORY_TYPES:
        if by_type[mtype]:
            print(f"\n## {mtype.upper()} ({len(by_type[mtype])})")
            for h in by_type[mtype][:10]:
                age = (datetime.now() - h.mtime).days
                desc = h.description or ""
                print(f"  - {h.filename} ({age}天前) — {desc}")
            if len(by_type[mtype]) > 10:
                print(f"  ... 还有 {len(by_type[mtype]) - 10} 个")


def cmd_check(args):
    """检查记忆新鲜度"""
    ensure_directories()
    headers = scan_memory_files()
    
    print(f"\n📅 记忆新鲜度报告")
    print("=" * 60)
    
    if not headers:
        print("  暂无记忆")
        return
    
    now = datetime.now()
    fresh = medium = stale = 0
    
    for h in headers:
        age = (now - h.mtime).days
        if age <= 7:
            fresh += 1
        elif age <= 30:
            medium += 1
        else:
            stale += 1
    
    print(f"  🟢 新鲜 (≤7天): {fresh}")
    print(f"  🟡 适中 (8-30天): {medium}")
    print(f"  🔴 过时 (>30天): {stale}")
    
    # 显示日志
    logs = read_daily_logs(days_back=7)
    print(f"\n📝 每日日志: {len(logs)} 天")
    for date in sorted(logs.keys(), reverse=True):
        lines = logs[date].strip().split("\n")
        print(f"  {date}: {len(lines)} 条")


def cmd_build_index(args):
    """从记忆文件重建 MEMORY.md 索引"""
    ensure_directories()
    headers = scan_memory_files()
    
    print(f"\n🔨 重建 MEMORY.md 索引")
    print("=" * 60)
    print(f"  找到 {len(headers)} 个记忆文件")
    
    content = build_memory_md_from_headers(headers)
    write_memory_md(content)
    
    lines = len(content.split("\n"))
    print(f"  ✅ MEMORY.md 已重建: {lines} 行")


def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw Auto Dream v3 - 记忆整合系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 追加记忆到今日日志
  python3 auto_dream.py append "用户想每周读完一本书" --type project

  # 运行蒸馏（AI 分析并整合记忆）
  python3 auto_dream.py dream

  # 列出所有记忆
  python3 auto_dream.py list

  # 检查新鲜度
  python3 auto_dream.py check

  # 从记忆文件重建索引
  python3 auto_dream.py build-index
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # append 命令
    append_parser = subparsers.add_parser("append", help="追加条目到每日日志")
    append_parser.add_argument("text", help="要记录的条目内容")
    append_parser.add_argument("--type", "-t", choices=MEMORY_TYPES, help="记忆类型（仅供提示）")
    append_parser.add_argument("--date", "-d", help="日期（YYYY-MM-DD），默认今天")
    append_parser.set_defaults(func=cmd_append)
    
    # dream 命令
    dream_parser = subparsers.add_parser("dream", help="运行 AI 蒸馏")
    dream_parser.add_argument("--days", type=int, default=7, help="回顾最近 N 天（默认7）")
    dream_parser.set_defaults(func=cmd_dream)
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出所有记忆")
    list_parser.set_defaults(func=cmd_list)
    
    # check 命令
    check_parser = subparsers.add_parser("check", help="检查记忆新鲜度")
    check_parser.set_defaults(func=cmd_check)
    
    # build-index 命令
    build_parser = subparsers.add_parser("build-index", help="重建 MEMORY.md 索引")
    build_parser.set_defaults(func=cmd_build_index)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == "__main__":
    main()
