#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v5.3.0 留出集评测 runner（公开口径，任何人都可复现）；v6.5.0 F59 扩展
--gate/--fidelity 真网闸门档。

评测对象：机械层判定（五态）。默认跑内置金标集（examples/demo_refs.json，
8 条其中 3 处预埋伪造——随包公开的设计性夹具）；--refs 指向带 expected
字段的标注集走同一核验栈。

指标（离线口径，逐项定义在 docs/benchmark.md）：
  capture_rate       预埋伪造被判非 verified 的比例（越高越好）
  strict_capture     预埋伪造被判 invalid 的比例（结构层能实锤的比例）
  false_kill_rate    非伪造条目被判 invalid 的比例（越低越好，误伤）
  distribution       五态判定分布
  fidelity_hit_rate  （--fidelity）忠实度标签与预期分级的命中率

闸门（--gate，F59）：
  标注集（expected planted/clean）  → capture=100% 且 false_kill=0 才 PASS
  腐蚀集（expected_fidelity）       → 忠实度命中率=100% 才 PASS
  退出码 1=闸门拦停。run_eval 直调 verify_one 逐条隔离——不走 CLI 批内
  leader-follower 缓存（同 DOI 腐蚀条目不被掩蔽，M5 教训的通路级保障），
  也不读写持久磁盘缓存（该缓存只在 CLI 主循环）——闸门数字对真网当日快照
  负责，逐条独立核验。

诚实边界：默认 --offline 只测结构层；online 注册库核验结果随上游数据
漂移，数字只对运行当日快照负责（docs/benchmark.md 有完整口径）。
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import verify_refs as vr  # noqa: E402

# 内置金标集的公开设计（examples/demo_refs.json 实测形态）：#6=良构假 DOI、
# #7=编造 URL（着陆页不存在、无注册库标识符）、#8=无任何标识符与 URL——
# offline 结构层实锤对象是 #8（缺标识符→invalid）；#6/#7 良构伪造 offline
# 诚实降 partial（docs/benchmark.md 边界 1）
GOLDEN_PLANTED = (6, 7, 8)
GOLDEN_CLEAN = (1, 2, 3, 4, 5)

_FID_TAG = re.compile(r"\[元数据漂移:(minor|major)\]")


def _fidelity_label(note: str) -> str:
    """从判定 note 提取忠实度标签：minor/major；无标签=exact（M5：标签是
    注记不是判定——分级只在 partial 内，verdict 语义零改动）。"""
    m = _FID_TAG.search(note or "")
    return m.group(1) if m else "exact"


def run_eval(refs_path: str = "", offline: bool = True, fidelity: bool = False) -> dict:
    """跑评测并返回指标 dict。refs_path 空=内置金标集。

    fidelity=True：refs 文件须含 expected_fidelity（{“1”: “exact|minor|major”}），
    逐条真网核验后比对 [元数据漂移:*] 标签与预期分级（腐蚀集工作流，
    holdout_fidelity.json 为随包实例）。"""
    if refs_path:
        doc = json.load(open(refs_path, encoding="utf-8"))
        refs = doc["refs"] if isinstance(doc, dict) else doc
        exp = (doc.get("expected") if isinstance(doc, dict) else None) or {}
        planted = {int(k) for k, v in exp.items() if v == "planted"}
        clean = {int(k) for k, v in exp.items() if v == "clean"}
        if fidelity:
            fid_exp = {
                int(k): str(v)
                for k, v in (
                    (doc.get("expected_fidelity") or {}) if isinstance(doc, dict) else {}
                ).items()
            }
            assert fid_exp, "fidelity 模式要求 refs 文件含 expected_fidelity 字段"
        else:
            assert planted or clean, '标注集须含 expected: {"1": "planted"|"clean", ...}'
    else:
        if fidelity:
            raise SystemExit("fidelity 模式须 --refs 指向带 expected_fidelity 的腐蚀集")
        _demo = os.path.join(HERE, "..", "examples", "demo_refs.json")
        refs = json.load(open(_demo, encoding="utf-8"))
        planted, clean = set(GOLDEN_PLANTED), set(GOLDEN_CLEAN)
    results = []
    for i, ref in enumerate(refs, 1):
        results.append(vr.verify_one(ref, i, offline, 10.0, False))
    v = {r["index"]: r["verdict"] for r in results}
    n_planted, n_clean = len(planted), len(clean)
    captured = sum(1 for i in planted if v.get(i) not in (None, "verified"))
    strict = sum(1 for i in planted if v.get(i) == "invalid")
    killed = sum(1 for i in clean if v.get(i) == "invalid")
    dist = {}
    for r in results:
        dist[r["verdict"]] = dist.get(r["verdict"], 0) + 1
    m = {
        "version": vr.VERSION,
        "mode": "offline 结构层" if offline else "online 注册库",
        "n": len(refs),
        "capture_rate": round(captured / n_planted, 4) if n_planted else None,
        "strict_capture": round(strict / n_planted, 4) if n_planted else None,
        "false_kill_rate": round(killed / n_clean, 4) if n_clean else None,
        "distribution": dist,
        "per_ref": {str(i): v.get(i) for i in sorted(v)},
    }
    if fidelity:
        obs = {r["index"]: _fidelity_label(r.get("note", "")) for r in results}
        hits = sum(1 for i, want in fid_exp.items() if obs.get(i) == want)
        m["fidelity_hit_rate"] = round(hits / len(fid_exp), 4) if fid_exp else None
        m["fidelity_expected"] = {str(i): fid_exp[i] for i in sorted(fid_exp)}
        m["fidelity_observed"] = {str(i): obs.get(i) for i in sorted(fid_exp)}
    # 内容绑定（v6.5.0 审计 P2）：全批 unreachable/unverified=判据无证据面
    # （capture/false_kill 在全网故障下可假满）——闸门以「至少一条 verified/
    # partial 证据」为放行前提
    m["network_liveness"] = any(r["verdict"] in ("verified", "partial") for r in results)
    return m


