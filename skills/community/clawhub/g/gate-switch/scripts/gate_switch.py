#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_switch.py — 通用概率执行门禁骨架（强制填充门 L2 档 · 实证族通用引擎，2026-08-15）

本源抽象：在决策/交付点用机械校验做 0/1 判定，剥夺 LLM 手写判定权。
与 dispatch_switch 的关系：dispatch_switch 是"路由族"专用开关（A/B 路径选择）；
本引擎是"实证族"通用骨架——任何"声称 X 已满足"的场景，把 X 写成检查项 spec，
引擎逐项机械核验，全过 → 掷点 A 放行，任一失败 → 掷点 B 阻断并列出违例。

四态退出码（与 dispatch_switch 同语义）：
  0 = A（全部检查通过，放行）   2 = B（有违例，阻断，violations 即 B 档理由）
  3 = CLARIFY（输入信号不足）   4 = VIOLATION（spec 本身非法，如未知检查类型）

检查原语（冻结集，新增需 ≥2 独立场景举证）：
  file_exists   {path}                                  文件/目录存在
  file_min_size {path, bytes}                           文件大小下限（防空壳）
  json_field    {path, field, op, value}                JSON 字段断言
                op: exists|not_empty|equals|in|min_len|min|max（field 支持 a.b.0.c 点路径）
  glob_count    {pattern, op: min|max|eq, value}        文件计数（截图数/素材数）
  grep_count    {pattern, path, op: min|max|eq, value}  特征串计数（零残留/章节数）
  mtime_after   {path, ref_path}                        产物新于参照（防旧证据冒充）
  script_exit   {cmd, expect}                           外部脚本退出码（复用既有工具）

用法：
  gate_switch.py --spec <spec.json> [--set key=value ...] [--log <path>]
  spec 中 {key} 占位符由 --set 注入；claims 场景由调用方即时生成 spec。

