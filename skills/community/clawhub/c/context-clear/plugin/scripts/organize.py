#!/usr/bin/env python3
"""
organize.py — SRS 时间衰减 + 摘要化 + 遗忘清理

三层职责按顺序执行：

1. mtime 分层（hot→warm→gist）
   - warm→gist 时：copy 到 gist（保留 warm 原文），gist 副本做摘要化
2. 遗忘检查（14d 无检索 → forgotten）
   - 从 refcount.json 读取最后检索时间，>14d 无调用则移入 forgotten
3. forgotten 清理（30d → 物理删除）
"""

import json, os, re, shutil, time
from pathlib import Path

STATE_DIR = Path(os.environ.get("OPENCLAW_STATE_DIR", Path.home() / ".openclaw"))
FS_BASE = STATE_DIR / "memory_fs"
REFCOUNT = STATE_DIR / "refcount.json"

# 信号词（用于 gist 摘要提取）
SUMMARY_SIGNALS = [
    "结论是", "核心发现", "关键决策", "一句话总结", "总之",
    "结论：", "核心发现：", "关键决策：", "一句话总结：", "总之：",
    "结论:", "核心发现:", "关键决策:", "一句话总结:", "总之:",
    "TL;DR", "tl;dr", "summary",
]


def load_refcount() -> dict:
    if REFCOUNT.exists():
        return json.loads(REFCOUNT.read_text(encoding="utf-8"))
    return {}


def save_refcount(data: dict):
    REFCOUNT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def ref_clean_path(rel: str) -> str:
    """统一 refcount key 格式：以 hot/warm/gist/forgotten/ 开头"""
    rel = rel.lstrip('/')
    if not rel.startswith(('hot/', 'warm/', 'gist/', 'forgotten/')):
        rel = 'forgotten/' + Path(rel).name
    return rel


