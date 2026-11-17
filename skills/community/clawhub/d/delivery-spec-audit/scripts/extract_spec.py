#!/usr/bin/env python3
"""extract_spec.py — 从 Coding Agent 会话记录确定性抽取「规格覆盖证据」。

从 Claude Code 会话 JSONL / OpenClaw trajectory JSONL 中抽取三类原始证据,
供 delivery-spec-audit Skill 做规格覆盖率审查(对应 CodeSpecWeave 的核心
论点:主目标之外的功能语义/接口/状态/错误处理规格最容易被漏做):

  1. touch_set   会话中真实读过的文件(Read/Glob/Grep 等路径参数)
  2. write_set   会话中真实写过的文件(Write/Edit 路径参数 + Bash 重定向推断)
  3. verify_evidence  验证行为证据:
     - test_run       测试命令执行次数(按测试框架命令模式匹配)
     - lint_typecheck lint / 类型检查命令次数
     - build          构建/编译命令次数
     - git_diff_view  git diff / status / log / show 查看改动的次数
     - manual_verify  grep/rg 等结果核验型命令次数

设计原则(与 CodeSpecWeave 对齐):
  - 只抽取「证据」,不做任何「评分」——判断某条规格是否被覆盖是语义判断,
    必须由 Agent 拿着证据对照规格清单完成;
  - 误报方向要明确:重定向推断(Bash 里 `> file`)证据强度标为 weak,
    可能混入调试输出,Agent 使用时须人工复核 weak 项。

支持的 OpenClaw trajectory 形态:
  - 交互会话(prompt.submitted.messages 含 toolCall)→ 完整证据(full)
  - cron/isolated 会话(model.completed 截断、messages 为空)→ 降级为
    trace.artifacts.toolMetas 描述层证据(partial),输出会显式标注

用法:
    python3 extract_spec.py <session.jsonl> [--json]
    python3 extract_spec.py <session.jsonl> --repo-root /path/to/repo
    # --repo-root: 相对路径会以此解析为绝对路径

输出: Markdown 摘要(默认)或 --json 机器可读结果。
退出码: 0 = 成功, 2 = 用法错误, 3 = 输入文件不存在。
"""
from __future__ import annotations

import argparse
import json
import re
import shlex
import sys
from pathlib import Path

# ---- 路径参数:按工具名归类的常见键 ----
PATH_KEYS = [
    "file_path", "path", "notebook_path", "abs_path",
    "filePath", "target_path",
]
WRITE_TOOLS = {"Write", "write", "edit", "Edit", "multiedit", "MultiEdit",
               "notebook_edit", "NotebookEdit", "apply_patch", "save_file",
               "str_replace_editor", "str_replace_based_edit_tool"}

# ---- 验证命令模式(Bash 命令文本包含即命中,可多重) ----
TEST_PATTERNS = [
    r"\b(?:npm|pnpm|yarn)\s+(?:run\s+)?test\b", r"\bpytest\b", r"\bjest\b",
    r"\bvitest\b", r"\bgo\s+test\b", r"\bcargo\s+test\b", r"\bpython3?\s+-m\s+pytest\b",
    r"\brake\s+test\b", r"\bmvn\s+(?:test|verify)\b", r"\bgradle\s+(?:test|check)\b",
    r"\bmake\s+test\b", r"\bcargo\s+nextest\b", r"\bphpunit\b", r"\bgo vet\b",
]
LINT_PATTERNS = [
    r"\beslint\b", r"\bpylint\b", r"\bflake8\b",
    r"\bruff\b", r"\bclippy\b", r"\btsc\b", r"\bmypy\b", r"\bbiome\b",
    r"\bstylelint\b", r"\bgolangci-lint\b",
]
BUILD_PATTERNS = [
    r"\b(?:npm|pnpm|yarn)\s+run\s+build\b", r"\bcargo\s+build\b",
    r"\bgo\s+build\b", r"\bwebpack\b", r"\bvite\s+build\b",
    r"\bturbo\s+build\b", r"\bgradle\s+build\b", r"\bxcodebuild\b",
]
DIFF_PATTERNS = [r"\bgit\s+diff\b", r"\bgit\s+status\b", r"\bgit\s+log\b", r"\bgit\s+show\b"]
INSPECT_PATTERNS = [r"\bgrep\b", r"\brg\b", r"\bsed\s+-n\b", r"\bawk\b", r"\bhead\b", r"\btail\b"]

