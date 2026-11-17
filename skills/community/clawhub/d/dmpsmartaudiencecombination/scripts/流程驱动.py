#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""流程驱动.py

目的：把 11122/11127 系列“Step 1-14”对话式流程，固化为可执行的“流程驱动器”，用于：
- 串联各步骤脚本的执行顺序
- 在关键卡点（Step2/6/6.5/7/8.5/9.5/13）输出强制交互提示
- 在缺少用户确认时硬拦截，避免跳步

重要说明：
- 该脚本不替用户做业务决策；只负责执行步骤与卡点拦截
- 该脚本支持“非交互模式”：用一个JSON一次性提供用户确认/选择（便于自动化与回归）

用法示例：
  python3 scripts/流程驱动.py --schema schema.json --out-dir data/run_flow

  # 非交互模式（自动跑到指定步骤或跑完整链路）：
  python3 scripts/流程驱动.py --schema schema.json --out-dir data/run_flow \
    --non-interactive --decisions decisions.json

其中 decisions.json 结构示例：
{
  "step2_confirm": true,
  "step6_expand": false,
  "step6_5_show_third_party": "auto",  // auto|force|skip
  "step7": {
    "must": [[34080, 34082], [15678, 34073], [34365, 34355]],
    "preferred": [],
    "optional": [],
    "exclude": []
  },
  "step8_5": {
    "trackType": "MOBILE",
    "idTypes": ["OAID","MD5_OAID"]
  },
  "step9_5": "B",  // A=直接创建最终组合; B=计算Overlap→出方案→确认→创建
  "step13_confirm": true,
  "step13_plan_name": "精准型",
  "final_name": "TP组合_示例_20260924"
}

说明：step7.must 推荐使用二维列表（or_groups）：每个子数组内是 OR；数组之间是 AND。

"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent


def _run(cmd: List[str]) -> Dict[str, Any]:
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = (r.stdout or "").strip()
    err = (r.stderr or "").strip()
    if r.returncode != 0:
        raise RuntimeError(f"command_failed: {' '.join(cmd)}\n{err or out}")
    # 尝试解析最后一行json
    last = out.splitlines()[-1] if out else ""
    try:
        return json.loads(last)
    except Exception:
        return {"ok": True, "raw": out}