def extract_summary(text: str) -> str:
    """规则提取摘要，零 LLM"""
    fm = re.search(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if fm:
        for line in fm.group(1).split('\n'):
            s = line.strip()
            if s.startswith('summary:'):
                return s.split(':', 1)[1].strip()
    for sig in SUMMARY_SIGNALS:
        m = re.search(rf'(?:{re.escape(sig)})\s*(.+?)(?=\n\n|\n#|\Z)', text, re.DOTALL)
        if m:
            return m.group(1).strip()[:200]
    h1 = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    if h1:
        return h1.group(1).strip()
    para = text.strip().split('\n\n')[0][:120].replace('\n', ' ')
    return para


def extract_tags(text: str) -> list[str]:
    return list(set(re.findall(r'#(\w[\w-]*)', text)))


def ensure_dirs():
    for name in ['hot', 'warm', 'gist', 'forgotten']:
        (FS_BASE / name).mkdir(parents=True, exist_ok=True)


def step_mtime_organize(now: int, refcount: dict) -> dict:
    """
    按 mtime 分层：
    hot  < 3h
    warm 3h~7d
    gist 7d~30d   （copy 到 gist，保留 warm 原文）
    """
    layers = [
        ("hot",  3 * 3600),
        ("warm", 7 * 86400),
        ("gist", 30 * 86400),
    ]
    stats = {"hot": 0, "warm": 0, "gist": 0}

    all_files: list[Path] = []
    for name, _ in layers:
        d = FS_BASE / name
        if d.exists():
            for f in d.iterdir():
                if f.is_file() and not f.name.startswith('.'):
                    all_files.append(f)

    for f in all_files:
        age = now - int(f.stat().st_mtime)
        current_layer = f.parent.name

        # 判定目标层
        target = "gist"
        for name, threshold in layers:
            if age <= threshold:
                target = name
                break

        # 同一层 → 跳过
        if current_layer == target:
            stats[target] += 1
            continue

        if target == "warm":
            # hot → warm: move
            dest = FS_BASE / "warm" / f.name
            shutil.move(str(f), str(dest))
            stats["warm"] += 1

        elif target == "gist":
            # warm → gist: copy 到 gist，warm 保留原文
            src = f
            dest = FS_BASE / "gist" / f.name
            shutil.copy2(str(src), str(dest))

            # gist 副本做摘要化
            summary = extract_summary(src.read_text(encoding="utf-8"))
            tags = extract_tags(src.read_text(encoding="utf-8"))
            header = f"# {dest.stem}\n"
            if tags:
                header += f"\n标签: {', '.join(tags)}\n"
            header += f"\n{summary}\n"
            dest.write_text(header, encoding="utf-8")

            # refcount: 记录 gist 副本
            grel = f"gist/{dest.name}"
            if grel not in refcount:
                refcount[grel] = {
                    "total": 0, "7d": 0, "timestamps": [],
                    "user_marked": False, "summarized": True,
                    "created": int(dest.stat().st_mtime),
                }
            else:
                refcount[grel]["summarized"] = True

            # warm 原文 refcount
            wrel = f"warm/{src.name}"
            if wrel not in refcount:
                refcount[wrel] = {
                    "total": 0, "7d": 0, "timestamps": [],
                    "user_marked": False, "summarized": False,
                    "created": int(src.stat().st_mtime),
                }

            stats["gist"] += 1

    return stats


def step_forgotten_check(now: int, refcount: dict) -> dict:
    """
    14d 无检索 → forgotten 区
    检查 warm/ 和 gist/ 中的文件，根据 refcount 的最后检索时间判定。
    """
    stats = {"forgotten": 0}

    for layer in ["warm", "gist"]:
        d = FS_BASE / layer
        if not d.exists():
            continue
        for f in d.iterdir():
            if not f.is_file() or f.name.startswith('.'):
                continue

            rel = f"{layer}/{f.name}"
            entry = refcount.get(rel)

            if not entry:
                # 没有 refcount 记录 → 按文件年龄判断，>14d 则遗忘
                age = now - int(f.stat().st_mtime)
                if age <= 14 * 86400:
                    continue
            else:
                # 有 refcount → 取最后检索时间
                timestamps = entry.get("timestamps", [])
                created = entry.get("created", int(f.stat().st_mtime))
                # 最后活跃时间 = max(最后检索, 创建时间)
                last_active = max(timestamps + [created])
                if now - last_active <= 14 * 86400:
                    continue  # 14d 内有活跃 → 跳过

            # 移到 forgotten
            dest = FS_BASE / "forgotten" / f.name
            shutil.move(str(f), str(dest))

            # 更新 refcount key
            if rel in refcount:
                refcount[f"forgotten/{f.name}"] = refcount.pop(rel)

            stats["forgotten"] += 1

    return stats


def step_forgotten_cleanup(now: int, refcount: dict) -> dict:
    """
    forgotten/ 中超过 30 天的文件物理删除
    但 user_marked=true 的文件跳过。
    """
    stats = {"deleted": 0, "preserved": 0}
    d = FS_BASE / "forgotten"
    if not d.exists():
        return stats

    for f in d.iterdir():
        if not f.is_file() or f.name.startswith('.'):
            continue

        age = now - int(f.stat().st_mtime)
        if age <= 30 * 86400:
            continue  # 未满 30 天

        rel = f"forgotten/{f.name}"
        entry = refcount.get(rel)
        if entry and entry.get("user_marked"):
            stats["preserved"] += 1
            continue  # 被标记 → 保留

        f.unlink()
        refcount.pop(rel, None)
        stats["deleted"] += 1

    return stats


def organize():
    now = int(time.time())
    refcount = load_refcount()
    ensure_dirs()

    stats_mtime = step_mtime_organize(now, refcount)
    stats_forgotten = step_forgotten_check(now, refcount)
    stats_cleanup = step_forgotten_cleanup(now, refcount)

    save_refcount(refcount)

    # 输出摘要
    parts = []
    for k, v in stats_mtime.items():
        if v > 0:
            parts.append(f"{k}: {v}")
    for k, v in stats_forgotten.items():
        if v > 0:
            parts.append(f"{k}: {v}")
    for k, v in stats_cleanup.items():
        if v > 0:
            parts.append(f"{k}: {v}")
    if parts:
        print(f"  {' | '.join(parts)}")
    else:
        print("  无变更")


if __name__ == "__main__":
    print("🔄 organize.py — SRS 衰减 + 遗忘")
    organize()
    print("✅ 完成")