# Bash 重定向弱证据过滤
REDIRECT_RE = re.compile(r"(?:^|[\s;|&)])>{1,2}\s*([^\s;|&>]+)")
WEAK_TARGET_BASENAMES = {
    ".env", ".gitignore", ".npmrc", ".nvmrc", ".editorconfig", "dockerfile",
    "makefile", "license", "readme", ".gitattributes", ".prettierrc",
}
WEAK_EXCLUDE = {"dev/null", "&1", "&2", "1", "2", "0"}


def classify_command(cmd: str) -> list[str]:
    """对一条 shell 命令给出验证行为分类(可多重命中)。"""
    hits = []
    for name, patterns in [
        ("test_run", TEST_PATTERNS), ("lint_typecheck", LINT_PATTERNS),
        ("build", BUILD_PATTERNS), ("git_diff_view", DIFF_PATTERNS),
        ("manual_verify", INSPECT_PATTERNS),
    ]:
        if any(re.search(p, cmd) for p in patterns):
            hits.append(name)
    return hits


def _looks_like_file(t: str) -> bool:
    """弱证据过滤:目标形似文件路径才保留。"""
    low = t.lower().rstrip(";")
    if low in WEAK_EXCLUDE or t.startswith("-") or "=" in t or "(" in t or ")" in t or "," in t:
        return False
    if "$" in t or "`" in t or ".*" in t:
        return False
    base = low.rsplit("/", 1)[-1]
    if base in WEAK_TARGET_BASENAMES:
        return True
    return "." in base and not base.split(".")[-1].isdigit()


def extract_bash_write_targets(cmd: str) -> list[str]:
    """从 Bash 命令的重定向推断写入目标(证据强度:弱)。"""
    targets = []
    try:
        parts = shlex.split(cmd)
    except ValueError:
        parts = cmd.split()
    joined = " ".join(parts)
    for m in REDIRECT_RE.finditer(joined):
        t = m.group(1).strip("'\"")
        if t and _looks_like_file(t):
            targets.append(t)
    return targets


def iter_tool_calls_cc(path: Path):
    """Claude Code JSONL: assistant.message.content[].tool_use。"""
    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            if '"tool_use"' not in line and '"toolUse"' not in line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("type") != "assistant":
                continue
            content = rec.get("message", {}).get("content") or []
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") in ("tool_use", "toolUse"):
                        yield block.get("name", ""), block.get("input", {}) or {}


def iter_tool_calls_oc(path: Path):
    """OpenClaw trajectory: model.completed.data 里的 toolCalls。"""
    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            if '"toolCall"' not in line and '"tool_calls"' not in line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            model = rec.get("model") if isinstance(rec.get("model"), dict) else {}
            completed = model.get("completed") if isinstance(model.get("completed"), dict) else {}
            data = completed.get("data", {}) if isinstance(completed.get("data"), dict) else {}
            calls = data.get("toolCalls") or data.get("tool_calls") or []
            if isinstance(calls, list):
                for call in calls:
                    if not isinstance(call, dict):
                        continue
                    fn = call.get("function") if isinstance(call.get("function"), dict) else {}
                    name = call.get("name") or fn.get("name") or ""
                    args = call.get("arguments", fn.get("arguments", {}))
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except json.JSONDecodeError:
                            args = {}
                    yield name, args if isinstance(args, dict) else {}


