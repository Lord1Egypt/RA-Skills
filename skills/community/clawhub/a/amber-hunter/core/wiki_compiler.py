"""
core/wiki_compiler.py — Knowledge Compiler

将同 category_path 下的多个胶囊编译成带 wikilinks 的 concept page。
支持手动触发（POST /admin/compile）和自动 daemon 触发。

v1.2.38: 新增 wiki_content 格式 + wikilinks + 覆盖缺口检测
"""

from __future__ import annotations

import json
import secrets
import threading
import time
from pathlib import Path
from typing import Optional

from core.llm import get_llm

# ── Prompt 模板 ──────────────────────────────────────────────────────────────

WIKI_COMPILER_SYSTEM = """You are a memory analyst building a personal wiki for a second-brain system.
Given capsules from the same topic, generate a structured concept page in markdown.
Rules:
- Output valid markdown starting with H1 title: ## {topic_title}
- Each capsule reference must use wikilink format: [[capsule_id:short_topic]]
- Include sections: ## Overview, ## Key Insights, ## Decisions & Conclusions
- Include a ## Related Capsules section that links to every source capsule
- Keep total under 400 words
- Do NOT fabricate capsule IDs — only use the IDs provided in the input"""

WIKI_COMPILER_USER = """path: {path}

source capsules (id | memo):
{capsules_text}

Generate a concept page in markdown for this topic.
Rules:
- H1 title: ## {topic_title}
- Overview: 2-3 sentence summary
- Key Insights: 3-5 bullet points synthesizing what these capsules teach
- Decisions & Conclusions: any decisions or conclusions drawn
- Related Capsules: one [[capsule_id:short_topic]] wikilink per source capsule
- Keep total under 400 words"""


# ── 编译函数 ──────────────────────────────────────────────────────────────────

def compile_concept_page(
    path: str,
    capsule_ids: list[str],
    memos: list[str],
    hotness: float,
) -> dict | None:
    """
    将同 path 的多个胶囊编译成一个 concept page dict。
    失败返回 None。
    """
    if not memos or not capsule_ids:
        return None

    try:
        llm = get_llm()

        # 构建胶囊文本 (id | memo 格式)
        capsules_text = "\n".join(
            f"[{cid}] {m[:200]}" for cid, m in zip(capsule_ids, memos)
        )

        # 从 path 提取 topic title（如 dev/python → Python）
        topic_title = _slug_to_title(path)

        prompt = WIKI_COMPILER_USER.format(
            path=path,
            topic_title=topic_title,
            capsules_text=capsules_text[:2500],
        )

        wiki_content = llm.complete(
            prompt,
            system=WIKI_COMPILER_SYSTEM.format(topic_title=topic_title),
            max_tokens=600,
            temperature=0.2,
        )

        if not wiki_content or wiki_content.startswith("[ERROR"):
            return None

        wiki_content = wiki_content.strip()

        # 提取第一段作为纯文本 summary（兼容旧 insight 格式）
        lines = wiki_content.split("\n")
        summary_parts = [
            l.lstrip("#* -").strip()
            for l in lines
            if l.strip() and not l.strip().startswith("#")
        ]
        summary = " ".join(summary_parts)[:200]

        concept_slug = _path_to_slug(path)

        return {
            "id": secrets.token_hex(6),
            "capsule_ids": json.dumps(capsule_ids),
            "summary": summary,
            "path": path,
            "concept_slug": concept_slug,
            "wiki_content": wiki_content,
            "hotness_score": hotness,
            "created_at": time.time(),
            "updated_at": time.time(),
        }

    except Exception as e:
        import sys
        print(f"[compile_concept_page] failed for path={path}: {e}", file=sys.stderr)
        return None


def _slug_to_title(path: str) -> str:
    """dev/python → Python; dev/fastapi-best-practices → Fastapi Best Practices"""
    parts = path.split("/")
    last = parts[-1] if parts else path
    return last.replace("-", " ").replace("_", " ").title()


def _path_to_slug(path: str) -> str:
    """dev/python → dev-python; dev/fastapi → dev-fastapi"""
    return path.replace("/", "-")


# ── 覆盖缺口检测 ─────────────────────────────────────────────────────────────

def detect_coverage_gaps(conn) -> list[dict]:
    """
    返回有 ≥3 个胶囊但无 concept page 的 category_path 列表。
    """
    c = conn.cursor()

    # 有胶囊但无 concept page 的 path
    rows = c.execute("""
        SELECT category_path, COUNT(*) as cnt
        FROM capsules
        WHERE category_path != 'general/default'
        GROUP BY category_path
        HAVING cnt >= 3
    """).fetchall()

    gaps = []
    for (path, cnt) in rows:
        # 检查是否已有带 wiki_content 的 insight
        existing = c.execute(
            "SELECT 1 FROM insights WHERE path=? AND wiki_content IS NOT NULL AND wiki_content != '' LIMIT 1",
            (path,),
        ).fetchone()
        if not existing:
            gaps.append({
                "path": path,
                "capsule_count": cnt,
                "reason": ">=3 capsules but no concept page",
            })

    return gaps


# ── 后台 Daemon ───────────────────────────────────────────────────────────────