def _load_json(path: Path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _save_json(path: Path, obj: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def _prompt_block(block_name: str, message: str, non_interactive: bool):
    """关键卡点：交互模式提示用户；非交互模式直接报错阻断。"""
    if non_interactive:
        raise SystemExit(f"[BLOCKED:{block_name}] {message}")
    print("\n" + "=" * 70)
    print(f"🔴 关键卡点：{block_name}")
    print("=" * 70)
    print(message)
    print("=" * 70 + "\n")
    raise SystemExit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True, help="schema.json")
    ap.add_argument("--out-dir", required=True, help="输出目录")
    ap.add_argument("--non-interactive", action="store_true", help="非交互模式：必须提供--decisions")
    ap.add_argument("--decisions", default="", help="决策JSON（非交互模式必填）")
    ap.add_argument("--stop-after", default="", help="跑到某一步就停止，如 6 / 7 / 8.5 / 9 / 14")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    schema_path = Path(args.schema)
    if not schema_path.exists():
        raise SystemExit(f"schema.json不存在: {args.schema}")

    decisions: Dict[str, Any] = {}
    if args.non_interactive:
        if not args.decisions:
            raise SystemExit("非交互模式必须提供 --decisions decisions.json")
        decisions = _load_json(Path(args.decisions), {}) or {}

    # Step 0：前置校验
    print("[Step0] preflight_check")
    _run(["python3", str(SCRIPT_DIR / "preflight_check.py")])
    if args.stop_after in ("0", "step0"):
        return

    # Step 1-2：需求解析/确认（此处仅检查schema存在；对话确认由调用方负责）
    # 11122要求：READY/NEED_CLARIFICATION 确认后才进入Step3。
    if args.non_interactive:
        if not decisions.get("step2_confirm"):
            _prompt_block("Step2需求确认", "需要用户确认需求解析结果(step2_confirm=true)，否则不得进入Step3。", True)
    else:
        _prompt_block(
            "Step2需求确认",
            "请先确认需求解析结果，然后再继续：\n- 回复“确认”继续\n- 回复“展开”查看详细解析\n（本驱动器在交互模式下不会替你等待回复）",
            False,
        )

    # Step 3：拉取标签池
    print("[Step3] query_tag_list")
    tag_pool_path = out_dir / "tag_pool.json"
    _run(["python3", str(SCRIPT_DIR / "query_tag_list.py"), "--only-leaf", "--out", str(tag_pool_path)])
    if args.stop_after in ("3", "step3"):
        return

    # Step 4：候选召回总控（含coverage/probe/queries/semantic/fallback/diag）
    print("[Step4] recall_candidates_pipeline")
    _run(["python3", str(SCRIPT_DIR / "recall_candidates_pipeline.py"), "--schema", str(schema_path), "--out-dir", str(out_dir)])
    if args.stop_after in ("4", "step4"):
        return

    # Step 5：画像补全
    print("[Step5] tag_profile_enrich")
    merged_path = out_dir / "merged_candidates.json"
    enriched_path = out_dir / "candidates_enriched.json"
    profile_xlsx = SKILL_DIR / "assets" / "标签指标表.xlsx"
    _run([
        "python3", str(SCRIPT_DIR / "tag_profile_enrich.py"),
        "--candidates", str(merged_path),
        "--profile", str(profile_xlsx),
        "--out", str(enriched_path),
    ])
    if args.stop_after in ("5", "step5"):
        return

    # Step 6：分组推荐
    print("[Step6] rank_candidates")
    step6_path = out_dir / "step6_ranked.json"
    _run(["python3", str(SCRIPT_DIR / "rank_candidates.py"),
          "--enriched", str(enriched_path),
          "--schema", str(schema_path),
          "--coverage", str(out_dir / "coverage_matrix.json"),
          "--queries", str(out_dir / "queries.json"),
          "--out", str(step6_path)])

    # Step 6交互卡点：必须先问用户是否展开（即使默认偏好“不展开”，也必须显式确认）
    if args.non_interactive:
        # 非交互模式：必须显式提供 step6_expand（true/false）
        if "step6_expand" not in decisions:
            _prompt_block("Step6是否展开候选标签详情", "非交互模式必须提供 step6_expand=true/false（显式确认是否展开）。", True)
        # 注意：step6_expand仅用于对话侧是否展示明细；流程执行不依赖该值。
    else:
        _prompt_block(
            "Step6是否展开候选标签详情",
            "已生成按维度分组的候选标签（step6_ranked.json）。\n请回复：\n- “展开”：展示候选标签详情\n- “确认/跳过”：不展开，进入Step7选择",
            False,
        )

    if args.stop_after in ("6", "step6"):
        return

    # Step 6.5：三方标签（可选）
    if args.non_interactive:
        mode = decisions.get("step6_5_show_third_party", "auto")
        if mode in ("auto", "force"):
            tp_out = out_dir / "third_party_matches.json"
            _run([
                "python3", str(SCRIPT_DIR / "match_third_party_tags.py"),
                "--tp-tags", str(SKILL_DIR / "assets" / "third_party_tags.json"),
                "--schema", str(schema_path),
                "--out", str(tp_out),
            ])
    # 交互模式下由对话决定是否提示/展开

    if args.stop_after in ("6.5", "step6.5"):
        return

    # Step 7：用户选择（必须）
    if args.non_interactive:
        step7 = decisions.get("step7") or {}
        must = step7.get("must") or []
        preferred = step7.get("preferred") or []
        optional = step7.get("optional") or []
        exclude = step7.get("exclude") or []
        if not must:
            _prompt_block("Step7用户选择", "非交互模式必须提供step7.must（至少一个tagId，或or_groups二维列表）。", True)
        # MUST 推荐使用二维or_groups：[[a,b],[c],[d,e]] 表示 (a OR b) AND c AND (d OR e)
        # 仍兼容一维列表：[a,b,c]（后续由create_must_baseline自动分组；但推荐二维，能显式表达OR）
        _save_json(out_dir / "must.json", must)
        _save_json(out_dir / "preferred.json", preferred)
        _save_json(out_dir / "optional.json", optional)
        _save_json(out_dir / "exclude.json", exclude)
    else:
        _prompt_block(
            "Step7用户选择(MUST/PREFERRED/OPTIONAL/EXCLUDE)",
            "请基于Step6结果完成选择（至少给出MUST）。\n交互模式下请在对话中完成选择后，再用非交互模式把选择写入decisions.json继续执行。",
            False,
        )

    if args.stop_after in ("7", "step7"):
        return

    # Step 8：冲突检测（静默，发现冲突才提示）
    # 此处由执行脚本内部完成父子/互斥处理；驱动器仅保留流程位置。

    # Step 8.5：执行口径确认（强制卡点）
    if args.non_interactive:
        p = decisions.get("step8_5") or {}
        track_type = p.get("trackType")
        id_types = p.get("idTypes") or []
        if not track_type or not id_types:
            _prompt_block("Step8.5执行口径确认", "非交互模式必须提供 step8_5.trackType 与 step8_5.idTypes。", True)
    else:
        _prompt_block(
            "Step8.5执行口径确认(trackType/idTypes)",
            "创建人群前必须确认执行口径：\n- trackType: MOBILE/PC/OTT\n- idTypes: 根据端选择\n请先在对话中确认，再用非交互模式提供 step8_5 参数继续。",
            False,
        )

    if args.stop_after in ("8.5", "step8.5"):
        return

    # Step 9：创建 MUST 基准
    if args.non_interactive:
        p = decisions.get("step8_5") or {}
        track_type = p.get("trackType")
        id_types = p.get("idTypes") or []
        must_path = out_dir / "must.json"
        print("[Step9] create_must_baseline")
        res = _run([
            "python3", str(SCRIPT_DIR / "create_must_baseline.py"),
            "--must", str(must_path),
            "--track-type", str(track_type),
            "--id-types", *[str(x) for x in id_types],
        ])
        _save_json(out_dir / "must_baseline_result.json", res)
    else:
        _prompt_block("Step9创建MUST基准", "交互模式不执行创建，请改用非交互模式并提供step8_5与step7。", False)

    if args.stop_after in ("9", "step9"):
        return

    # Step 9.5：是否做Overlap
    if args.non_interactive:
        branch = str(decisions.get("step9_5") or "B").upper()
        if branch not in ("A", "B"):
            branch = "B"
    else:
        _prompt_block("Step9.5分支选择", "请选择：A直接创建 / B计算Overlap并给方案。", False)

    if branch == "A":
        _prompt_block("Step9.5直接创建分支", "当前驱动器仅实现到Step9基础链路；直接创建分支请在后续版本补齐。", True)

    # Step 10-12：Overlap/扩缩量/方案生成（留给后续补齐）
    _prompt_block("Step10-12未实现", "当前驱动器已实现到Step9，并提供关键交互卡点拦截。Step10-14将按同样方式继续补齐。", True)


if __name__ == "__main__":
    main()
