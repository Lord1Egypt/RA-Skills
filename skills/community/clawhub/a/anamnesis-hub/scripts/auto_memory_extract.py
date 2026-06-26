#!/usr/bin/env python3
"""
auto-memory-extract — 自动记忆提取 v2

从 MemOS Cloud 已提取的结构化事实中，用本地 qwen3 精加工后写入 MEMORY.md。

流程:
  MemOS agent_end → 云端 LLM 提取 → sync 30min 拉回本地
                                      ↓
                            memos-cloud-YYYY-MM-DD.md
                            （已提取好但含大量噪声）
                                      ↓
                            本脚本：qwen3 过滤+去重+格式化
                                      ↓
                            MEMORY.md（只有高度相关的长期记忆）

用法:
  python3 auto_memory_extract.py [--mode full|status|dry-run] [--days 1]
"""

import argparse
import json
import hashlib
import re
import sys
import urllib.request
import os
from datetime import datetime, timezone
from pathlib import Path

# ── 路径配置 ──────────────────────────────────────────────────────────────────

WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
CACHE_DIR = WORKSPACE / "user_workspace" / "memos-cloud-cache"
MEMORY_MD = WORKSPACE / "MEMORY.md"
ARCHIVE_MD = WORKSPACE / "ARCHIVE.md"
WRITER_SCRIPT = Path(__file__).resolve().parent / "write_file.py"

# qwen3 本地调用
OLLAMA_BASE = "http://127.0.0.1:11434"
LLM_MODEL = "qwen3:8b"

# MemOS 自研模型 API
MEMOS_BASE_URL = "https://memos.memtensor.cn/api/openmem/v1"
MEMOS_API_KEY = ""  # 从环境变量读取

# ── 噪音过滤关键词（标题中包含这些的条目跳过不处理） ────────────────────────

NOISE_KEYWORDS = [
    "Cron delivery check", "Cron delivery process",
    "OpenClaw doctor", "Dreams of a rack", "Dashboard URL",
    "Wiki同步", "Cron delivery result",
    "无待投递", "已搬运", "heartbeat",
    "HEARTBEAT", "cron-delivery",
    "/get/memory 获取", "sync-cloud",
    "已确认", "确认工作", "确认通知",
    "Home Assistant 版本",
]

# ── Prompt（精简：只需去重+格式化） ──────────────────────────────────────────

EXTRACT_PROMPT = """你是一个记忆整理助手。我已从 MemOS Cloud 中拉回已提取好的事实和偏好，其中有大量系统级噪音（如 cron 检测、重复记录等），也有少量真正值得写入长期记忆（MEMORY.md）的用户信息。

任务：
1. 过滤掉噪音（cron 检测、系统自动任务、重复记录等）
2. 识别出真正有价值的用户记忆：偏好、习惯、配置、项目决策、重要事件
3. 与已有 MEMORY.md 对比去重（完全相同的内容不重复写入）

已有 MEMORY.md 内容：
```
{memory_md}
```

待处理的新记忆（已从 MemOS Cloud 拉取）：
```
{memos_entries}
```

输出格式（只输出 JSON，不要任何其他文字）：
{{"add":[{{"category":"分类","content":"具体事实"}}],"update":[],"remove":[]}}

分类建议：偏好/习惯、兴趣/爱好、项目/工作、技术/配置、设备/环境、社交/关系、计划/目标、重要事件
原则：宁少勿多，不确定的条目不输出；无有价值信息则输出 {{"add":[],"update":[],"remove":[]}}"""


# ── 工具函数 ──────────────────────────────────────────────────────────────────