_compile_daemon_thread: Optional[threading.Thread] = None
_compile_daemon_running = False
_compile_daemon_consecutive_failures = 0
_compile_daemon_last_error: Optional[str] = None
_compile_daemon_last_success_at: Optional[float] = None
_compile_daemon_compilations_count = 0


def _compile_daemon_loop(interval_hours: float = 6.0, capsule_threshold: int = 100):
    """
    后台编译 daemon：
    - 每 interval_hours 小时编译一次所有覆盖缺口 path
    - 同时监听胶囊增量，达到 threshold 后立即编译一次
    """
    global _compile_daemon_running, _compile_daemon_compilations_count
    global _compile_daemon_consecutive_failures, _compile_daemon_last_error
    global _compile_daemon_last_success_at

    import core.db as db_module

    last_compile_at = 0.0
    last_capsule_count = 0

    while _compile_daemon_running:
        try:
            conn = db_module._get_conn()
            c = conn.cursor()

            # 检测胶囊增量
            current_count = c.execute("SELECT COUNT(*) FROM capsules").fetchone()[0]
            delta = current_count - last_capsule_count

            # 触发条件：超过阈值 或 超过 interval
            should_compile = (
                (last_capsule_count > 0 and delta >= capsule_threshold) or
                (time.time() - last_compile_at >= interval_hours * 3600)
            )

            if should_compile:
                stats = _run_batch_compile(conn)
                last_compile_at = time.time()
                last_capsule_count = current_count
                if stats["compiled"] > 0:
                    _compile_daemon_compilations_count += stats["compiled"]
                    _compile_daemon_consecutive_failures = 0
                    _compile_daemon_last_success_at = time.time()

            conn.close()

        except Exception as e:
            import sys
            print(f"[_compile_daemon] error: {e}", file=sys.stderr)
            _compile_daemon_consecutive_failures += 1
            _compile_daemon_last_error = str(e)

        time.sleep(300)  # 每 5 分钟检查一次


def _run_batch_compile(conn) -> dict:
    """
    批量编译所有覆盖缺口 path。返回统计。
    """
    c = conn.cursor()
    gaps = detect_coverage_gaps(conn)
    stats = {"compiled": 0, "skipped": 0, "failed": 0, "paths": []}

    # 最多每次处理 3 个 path
    for gap in gaps[:3]:
        path = gap["path"]

        # 跳过 7 天内已更新的
        recent = c.execute(
            "SELECT 1 FROM insights WHERE path=? AND updated_at>? LIMIT 1",
            (path, time.time() - 86400 * 7),
        ).fetchone()
        if recent:
            stats["skipped"] += 1
            continue

        rows = c.execute(
            "SELECT id, memo, hotness_score FROM capsules WHERE category_path=? ORDER BY hotness_score DESC LIMIT 20",
            (path,),
        ).fetchall()

        if len(rows) < 3:
            stats["skipped"] += 1
            continue

        ids = [r[0] for r in rows]
        memos = [r[1] for r in rows if r[1]]
        avg_hot = sum(r[2] or 0 for r in rows) / len(rows)

        insight = compile_concept_page(path, ids, memos, avg_hot)
        if insight:
            # 防止同一 path 重复编译（先删后插）
            # id 每次随机生成，INSERT OR REPLACE 无法识别为同一 record
            c.execute("DELETE FROM insights WHERE path=?", (path,))
            c.execute("""
                INSERT INTO insights
                  (id, capsule_ids, summary, path, concept_slug, wiki_content, hotness_score, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                insight["id"], insight["capsule_ids"], insight["summary"],
                insight["path"], insight["concept_slug"], insight["wiki_content"],
                insight["hotness_score"], insight["created_at"], insight["updated_at"],
            ))
            conn.commit()
            stats["compiled"] += 1
            stats["paths"].append(path)
        else:
            stats["failed"] += 1

    return stats


def start_compile_daemon(interval_hours: float = 6.0, capsule_threshold: int = 100):
    """启动编译 daemon（幂等）"""
    global _compile_daemon_thread, _compile_daemon_running

    if _compile_daemon_thread is not None and _compile_daemon_thread.is_alive():
        return  # 已在运行

    _compile_daemon_running = True
    _compile_daemon_thread = threading.Thread(
        target=_compile_daemon_loop,
        args=(interval_hours, capsule_threshold),
        name="wiki-compile-daemon",
        daemon=True,
    )
    _compile_daemon_thread.start()


def stop_compile_daemon():
    global _compile_daemon_running
    _compile_daemon_running = False


def get_compile_daemon_status() -> dict:
    """
    返回 daemon 健康状态，供 /admin/compile/status API 使用。
    """
    is_running = (
        _compile_daemon_thread is not None
        and _compile_daemon_thread.is_alive()
        and _compile_daemon_running
    )
    return {
        "is_running": is_running,
        "consecutive_failures": _compile_daemon_consecutive_failures,
        "last_error": _compile_daemon_last_error,
        "last_success_at": _compile_daemon_last_success_at,
        "total_compilations": _compile_daemon_compilations_count,
        "alert": (
            "CRITICAL" if _compile_daemon_consecutive_failures >= 3
            else "WARNING" if _compile_daemon_consecutive_failures >= 1
            else "OK"
        ) if is_running else "STOPPED",
    }