def iter_messages_oc(path: Path):
    """OpenClaw trajectory: data.messages[] 内 assistant 消息的 content[].toolCall 块。
    每行 trace 事件的 data.messages 只含增量消息,按 responseId 去重防止重复计数。"""
    seen_response_ids: set[str] = set()
    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            if '"toolCall"' not in line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            data = rec.get("data") if isinstance(rec.get("data"), dict) else {}
            msgs = data.get("messages") or []
            if not isinstance(msgs, list):
                continue
            for m in msgs:
                if not isinstance(m, dict) or m.get("role") != "assistant":
                    continue
                rid = m.get("responseId")
                if rid and rid in seen_response_ids:
                    continue
                if rid:
                    seen_response_ids.add(rid)
                content = m.get("content") or []
                if not isinstance(content, list):
                    continue
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "toolCall":
                        args = block.get("arguments", {})
                        if isinstance(args, str):
                            try:
                                args = json.loads(args)
                            except json.JSONDecodeError:
                                args = {}
                        yield block.get("name", ""), args if isinstance(args, dict) else {}


def iter_tool_metas_oc(path: Path):
    """OpenClaw trajectory(降级形态): trace.artifacts.data.toolMetas。

    cron/isolated 会话的 model.completed 被截断、prompt.submitted.messages 为空,
    完整 toolCalls 不可得;此时 trace.artifacts.toolMetas 仍保留每次工具调用的
    toolName + meta 描述(自身可能被 trajectory-array-size-limit 截断)。
    产出 (toolName, meta_text) 二元组,meta 是描述层证据(无结构化参数)。"""
    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            if '"toolMetas"' not in line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("type") != "trace.artifacts":
                continue
            data = rec.get("data") if isinstance(rec.get("data"), dict) else {}
            metas = data.get("toolMetas") or []
            if isinstance(metas, list):
                for m in metas:
                    if isinstance(m, dict) and m.get("toolName"):
                        yield m["toolName"], m.get("meta", "") or ""


def detect_format(path: Path) -> str:
    with path.open(encoding="utf-8", errors="replace") as f:
        head = f.read(64 * 1024)
    if "trajectory" in head and ("traceSchema" in head or "model.completed" in head):
        return "openclaw"
    return "claude-code"


def openclaw_detail_level(path: Path) -> str:
    """判定 OpenClaw trajectory 的细节层级:
    full   = prompt.submitted.messages 含 assistant toolCall(交互会话形态)
    partial = messages 为空,仅 trace.artifacts.toolMetas 可用(cron/isolated 形态)
    """
    has_messages = False
    has_tool_metas = False
    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            if '"messages"' in line and not has_messages:
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("type") == "prompt.submitted":
                    data = rec.get("data") if isinstance(rec.get("data"), dict) else {}
                    msgs = data.get("messages") or []
                    if isinstance(msgs, list) and msgs:
                        has_messages = True
            if '"toolMetas"' in line:
                has_tool_metas = True
            if has_messages:
                break
    return "full" if has_messages else ("partial" if has_tool_metas else "empty")