def _get_memos_api_key() -> str:
    """从环境变量或 .env 读取 API Key"""
    key = os.environ.get("MEMOS_API_KEY", "")
    if not key:
        env_path = Path.home() / ".openclaw" / ".env"
        if env_path.exists():
            for line in env_path.read_text().split("\n"):
                if line.startswith("MEMOS_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    return key


def call_memos_extractor(entries_text: str) -> dict:
    """调用 memos-extractor-0.6b API 做结构化提取"""
    key = _get_memos_api_key()
    if not key or not entries_text.strip():
        return {"memory_detail_list": [], "preference_detail_list": []}

    # 将条目包装为简短的助理-用户对话格式
    messages = [
        {"role": "system", "content": "你是一个智能记忆提取系统，负责从对话内容中提取用户事实记忆和偏好记忆。"},
        {"role": "user", "content": f"请分析以下对话内容，提取结构化记忆。\n\n{entries_text[:7000]}"},
    ]

    payload = json.dumps({"messages": messages}).encode("utf-8")
    req = urllib.request.Request(
        f"{MEMOS_BASE_URL}/extract/memory",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Token {key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("data", {}) or {}
    except Exception as e:
        print(json.dumps({
            "status": "warn",
            "step": "memos_extractor",
            "message": str(e),
        }), file=sys.stderr)
        return {"memory_detail_list": [], "preference_detail_list": []}


def call_llm(prompt: str, max_tokens: int = 2000) -> str:
    """通过本地 Ollama 调用 qwen3"""
    payload = json.dumps({
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": max_tokens, "temperature": 0},
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{OLLAMA_BASE}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("response", "").strip()
    except Exception as e:
        print(json.dumps({"status": "error", "step": "llm_call", "message": str(e)}), file=sys.stderr)
        return ""


def parse_extraction_result(text: str) -> dict:
    """解析 JSON 输出"""
    code_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if code_match:
        text = code_match.group(1)
    text = text.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        text = text[start:end+1]
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"add": [], "update": [], "remove": []}


def read_memos_cloud(days: int = 1) -> str:
    """
    读取最新的 memos-cloud-YYYY-MM-DD.md 文件的最新同步批次。
    文件存储在 user_workspace/memos-cloud-cache/ 避免污染索引。
    """
    today = datetime.now().astimezone()
    entries = []

    for d in range(days):
        date_str = (today - __import__("datetime").timedelta(days=d)).strftime("%Y-%m-%d")
        path = CACHE_DIR / f"memos-cloud-{date_str}.md"
        if not path.exists():
            continue

        content = path.read_text(encoding="utf-8", errors="replace")

        # 只处理最后一个同步批次（最新拉取的记忆）
        last_sync = content.rfind("# MemOS Cloud 同步 @")
        if last_sync < 0:
            continue
        content = content[last_sync:]

        # 解析该批次内的条目
        lines = content.split("\n")
        current_title = None
        current_time = None
        current_text = None

        for line in lines:
            title_m = re.match(r"^### (.+)", line)
            if title_m:
                if current_title and current_text and current_time:
                    if not any(kw.lower() in current_title.lower() for kw in NOISE_KEYWORDS):
                        entries.append(f"[{current_time}] {current_title} → {current_text[:200]}")
                current_title = title_m.group(1)
                current_time = None
                current_text = None
                continue

            time_m = re.match(r"^- 类型: \S+\s+\|\s+记录时间:\s+(.+)", line)
            if time_m and current_title:
                current_time = time_m.group(1).strip()
                continue

            if current_title and current_time and line.startswith("- ") and "类型:" not in line:
                current_text = line[2:].strip()

        # 最后一条
        if current_title and current_text and current_time:
            if not any(kw.lower() in current_title.lower() for kw in NOISE_KEYWORDS):
                entries.append(f"[{current_time}] {current_title} → {current_text[:200]}")

    seen = set()
    unique = []
    for e in entries:
        if e not in seen:
            seen.add(e)
            unique.append(e)

    return "\n".join(unique) if unique else ""


def read_memory_md() -> str:
    try:
        return MEMORY_MD.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "# 长期记忆\n"


def compute_content_hash(text: str) -> str:
    """计算条目内容的 SHA-256 哈希，用于去重"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def get_archive_hashes() -> set:
    """从 ARCHIVE.md 提取所有已存在条目的 SHA-256 哈希"""
    hashes = set()
    try:
        content = ARCHIVE_MD.read_text(encoding="utf-8")
    except FileNotFoundError:
        return hashes
    for match in re.finditer(r"<!-- hash:([a-f0-9]{16}) -->", content):
        hashes.add(match.group(1))
    return hashes


def stage_one_archive(entries: list, today: str) -> dict:
    """阶段一：归档到 ARCHIVE.md，SHA-256 去重"""
    existing_hashes = get_archive_hashes()
    new_entries = []
    skipped = 0

    for item in entries:
        if isinstance(item, dict):
            cat = item.get("category", "其他")
            content = item.get("content", "")
            line = f"- **{cat}**: {content}"
        else:
            line = f"- {item}"

        h = compute_content_hash(line)
        if h in existing_hashes:
            skipped += 1
            continue
        existing_hashes.add(h)
        new_entries.append(f"<!-- hash:{h} -->\n{line}")

    if not new_entries:
        return {"added": 0, "skipped": skipped, "section_line": None}

    try:
        archive_content = ARCHIVE_MD.read_text(encoding="utf-8")
    except FileNotFoundError:
        archive_content = "# 详细档案 ARCHIVE.md\n"

    section_mark = "## Auto-Extracted 历史归档"
    new_block = f"\n\n### {today}\n" + "\n".join(new_entries)

    if section_mark in archive_content:
        insert_at = archive_content.find(section_mark) + len(section_mark)
        # 跳过已有内容找到合适插入点
        next_section = archive_content.find("\n## ", insert_at + 1)
        if next_section < 0:
            next_section = len(archive_content)
        archive_content = archive_content[:next_section] + new_block + archive_content[next_section:]
    else:
        archive_content = archive_content.rstrip() + f"\n\n{section_mark}\n{new_block}"

    write_with_script(str(ARCHIVE_MD), archive_content)

    # 确定插入位置的行号
    section_line = None
    for i, line in enumerate(archive_content.split("\n"), 1):
        if line.strip() == section_mark:
            section_line = i
            break

    return {"added": len(new_entries), "skipped": skipped, "section_line": section_line}


def stage_two_summarize(today: str, archive_section_line: int, added_count: int) -> dict:
    """阶段二：将一行摘要写入 MEMORY.md"""
    try:
        memory_content = MEMORY_MD.read_text(encoding="utf-8")
    except FileNotFoundError:
        memory_content = "# 长期记忆\n"

    summary_line = f"Auto-Extracted ({today}): {added_count} 条新记忆 → `ARCHIVE.md:{archive_section_line}`"
    summary_marker = "Auto-Extracted 索引:"

    if summary_marker in memory_content:
        # 替换已有索引行
        pattern = rf"{re.escape(summary_marker)}.*"
        memory_content = re.sub(pattern, f"{summary_marker} {summary_line}", memory_content)
    else:
        # 在文件末尾追加
        memory_content = memory_content.rstrip() + f"\n\n{summary_marker} {summary_line}\n"

    result = write_with_script(str(MEMORY_MD), memory_content)
    return {"memory_md_updated": result["status"] == "ok", "summary": summary_line}


def write_with_script(path: str, content: str) -> dict:
    import subprocess
    tmp = Path(f"/tmp/_tw_auto_{Path(path).name}.txt")
    tmp.write_text(content, encoding="utf-8")
    cmd = [sys.executable, str(WRITER_SCRIPT), "--path", path, "--content-file", str(tmp)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    tmp.unlink(missing_ok=True)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"status": "error", "message": result.stderr or result.stdout}


# ── 运行模式 ──────────────────────────────────────────────────────────────────

def run_status(days: int = 1) -> dict:
    """查看状态"""
    memos_files = sorted(CACHE_DIR.glob("memos-cloud-*.md"), reverse=True)[:days]
    entries_text = read_memos_cloud(days)
    return {
        "status": "ok",
        "memos_files": [f.name for f in memos_files],
        "filtered_entries_count": len([l for l in entries_text.split("\n") if l.strip()]),
        "total_chars": len(entries_text),
    }


def run_extract(days: int = 1, dry_run: bool = False) -> dict:
    """执行记忆提取"""
    entries_text = read_memos_cloud(days)
    if not entries_text:
        return {"status": "ok", "message": "没有找到新的记忆条目", "skipped": True}

    entry_count = len([l for l in entries_text.split("\n") if l.strip()])
    if entry_count < 2:
        return {"status": "ok", "message": "有效条目太少，跳过", "skipped": True}

    current_md = read_memory_md()

    print(json.dumps({"status": "info", "step": "extract", "entries": entry_count, "chars": len(entries_text)}))

    if dry_run:
        return {"status": "dry_run", "entries_preview": entries_text[:500], "total_entries": entry_count}

    # ── 通道A: qwen3:8b 过滤去重 ──
    prompt = EXTRACT_PROMPT.format(memory_md=current_md[:2000], memos_entries=entries_text[:5000])
    result = call_llm(prompt, max_tokens=2000)
    qwen3_ops = parse_extraction_result(result)
    qwen3_adds = qwen3_ops.get("add", []) or []

    # ── 通道B: memos-extractor-0.6b 结构化提取 ──
    extractor_result = call_memos_extractor(entries_text)
    extractor_memories = extractor_result.get("memory_detail_list", []) or []
    extractor_prefs = extractor_result.get("preference_detail_list", []) or []

    # ── 两通道交叉验证 ──
    extractor_adds = []
    for m in extractor_memories:
        val = m.get("memory_value", "") or ""
        key = m.get("memory_key", "") or ""
        if val and len(val) > 10:  # 过滤空/短条目
            extractor_adds.append({
                "category": "技术/配置",
                "content": f"{key}: {val}",
                "source": "memos-extractor",
            })
    for p in extractor_prefs:
        pref = p.get("preference", "") or ""
        if pref and len(pref) > 10:
            extractor_adds.append({
                "category": "偏好/习惯",
                "content": pref,
                "source": "memos-extractor",
            })

    # 交叉匹配：qwen3 有的，查 extractor 有没有相似内容
    qwen3_texts = set()
    for item in qwen3_adds:
        if isinstance(item, dict):
            qwen3_texts.add(item.get("content", "")[:50])
        else:
            qwen3_texts.add(str(item)[:50])

    merged_adds = list(qwen3_adds)  # qwen3 的全都保留（原有行为）
    extractor_extra = []
    for item in extractor_adds:
        prefix = item["content"][:50]
        # 只在 qwen3 没覆盖到时补充
        if not any(t == prefix for t in qwen3_texts):
            extractor_extra.append({
                "category": item["category"],
                "content": f"[提取器补充] {item['content']}",
            })
    merged_adds.extend(extractor_extra)

    merged_ops = {"add": merged_adds, "update": [], "remove": []}
    add_count = len(merged_adds)
    today = datetime.now().astimezone().strftime("%Y-%m-%d")

    archive_result = {"added": 0, "skipped": 0}
    memory_result = {"memory_md_updated": False, "summary": ""}

    if add_count > 0:
        # 阶段一：归档到 ARCHIVE.md（含 SHA-256 去重）
        archive_result = stage_one_archive(merged_adds, today)

        # 阶段二：一行摘要写入 MEMORY.md
        if archive_result["added"] > 0 and archive_result["section_line"]:
            memory_result = stage_two_summarize(today, archive_result["section_line"], archive_result["added"])

    return {
        "status": "ok",
        "pipeline": "two-stage (archive → summarize)",
        "stage1_archive": archive_result,
        "stage2_memory": memory_result,
        "summary": {
            "total_candidates": add_count,
            "added_after_dedup": archive_result.get("added", 0),
            "duplicates_skipped": archive_result.get("skipped", 0),
            "qwen3_count": len(qwen3_adds),
            "extractor_count": len(extractor_adds),
            "extractor_extra": len(extractor_extra),
            "result_preview": result[:300] if result else "(empty)",
        },
    }


def main():
    parser = argparse.ArgumentParser(description="auto-memory v2")
    parser.add_argument("--mode", choices=["status", "dry-run", "full"], default="full")
    parser.add_argument("--days", type=int, default=1)
    args = parser.parse_args()

    if args.mode == "status":
        result = run_status(args.days)
    elif args.mode == "dry-run":
        result = run_extract(args.days, dry_run=True)
    else:
        result = run_extract(args.days)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result.get("skipped") else 0


if __name__ == "__main__":
    sys.exit(main())
