#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测量 Codex 七块固定注入：字节、SHA-256(12)、来源、闸门、对账。

只读工具：
- 在 /tmp 执行 `codex debug prompt-input "x"`，解析所有 input_text 块；
- CLI 调试视图不渲染的块用明确来源补齐：
  * 记忆摘要：读 ${CODEX_HOME}/memories/memory_summary.md（measured）；
  * 基础系统提示：2026-11-09 app instructions_template 静态基线（static）；
  * MCP schema：3,900 B 仅为“七块占位”，不是 App 实际注入；s2 已实测
    原始 tools/list：github 126,805 / node_repl 2,400 / lis-skill-bus 1,276 B，
    codex_app 不可测（31 工具，上界 12,400 B）。App 首请求实际注入仍 UNMEASURED。
    因此本工具把闸门拆成“文本块闸门”和“整体口径”，整体缺实测时输出 UNMEASURED。
- 不读取聊天正文，不写入 ${CODEX_HOME} 下任何文件。

退出码：
  0  测量成功且未超闸门
  1  测量成功但超过 --gate
  2  对账失败 / 基线 JSON 内部不一致（MISMATCH）
  3  测量命令或输入解析失败
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REQUIRED_IDS = ["memory", "base", "skills", "permissions", "AGENTS", "mcp", "env"]
LABELS = {
    "memory": "记忆摘要",
    "base": "基础系统提示",
    "skills": "技能目录",
    "permissions": "权限块",
    "AGENTS": "全局 AGENTS",
    "mcp": "MCP schema",
    "env": "环境上下文",
}
ORDER = {k: i for i, k in enumerate(REQUIRED_IDS)}

DEFAULT_GATE = 57344  # 56 KiB
TRUNCATION_MARKER = "[Some commands were truncated]"

# 2026-11-09 从 ChatGPT.app 内置 codex 二进制抽取的最大 instructions_template。
# 只作为静态基线；若 App 升级，应重新抽取并更新这两个常量。
STATIC_BASE_PROMPT_BYTES = 21779
STATIC_BASE_PROMPT_SHA256 = "e1bdd4f8f0df4b20f4a0ffc8a861ce819df45325d8cecdfb92e80379cf8d142e"
STATIC_BASE_BINARY = Path("/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex")

# 11-05 的 MCP schema 假设值；s2 实测前不得写成 measured。
ASSUMED_MCP_BYTES = 3900  # 仅七块占位，不是实测注入
NODE_REPL_MCP_MEASURED_BYTES = 2400
CODEX_APP_MCP_UPPER_BYTES = 12400
RAW_MCP_KNOWN_BYTES = 130481
RAW_MCP_UPPER_BYTES = 142881

CODEX_HOME = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))


class MeasureError(RuntimeError):
    """测量阶段错误（退出码 3）。"""


class ReconcileError(RuntimeError):
    """对账失败（退出码 2）。"""


def sha12(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:12]


def iso_mtime(path: Path | None) -> str | None:
    if path is None:
        return None
    try:
        return datetime.fromtimestamp(path.stat().st_mtime).astimezone().isoformat(timespec="seconds")
    except OSError:
        return None