def collect(path: Path, repo_root: Path | None) -> dict:
    fmt = detect_format(path)
    detail = "full"
    if fmt == "openclaw":
        detail = openclaw_detail_level(path)
    if fmt == "openclaw" and detail == "full":
        iterator = iter_messages_oc(path)
    elif fmt == "openclaw" and detail == "partial":
        iterator = iter_tool_metas_oc(path)
    else:
        iterator = iter_tool_calls_cc(path)

    touch_set: set[str] = set()
    write_set: dict[str, str] = {}
    verify = {"test_run": 0, "lint_typecheck": 0, "build": 0,
              "git_diff_view": 0, "manual_verify": 0}
    bash_write_targets: list[str] = []
    commands_total = 0
    tool_names: dict[str, int] = {}

    def record_file(p: str, is_write_tool: bool) -> None:
        p = p.strip()
        if not p or p.startswith(("http://", "data:")):
            return
        rp = Path(p)
        if repo_root and not rp.is_absolute():
            rp = repo_root / rp
        try:
            rp = rp.resolve()
        except OSError:
            pass
        s = str(rp)
        if is_write_tool:
            write_set[s] = "strong"
        else:
            touch_set.add(s)

    meta_write_hints: list[str] = []

    for name, inp in iterator:
        tool_names[name] = tool_names.get(name, 0) + 1

        # partial 模式:inp 是 meta 描述文本(证据弱一层,无结构化参数)
        if isinstance(inp, str):
            meta = inp
            if name in WRITE_TOOLS:
                meta_write_hints.append(meta)
            else:
                commands_total += 1
                for k in classify_command(meta):
                    verify[k] += 1
            continue

        for key in PATH_KEYS:
            v = inp.get(key)
            if isinstance(v, str) and v:
                record_file(v, is_write_tool=(name in WRITE_TOOLS))
                break
        for key in ("edits", "patches"):
            v = inp.get(key)
            if isinstance(v, list):
                for item in v:
                    if isinstance(item, dict) and isinstance(item.get("path"), str):
                        record_file(item["path"], True)
        cmd = inp.get("command")
        if isinstance(cmd, str) and cmd:
            commands_total += 1
            for k in classify_command(cmd):
                verify[k] += 1
            for target in extract_bash_write_targets(cmd):
                rp = Path(target)
                if repo_root and not rp.is_absolute():
                    rp = repo_root / rp
                bash_write_targets.append(str(rp))
                if str(rp) not in write_set:
                    write_set[str(rp)] = "weak"

    return {
        "format": fmt,
        "detail": detail if fmt == "openclaw" else "full",
        "meta_write_hints": meta_write_hints,
        "session": str(path),
        "repo_root": str(repo_root) if repo_root else None,
        "counts": {
            "files_touched_read": len(touch_set),
            "files_written": len(write_set),
            "writes_strong": sum(1 for v in write_set.values() if v == "strong"),
            "writes_weak_redirected": sum(1 for v in write_set.values() if v == "weak"),
            "bash_commands": commands_total,
        },
        "verify_evidence": verify,
        "write_set": [{"path": p, "evidence": e} for p, e in sorted(write_set.items())],
        "touch_set": sorted(touch_set),
        "bash_write_targets_weak": bash_write_targets,
        "tool_usage": tool_names,
    }


