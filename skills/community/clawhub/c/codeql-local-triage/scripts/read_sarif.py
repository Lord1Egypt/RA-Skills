#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read a CodeQL SARIF file and print the **source -> ... -> sink** path of every alert.

读 CodeQL 的 SARIF，把告警的 **source -> ... -> sink 完整路径** 打出来。

Why you need it / 为什么需要它
------------------------------
GitHub's alert page **gives you no data flow** — it shows the sink line and nothing about where the
taint came from. The output of ``codeql database analyze --format=sarif-latest`` contains
``runs[].results[].codeFlows[].threadFlows[].locations[]``, which *is* the complete path. When you
are asking "why does this fire?", this step is usually where the answer is.

GitHub 的告警页面**不给数据流**——只告诉你 sink 在哪一行，不告诉你污染是从哪来的。
而 ``codeql database analyze --format=sarif-latest`` 的产物里有
``runs[].results[].codeFlows[].threadFlows[].locations[]``，那才是完整路径。
排查「为什么报这个」时，这一步通常是答案所在。

Usage / 用法
------------
    python read_sarif.py out.sarif                 # full path / 完整路径
    python read_sarif.py out.sarif --paths-only    # sink locations only / 只列 sink 位置
    python read_sarif.py out.sarif --json          # machine-readable / 机器可读
    python read_sarif.py out.sarif --expect 0      # assert the result count (CI) / 断言结果条数

Exit codes / 退出码：0 = zero results (or ``--expect`` matched) / 无结果或断言通过；
1 = results present or assertion failed / 有结果或断言失败。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from i18n import tr, set_lang  # noqa: E402


class SarifError(Exception):
    """SARIF 结构非法（已打印人可读的定位信息）。用��与「文件不存在」区分开。"""


def _snippet(region: dict) -> str:
    txt = (region.get("snippet") or {}).get("text", "")
    return " ".join(txt.split())[:100]


def _clean_message(text: str) -> str:
    """CodeQL 的 SARIF message 会把同一句重复一遍（带 (1) 链接标注），去掉相邻重复行。"""
    lines, out = [ln.strip() for ln in text.splitlines() if ln.strip()], []
    for ln in lines:
        if not out or out[-1] != ln:
            out.append(ln)
    return " ".join(out)


def _loc_desc(loc: dict) -> dict:
    """把 SARIF 的一层 location 压成扁平描述。"""
    pl = loc.get("physicalLocation", {})
    reg = pl.get("region", {}) or {}
    return {
        "file": pl.get("artifactLocation", {}).get("uri", "?"),
        "line": reg.get("startLine"),
        "endLine": reg.get("endLine"),
        "col": reg.get("startColumn"),
        "role": (loc.get("message") or {}).get("text", ""),
        "snippet": _snippet(reg),
    }


def parse_sarif(path: Path) -> dict:
    """返回 {tool, version, artifacts, results:[{rule, level, message, sink, flows:[[step,...]]}]}

    对顶层结构做显式校验：不是 SARIF / runs 结构畸形时**抛异常**，
    绝不静默返回「0 条结果」——那是最危险的误判（把「读错了文件」当成「干净」）。
    """
    raw = path.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(tr("err_not_json", p=path, line=getattr(exc, "lineno", 0),
                 col=getattr(exc, "colno", 0), reason=exc.msg), file=sys.stderr)
        lines = raw.splitlines()
        ln = getattr(exc, "lineno", 0)
        if 0 < ln <= len(lines) and lines[ln - 1].strip():
            print(tr("err_json_near", near=lines[ln - 1].strip()[:60]), file=sys.stderr)
        print(tr("how_to_fix", hint=tr("hint_sarif_json")), file=sys.stderr)
        raise SarifError(str(exc)) from exc

    if not isinstance(data, dict) or "runs" not in data:
        print(tr("err_not_sarif", p=path), file=sys.stderr)
        print(tr("how_to_fix", hint=tr("hint_sarif_json")), file=sys.stderr)
        raise SarifError("not a SARIF file")
    runs = data["runs"]
    if not isinstance(runs, list):
        print(tr("err_sarif_shape", p=path, idx=0, reason="not a list"), file=sys.stderr)
        print(tr("how_to_fix", hint=tr("hint_sarif_shape")), file=sys.stderr)
        raise SarifError("runs is not a list")
    for i, run in enumerate(runs):
        if not isinstance(run, dict):
            print(tr("err_sarif_shape", p=path, idx=i, reason="entry is not an object"),
                  file=sys.stderr)
            print(tr("how_to_fix", hint=tr("hint_sarif_shape")), file=sys.stderr)
            raise SarifError(f"runs[{i}] is not an object")
        if "results" in run and run["results"] is not None and not isinstance(run["results"], list):
            print(tr("err_sarif_shape", p=path, idx=i, reason="results is not a list"),
                  file=sys.stderr)
            print(tr("how_to_fix", hint=tr("hint_sarif_shape")), file=sys.stderr)
            raise SarifError(f"runs[{i}].results is not a list")
        # results 列表内的元素也必须是对象，否则下游 r.get() 会炸成 AttributeError
        for j, r in enumerate(run.get("results") or []):
            if not isinstance(r, dict):
                print(tr("err_sarif_shape", p=path, idx=i,
                         reason=f"results[{j}] is not an object"), file=sys.stderr)
                print(tr("how_to_fix", hint=tr("hint_sarif_shape")), file=sys.stderr)
                raise SarifError(f"runs[{i}].results[{j}] is not an object")

    out = {"file": str(path), "tool": "?", "version": "?", "artifacts": 0, "results": []}
    for run in runs:
        driver = (run.get("tool") or {}).get("driver") or {}
        out["tool"] = driver.get("name", "?")
        # 版本在 semanticVersion（CodeQL 不填 version 字段）
        out["version"] = driver.get("semanticVersion") or driver.get("version") or "?"
        # result 级 level 常缺省，回退到 rules[].defaultConfiguration.level
        level_by_rule = {r.get("id"): (r.get("defaultConfiguration") or {}).get("level")
                         for r in driver.get("rules", []) or []}
        out["artifacts"] += len(run.get("artifacts", []) or [])
        for r in run.get("results", []) or []:
            rule_id = r.get("ruleId", "?")
            sink = None
            for loc in r.get("locations", []) or []:
                sink = _loc_desc(loc)
                break
            flows = []
            for cf in r.get("codeFlows", []) or []:
                for tf in cf.get("threadFlows", []) or []:
                    steps = [_loc_desc(lf["location"]) for lf in tf.get("locations", []) or []]
                    if steps:
                        flows.append(steps)
            out["results"].append({
                "rule": rule_id,
                "level": r.get("level") or level_by_rule.get(rule_id) or "?",
                "message": _clean_message((r.get("message") or {}).get("text", "")),
                "sink": sink,
                "flows": flows,
            })
    return out