def run_prompt_input() -> tuple[list[str], dict]:
    """在 /tmp 运行 codex debug prompt-input "x"，返回 input_text 文本列表。"""
    exe = shutil.which("codex")
    if not exe:
        raise MeasureError("找不到 codex 命令（PATH 中没有）")
    cmd = [exe, "debug", "prompt-input", "x"]
    try:
        proc = subprocess.run(
            cmd,
            cwd="/tmp",
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise MeasureError("codex debug prompt-input 超时（>120s）") from exc
    if proc.returncode != 0:
        stderr = (proc.stderr or "").strip().replace("\n", " ")[:500]
        raise MeasureError(f"codex debug prompt-input 失败 rc={proc.returncode}: {stderr}")

    try:
        payload = json.loads(proc.stdout.lstrip("\ufeff"))
    except json.JSONDecodeError as exc:
        raise MeasureError(f"codex debug prompt-input 输出不是合法 JSON: {exc}") from exc

    texts: list[str] = []
    if isinstance(payload, list):
        for item in payload:
            if not isinstance(item, dict):
                continue
            content = item.get("content")
            if not isinstance(content, list):
                continue
            for block in content:
                if isinstance(block, dict) and block.get("type") == "input_text":
                    text = block.get("text")
                    if isinstance(text, str):
                        texts.append(text)
    else:
        raise MeasureError("codex debug prompt-input 顶层不是 JSON 数组")

    digest = hashlib.sha256()
    for text in texts:
        digest.update(text.encode("utf-8"))
        digest.update(b"\x00")
    meta = {
        "command": ["codex", "debug", "prompt-input", "x"],
        "cwd": "/tmp",
        "input_text_blocks": len(texts),
        "prompt_sha256_12": digest.hexdigest()[:12],
        "truncation_detected": any(TRUNCATION_MARKER in t for t in texts),
    }
    return texts, meta


def classify_prompt_blocks(texts: list[str]) -> dict[str, str]:
    """按内容特征识别 prompt JSON 中实际渲染的块。"""
    found: dict[str, str] = {}

    def add(key: str, text: str) -> None:
        if key not in found:
            found[key] = text

    for text in texts:
        stripped = text.lstrip("\ufeff \t\r\n")
        head = stripped[:4000].lower()
        first = stripped[:120].lower()

        if stripped.startswith("<skills_instructions>") or (
            "## skills" in head and "skill roots" in head
        ):
            add("skills", text)
        elif stripped.startswith("<permissions instructions>") or "permissions instructions" in first:
            add("permissions", text)
        elif stripped.startswith("# agents.md instructions") or (
            "agents.md instructions" in first and "<instructions>" in head
        ):
            add("AGENTS", text)
        elif stripped.startswith("<environment_context>") or "environment_context" in first:
            add("env", text)
        elif "<memory_summary>" in first or (
            "memory_summary begins" in head and "user profile" in head
        ):
            add("memory", text)
        elif (
            ('"tools"' in stripped[:300] or '"inputschema"' in head[:6000])
            and ('"input_schema"' in head[:8000] or '"inputschema"' in head[:8000])
        ):
            add("mcp", text)
        elif (
            ("you are codex" in head[:6000] or "you are a coding agent" in head[:6000])
            and len(text.encode("utf-8")) > 8000
        ):
            add("base", text)

    return found


def block_from_text(key: str, text: str, source_detail: str, source_file: Path | None) -> dict:
    data = text.encode("utf-8")
    return {
        "id": key,
        "label": LABELS[key],
        "bytes": len(data),
        "sha256_12": sha12(data),
        "source": "measured",
        "source_detail": source_detail,
        "source_file": str(source_file) if source_file else None,
        "source_mtime": iso_mtime(source_file),
        "note": "",
    }


def build_blocks(texts: list[str], prompt_meta: dict) -> list[dict]:
    prompt_blocks = classify_prompt_blocks(texts)
    memory_file = CODEX_HOME / "memories" / "memory_summary.md"
    agents_file = CODEX_HOME / "AGENTS.md"
    config_file = CODEX_HOME / "config.toml"
    skills_dir = CODEX_HOME / "skills"

    blocks: dict[str, dict] = {}

    # 1 记忆摘要：优先用 prompt 中真实渲染的块；CLI 调试视图不渲染时读源文件。
    if "memory" in prompt_blocks:
        blocks["memory"] = block_from_text(
            "memory",
            prompt_blocks["memory"],
            "prompt:<memory_summary>",
            memory_file if memory_file.exists() else None,
        )
        blocks["memory"]["note"] = "prompt JSON 中检测到记忆块"
    else:
        if not memory_file.exists():
            raise MeasureError(f"找不到记忆摘要文件，且 prompt JSON 中无记忆块: {memory_file}")
        raw = memory_file.read_bytes()
        blocks["memory"] = {
            "id": "memory",
            "label": LABELS["memory"],
            "bytes": len(raw),
            "sha256_12": sha12(raw),
            "source": "measured",
            "source_detail": "file:memory_summary.md",
            "source_file": str(memory_file),
            "source_mtime": iso_mtime(memory_file),
            "note": "CLI 调试视图未渲染记忆块，按源文件字节计",
        }

    # 2 基础系统提示：prompt 中若出现则实测，否则用静态基线。
    if "base" in prompt_blocks:
        blocks["base"] = block_from_text(
            "base", prompt_blocks["base"], "prompt:base-system-prompt", None
        )
        blocks["base"]["note"] = "prompt JSON 中检测到基础系统提示"
    else:
        base_bin = STATIC_BASE_BINARY if STATIC_BASE_BINARY.exists() else None
        blocks["base"] = {
            "id": "base",
            "label": LABELS["base"],
            "bytes": STATIC_BASE_PROMPT_BYTES,
            "sha256_12": STATIC_BASE_PROMPT_SHA256[:12],
            "source": "static",
            "source_detail": "static:app instructions_template max (2026-11-09)",
            "source_file": str(base_bin) if base_bin else None,
            "source_mtime": iso_mtime(base_bin),
            "note": "2026-11-09 app 二进制最大 instructions_template；CLI 调试视图不渲染",
        }

    # 3 技能目录
    if "skills" not in prompt_blocks:
        raise MeasureError("prompt JSON 中未识别到技能目录块")
    blocks["skills"] = block_from_text(
        "skills", prompt_blocks["skills"], "prompt:<skills_instructions>", skills_dir
    )
    blocks["skills"]["note"] = "按 prompt input_text 字节计；mtime 取技能根目录"

    # 4 权限块
    if "permissions" not in prompt_blocks:
        raise MeasureError("prompt JSON 中未识别到权限块")
    blocks["permissions"] = block_from_text(
        "permissions",
        prompt_blocks["permissions"],
        "prompt:<permissions instructions>",
        config_file,
    )
    blocks["permissions"]["note"] = "含 Codex 固定权限模板；mtime 取 config.toml"

    # 5 全局 AGENTS
    if "AGENTS" not in prompt_blocks:
        raise MeasureError("prompt JSON 中未识别到全局 AGENTS 块")
    blocks["AGENTS"] = block_from_text(
        "AGENTS",
        prompt_blocks["AGENTS"],
        "prompt:# AGENTS.md instructions",
        agents_file,
    )
    blocks["AGENTS"]["note"] = "含 41 B 前缀 + 15 B 后缀包装；mtime 取 AGENTS.md"

    # 6 MCP schema：CLI 调试视图不输出 tools schema，只能标 assumption。
    if "mcp" in prompt_blocks:
        blocks["mcp"] = block_from_text(
            "mcp", prompt_blocks["mcp"], "prompt:mcp-tools-schema", None
        )
        blocks["mcp"]["note"] = "prompt JSON 中检测到 MCP tools schema"
    else:
        blocks["mcp"] = {
            "id": "mcp",
            "label": LABELS["mcp"],
            "bytes": ASSUMED_MCP_BYTES,
            "sha256_12": None,
            "source": "assumption",
            "source_detail": "assumption:2026-11-05-baseline",
            "source_file": None,
            "source_mtime": None,
            "note": "七块占位 3,900 B，不是 App 实际注入；s2 原始 schema 130,481 B，App 注入 UNMEASURED",
        }

    # 7 环境上下文
    if "env" not in prompt_blocks:
        raise MeasureError("prompt JSON 中未识别到环境上下文块")
    blocks["env"] = block_from_text(
        "env", prompt_blocks["env"], "prompt:<environment_context>", None
    )
    blocks["env"]["note"] = "按 /tmp 工作目录渲染；cwd 不同字节会略有差异"

    return [blocks[k] for k in REQUIRED_IDS]


def load_baseline(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise MeasureError(f"读不到基线 JSON: {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise MeasureError(f"基线 JSON 不合法: {path}: {exc}") from exc

    blocks = data.get("blocks")
    if isinstance(blocks, dict):
        rows = []
        for key in REQUIRED_IDS:
            item = blocks.get(key)
            if not isinstance(item, dict):
                raise ReconcileError(f"基线缺少块 {key}")
            rows.append({"id": key, **item})
        data["blocks"] = rows
    elif isinstance(blocks, list):
        rows = blocks
    else:
        raise ReconcileError("基线 JSON 缺少 blocks 数组/对象")

    ids = [str(row.get("id")) for row in rows if isinstance(row, dict)]
    missing = [key for key in REQUIRED_IDS if key not in ids]
    if missing:
        raise ReconcileError(f"基线缺少块: {', '.join(missing)}")

    try:
        baseline_total = int(data["total"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ReconcileError("基线 JSON 缺少可解析的 total") from exc

    rows_sum = 0
    for row in rows:
        if not isinstance(row, dict):
            raise ReconcileError("基线 blocks 中存在非对象行")
        try:
            rows_sum += int(row["bytes"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ReconcileError(f"基线块 {row.get('id', '?')} 缺少可解析的 bytes") from exc

    if rows_sum != baseline_total:
        raise ReconcileError(
            f"baseline rows_sum={rows_sum} total={baseline_total} delta={rows_sum - baseline_total:+d}"
        )
    data["_rows_sum"] = rows_sum
    return data


def make_result(blocks: list[dict], prompt_meta: dict, gate: int, baseline: dict | None) -> dict:
    sum_bytes = sum(int(b["bytes"]) for b in blocks)
    total = sum_bytes
    reconciliation = "PASS" if sum_bytes == total else "MISMATCH"
    # 闸门只对可测的“文本块”负责；MCP 3,900 B 只是占位，不能冒充实测。
    mcp_bytes = sum(int(b["bytes"]) for b in blocks if b.get("id") == "mcp")
    text_total = total - mcp_bytes
    gate_status = "PASS" if text_total <= gate else "FAIL"
    overall_upper_total = text_total + NODE_REPL_MCP_MEASURED_BYTES + CODEX_APP_MCP_UPPER_BYTES
    overall_upper_status = "PASS" if overall_upper_total <= gate else "FAIL"
    truncation = "WARN" if prompt_meta.get("truncation_detected") else "OK"

    result = {
        "tool": "measure_prompt.py",
        "schema_version": 1,
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "cwd": prompt_meta.get("cwd", "/tmp"),
        "command": prompt_meta.get("command"),
        "input_text_blocks": prompt_meta.get("input_text_blocks"),
        "prompt_sha256_12": prompt_meta.get("prompt_sha256_12"),
        "gate_bytes": gate,
        "gate_label": "56 KiB" if gate == 57344 else f"{gate} B",
        "gate_scope": "text_blocks_excluding_mcp",
        "gate_status": gate_status,
        "headroom_bytes": gate - text_total,
        "text_blocks_total": text_total,
        "seven_block_total_with_mcp_placeholder": total,
        "overall_status": "UNMEASURED",
        "overall_upper_total": overall_upper_total,
        "overall_upper_gate_status": overall_upper_status,
        "mcp_calibers": {
            "app_injection_status": "UNMEASURED",
            "seven_block_placeholder_bytes": mcp_bytes,
            "node_repl_measured_bytes": NODE_REPL_MCP_MEASURED_BYTES,
            "codex_app_upper_bound_bytes": CODEX_APP_MCP_UPPER_BYTES,
            "raw_schema_known_bytes": RAW_MCP_KNOWN_BYTES,
            "raw_schema_upper_bytes": RAW_MCP_UPPER_BYTES,
            "note": "原始 tools/list 总量不是每请求注入；github/lis-skill-bus 当前会话未下发（deferred 旁证）",
        },
        "truncation": {
            "marker": TRUNCATION_MARKER,
            "detected": bool(prompt_meta.get("truncation_detected")),
            "status": truncation,
        },
        "blocks": blocks,
        "sum_bytes": sum_bytes,
        "total": total,
        "reconciliation": reconciliation,
    }

    if baseline is not None:
        base_map = {str(b["id"]): int(b["bytes"]) for b in baseline["blocks"]}
        deltas = {}
        for block in blocks:
            key = block["id"]
            cur = int(block["bytes"])
            old = base_map.get(key)
            deltas[key] = {
                "label": block["label"],
                "baseline": old,
                "current": cur,
                "delta": (cur - old) if old is not None else None,
            }
        baseline_total = int(baseline["total"])
        result["baseline"] = {
            "path": str(baseline.get("_path", "")),
            "total": baseline_total,
            "gate_bytes": baseline.get("gate_bytes"),
            "rows_sum": baseline["_rows_sum"],
            "reconciliation": "PASS",
            "deltas": deltas,
            "total_delta": total - baseline_total,
        }

    result["exit_code"] = 2 if reconciliation != "PASS" else (1 if gate_status == "FAIL" else 0)
    result["status"] = "MISMATCH" if reconciliation != "PASS" else gate_status
    result["status_label"] = (
        "MISMATCH" if reconciliation != "PASS"
        else f"文本块 {gate_status} / 整体 UNMEASURED"
    )
    return result


def render_text(result: dict) -> str:
    lines = [
        "Agent 固定注入测量（七块）",
        f"时间: {result['timestamp']}",
        f"命令: {' '.join(result.get('command') or [])}  (cwd={result.get('cwd')})",
        f"prompt SHA-256(12): {result.get('prompt_sha256_12')}  input_text 块: {result.get('input_text_blocks')}",
        "",
        f"{'ID':<12}{'块':<14}{'字节':>8}  {'SHA-256(12)':<14}{'来源':<11}{'来源文件 mtime':<26}说明",
        "-" * 132,
    ]
    for b in result["blocks"]:
        mtime = b.get("source_mtime") or "-"
        digest = b.get("sha256_12") or "n/a"
        lines.append(
            f"{b['id']:<12}{b['label']:<14}{int(b['bytes']):>8}  {digest:<14}{b['source']:<11}{mtime:<26}{b.get('note','')}"
        )
    lines.append("-" * 132)
    lines.append(f"{'TOTAL':<12}{'七块合计':<14}{int(result['total']):>8}")
    lines.append("")
    lines.append(
        f"对账: {result['reconciliation']}  ({result['sum_bytes']} = {result['total']})"
    )
    lines.append(
        f"文本块闸门: {result['text_blocks_total']} / {result['gate_bytes']} B "
        f"({result['gate_label']}) -> {result['gate_status']}  余量 {result['headroom_bytes']} B"
    )
    lines.append(
        f"整体（含 MCP 注入）: {result['overall_status']}；"
        f"上界 {result['overall_upper_total']} B（node_repl 2,400 + codex_app ≤12,400）"
        f" -> {result['overall_upper_gate_status']}"
    )
    lines.append(f"截断标记: {result['truncation']['status']}  ({TRUNCATION_MARKER})")
    if "baseline" in result:
        base = result["baseline"]
        lines.append("")
        lines.append(f"基线对比: {base['path']}")
        lines.append(f"{'ID':<12}{'基线':>8}{'当前':>8}{'增减':>8}")
        for key in REQUIRED_IDS:
            item = base["deltas"].get(key)
            if not item:
                continue
            delta = item["delta"]
            delta_txt = "n/a" if delta is None else f"{delta:+d}"
            lines.append(f"{key:<12}{item['baseline']!s:>8}{item['current']!s:>8}{delta_txt:>8}")
        lines.append(f"{'TOTAL':<12}{base['total']!s:>8}{result['total']!s:>8}{base['total_delta']:>+8d}")
    lines.append("")
    lines.append(f"STATUS: {result['status_label']}  EXIT: {result['exit_code']}")
    return "\n".join(lines)


def render_md(result: dict) -> str:
    lines = [
        "# Agent 固定注入测量（七块）",
        "",
        f"- 时间：`{result['timestamp']}`",
        f"- 命令：`{' '.join(result.get('command') or [])}`（cwd=`{result.get('cwd')}`）",
        f"- prompt SHA-256(12)：`{result.get('prompt_sha256_12')}`；input_text 块：{result.get('input_text_blocks')}",
        "",
        "| # | 块 | 字节 | SHA-256(12) | 来源 | 来源文件 mtime | 说明 |",
        "|---:|---|---:|---|---|---|---|",
    ]
    for i, b in enumerate(result["blocks"], 1):
        digest = b.get("sha256_12") or "n/a"
        mtime = b.get("source_mtime") or "-"
        lines.append(
            f"| {i} | {b['label']} | {int(b['bytes']):,} | `{digest}` | {b['source']} | `{mtime}` | {b.get('note','')} |"
        )
    lines.append(f"| | **合计** | **{int(result['total']):,}** | | | | |")
    lines.append("")
    lines.append(f"- 对账：**{result['reconciliation']}**（{result['sum_bytes']} = {result['total']}）")
    lines.append(
        f"- 文本块闸门：**{result['gate_status']}**（{result['text_blocks_total']:,} / {result['gate_bytes']:,} B，{result['gate_label']}，余量 {result['headroom_bytes']:,} B）"
    )
    lines.append(
        f"- 整体（含 MCP 注入）：**{result['overall_status']}**；上界 {result['overall_upper_total']:,} B → {result['overall_upper_gate_status']}"
    )
    lines.append(f"- 截断标记：**{result['truncation']['status']}**（`{TRUNCATION_MARKER}`）")
    if "baseline" in result:
        base = result["baseline"]
        lines.extend(["", f"## 基线对比：`{base['path']}`", "", "| 块 | 基线 | 当前 | 增减 |", "|---|---:|---:|---:|"])
        for key in REQUIRED_IDS:
            item = base["deltas"].get(key)
            if not item:
                continue
            delta = item["delta"]
            delta_txt = "n/a" if delta is None else f"{delta:+,}"
            lines.append(f"| {item['label']} | {item['baseline']:,} | {item['current']:,} | {delta_txt} |")
        lines.append(f"| **合计** | **{base['total']:,}** | **{result['total']:,}** | **{base['total_delta']:+,}** |")
    lines.append("")
    lines.append(f"**STATUS: {result['status_label']}  EXIT: {result['exit_code']}**")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="测量 Codex 七块固定注入（只读，不写 ${CODEX_HOME}）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例：\n"
            "  python3 measure_prompt.py\n"
            "  python3 measure_prompt.py --json\n"
            "  python3 measure_prompt.py --md --baseline injection-baseline-20261109.json\n"
            "  python3 measure_prompt.py --gate 57344\n"
        ),
    )
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    parser.add_argument("--md", action="store_true", help="输出 Markdown")
    parser.add_argument("--gate", type=int, default=None, help="闸门字节数；超限退出码 1（默认 57344）")
    parser.add_argument("--baseline", type=Path, default=None, help="基线 JSON；打印每块增减并校验基线 total")
    args = parser.parse_args(argv)

    if args.json and args.md:
        parser.error("--json 与 --md 不能同时使用")
    if args.gate is not None and args.gate <= 0:
        parser.error("--gate 必须是正整数")

    baseline = None
    if args.baseline:
        try:
            baseline = load_baseline(args.baseline)
            baseline["_path"] = str(args.baseline.resolve())
        except ReconcileError as exc:
            print(f"MISMATCH: {exc}")
            return 2
        except MeasureError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 3

    gate = args.gate
    if gate is None:
        if baseline is not None and isinstance(baseline.get("gate_bytes"), int):
            gate = baseline["gate_bytes"]
        else:
            gate = DEFAULT_GATE

    try:
        texts, prompt_meta = run_prompt_input()
        blocks = build_blocks(texts, prompt_meta)
        result = make_result(blocks, prompt_meta, gate, baseline)
    except MeasureError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3

    # 当前测量强制对账；正常路径 total=sum，这里保留结构闸门。
    if result["reconciliation"] != "PASS":
        print(
            f"MISMATCH: current rows_sum={result['sum_bytes']} total={result['total']} "
            f"delta={result['sum_bytes'] - result['total']:+d}"
        )
        return 2

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.md:
        print(render_md(result))
    else:
        print(render_text(result))

    return int(result["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