def render_md(r: dict) -> str:
    c, v = r["counts"], r["verify_evidence"]
    lines = [
        f"# 规格覆盖证据抽取 — {Path(r['session']).name}",
        "",
        f"- 会话格式: {r['format']}" + (f"(repo-root: {r['repo_root']})" if r["repo_root"] else ""),
    ]
    if r.get("detail") == "partial":
        lines += [
            "- ⚠️ 证据层级: partial——该 trajectory 为 cron/isolated 会话形态,"
            "完整工具调用参数不可得,以下证据来自 trace.artifacts.toolMetas 的描述层摘要",
            "  (写入无结构化路径,验证分类基于 meta 文本;toolMetas 自身也可能被截断,"
            "计数可能少于真实调用数)",
        ]
    lines += [
        f"- 读过的文件: {c['files_touched_read']} 个",
        f"- 写过的文件: {c['files_written']} 个(工具写入 strong {c['writes_strong']},"
        f" 重定向推断 weak {c['writes_weak_redirected']})",
        f"- Bash 命令: {c['bash_commands']} 条",
        "",
        "## 验证行为证据",
        "",
        f"- 测试执行: {v['test_run']} 次",
        f"- lint / 类型检查: {v['lint_typecheck']} 次",
        f"- 构建: {v['build']} 次",
        f"- git 改动查看: {v['git_diff_view']} 次",
        f"- grep/rg 核验: {v['manual_verify']} 次",
        "",
        "> 注意: 以上是命令出现次数,不代表通过/失败;验证结果需另行查看会话记录。",
        "",
    ]
    if r["write_set"]:
        lines += ["## 写入文件清单", ""]
        for item in r["write_set"]:
            mark = "✅ 工具写入" if item["evidence"] == "strong" else "⚠️ 重定向推断(需人工复核)"
            lines.append(f"- [{mark}] {item['path']}")
        lines.append("")
    if r.get("meta_write_hints"):
        lines += ["## 写入线索(partial 证据:仅工具描述,无结构化路径,须结合 git 复核)", ""]
        for hint in r["meta_write_hints"]:
            lines.append(f"- [📝 meta 线索] {hint}")
        lines += [
            "",
            "> git 补齐指引: 若 `git status` 输出为空,改动大概率已被提交(自动化会话"
            "常见). 改用提交定位: `git log --since=\"<会话开始时间>\" --oneline` "
            "找到候选提交,再 `git show <sha> --stat` 核对文件清单. 不要因 status "
            "为空而误判「没有写入」.",
        ]
        lines.append("")
    if r["bash_write_targets_weak"]:
        lines += ["## 重定向推断目标(弱证据,可能含调试输出)", ""]
        for t in r["bash_write_targets_weak"]:
            lines.append(f"- {t}")
        lines.append("")
    lines += [
        "## 使用说明(给审查 Agent)",
        "",
        "本文件只是「证据」,不是「结论」。接下来由你完成语义审查:",
        "",
        "1. 向用户(或从任务描述)收集本次交付的规格清单,主目标之外特别追问:",
        "   功能边界 / 接口兼容 / 状态一致 / 错误处理 / 回归风险;",
        "2. 逐条规格对照写入文件与验证证据,判定: 已覆盖 / 疑似遗漏 / 证据不足;",
        "3. 「疑似遗漏」给出具体反例场景(哪个输入/哪条路径会暴露遗漏);",
        "4. weak 证据必须人工复核后再下结论;",
        "5. partial 证据层级下,先跑 git status/diff 补齐写入清单再做覆盖判定;"
        "status 为空时按上方指引改用 git log/show 定位已提交的改动。",
        "",
        "设计参照: CodeSpecWeave(arXiv:2610.40256)——互依规格最容易被逐条打勾式交付漏掉。",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract spec-coverage evidence from agent session logs")
    ap.add_argument("session", help="session JSONL path (Claude Code or OpenClaw trajectory)")
    ap.add_argument("--repo-root", default=None, help="resolve relative paths against this root")
    ap.add_argument("--json", action="store_true", dest="as_json", help="machine-readable output")
    args = ap.parse_args()

    path = Path(args.session).expanduser()
    if not path.is_file():
        pointer = path.with_suffix(".jsonl").parent / (path.name[:-len(".jsonl")] if path.name.endswith(".jsonl") else path.name)
        hint = ""
        # OpenClaw 轨迹指针存在但 runtime 文件缺失 => 会话仍在进行中,轨迹尚未落盘
        stem = path.name
        if stem.endswith(".trajectory.jsonl"):
            stem = stem[: -len(".trajectory.jsonl")]
        elif stem.endswith(".jsonl"):
            stem = stem[: -len(".jsonl")]
        ptr = path.parent / (stem + ".trajectory-path.json")
        try:
            import json as _json
            if ptr.is_file():
                rt = _json.load(open(ptr, encoding="utf-8")).get("runtimeFile", "")
                hint = (f"\nhint: found trajectory pointer {ptr.name} -> runtime file not created yet. "
                        f"The session is likely STILL RUNNING; trajectory is persisted after the turn completes. "
                        f"Wait for the run to finish, then audit '{rt}'.")
        except Exception:
            pass
        print(f"error: file not found: {path}{hint}", file=sys.stderr)
        return 3
    repo_root = Path(args.repo_root).expanduser().resolve() if args.repo_root else None

    result = collect(path, repo_root)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_md(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