def render_md(m: dict) -> str:
    def _pct(x):
        return f"{x:.0%}" if isinstance(x, (int, float)) else "—（无该侧样本）"

    lines = [
        "# 留出集评测摘要（cite-holmes 公开口径）",
        "",
        f"- 引擎：v{m['version']} · 模式：{m['mode']} · 条数：{m['n']}",
        f"- 捕获率 capture_rate：{_pct(m['capture_rate'])}（预埋伪造被判非 verified）",
        f"- 实锤率 strict_capture：{_pct(m['strict_capture'])}（预埋伪造被判 invalid）",
        f"- 误伤率 false_kill_rate：{_pct(m['false_kill_rate'])}（非伪造被判 invalid）",
        f"- 判定分布：{m['distribution']}",
    ]
    if "fidelity_hit_rate" in m:
        lines.append(
            f"- 忠实度命中率 fidelity_hit_rate："
            f"{_pct(m['fidelity_hit_rate'])}（标签与预期分级一致）"
        )
        lines.append(f"- 预期分级：{m['fidelity_expected']}")
        lines.append(f"- 实测分级：{m['fidelity_observed']}")
    lines += [
        "",
        "复现：python tools/run_eval.py（默认内置金标集 offline 口径）；"
        "完整方法论与历史数字见 docs/benchmark.md。",
    ]
    return "\n".join(lines) + "\n"


def gate_check(m: dict) -> list:
    """F59 闸门判据：返回违例清单（空=PASS）。"""
    bad = []
    if m.get("capture_rate") is not None and m["capture_rate"] != 1.0:
        bad.append(f"capture_rate={m['capture_rate']}（要求 1.0——预埋伪造全部非 verified）")
    if m.get("false_kill_rate") is not None and m["false_kill_rate"] != 0.0:
        bad.append(f"false_kill_rate={m['false_kill_rate']}（要求 0.0——clean 零误杀）")
    if m.get("fidelity_hit_rate") is not None and m["fidelity_hit_rate"] != 1.0:
        bad.append(
            f"fidelity_hit_rate={m['fidelity_hit_rate']}"
            f"（要求 1.0——预期 {m.get('fidelity_expected')}，"
            f"实测 {m.get('fidelity_observed')}）"
        )
    if m.get("capture_rate") is None and m.get("fidelity_hit_rate") is None:
        bad.append("无可闸判据（需 planted 标注或 expected_fidelity 之一）")
    if m.get("network_liveness") is False:
        bad.append(
            "全批 unreachable/unverified（无任何 verified|partial 证据）"
            "——网络态存疑，判据面失效，拒绝放行（内容绑定）"
        )
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description="cite-holmes 留出集评测（公开口径）")
    ap.add_argument("--refs", default="", help="标注集 JSON（含 expected 字段；缺省用内置金标集）")
    ap.add_argument("--net", action="store_true", help="online 注册库口径（数字只对当日快照负责）")
    ap.add_argument(
        "--fidelity",
        action="store_true",
        help="忠实度腐蚀集模式（refs 须含 expected_fidelity；标签比对，判定语义零改动）",
    )
    ap.add_argument(
        "--gate",
        action="store_true",
        help="F59 闸门：capture=100%+false_kill=0（标注集）或忠实度命中=100%（腐蚀集），"
        "违例退出码 1（run_tests.sh --held-out 调用形态）",
    )
    ap.add_argument("--json-out", default="eval_result.json")
    ap.add_argument("--md-out", default="eval_summary.md")
    args = ap.parse_args()
    if args.fidelity and not args.net:
        # 忠实度标签产自注册库元数据比对——offline 无标签可提取
        print("fidelity 模式需 --net（标签产自注册库元数据，offline 无标签）", file=sys.stderr)
        return 2
    if args.gate and not args.net:
        # v6.5.0 审计 P2：闸门与 fidelity 同规——offline 判据无证据面
        print("--gate 需 --net（真网闸门；offline 判据无证据面）", file=sys.stderr)
        return 2
    m = run_eval(args.refs, offline=not args.net, fidelity=args.fidelity)
    gate_bad = gate_check(m) if args.gate else None
    try:  # 审计 P2-2：输出不可写=友好失败（对齐 v5.2 自立标准）
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(m, f, ensure_ascii=False, indent=2)
        with open(args.md_out, "w", encoding="utf-8") as f:
            f.write(render_md(m))
    except OSError as e:
        print(
            f"评测输出写入失败：{type(e).__name__}（{args.json_out} / {args.md_out}）",
            file=sys.stderr,
        )
        return 2
    print(render_md(m))
    if gate_bad is not None:
        if gate_bad:
            print("GATE: FAIL")
            for b in gate_bad:
                print(f"  ✗ {b}")
            return 1
        parts = []
        if m.get("capture_rate") is not None:
            parts.append("capture=100% / false_kill=0")
        if m.get("fidelity_hit_rate") is not None:
            parts.append("fidelity=100%")
        print("GATE: PASS（" + "；".join(parts) + "；网络活性=有证据）")
    print(f"JSON：{args.json_out}\nMD：{args.md_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