留痕：~/.agents/logs/gate_switch.jsonl（时间/门禁名/掷点/违例/输入），B/A 比率进复盘。
"""
import argparse
import datetime
import glob
import json
import os
import re
import subprocess
import sys

DEFAULT_LOG = os.path.expanduser("~/.agents/logs/gate_switch.jsonl")
EXIT_A, EXIT_B, EXIT_CLARIFY, EXIT_VIOLATION = 0, 2, 3, 4


class SpecError(Exception):
    pass


def _dig(obj, dotted):
    """按 a.b.0.c 点路径取值，缺失返回 _MISS。"""
    cur = obj
    for part in dotted.split("."):
        if isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except (ValueError, IndexError):
                return _MISS
        elif isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return _MISS
    return cur


class _Miss:
    def __repr__(self):
        return "<MISS>"


_MISS = _Miss()


def _cmp(op, actual, value):
    if op == "exists":
        return actual is not _MISS
    if op == "not_empty":
        return actual is not _MISS and actual not in (None, "", [], {})
    if op == "equals":
        return actual == value
    if op == "in":
        return actual in value
    if op == "min_len":
        return hasattr(actual, "__len__") and len(actual) >= value
    if op == "min":
        return isinstance(actual, (int, float)) and actual >= value
    if op == "max":
        return isinstance(actual, (int, float)) and actual <= value
    if op == "eq":
        return actual == value
    raise SpecError(f"未知比较符: {op}")


def run_check(c):
    """执行单条检查，返回 (ok, detail)。"""
    t = c.get("type")
    label = c.get("label", t)
    if t == "file_exists":
        ok = os.path.exists(c["path"])
        return ok, f"{label}: {c['path']} {'存在' if ok else '不存在'}"
    if t == "file_min_size":
        if not os.path.isfile(c["path"]):
            return False, f"{label}: {c['path']} 不存在"
        size = os.path.getsize(c["path"])
        return size >= c["bytes"], f"{label}: {size}B（下限 {c['bytes']}B）"
    if t == "json_field":
        if not os.path.isfile(c["path"]):
            return False, f"{label}: {c['path']} 不存在"
        try:
            data = json.load(open(c["path"], encoding="utf-8"))
        except Exception as e:
            return False, f"{label}: JSON 解析失败 {e}"
        actual = _dig(data, c["field"])
        ok = _cmp(c["op"], actual, c.get("value"))
        return ok, f"{label}: {c['field']}={actual!r} op={c['op']} expect={c.get('value')!r}"
    if t == "glob_count":
        n = len(glob.glob(c["pattern"], recursive=True))
        return _cmp(c["op"], n, c["value"]), f"{label}: 计数={n} op={c['op']} expect={c['value']}"
    if t == "grep_count":
        n = 0
        for p in glob.glob(c["path"], recursive=True):
            if os.path.isfile(p):
                n += sum(1 for line in open(p, encoding="utf-8", errors="ignore")
                         if re.search(c["pattern"], line))
        return _cmp(c["op"], n, c["value"]), f"{label}: 命中={n} op={c['op']} expect={c['value']}"
    if t == "mtime_after":
        if not os.path.exists(c["path"]):
            return False, f"{label}: {c['path']} 不存在"
        if not os.path.exists(c["ref_path"]):
            return False, f"{label}: 参照 {c['ref_path']} 不存在"
        ok = os.path.getmtime(c["path"]) > os.path.getmtime(c["ref_path"])
        return ok, f"{label}: 产物{'新于' if ok else '不新于'}参照"
    if t == "script_exit":
        r = subprocess.run(c["cmd"], shell=True, capture_output=True, text=True, timeout=300)
        expect = c.get("expect", 0)
        ok = r.returncode == expect
        tail = (r.stdout or r.stderr).strip().splitlines()
        return ok, f"{label}: exit={r.returncode} expect={expect} {tail[-1] if tail else ''}"
    raise SpecError(f"未知检查类型: {t}")


def flip(spec_path, bindings):
    if not os.path.isfile(spec_path):
        return {"verdict": "CLARIFY", "reasons": [f"spec 不存在: {spec_path}"]}, EXIT_CLARIFY
    try:
        raw = open(spec_path, encoding="utf-8").read()
        for k, v in bindings.items():
            raw = raw.replace("{%s}" % k, v)
        unresolved = re.findall(r"\{[a-zA-Z_][a-zA-Z0-9_]*\}", raw)
        if unresolved:
            return {"verdict": "CLARIFY",
                    "reasons": [f"spec 存在未注入占位符 {unresolved}，用 --set key=value 补齐"]}, EXIT_CLARIFY
        spec = json.loads(raw)
    except Exception as e:
        return {"verdict": "CLARIFY", "reasons": [f"spec 解析失败: {e}"]}, EXIT_CLARIFY

    checks = spec.get("checks")
    if not checks:
        return {"verdict": "CLARIFY", "reasons": ["spec 无 checks 检查项"]}, EXIT_CLARIFY

    violations, passed = [], []
    try:
        for c in checks:
            ok, detail = run_check(c)
            (passed if ok else violations).append(detail)
    except SpecError as e:
        return {"verdict": "VIOLATION", "reasons": [str(e)]}, EXIT_VIOLATION
    except (KeyError, TypeError) as e:
        return {"verdict": "VIOLATION", "reasons": [f"检查项字段缺失/类型错误: {e}"]}, EXIT_VIOLATION

    if not violations:
        return {"verdict": "A", "throw": "A", "gate": spec.get("gate"),
                "passed": passed,
                "directive": "全部机械核验通过，照抄本结论放行"}, EXIT_A
    return {"verdict": "B", "throw": "B", "gate": spec.get("gate"),
            "violations": violations, "passed": passed,
            "directive": "存在违例，阻断；violations 即 B 档理由，修复后重新扳动"}, EXIT_B


def append_log(path, entry):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser(description="通用概率执行门禁骨架（实证族 L2 引擎）")
    ap.add_argument("--spec", required=True, help="检查项 spec JSON 路径")
    ap.add_argument("--set", dest="sets", action="append", default=[],
                    help="占位符注入 key=value（可多次）")
    ap.add_argument("--log", default=DEFAULT_LOG, help="留痕 jsonl 路径")
    args = ap.parse_args()

    bindings = {}
    for s in args.sets:
        if "=" not in s:
            print(f"[gate_switch] --set 格式错误: {s}（需 key=value）", file=sys.stderr)
            sys.exit(EXIT_CLARIFY)
        k, v = s.split("=", 1)
        bindings[k] = v

    result, code = flip(args.spec, bindings)
    append_log(args.log, {
        "ts": datetime.datetime.now().isoformat(timespec="seconds"),
        "spec": args.spec, "bindings": bindings or None,
        "verdict": result["verdict"],
        "violations": result.get("violations"),
    })
    result["logged"] = args.log
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    sys.exit(code)


if __name__ == "__main__":
    main()