def print_report(info: dict, paths_only: bool = False) -> None:
    print("=" * 78)
    print(tr("header_sarif", file=info["file"]))
    print(tr("header_tool", tool=info["tool"], version=info["version"],
             artifacts=info["artifacts"]))
    print("=" * 78)
    n = len(info["results"])
    print(tr("result_prefix", n=n) + (tr("status_clean") if not n else tr("status_alerts")))
    for i, r in enumerate(info["results"], 1):
        sink = r["sink"] or {}
        print(f"[{i}] {r['rule']}  ({r['level']})")
        if r["message"]:
            print(f"    {r['message']}")
        print(f"    sink: {sink.get('file')}:{sink.get('line')}")
        if paths_only:
            continue
        for fi, steps in enumerate(r["flows"], 1):
            print("    " + tr("flow_header", fi=fi, steps=len(steps)))
            for si, s in enumerate(steps):
                tag = "SOURCE" if si == 0 else ("SINK  " if si == len(steps) - 1 else "      ")
                print(f"      {tag} {si:2d}. {s['file']}:{s['line']:<5} {s['role']}")
                if s["snippet"]:
                    print(f"                  | {s['snippet']}")
        print()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=tr("read_desc"),
                                epilog=tr("read_epilog"))
    ap.add_argument("sarif", nargs="+", help=tr("sarif_help"))
    ap.add_argument("--json", action="store_true", help=tr("r_json_help"))
    ap.add_argument("--paths-only", action="store_true", help=tr("paths_only_help"))
    ap.add_argument("--expect", type=int, metavar="N", help=tr("expect_help"))
    ap.add_argument("--lang", choices=["auto", "zh", "en"], default="auto",
                    help=tr("lang_help"))
    args = ap.parse_args(argv)
    set_lang(args.lang)

    infos = []
    for raw in args.sarif:
        p = Path(raw)
        if not p.is_file():
            print(tr("err_file_missing", p=p), file=sys.stderr)
            return 2
        try:
            infos.append(parse_sarif(p))
        except SarifError:
            # parse_sarif 内部已打印行列号 / 结构问题 / 修复建议，此处不重复输出
            return 2
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            print(tr("err_parse_fail", p=p, type=type(exc).__name__, exc=exc),
                  file=sys.stderr)
            return 2

    total = sum(len(i["results"]) for i in infos)

    if args.json:
        print(json.dumps({"sarifs": infos, "total_results": total},
                         ensure_ascii=False, indent=2))
    else:
        for info in infos:
            print_report(info, paths_only=args.paths_only)
        if len(infos) > 1:
            print(tr("total_sarif", n=len(infos), total=total))

    if args.expect is not None:
        if total != args.expect:
            print(tr("assert_fail", expect=args.expect, total=total), file=sys.stderr)
            return 1
        print(tr("assert_pass", expect=args.expect))
        return 0
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
