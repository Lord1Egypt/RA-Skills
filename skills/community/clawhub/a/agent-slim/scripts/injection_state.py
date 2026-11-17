#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Codex 固定注入状态机：源文件指纹 -> 重启后复核实际注入 -> OK/DRIFT/UNKNOWN。

子命令：
  --record    记录 5 个源文件的 sha256 / 字节 / mtime，并抓取当前注入块字节
  --check     比对源文件指纹与实际注入块；输出每项 OK/DRIFT/MISSING 与 VERIFIED/UNVERIFIED
  --volatile  列出插件缓存技能，标 volatile=true，并记录当前描述字节（不计永久收益）

范围（只读源文件）：
  ${CODEX_HOME}/memories/memory_summary.md
  ${CODEX_HOME}/AGENTS.md
  ${CODEX_HOME}/rules/default.rules
  ${CODEX_HOME}/lessons/LESSONS.md
  ${CODEX_HOME}/skills/*/SKILL.md（只记 description 行 hash 与总字节）
  ${CODEX_HOME}/plugins/cache/**/skills/*/SKILL.md（volatile，仅清单与描述字节）

状态文件默认 ${CODEX_HOME}/memory/injection-state.json；写前备份旧文件到
${CODEX_HOME}/backups/injection-state/。不修改任何被监控文件。

退出码：
  0  OK / VERIFIED（MCP 未实测记 UNKNOWN，不误报为已验）
  1  DRIFT / MISSING / 注入字节不一致（UNVERIFIED）
  2  状态文件损坏、测量失败或参数错误
  3  未预期异常
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

SCHEMA_VERSION = 1
DEFAULT_GATE = 57344

CODEX_HOME = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
DEFAULT_STATE = CODEX_HOME / "memory" / "injection-state.json"
BACKUP_DIR = CODEX_HOME / "backups" / "injection-state"

# 5 个受监控源文件；skills 目录单独处理。
SOURCE_FILES = {
    "memory": CODEX_HOME / "memories" / "memory_summary.md",
    "AGENTS": CODEX_HOME / "AGENTS.md",
    "default_rules": CODEX_HOME / "rules" / "default.rules",
    "LESSONS": CODEX_HOME / "lessons" / "LESSONS.md",
}
SKILLS_DIR = CODEX_HOME / "skills"
PLUGINS_CACHE = CODEX_HOME / "plugins" / "cache"

# 实际注入块里可逐字节核验的块；mcp/base 不可由 CLI 调试视图实测。
VERIFIABLE_BLOCKS = ["memory", "skills", "permissions", "AGENTS"]
BLOCK_LABELS = {
    "memory": "记忆摘要",
    "skills": "技能目录",
    "permissions": "权限块",
    "AGENTS": "全局 AGENTS",
    "base": "基础系统提示",
    "mcp": "MCP schema",
    "env": "环境上下文",
}

# s3 开工时给定的参考值（仅用于 record 时对照，不替代实测）。
REFERENCE_INJECTION = {
    "memory": 8081,
    "skills": 7744,
    "permissions": 5665,
    "AGENTS": 5443,
    "mcp": 3900,
}
# s2 的 MCP 结论：原始 schema 实测已知 + codex_app 上界；App 实际注入仍未测。
S2_MCP = {
    "measured_known_raw_schema_bytes": 130481,
    "codex_app_upper_bound_bytes": 12400,
    "raw_known_plus_upper_bytes": 142881,
    "app_injection_status": "UNMEASURED",
    "source": "outputs/mcp-schema-20261109.json",
}


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_fingerprint(path: Path) -> dict:
    try:
        st = path.stat()
        data = path.read_bytes()
    except FileNotFoundError:
        return {"path": str(path), "status": "MISSING", "exists": False}
    except OSError as exc:
        return {"path": str(path), "status": "MISSING", "exists": False,
                "error": f"{type(exc).__name__}: {exc}"}
    return {
        "path": str(path),
        "status": "OK",
        "exists": True,
        "bytes": len(data),
        "sha256": sha256_bytes(data),
        "mtime": datetime.fromtimestamp(st.st_mtime).astimezone().isoformat(timespec="seconds"),
        "mtime_epoch": st.st_mtime,
    }


def parse_description(path: Path) -> dict | None:
    """解析 YAML frontmatter 的 description（支持单行引号与 |/> 块）。"""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None

    for i in range(1, end):
        line = lines[i]
        if not line.startswith("description:"):
            continue
        value_raw = line[len("description:"):].strip()
        if value_raw in ("|", ">", "|-", ">-", "|+", ">+"):
            block = []
            j = i + 1
            while j < end:
                nxt = lines[j]
                if nxt.startswith((" ", "\t")) or nxt.strip() == "":
                    block.append(nxt)
                    j += 1
                else:
                    break
            indents = [len(x) - len(x.lstrip(" ")) for x in block if x.strip()]
            cut = min(indents) if indents else 0
            body = [x[cut:] if len(x) >= cut else "" for x in block]
            value = ("\n" if value_raw.startswith("|") else " ").join(
                x for x in body if x.strip()
            ).strip()
            raw = "\n".join(block)
        else:
            value = value_raw
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
                value = value[1:-1]
            raw = value_raw
        return {
            "description": value,
            "description_sha256": sha256_bytes(value.encode("utf-8")),
            "description_bytes": len(value.encode("utf-8")),
            "description_raw_sha256": sha256_bytes(raw.encode("utf-8")),
        }
    return None


def skill_fingerprint(path: Path, root: Path) -> dict:
    fp = file_fingerprint(path)
    desc = parse_description(path) or {}
    slug = path.parent.name
    try:
        rel = str(path.relative_to(root))
    except ValueError:
        rel = str(path)
    return {
        "slug": slug,
        "rel_path": rel,
        "path": str(path),
        "skill_md_bytes": fp.get("bytes"),
        "skill_md_sha256": fp.get("sha256"),
        "skill_md_mtime": fp.get("mtime"),
        "description_bytes": desc.get("description_bytes"),
        "description_sha256": desc.get("description_sha256"),
        "description_raw_sha256": desc.get("description_raw_sha256"),
        "description": desc.get("description"),
    }


def skills_fingerprint() -> dict:
    paths = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    entries = [skill_fingerprint(p, SKILLS_DIR) for p in paths]
    agg = hashlib.sha256()
    for e in entries:
        agg.update((e.get("slug") or "").encode("utf-8"))
        agg.update(b"\0")
        agg.update((e.get("description_sha256") or "").encode("ascii"))
        agg.update(b"\n")
    return {
        "path": str(SKILLS_DIR),
        "status": "OK" if paths else "MISSING",
        "count": len(entries),
        "total_skill_md_bytes": sum(e.get("skill_md_bytes") or 0 for e in entries),
        "total_description_bytes": sum(e.get("description_bytes") or 0 for e in entries),
        "description_aggregate_sha256": agg.hexdigest(),
        "skills": entries,
    }


def volatile_fingerprint() -> dict:
    pattern = "**/skills/*/SKILL.md"
    paths = sorted(PLUGINS_CACHE.glob(pattern)) if PLUGINS_CACHE.exists() else []
    entries = []
    for p in paths:
        desc = parse_description(p) or {}
        fp = file_fingerprint(p)
        try:
            rel = p.relative_to(PLUGINS_CACHE)
        except ValueError:
            rel = p
        entries.append({
            "slug": p.parent.name,
            "rel_path": str(rel),
            "path": str(p),
            "volatile": True,
            "counted_in_permanent_savings": False,
            "skill_md_bytes": fp.get("bytes"),
            "description_bytes": desc.get("description_bytes"),
            "description_sha256": desc.get("description_sha256"),
            "expected_behavior": "App/插件升级可能复原描述；变化属预期，不计失败、不计永久收益",
        })
    return {
        "path": str(PLUGINS_CACHE),
        "pattern": pattern,
        "count": len(entries),
        "total_description_bytes": sum(e.get("description_bytes") or 0 for e in entries),
        "total_skill_md_bytes": sum(e.get("skill_md_bytes") or 0 for e in entries),
        "entries": entries,
    }


def run_measure() -> dict:
    measure = Path(__file__).with_name("measure_prompt.py")
    if not measure.exists():
        raise RuntimeError(f"找不到测量器: {measure}")
    proc = subprocess.run(
        [sys.executable, str(measure), "--json"],
        cwd=str(measure.parent),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=180,
        check=False,
    )
    if proc.returncode not in (0, 1):
        err = (proc.stderr or "").strip().replace("\n", " ")[:500]
        raise RuntimeError(f"measure_prompt.py 失败 rc={proc.returncode}: {err}")
    try:
        data = json.loads(proc.stdout.lstrip("\ufeff"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"measure_prompt.py 输出不是合法 JSON: {exc}") from exc
    return data


def injection_blocks_from_measure(measured: dict) -> dict:
    blocks = {}
    for b in measured.get("blocks", []):
        bid = b.get("id")
        if not bid:
            continue
        source = b.get("source")
        if bid == "mcp":
            verifiable_flag = False
            status_note = "assumption；App 实际注入未实测（s2 raw schema 已知 130,481 B + codex_app 上界 12,400 B）"
        elif bid == "base":
            verifiable_flag = False
            status_note = "static 基线；CLI 调试视图不渲染"
        elif bid in VERIFIABLE_BLOCKS:
            verifiable_flag = True
            status_note = "逐字节核验"
        else:
            verifiable_flag = False
            status_note = "参考值"
        blocks[bid] = {
            "bytes": b.get("bytes"),
            "sha256_12": b.get("sha256_12"),
            "source": source,
            "verifiable": verifiable_flag,
            "note": status_note,
        }
    return blocks


def backup_state(path: Path) -> str | None:
    if not path.exists():
        return None
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = BACKUP_DIR / f"{path.stem}-{ts}.json"
    n = 1
    while target.exists():
        target = BACKUP_DIR / f"{path.stem}-{ts}-{n}.json"
        n += 1
    shutil.copy2(path, target)
    return str(target)


def save_state(state: dict, path: Path) -> str | None:
    path.parent.mkdir(parents=True, exist_ok=True)
    backup = backup_state(path)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(state, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    return backup


def load_state(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"状态文件不存在: {path}（先跑 --record）") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"状态文件不是合法 JSON: {path}: {exc}") from exc


def build_record(state_path: Path) -> dict:
    files = {name: file_fingerprint(p) for name, p in SOURCE_FILES.items()}
    skills = skills_fingerprint()
    volatile = volatile_fingerprint()
    measured = run_measure()
    inj_blocks = injection_blocks_from_measure(measured)
    reference_diff = {}
    for bid, ref in REFERENCE_INJECTION.items():
        got = (inj_blocks.get(bid) or {}).get("bytes")
        reference_diff[bid] = {"reference": ref, "measured": got,
                               "delta": (got - ref) if isinstance(got, int) else None}
    return {
        "schema_version": SCHEMA_VERSION,
        "project": "agent-slim-r2",
        "step": "s3",
        "recorded_at": now_iso(),
        "codex_home": str(CODEX_HOME),
        "state_path": str(state_path),
        "monitor_mode": "read_only_sources",
        "files": files,
        "skills": skills,
        "injection_expect": {
            "measured_at": measured.get("timestamp"),
            "measure_command": f"{sys.executable} {Path(__file__).with_name('measure_prompt.py')} --json",
            "gate_bytes": measured.get("gate_bytes", DEFAULT_GATE),
            "gate_status": measured.get("gate_status"),
            "text_blocks_total": measured.get("text_blocks_total"),
            "total_bytes": measured.get("total"),
            "overall_status": measured.get("overall_status", "UNMEASURED"),
            "overall_upper_total": measured.get("overall_upper_total"),
            "blocks": inj_blocks,
            "verifiable_blocks": VERIFIABLE_BLOCKS,
            "reference_diff": reference_diff,
            "mcp_s2": S2_MCP,
        },
        "volatile": volatile,
    }


def compare_skills(recorded: dict) -> dict:
    current = skills_fingerprint()
    old = {e.get("slug"): e for e in recorded.get("skills", [])}
    new = {e.get("slug"): e for e in current.get("skills", [])}
    changed = []
    body_changed = []
    for slug in sorted(set(old) & set(new)):
        a, b = old[slug], new[slug]
        fields = []
        if a.get("description_sha256") != b.get("description_sha256"):
            fields.append("description")
        if a.get("skill_md_sha256") != b.get("skill_md_sha256"):
            fields.append("skill_md")
        if fields:
            entry = {
                "slug": slug,
                "fields": fields,
                "recorded_description_bytes": a.get("description_bytes"),
                "current_description_bytes": b.get("description_bytes"),
                "recorded_skill_md_bytes": a.get("skill_md_bytes"),
                "current_skill_md_bytes": b.get("skill_md_bytes"),
            }
            # 只有 description 才进入技能目录注入；正文/脚本改动不影响注入字节。
            if "description" in fields:
                changed.append(entry)
            else:
                body_changed.append(entry)
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    count_drift = current.get("count") != recorded.get("count")
    if changed or added or removed or count_drift:
        status = "DRIFT"
    elif body_changed:
        status = "BODY_CHANGED"
    else:
        status = "OK"
    return {
        "status": status,
        "count_recorded": recorded.get("count"),
        "count_current": current.get("count"),
        "total_skill_md_bytes_recorded": recorded.get("total_skill_md_bytes"),
        "total_skill_md_bytes_current": current.get("total_skill_md_bytes"),
        "total_description_bytes_recorded": recorded.get("total_description_bytes"),
        "total_description_bytes_current": current.get("total_description_bytes"),
        "description_aggregate_sha256_recorded": recorded.get("description_aggregate_sha256"),
        "description_aggregate_sha256_current": current.get("description_aggregate_sha256"),
        "changed": changed,
        "body_changed": body_changed,
        "added": added,
        "removed": removed,
    }


def compare_volatile(recorded: dict) -> dict:
    current = volatile_fingerprint()
    old = {e.get("path"): e for e in recorded.get("entries", [])}
    new = {e.get("path"): e for e in current.get("entries", [])}
    changed = []
    for path in sorted(set(old) & set(new)):
        if old[path].get("description_sha256") != new[path].get("description_sha256"):
            changed.append({
                "slug": new[path].get("slug"),
                "rel_path": new[path].get("rel_path"),
                "recorded_description_bytes": old[path].get("description_bytes"),
                "current_description_bytes": new[path].get("description_bytes"),
                "status": "VOLATILE_CHANGED_EXPECTED",
            })
    added = [new[p].get("rel_path") for p in sorted(set(new) - set(old))]
    removed = [old[p].get("rel_path") for p in sorted(set(old) - set(new))]
    return {
        "count_recorded": recorded.get("count"),
        "count_current": current.get("count"),
        "changed_expected": changed,
        "added": added,
        "removed": removed,
        "note": "插件缓存为易挥发层；变化不影响整体判定，不计永久收益",
    }


def run_check(state_path: Path) -> dict:
    state = load_state(state_path)
    if state.get("schema_version") != SCHEMA_VERSION:
        raise RuntimeError(f"状态文件 schema_version 不支持: {state.get('schema_version')}")

    files = {}
    for name, p in SOURCE_FILES.items():
        rec = (state.get("files") or {}).get(name) or {}
        cur = file_fingerprint(p)
        if cur.get("status") == "MISSING":
            status = "MISSING"
        elif rec.get("sha256") and rec.get("sha256") == cur.get("sha256") and rec.get("bytes") == cur.get("bytes"):
            status = "OK"
        else:
            status = "DRIFT"
        files[name] = {
            "status": status,
            "path": str(p),
            "recorded_bytes": rec.get("bytes"),
            "current_bytes": cur.get("bytes"),
            "recorded_sha256": rec.get("sha256"),
            "current_sha256": cur.get("sha256"),
            "recorded_mtime": rec.get("mtime"),
            "current_mtime": cur.get("mtime"),
            "delta_bytes": (cur.get("bytes") - rec.get("bytes"))
            if isinstance(cur.get("bytes"), int) and isinstance(rec.get("bytes"), int) else None,
        }
    skills = compare_skills(state.get("skills") or {})
    files["skills"] = skills

    injection = {"status": "UNVERIFIED", "blocks": {}, "error": None}
    try:
        measured = run_measure()
        expect = state.get("injection_expect") or {}
        exp_blocks = expect.get("blocks") or {}
        all_ok = True
        for bid in VERIFIABLE_BLOCKS:
            exp = exp_blocks.get(bid) or {}
            cur = next((b for b in measured.get("blocks", []) if b.get("id") == bid), None)
            if cur is None:
                injection["blocks"][bid] = {"status": "UNKNOWN", "reason": "测量结果缺少该块"}
                all_ok = False
                continue
            same = cur.get("bytes") == exp.get("bytes") and cur.get("sha256_12") == exp.get("sha256_12")
            if not same:
                all_ok = False
            injection["blocks"][bid] = {
                "status": "VERIFIED" if same else "UNVERIFIED",
                "label": BLOCK_LABELS.get(bid, bid),
                "expected_bytes": exp.get("bytes"),
                "measured_bytes": cur.get("bytes"),
                "delta_bytes": (cur.get("bytes") - exp.get("bytes"))
                if isinstance(cur.get("bytes"), int) and isinstance(exp.get("bytes"), int) else None,
                "expected_sha256_12": exp.get("sha256_12"),
                "measured_sha256_12": cur.get("sha256_12"),
            }
        # MCP：明确 UNKNOWN，不用假设值冒充已验证。
        mcp_exp = exp_blocks.get("mcp") or {}
        mcp_cur = next((b for b in measured.get("blocks", []) if b.get("id") == "mcp"), None)
        injection["blocks"]["mcp"] = {
            "status": "UNKNOWN",
            "label": BLOCK_LABELS["mcp"],
            "expected_bytes": mcp_exp.get("bytes"),
            "measured_bytes": (mcp_cur or {}).get("bytes"),
            "source": (mcp_cur or {}).get("source"),
            "reason": "App 实际 MCP 注入未实测；s2 raw schema 已知 130,481 B + codex_app 上界 12,400 B",
        }
        # base：静态参考，不参与判定。
        base_cur = next((b for b in measured.get("blocks", []) if b.get("id") == "base"), None)
        if base_cur:
            injection["blocks"]["base"] = {
                "status": "UNKNOWN",
                "label": BLOCK_LABELS["base"],
                "measured_bytes": base_cur.get("bytes"),
                "source": base_cur.get("source"),
                "reason": "静态基线，CLI 调试视图不渲染",
            }
        injection["status"] = "VERIFIED" if all_ok else "UNVERIFIED"
        injection["measured_at"] = measured.get("timestamp")
        injection["gate_bytes"] = measured.get("gate_bytes")
        injection["gate_status"] = measured.get("gate_status")
        injection["text_blocks_total"] = measured.get("text_blocks_total")
        injection["total_bytes"] = measured.get("total")
        injection["overall_status"] = measured.get("overall_status", "UNMEASURED")
        injection["overall_upper_total"] = measured.get("overall_upper_total")
    except Exception as exc:  # noqa: BLE001 - 状态机需把测量失败降级为 UNVERIFIED
        injection["status"] = "UNVERIFIED"
        injection["error"] = f"{type(exc).__name__}: {exc}"

    volatile = compare_volatile(state.get("volatile") or {})

    files_ok = all(
        (v.get("status") == "OK") for k, v in files.items() if k != "skills"
    ) and skills.get("status") in ("OK", "BODY_CHANGED")
    overall = "OK" if files_ok and injection.get("status") == "VERIFIED" else "FAIL"
    return {
        "schema_version": SCHEMA_VERSION,
        "project": state.get("project", "agent-slim-r2"),
        "checked_at": now_iso(),
        "state_path": str(state_path),
        "recorded_at": state.get("recorded_at"),
        "files_status": "OK" if files_ok else "DRIFT",
        "files": files,
        "injection_status": injection.get("status"),
        "injection": injection,
        "volatile": volatile,
        "overall": overall,
        "restart_recheck_command": f"python3 {Path(__file__).resolve()} --check",
        "notes": [
            "MCP 块为 UNKNOWN：s2 只测到服务端 raw schema，App 实际注入仍未实测；不得写 VERIFIED。",
            "插件缓存为易挥发层：描述被 App/插件升级复原属预期行为，不计失败、不计永久收益。",
            "技能正文/脚本变更记为 BODY_CHANGED：不改技能目录注入字节，不判失败；只有 description、增删或数量变化才记 DRIFT。",
        ],
    }


def print_record(state: dict, state_path: Path, backup: str | None, as_json: bool) -> None:
    if as_json:
        print(json.dumps({"state_path": str(state_path), "backup": backup, "record": state},
                         ensure_ascii=False, indent=2))
        return
    print(f"state: {state_path}")
    print(f"backup: {backup or '(首次写入，无旧状态)'}")
    print(f"recorded_at: {state['recorded_at']}")
    print("files:")
    for name, f in state["files"].items():
        print(f"  {name:14s} {f.get('status'):7s} {f.get('bytes')!s:>8} B  {str(f.get('sha256'))[:12]}")
    s = state["skills"]
    print(f"  {'skills':14s} {s.get('status'):7s} {s.get('total_skill_md_bytes')!s:>8} B  "
          f"count={s.get('count')} desc_bytes={s.get('total_description_bytes')}")
    e = state["injection_expect"]
    print(f"injection: total_with_mcp_placeholder={e.get('total_bytes')} text={e.get('text_blocks_total')} "
          f"text_gate={e.get('gate_bytes')}/{e.get('gate_status')} overall={e.get('overall_status', 'UNMEASURED')}")
    for bid, diff in e.get("reference_diff", {}).items():
        print(f"  {bid:12s} measured={diff['measured']!s:>8} reference={diff['reference']!s:>8} delta={diff['delta']}")
    v = state["volatile"]
    print(f"volatile: {v.get('count')} plugin skills, desc_bytes={v.get('total_description_bytes')} "
          "(不计永久收益)")


def print_check(result: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"state: {result['state_path']}  recorded_at: {result.get('recorded_at')}")
    print("source files:")
    for name, f in result["files"].items():
        if name == "skills":
            print(f"  {'skills':12s} {f['status']:7s} count {f.get('count_recorded')}->{f.get('count_current')}  "
                  f"desc {f.get('total_description_bytes_recorded')}->{f.get('total_description_bytes_current')} B")
            for c in f.get("changed", []):
                print(f"    DRIFT {c['slug']}: {','.join(c['fields'])} "
                      f"desc {c.get('recorded_description_bytes')}->{c.get('current_description_bytes')} B")
            for c in f.get("body_changed", []):
                print(f"    BODY_CHANGED {c['slug']}: md {c.get('recorded_skill_md_bytes')}->"
                      f"{c.get('current_skill_md_bytes')} B（不影响技能目录注入）")
            for a in f.get("added", []):
                print(f"    ADDED {a}")
            for r in f.get("removed", []):
                print(f"    REMOVED {r}")
        else:
            print(f"  {name:12s} {f['status']:7s} {f.get('recorded_bytes')}->{f.get('current_bytes')} B "
                  f"delta={f.get('delta_bytes')}")
    print(f"injection: {result['injection_status']}  total_with_mcp_placeholder={result['injection'].get('total_bytes')} "
          f"text={result['injection'].get('text_blocks_total')} text_gate={result['injection'].get('gate_bytes')}/"
          f"{result['injection'].get('gate_status')} overall={result['injection'].get('overall_status', 'UNMEASURED')}")
    for bid, b in result["injection"].get("blocks", {}).items():
        print(f"  {bid:12s} {b['status']:10s} "
              f"expected={b.get('expected_bytes')} measured={b.get('measured_bytes')} "
              f"delta={b.get('delta_bytes')}")
    v = result.get("volatile") or {}
    print(f"volatile: {v.get('count_recorded')}->{v.get('count_current')}  "
          f"changed_expected={len(v.get('changed_expected') or [])} added={len(v.get('added') or [])} "
          f"removed={len(v.get('removed') or [])}")
    for c in v.get("changed_expected") or []:
        print(f"  VOLATILE_CHANGED(预期) {c.get('slug')} "
              f"desc {c.get('recorded_description_bytes')}->{c.get('current_description_bytes')} B")
    print(f"overall: {result['overall']}")
    print(f"重启后一条命令复核: {result['restart_recheck_command']}")


def print_volatile(vol: dict, as_json: bool, persisted: str | None, backup: str | None) -> None:
    if as_json:
        print(json.dumps({"volatile": vol, "persisted_to": persisted, "backup": backup},
                         ensure_ascii=False, indent=2))
        return
    print(f"plugin cache: {vol['path']}  ({vol['count']} SKILL.md)")
    for e in vol["entries"]:
        print(f"  volatile=true  desc={e.get('description_bytes')!s:>4} B  "
              f"md={e.get('skill_md_bytes')!s:>6} B  {e.get('rel_path')}")
    print(f"total_description_bytes: {vol['total_description_bytes']}")
    print("note: 插件缓存易挥发；描述被复原属预期，不计永久收益。")
    if persisted:
        print(f"persisted_to: {persisted}")
        print(f"backup: {backup or '(无旧状态)'}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Codex 固定注入状态机（record/check/volatile）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--record", action="store_true", help="记录源文件指纹与当前注入块")
    action.add_argument("--check", action="store_true", help="比对源文件与当前注入块")
    action.add_argument("--volatile", action="store_true", help="列出插件缓存技能并标 volatile")
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE, help="状态文件路径")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args(argv)

    try:
        if args.record:
            state = build_record(args.state)
            backup = save_state(state, args.state)
            print_record(state, args.state, backup, args.json)
            return 0

        if args.check:
            result = run_check(args.state)
            print_check(result, args.json)
            return 0 if result["overall"] == "OK" else 1

        vol = volatile_fingerprint()
        persisted = None
        backup = None
        if args.state.exists():
            state = load_state(args.state)
            state["volatile"] = vol
            state["volatile_recorded_at"] = now_iso()
            backup = save_state(state, args.state)
            persisted = str(args.state)
        print_volatile(vol, args.json, persisted, backup)
        return 0
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001
        print(f"UNEXPECTED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
