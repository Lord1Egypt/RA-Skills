"""cite-holmes v6.0.0 模块层：ch_reports（由手术脚本从单文件引擎分层，
判定语义与 API 见壳 verify_refs.py 与 ADR-0010）。一切跨层符号与被
测试 patch 的函数一律经 _ROOT（由壳注入主壳命名空间）——patch 语义
与 trunk/mcp 双壳隔离（目录前缀加载）共同由该机制保证。"""

import argparse
import csv
import difflib
import hashlib
import ipaddress
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import escape as html_escape
from urllib.parse import urlparse, urlunparse, quote

_ROOT = None  # 由 verify_refs 壳注入


def _bind(root):
    global _ROOT
    _ROOT = root


SCORE_WEIGHTS = {"verified": 10, "partial": 4, "unreachable": 0, "unverified": -2, "invalid": -8}


def render_bluf_dict(results: list, scorecard: dict) -> dict:
    """v3.2.0 BLUF 结构化块(BLUF Report Specification v1.0 L1):
    五键字典 + typed 附加(score/counts)——JSON 报告 bluf 字段直接用它。
    worst-actionable 规则(规范第 4 节):invalid>未验>partial 分支措辞。"""
    c = scorecard["counts"]
    n = scorecard["total"]
    if c["invalid"]:
        verdict = f"不建议直接使用：{c['invalid']} 条编造/无效引用必须先清除"
        blocker = f"{c['invalid']} 条 invalid"
        action = "删除或更换 invalid 信源后重跑"
    elif c["unreachable"] or c["unverified"]:
        verdict = (
            f"基本可用但有保留：{c['unreachable']} 条不可达/{c['unverified']} 条未验需人工复核"
        )
        blocker = f"{c['unreachable'] + c['unverified']} 条待复核"
        action = "打开 Wayback 链核对不可达项,或联网重跑"
    elif c["partial"]:
        verdict = f"可用：{c['verified']}/{n} 条 verified,{c['partial']} 条 partial 需降级使用"
        blocker = f"{c['partial']} 条 partial"
        action = "partial 项在正文引用时注明保留意见"
    else:
        verdict = f"全部 verified（{n} 条）——可进入投稿/正文流程"
        blocker = "无"
        action = "可直接 --export bibtex 导出参考文献"
    _retr = sum(
        1 for r in results if ((r.get("checks") or {}).get("retraction") or {}).get("retracted")
    )
    _rev = sum(1 for r in results if r.get("needs_human_check"))
    kn = (
        f"CiteScore {scorecard['score']}/100 ({scorecard['grade']}), "
        f"verified {c['verified']}/{n}, invalid {c['invalid']}, "
        f"复核 {_rev} 条（其中撤稿 {_retr} 条）"
    )
    return {
        "verdict": verdict,
        "key_numbers": kn,
        "blocker": blocker,
        "next_action": action,
        "cite_holmes_version": _ROOT.VERSION,
        "score": scorecard["score"],
        "grade": scorecard["grade"],
        "counts": dict(c),
    }


def render_bluf(results: list, scorecard: dict) -> str:
    """v3.0.0 YAML 前置块(md/html 用);v3.2.0 起从 render_bluf_dict 单一真源渲染。"""
    d = render_bluf_dict(results, scorecard)
    return (
        "---\n"
        f"verdict: {d['verdict']}\n"
        f"key_numbers: {d['key_numbers']}\n"
        f"blocker: {d['blocker']}\n"
        f"next_action: {d['next_action']}\n"
        f"cite_holmes_version: {d['cite_holmes_version']}\n"
        "---"
    )


def compute_scorecard(results: list) -> dict:
    counts = {v: sum(1 for r in results if r["verdict"] == v) for v in SCORE_WEIGHTS}
    n = len(results)
    raw = sum(SCORE_WEIGHTS[v] * c for v, c in counts.items())
    score = round(100 * max(raw, 0) / (10 * n)) if n else 0
    grade = "A" if score >= 85 else "B" if score >= 70 else "C" if score >= 50 else "D"
    return {"score": score, "grade": grade, "total": n, "counts": counts, "weights": SCORE_WEIGHTS}


def capability_matrix() -> dict:
    """能力边界矩阵（v1.7）：机械层已抓伪造类型 vs 仍需语义层把关的类型。
    结构化呈现边界——「不能做什么」与「能做什么」同样值得写清楚。"""
    return {
        "caught": [
            "假 DOI（DOI.org 查无）",
            "真 DOI 配假论文（错引/张冠李戴）",
            "假 PMID（E-utilities 查无）",
            "假 arXiv ID（官方 API 查无）",
            "DOI↔PMID 拼接（两键各真但指向不同论文）",
            "期刊名不符",
            "作者名不符",
            "真实但已撤稿（Crossref/Retraction Watch 撤稿库）",
            "死链/不可达（自动附 Wayback 存档对照）",
            "重复引用（URL/DOI/PMID 三键去重）",
            "中文原题 vs 登记英文题名（v3.10 跨语言三级桥接核验）",
            "克隆引用对（v3.10 同题不同 DOI / 同 DOI 不同题，成对警示）",
            "整批伪装指纹（v3.11 清单画像：标识符近邻簇/年份集中/信源集中，人工抽查建议）",
            "预印本已正式发表未引用（v3.11 arXiv→期刊版 DOI 升级提示，注记级）",
        ],
        "semantic": [
            "指向真实、可信页面的精心伪造——内容是否真支撑论断由模型的语义层判断"
            "（research_refs.json 的 semantic 字段），机械层不承诺捕获",
        ],
        "unsupported": [
            "PDF/Word 文档直读（请先手工提取引用条目再投喂）",
            "万方号/维普号等中文库专属编号（可经 URL 或标题间接核验）",
            "网页所述事实本身的对错（机械层只验来源存在与一致性，语义层归模型/人工）",
        ],
    }


# ---------------- 输出编码（Windows GBK 控制台兜底） ----------------
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

# ---------------- 域名权威度分层 ----------------
# 自上而下首个命中者生效；未命中默认 blog。
_CALIBRATE_KEYS = ("scope", "timeframe", "audience", "format")


def render_plan_artifact(plan: dict, out_path: str):
    """v5.2.0 F28 协作式研究计划工件（Google DR collaborative_planning 借鉴）：
    PLAN 阶段的机械层——校验计划 JSON 完整性并渲染人读 md 工件
    （CALIBRATE 四要素表+子问题复选框+预算台账脚手架）。
    硬失败（subquestions 空/budget_searches 非正整数/结构非对象）返回 None
    （错误已打印，调用方 return 2）；CALIBRATE 要素缺失=软 WARN（agent 可用
    声明过的默认值，不阻断协作流）。引擎只校验与渲染，绝不替用户改计划。"""
    if not isinstance(plan, dict):
        print("❌ 研究计划须为 JSON 对象（--plan plan.json）", file=sys.stderr)
        return None
    subs = plan.get("subquestions")
    if (
        not isinstance(subs, list)
        or not subs
        or not all(isinstance(s, str) and s.strip() for s in subs)
    ):
        print("❌ subquestions 必填：非空字符串数组（研究计划的子问题清单）", file=sys.stderr)
        return None
    budget = plan.get("budget_searches")
    if not isinstance(budget, int) or isinstance(budget, bool) or budget < 1:
        print("❌ budget_searches 必填：正整数（本轮检索预算上限）", file=sys.stderr)
        return None
    try:
        _bstr = str(budget)  # 审计 P2-1：CPython int→str 4300 位上限——超长友好失败
    except ValueError:
        print("❌ budget_searches 数值超长（>4300 位）——请给合理预算（如 40）", file=sys.stderr)
        return None
    warns = [
        f"calibrate.{k} 未填写——agent 侧应以声明过的默认值补齐"
        for k in _CALIBRATE_KEYS
        if not str(plan.get(k) or "").strip()
    ]
    lines = [
        "# 研究计划（协作工件）",
        "",
        f"- 生成：{time.strftime('%Y-%m-%d %H:%M')} · cite-holmes v{_ROOT.VERSION}"
        " 机械层校验渲染（计划由 agent 与用户协作定稿，引擎绝不代改）",
        "",
    ]
    lines += ["## CALIBRATE 四要素", "", "| 要素 | 值 |", "|---|---|"]
    for k in _CALIBRATE_KEYS:
        v = str(plan.get(k) or "").strip()
        lines.append(f"| {k} | {_ROOT.md_cell(v, 80) if v else '⚠️ 未填写（建议补齐）'} |")
    lines += ["", "## 子问题清单", ""]
    for i, s_ in enumerate(subs, 1):
        lines.append(f"- [ ] Q{i}. {_ROOT.md_cell(s_.strip(), 120)}")
    lines += [
        "",
        "## 预算台账（SEARCH 期逐轮回填）",
        "",
        "| 轮 | 子问题 | 检索式 | 命中 | 取舍 |",
        "|---|---|---|---|---|",
    ]
    for i in range(1, min(len(subs), 12) + 1):
        lines.append(f"| {i} | Q{i} |  |  |  |")
    lines += [
        "",
        f"- 预算上限：{_bstr} 次检索（QUICK≤6 / FULL≤15 / DEEP≤40；"
        "超预算诚实说明缺口，不硬凑结论）",
    ]
    if plan.get("source_policy"):
        lines.append(f"- 信源政策：{plan['source_policy']}")
    lines += [
        "",
        "> 编辑本文件后请同步改 plan.json 再重跑 --plan 校验（md 是渲染"
        "产物，JSON 才是执行锚点）。",
    ]
    try:  # 审计 P2-2：不可写路径（目录/无权限）友好失败不裸崩
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    except OSError as e:
        print(f"❌ 计划工件写入失败：{out_path}（{type(e).__name__}）", file=sys.stderr)
        return None
    print(f"[plan] 计划工件已渲染：{out_path}（{len(subs)} 子问题 · 预算 {_bstr}）")
    return warns


def render_audit_report(results: list, cd, scorecard: dict) -> str:
    """v5.4.0 F35 稿件审计报告（面向编辑/审稿人/教师）：把核验结果重组为
    分级疑点清单——P0 编造嫌疑（invalid）/P1 高风险线索（撤稿/不可达）/
    P2 复核项（政策注记/partial 缺字段）+完整性（覆盖率/孤儿，如有）+
    行动清单。机械层口径：只重组既有判定与线索，绝不新造判定（ADR-0005）。"""
    lines = [
        "# 引用审计报告（audit）",
        "",
        f"- 生成：{time.strftime('%Y-%m-%d %H:%M')} · cite-holmes v{_ROOT.VERSION}"
        " · 机械层口径（非语义判断）",
        f"- 对象：{len(results)} 条引用 · CiteScore {scorecard['score']}/100"
        f"（{scorecard['grade']} 级）",
        "",
    ]
    p0 = [r for r in results if r["verdict"] == "invalid"]
    if p0:
        lines.append(f"### P0 编造嫌疑（{len(p0)} 条，最高优先）\n")
        for r in p0:
            codes = "、".join(r.get("error_codes") or []) or "—"
            lines.append(
                f"- #{r['index']} {_ROOT.md_cell(r.get('title'), 60)}"
                f"（错误码 {codes}）：{_ROOT.md_cell(r.get('note'), 110)}"
            )
        lines.extend(
            [
                "",
                "**建议动作**：逐条移除或替换信源；若作者坚持存在，" "要求提供可访问的原始出处。",
                "",
            ]
        )

    def _is_retr(r):
        # 审计 P1-1 修复：撤稿信号在嵌套 checks.retraction.retracted（引擎从不在
        # 顶层设 retracted 键——旧判据读顶层是死键，真实撤稿条目全漏进 P2）
        return bool(((r.get("checks") or {}).get("retraction") or {}).get("retracted"))

    _p0_ids = {id(r) for r in p0}
    retr = [r for r in results if _is_retr(r) and id(r) not in _p0_ids]
    unreach = [
        r
        for r in results
        if r["verdict"] == "unreachable" and id(r) not in _p0_ids and not _is_retr(r)
    ]  # 审计 P1-2：与 retr 互斥，防同条双计
    p1 = retr + unreach
    if p1:
        lines.append(f"### P1 高风险线索（{len(p1)} 条）\n")
        for r in p1:
            tag = "撤稿⚠" if _is_retr(r) else "不可达"
            lines.append(
                f"- #{r['index']} [{tag}] {_ROOT.md_cell(r.get('title'), 60)}："
                f"{_ROOT.md_cell(r.get('note'), 110)}"
            )
        lines.extend(
            [
                "",
                "**建议动作**：要求作者提供可访问版本（撤稿条目必须"
                "处理；不可达≠不存在，换网络/代理复核后再定）。",
                "",
            ]
        )
    _p1_ids = {id(r) for r in p1}
    p2 = [
        r
        for r in results
        if id(r) not in _p1_ids
        and r["verdict"] != "invalid"
        and ((r.get("checks", {}) or {}).get("source_policy") or r["verdict"] == "partial")
    ]
    if p2:
        lines.append(f"### P2 复核项（{len(p2)} 条）\n")
        for r in p2:
            pol = (r.get("checks", {}) or {}).get("source_policy") or {}
            tag = "政策" if pol else "partial"
            lines.append(
                f"- #{r['index']} [{tag}] {_ROOT.md_cell(r.get('title'), 60)}："
                f"{_ROOT.md_cell(r.get('note'), 110)}"
            )
        lines.extend(["", "**建议动作**：按注记人工过目；政策注记反映策展偏好" "（非真伪）。", ""])
    if cd is not None:
        lines.extend(
            [
                "### 完整性",
                "",
                f"- 正文 in-text 引用 {cd['n_citations']} 处：未绑定 "
                f"{cd['n_unbound']}、锚词不足 {cd['n_low_anchor']}",
                f"- 引用覆盖率 {cd.get('coverage', 0):.0%}"
                + (
                    f"（{cd.get('n_uncited')} 条列而未引——漏引或冗列）"
                    if cd.get("n_uncited")
                    else ""
                ),
                "",
            ]
        )
    lines += [
        "## 行动清单",
        "",
        f"1. P0 {len(p0)} 条：移除/替换或索要原始出处",
        f"2. P1 {len(p1)} 条：撤稿必处理；不可达复核后再定",
        f"3. P2 {len(p2)} 条：人工过目",
        "4. 完整性问题（如有）：补引或删冗",
        "",
        "---",
        "免责：本报告为机械层核验重组（存在性/一致性/结构），"
        "「来源是否支撑论断」属语义层，不在本报告范围。",
    ]
    return "\n".join(lines) + "\n"


def submission_readiness(results: list, cd=None) -> dict:
    """v6.1.0 F51 投稿就绪判据（机械层，纯计算）：与 render_audit_report 同源
    分级口径——P0=invalid（编造嫌疑实锤）/P1=撤稿+不可达/P2=partial+政策注记。
    ready 判据：P0=0 且撤稿=0 且不可达=0（这些都须先处理）；P2 与完整性
    问题不阻断（有明确人工复核路径），只列为待办。
    返回 {"ready": bool, "p0": n, "p1": n, "p2": n, "n_invalid": n,
          "n_unverified_or_unreachable": n, "blockers": [..], "todos": [..]}。
    诚实边界：机械层就绪 ≠ 学术就绪（语义支撑/查重/期刊格式不在判据内）——
    结论行必须随附边界声明。"""
    p0 = [r for r in results if r.get("verdict") == "invalid"]

    def _is_retr(r):
        return bool(((r.get("checks") or {}).get("retraction") or {}).get("retracted"))

    retr = [r for r in results if _is_retr(r) and r not in p0]
    unreach = [
        r for r in results if r.get("verdict") == "unreachable" and r not in p0 and not _is_retr(r)
    ]
    p1 = retr + unreach
    p2 = [
        r
        for r in results
        if r not in p1
        and r not in p0
        and r.get("verdict") != "invalid"
        and ((r.get("checks", {}) or {}).get("source_policy") or r.get("verdict") == "partial")
    ]
    blockers, todos = [], []
    if p0:
        blockers.append(f"P0 编造嫌疑 {len(p0)} 条（invalid——逐条移除/替换或索要原始出处）")
    if retr:
        blockers.append(f"撤稿条目 {len(retr)} 条（必须处理后再投）")
    if unreach:
        blockers.append(f"不可达条目 {len(unreach)} 条（复核可访问性后再定）")
    if p2:
        todos.append(f"P2 复核项 {len(p2)} 条（partial/政策注记——人工过目）")
    if cd is not None:
        if cd.get("n_unbound"):
            todos.append(f"正文引用未绑定 {cd['n_unbound']} 处（编号/条目对不上）")
        if cd.get("n_uncited"):
            todos.append(f"列而未引 {cd.get('n_uncited')} 条（漏引或冗列）")
    n_open = sum(1 for r in results if r.get("verdict") in ("unverified", "unreachable"))
    return {
        "ready": not blockers,
        "p0": len(p0),
        "p1": len(p1),
        "p2": len(p2),
        "n_invalid": len(p0),
        "n_unverified_or_unreachable": n_open,
        "blockers": blockers,
        "todos": todos,
    }


def build_submission_index(results: list, cd, scorecard: dict, artifacts: list = None) -> str:
    """v6.1.0 F51 投稿前审计包 INDEX（--check-paper 总览件）：就绪结论+
    判定分布+分级计数+包内工件导航+人工边界声明。只装配既有判定与线索，
    绝不新造判定（ADR-0005 宪法同 render_audit_report）。"""
    rd = submission_readiness(results, cd)
    counts = {}
    for r in results:
        counts[r.get("verdict")] = counts.get(r.get("verdict"), 0) + 1
    order = ["verified", "partial", "unreachable", "unverified", "invalid"]
    dist = "｜".join(f"{_ROOT.VERDICT_ZH.get(v, v)} {counts[v]}" for v in order if counts.get(v))
    if rd["ready"]:
        lines = [
            "# 投稿前审计包 INDEX",
            "",
            "## 结论：READY（机械层零阻断项）",
            "",
            "- 机械层判定无 P0 编造嫌疑、无撤稿、无未决不可达——引用层"
            "不存在已知硬伤。**这不是学术就绪声明**：语义支撑、查重、"
            "期刊格式由作者与期刊流程负责；partial/复核项请人工过目。",
        ]
    else:
        lines = [
            "# 投稿前审计包 INDEX",
            "",
            "## 结论：NOT READY（存在机械层阻断项）",
            "",
            "**阻断清单**：",
            *[f"- {b}" for b in rd["blockers"]],
        ]
    lines += [
        "",
        f"- 对象：{len(results)} 条引用 · 判定分布：{dist}",
        f"- CiteScore {scorecard['score']}/100"
        f"（{scorecard['grade']} 级） · "
        f"未决（unverified/unreachable）"
        f"{rd['n_unverified_or_unreachable']} 条",
        "",
    ]
    if rd["todos"]:
        lines += ["**不阻断但建议处理**：", *[f"- {t}" for t in rd["todos"]], ""]
    if artifacts:
        lines += ["## 包内工件", "", *[f"- {a}" for a in artifacts], ""]
    lines += [
        "## 使用说明",
        "",
        "- 本 INDEX 汇总同批生成的核验报告（verify_report）、稿件审计"
        "分级（audit.md）与参考文献导出；各文件口径一致（同一次核验）。",
        "- 复跑强制重验加 --refresh-cache；语义支撑判断请用语境层"
        "（学界用法面板/citation contexts）辅助人工复核。",
        "",
        "---",
        f"生成：{time.strftime('%Y-%m-%d %H:%M')} · cite-holmes "
        f"v{_ROOT.VERSION} · 机械层口径（存在性/一致性/结构），"
        "非语义判断。",
    ]
    return "\n".join(lines) + "\n"


def profile_bibliography(results: list) -> dict:
    """v3.11 清单级伪造画像（纯本地，零网络）：LLM 批量编造参考文献表时
    会留下统计指纹——标识符近号成簇、年份过度集中/超前、期刊过度集中。
    逐条核验抓「单条伪造」，本画像抓「整批伪装」。画像只描述分布并给出
    人工抽查建议，绝不改变任何单条判定（集中也可能是合法的专题综述）。
    返回 {"flags": [{kind, detail}], "stats": {...}}；flags 为空=画像干净。"""
    import datetime as _dt

    flags, stats = [], {}
    n = len(results)
    if n < 4:
        return {"flags": [], "stats": {"n": n, "skipped": "条目过少，画像不具统计意义"}}

    # ① 标识符近邻簇：同前缀 DOI 的尾部数字段数值近邻（差 ≤2）成簇 ≥3 条
    #    ——批量生成器的典型指纹；合法的连续页码/论文集编号同样会命中，
    #    因此只给「人工抽查」建议，不判伪造。
    clusters = {}
    for r in results:
        doi = str(r.get("doi") or "").lower()
        m = re.match(r"^(10\.\d{4,9}/\S*?)(\d{3,})$", doi)
        if not m:
            continue
        clusters.setdefault(m.group(1), []).append((int(m.group(2)), r["index"]))
    seen_cluster = set()
    for prefix, seqs in sorted(clusters.items()):
        if len(seqs) < 3:
            continue
        seqs = sorted(seqs)
        run = [seqs[0]]
        best = []
        for prev, cur in zip(seqs, seqs[1:]):
            if cur[0] - prev[0] <= 2:
                run.append(cur)
            else:
                best = max(best, run, key=len)
                run = [cur]
        best = max(best, run, key=len)
        if len(best) >= 3:
            key = (prefix, tuple(x[1] for x in best))
            if key not in seen_cluster:
                seen_cluster.add(key)
                flags.append(
                    {
                        "kind": "serial_cluster",
                        "detail": (
                            f"标识符近邻簇：{prefix}* 尾号 "
                            f"{'、'.join(str(x[0]) for x in best[:6])}"
                            f"{'…' if len(best) > 6 else ''} 共 {len(best)} 条连续"
                            f"（条目 {'/'.join('#' + str(x[1]) for x in best[:6])}"
                            f"{'…' if len(best) > 6 else ''}）——批量生成常见指纹，"
                            "也可能是合法连续编号，建议逐条抽查该簇"
                        ),
                    }
                )

    # ② 年份画像：未来年份逐项注记 + 清单级过度集中
    now_y = _dt.date.today().year
    years = []
    for r in results:
        y = r.get("year")
        try:
            y = int(y)
        except (TypeError, ValueError):
            continue
        years.append((y, r["index"]))
    future = [(y, i) for y, i in years if y > now_y + 1]
    if future:
        flags.append(
            {
                "kind": "future_year",
                "detail": f"声称年份超前当前时间（{'、'.join(f'{y}(#{i})' for y, i in future[:5])}"
                f"{'…' if len(future) > 5 else ''}）——尚未发生的文献年份，重点核查",
            }
        )
    if years:
        ys = [y for y, _ in years]
        from collections import Counter as _C

        top_y, top_n = _C(ys).most_common(1)[0]
        stats["year"] = {
            "min": min(ys),
            "max": max(ys),
            "mode": top_y,
            "mode_share": round(top_n / len(ys), 2),
        }
        if len(ys) >= 8 and top_n / len(ys) >= 0.8:
            flags.append(
                {
                    "kind": "year_concentration",
                    "detail": f"{top_n}/{len(ys)} 条声称同年（{top_y}）——"
                    "综述专辑可能合法，但整批同年的参考文献表更像一次性生成，建议抽查",
                }
            )

    # ③ 期刊集中度：单一信源占比过高（合法专题综述 vs 编造窄源，两可→仅提示）
    srcs = [str(r.get("source") or "").strip() for r in results]
    srcs = [s for s in srcs if s]
    if len(srcs) >= 8:
        from collections import Counter as _C

        top_s, top_n = _C(srcs).most_common(1)[0]
        stats["source_top"] = {"name": top_s[:40], "share": round(top_n / len(srcs), 2)}
        if top_n / len(srcs) >= 0.6:
            flags.append(
                {
                    "kind": "source_concentration",
                    "detail": f"{top_n}/{len(srcs)} 条同信源「{top_s[:40]}」（占比 "
                    f"{top_n/len(srcs):.0%}）——确认该刊是否真的承载这些论文",
                }
            )

    # ④ 标识符构成比：完全无标识符（doi/pmid/arxiv/url 全空）的条目占比
    bare = [
        r["index"]
        for r in results
        if not any((r.get(k) or "").strip() for k in ("doi", "pmid", "arxiv", "url"))
    ]
    stats["identifier_mix"] = {"bare": len(bare), "n": n, "bare_share": round(len(bare) / n, 2)}
    if bare and len(bare) / n >= 0.5:
        flags.append(
            {
                "kind": "bare_refs",
                "detail": f"{len(bare)}/{n} 条无任何可机验标识符（DOI/PMID/arXiv/URL 均空）"
                f"（如 #{'、#'.join(str(x) for x in bare[:5])}…）——无法机械核验，"
                "建议补全标识符后重跑",
            }
        )
    return {"flags": flags, "stats": stats}


def completeness_for_ref(ref: dict) -> dict:
    """v3.11 逐条完整度评分（纯本地）：verified 条目能从注册库 CSL 回填多少
    导出字段（作者/刊名/年份/卷/期/页）——GB/T 与 BibTeX 导出「宁缺毋错」的
    下一代：不仅告诉你能不能导，还告诉你差哪些字段。评分口径：authors 30 /
    container 20 / year 20 / volume·issue·page 各 10；csl 缺失（如非 DOI 源）
    返回 score=None（未知≠零分）。只读不写。"""
    csl = ((ref.get("checks") or {}).get("doi_metadata") or {}).get("csl") or {}
    if not csl:
        return {"score": None, "missing": [], "suggestion": ""}
    have = {
        "authors": bool(csl.get("authors")),
        "container": bool(csl.get("container")),
        "year": bool(csl.get("year")),
        "volume": bool(csl.get("volume")),
        "issue": bool(csl.get("issue")),
        "page": bool(csl.get("page")),
    }
    weights = {"authors": 30, "container": 20, "year": 20, "volume": 10, "issue": 10, "page": 10}
    score = sum(w for k, w in weights.items() if have[k])
    missing = [k for k, v in have.items() if not v]
    zh = {
        "authors": "作者",
        "container": "刊名",
        "year": "年份",
        "volume": "卷",
        "issue": "期",
        "page": "页码",
    }
    sug = ""
    if missing:
        sug = (
            "注册库未登记："
            + "、".join(zh[m] for m in missing)
            + "——可对照原文补全后再导出（导出策略仍为宁缺毋错）"
        )
    return {"score": score, "missing": missing, "suggestion": sug}


def annotate_completeness(results: list) -> int:
    """v3.11 批处理接线：给 verified 且 csl 在场的条目写 completeness 字段。
    返回有 completeness 的条数（JSON 报告逐条透出，md/html 不逐条展开）。"""
    n = 0
    for r in results:
        if r.get("verdict") != "verified":
            continue
        c = completeness_for_ref(r)
        if c["score"] is not None:
            r["completeness"] = c
            n += 1
    return n


# v6.6.0 F63 顶层错误码单一来源注册表（稳定契约，MCP/脚本可依赖）：
# code → { "zh": 人话翻译 }。derive_error_codes 与 --explain 翻译表均由本表
# 派生——评测「顶层错误码体系不完全统一」（派生表/翻译表两处手工维护漂移）
# 的机制根除；E_DOU→E_DOI 更名经 _ERR_CODE_ALIAS 向后兼容。
ERROR_CODE_META = {
    "E_DOI_NOT_FOUND": {"zh": "DOI 在 DOI.org 不存在（404）——疑似编造引用",
                        "grill": "该 DOI 从何而来（AI 生成/笔记转抄/数据库导出）？拼写逐字符核对过吗？"},
    "E_TITLE_MISMATCH": {"zh": "DOI 存在但登记标题与声称不符——错引或张冠李戴",
                         "grill": "登记论文与你要引的论文是同一篇吗？给出登记原文题名并说明差异成因。"},
    "E_CROSS_LANG": {"zh": "跨语言标题无法机器比对——已保守处理，建议人工核对",
                     "grill": "请附登记语言原题或罗马化题名，说明人工核对路径。"},
    "E_ARXIV_NOT_FOUND": {"zh": "arXiv ID 官方 API 查无",
                          "grill": "该 arXiv ID 的出处？是否与正式发表版 DOI 重复登记？"},
    "E_PMID_NOT_FOUND": {"zh": "PMID 在 PubMed E-utilities 查无",
                         "grill": "该 PMID 来源与位数核对过吗（8 位段常见拼误）？"},
    "E_STITCHED": {"zh": "标识符拼接嫌疑（两键各真但疑似指向不同论文）",
                   "grill": "DOI 与 PMID 分别指向哪两篇？说明拼接成因与正确标识符。"},
    "E_RETRACTED": {"zh": "命中撤稿记录（Crossref/Retraction Watch）",
                    "grill": "撤稿通告原文怎么说的？你的论断是否只依赖被撤部分？"},
    "E_EXPRESSION_OF_CONCERN": {"zh": "编辑关注通告（Expression of Concern）——证据效力存疑，转人工",
                                "grill": "EoC 范围覆盖你的论断吗？后续更正版是否已引用？"},
    "E_AUTHOR_MISMATCH": {"zh": "作者姓氏与登记列表不符",
                          "grill": "作者列表差异是姓氏拼写、名字顺序还是他人论文？逐一说明。"},
    "E_JOURNAL_MISMATCH": {"zh": "期刊名与登记不符",
                           "grill": "期刊名差异是更名/缩写/冒名？给出登记期刊全名与 ISSN。"},
    "E_UNREACHABLE": {"zh": "来源抓取失败（超时/反爬/网络）——不等于不存在",
                      "grill": "换网络/代理重跑结果？URL 是否仍可在浏览器打开？"},
    "E_OFFLINE": {"zh": "离线模式未执行核验",
                  "grill": "本条未经注册库核验——联网重跑前不得作为已核实引用。"},
}
# v6.5.0 及更早版本的拼写码兼容读取（只进解释器，不再产出）
_ERR_CODE_ALIAS = {"E_DOU_NOT_FOUND": "E_DOI_NOT_FOUND"}


def derive_error_codes(r: dict) -> list:
    """从单条 result 的 checks/note 派生结构化错误码(纯函数,零网络)。
    码表唯一来源=上方 ERROR_CODE_META(v6.6.0 F63 顶层注册表;本函数只描述
    派生判据,码的含义与人话翻译一律查注册表——此前「派生 docstring/
    --explain 翻译表」两处手工维护+一处拼写(E_DOU→E_DOI)的不一致已根除)。
    v6.6.0 更名: E_DOU_NOT_FOUND → E_DOI_NOT_FOUND(旧码经
    _ERR_CODE_ALIAS 兼容读取,报告/导出自本版起只发新码)。
    无问题返回 [](空=没有可断言的错误信号,不等于"证明正确")。"""
    codes = []
    v = r.get("verdict")
    c = r.get("checks") or {}
    note = r.get("note") or ""
    doi_m = c.get("doi_metadata") or {}
    if "DOI 在 DOI.org 不存在" in note or (
        doi_m.get("matched") is False and "404" in note and r.get("doi")
    ):
        codes.append("E_DOI_NOT_FOUND")
    elif "疑似编造或错引" in note or doi_m.get("adjust") == "invalid":
        codes.append("E_TITLE_MISMATCH")
    if "跨语言" in note:
        codes.append("E_CROSS_LANG")
    if "拼接" in note:
        codes.append("E_STITCHED")
    ax = c.get("arxiv_metadata") or {}
    if ax.get("matched") is False and r.get("arxiv"):
        codes.append("E_ARXIV_NOT_FOUND")
    if "E-utilities 查无" in note or ("E-utilities" in note and r.get("pmid") and v == "invalid"):
        codes.append("E_PMID_NOT_FOUND")
    if (c.get("retraction") or {}).get("retracted"):
        codes.append("E_RETRACTED")
    if (c.get("retraction") or {}).get("nature") == "expression_of_concern":
        codes.append("E_EXPRESSION_OF_CONCERN")
    if "作者" in note and ("不符" in note or "不一致" in note):
        codes.append("E_AUTHOR_MISMATCH")
    if "期刊名不符" in note or "期刊" in note and "不符" in note:
        codes.append("E_JOURNAL_MISMATCH")
    if v == "unreachable":
        codes.append("E_UNREACHABLE")
    if r.get("note") and "offline" in str(r.get("note", "")).lower():
        codes.append("E_OFFLINE")
    return codes


def export_bibtex(results: list, path: str) -> int:
    """仅导出 verified 条目为 BibTeX（可直接导入论文参考文献管理器）。返回条数。
    字段值经 bib_safe 加固（剥除花括号/换行，防 @entry 逃逸），citation key 保证唯一。"""
    n = 0
    used_keys = set()
    with open(path, "w", encoding="utf-8") as f:
        for r in results:
            if r["verdict"] != "verified":
                continue
            n += 1
            title = _ROOT.bib_safe(r.get("title") or "untitled").strip() or "untitled"
            # 评审修正：year 未经消毒可携带换行/花括号逃逸 @entry，只留数字
            ys = re.sub(r"[^0-9]", "", str(r.get("year") or ""))[:4] if r.get("year") else ""
            year = ys or "n.d."
            words = re.findall(r"[A-Za-z0-9\u4e00-\u9fff]+", title)[:3]
            key = ("holmes" + ys + "".join(words))[:42] or f"ref{r['index']}"
            k2 = key
            sfx = 2
            while k2 in used_keys:
                k2 = f"{key}_{sfx}"
                sfx += 1
            used_keys.add(k2)
            fields = [f"  title = {{{_ROOT.bib_safe(title)}}}"]
            if r.get("source"):
                fields.append(f"  journal = {{{_ROOT.bib_safe(r.get('source'))}}}")
            if r.get("year"):
                fields.append(f"  year = {{{year}}}")
            if r.get("url"):
                fields.append(f"  url = {{{_ROOT.bib_safe(r.get('url'))}}}")
            if r.get("doi"):
                fields.append(f"  doi = {{{_ROOT.bib_safe(r.get('doi'))}}}")
            if r.get("arxiv"):
                fields.append(f"  eprint = {{{_ROOT.bib_safe(r.get('arxiv'))}}}")
                fields.append("  archivePrefix = {arXiv}")
            notes = ["cite-holmes verified"]
            if r.get("pmid"):
                notes.append(f"PMID: {r['pmid']}")
            fields.append("  note = {{{}}}".format(_ROOT.bib_safe("; ".join(notes))))
            f.write("@misc{" + k2 + ",\n" + ",\n".join(fields) + "}\n\n")
    return n


def _gbt_type_code(r: dict) -> tuple:
    """GB/T 7714 文献类型标识:期刊[J];预印本/网页[EB/OL];无卷期页的电子资源兜底[EB/OL]。
    返回 (类型码, 是否电子资源)。"""
    if r.get("arxiv"):
        return "EB/OL", True
    if (r.get("checks", {}).get("doi_metadata", {}) or {}).get("csl", {}).get("container"):
        return "J", False
    if r.get("url"):
        return "EB/OL", True
    return "EB/OL", True


def _gbt7714_entry(r: dict, cite_date: str) -> str:
    """v4.9.0 单条 GB/T 7714 行构造（自 export_gbt7714 抽出——综述工作台内联
    复用同一构造器，杜绝双实现漂移）。不满足收录判定返回 None。
    收录策略:verified 全收;partial 仅当 DOI 元数据**一致**(adjust=="" 且有 CSL,
    如仅缺可选输入字段)——标题/期刊存疑的 partial 不收(宁缺毋错)。"""
    dm = r.get("checks", {}).get("doi_metadata", {}) or {}
    if r["verdict"] == "verified":
        pass
    elif (
        r["verdict"] == "partial" and dm.get("adjust") == "" and dm.get("matched") and dm.get("csl")
    ):
        pass  # 元数据一致、仅缺可选输入字段的 partial:注册库已确认存在与内容
    else:
        return None
    csl = (r.get("checks", {}).get("doi_metadata", {}) or {}).get("csl") or {}
    title = (csl.get("title") or r.get("title") or "").strip() or "untitled"
    year = str(csl.get("year") or r.get("year") or "").strip()
    authors = list(csl.get("authors") or [])
    if not authors:
        raw = re.split(r"[,，;；、]", str(r.get("authors") or ""))
        authors = [a.strip() for a in raw if a.strip()]
    cjk_title = any("\u4e00" <= c <= "\u9fff" for c in title)
    et_al = "等" if cjk_title else "et al"
    if len(authors) > 3:
        authors = authors[:3] + [et_al]
    author_str = ", ".join(authors)
    tcode, is_e = _gbt_type_code(r)
    seg = []
    if author_str:
        seg.append(author_str + ".")
    seg.append(f"{title}[{tcode}].")
    container = (csl.get("container") or r.get("source") or "").strip()
    vol = csl.get("volume") or ""
    iss = csl.get("issue") or ""
    page = csl.get("page") or ""
    if tcode == "J" and container:
        part = f"{container}, {year or 's.d.'}"
        if vol:
            part += f", {vol}"
            if iss:
                part += f"({iss})"
        if page:
            part += f": {page}"
        seg.append(part + ".")
    else:
        if year:
            seg.append(f"({year}).")
        seg.append(f"[{cite_date}].")
    url = (r.get("url") or "").strip()
    doi = (r.get("doi") or "").strip()
    if doi and not url.lower().startswith("https://doi.org/"):
        seg.append(f"DOI: {doi}.")  # DOI 尾注(规范形);url 为 doi.org 链接时已承载
    if url:
        seg.append(f"{url}.")
    return " ".join(seg)


def export_gbt7714(results: list, path: str) -> int:
    """v3.6 GB/T 7714-2025 参考文献表导出(verified + 元数据一致的 partial,返回条数)。
    每条以注册库权威 CSL 元数据为准(mcp:checks.doi_metadata.csl;输入声称值兜底):
      期刊: 作者1, 作者2, 作者3, 等. 题名[J]. 刊名, 年, 卷(期): 页码.
      电子: 题名[EB/OL]. (发布年)[引用日期]. URL. DOI: ...
    作者规则:≤3 全列;>3 取前 3 + ", 等"(中文条目)/", et al."(拉丁条目);
    拉丁作者姓全大写+名首字母(取自 CSL 预格式化)。正文中文条目判定=题名含 CJK。
    v4.9.0 起行构造抽为 _gbt7714_entry（综述工作台内联复用同一构造器）。"""
    cite_date = time.strftime("%Y-%m-%d")
    lines_out = [ln for ln in (_gbt7714_entry(r, cite_date) for r in results) if ln]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines_out) + ("\n" if lines_out else ""))
    return len(lines_out)


def build_review_kit(results: list, refs: list = None, topic: str = "", cite_date: str = "") -> str:
    """v4.9.0 F25 综述工作台：把核验批转成「综述就绪」Markdown 三件套——
    综述表格（verified 优先）/标注书目/即贴 GB/T 参考文献表。
    零新增外呼：被引数复用核验期已取的 S2 citation contexts（checks.
    citation_contexts.cited_by），discover 场景回退检索时顺带的 OpenAlex
    cited_by_count（refs[i]["_cited_by"]）——两处皆无则诚实「—」。
    判定语义原样透出：partial/invalid 条目绝不混入「已核实」观感（铁律：
    存在性佐证与判定分离）；GB/T 内联表与 export_gbt7714 同一构造器
    （_gbt7714_entry），收录策略同为宁缺毋错。"""
    refs = refs or []
    cite_date = cite_date or time.strftime("%Y-%m-%d")
    order = {"verified": 0, "partial": 1, "unreachable": 2, "unverified": 3, "invalid": 4}
    rows = sorted(results, key=lambda r: (order.get(r.get("verdict"), 9), r.get("index", 0)))
    counts = {}
    for r in results:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    stat = "｜".join(
        f"{_ROOT.VERDICT_ZH.get(v, v)} {c}"
        for v, c in sorted(counts.items(), key=lambda kv: order.get(kv[0], 9))
    )

    def _cited(r):
        # 审计 P2-2：0 是测得的零，与未知（—）必须可区分——isinstance 门而非 truthy
        cc = (r.get("checks", {}) or {}).get("citation_contexts") or {}
        if cc.get("ran") and isinstance(cc.get("cited_by"), int):
            return f"{cc['cited_by']}（Semantic Scholar）"
        i = r.get("index")
        cb = (
            refs[i - 1].get("_cited_by")
            if isinstance(refs, list)
            and isinstance(i, int)
            and 0 <= i - 1 < len(refs)
            and isinstance(refs[i - 1], dict)
            else None
        )
        if isinstance(cb, int):
            return f"{cb}（OpenAlex）"
        return "—"

    def _authors_short(r):
        csl = (r.get("checks", {}).get("doi_metadata", {}) or {}).get("csl") or {}
        authors = list(csl.get("authors") or [])
        if not authors:
            raw = re.split(r"[,，;；、]", str(r.get("authors") or ""))
            authors = [a.strip() for a in raw if a.strip()]
        if not authors:
            return ""
        cjk = any("\u4e00" <= c <= "\u9fff" for c in str(r.get("title") or ""))
        return ", ".join(authors[:3]) + (
            "，等" if (cjk and len(authors) > 3) else "，et al" if len(authors) > 3 else ""
        )

    out = []
    out.append("# 文献综述工作台（review-kit）\n")
    out.append(
        f"- 主题：{topic or '（输入清单）'}｜生成：{cite_date}｜" f"cite-holmes v{_ROOT.VERSION}"
    )
    out.append(f"- 核验总览：共 {len(results)} 条——{stat}")
    out.append(
        "- 判定语义：verified=官方注册库核验一致；partial=部分确认，"
        "引用前请人工过目；invalid=编造或错引（不得引用）；"
        "unverified/unreachable=未能核验（查无永不判死）\n"
    )

    out.append("## 一、综述表格（verified 优先，同判定保持原序）\n")
    out.append("| # | 文献 | 年份 | 出处 | 被引 | 判定 |")
    out.append("|---|---|---|---|---|---|")
    for n_, r in enumerate(rows, 1):
        t = re.sub(r"[|\n]", "／", str(r.get("title") or ""))  # P3③ 剥换行对齐 _ROOT.md_cell
        src = re.sub(r"[|\n]", "／", str(r.get("source") or "")) or "—"
        yr = r.get("year") or "—"
        flag = "⚠需人工" if r.get("needs_human_check") else ""
        out.append(
            f"| {n_} | {t} | {yr} | {src} | {_cited(r)} "
            f"| {_ROOT.VERDICT_ZH.get(r.get('verdict'), r.get('verdict'))}{flag} |"
        )
    out.append("")

    out.append("## 二、标注书目\n")
    for n_, r in enumerate(rows, 1):
        au = _authors_short(r)
        head = f"**[{n_}] {r.get('title') or '(无标题)'}**"
        meta = " — ".join(
            x for x in (au, str(r.get("source") or ""), str(r.get("year") or "")) if x
        )
        out.append(f"{head}" + (f"  \n{meta}" if meta else ""))
        vline = f"判定：{_ROOT.VERDICT_ZH.get(r.get('verdict'), r.get('verdict'))}"
        if r.get("needs_human_check"):
            vline += " ⚠需人工"  # 审计 P2-3：与综述表格旗标对齐
        note = re.sub(r"\s+", " ", str(r.get("note") or ""))[:140]
        if note:
            vline += f"——{note}"
        out.append(f"  - {vline}")
        if str(r.get("doi") or "").strip():
            out.append(f"  - DOI: https://doi.org/{str(r['doi']).strip()}")
        if str(r.get("pmid") or "").strip():
            out.append(f"  - PMID: https://pubmed.ncbi.nlm.nih.gov/" f"{str(r['pmid']).strip()}/")
        _ul = usage_line(r.get("citation_contexts"))
        if _ul:
            out.append(f"  - 学界用法（≤3 条抽样）：{_ul}")  # 审计 P3-2：kit 无区级免责，就地声明
        _sig = context_signal(r.get("citation_contexts"))  # v5.9.0
        if _sig:
            out.append(f"  - 语境信号（advisory）：{_sig}")
        _oa = (r.get("checks") or {}).get("open_access") or {}
        if _oa.get("ran"):
            if _oa.get("is_oa"):
                out.append(
                    f"  - 开放获取：{_oa.get('license') or '许可未知'}"
                    + (f" · {_oa['oa_url']}" if _oa.get("oa_url") else "")
                )
            else:
                out.append("  - 开放获取：无免费全文（Unpaywall 未收录 OA 版本）")
    out.append("")

    out.append(
        "## 三、即贴参考文献表（GB/T 7714-2025，宁缺毋错：仅收 verified"
        "与元数据一致的 partial）\n"
    )
    gbt = [(i, _gbt7714_entry(r, cite_date)) for i, r in enumerate(rows, 1)]
    gbt = [(i, ln) for i, ln in gbt if ln]
    if gbt:
        for i, ln in gbt:
            out.append(f"[{i}] {ln}")
    else:
        out.append(
            "（本批无满足收录判定的条目——非编造信号，仅按「宁缺毋错」"
            "策略暂不收录；判定明细见正文报告）"
        )
    out.append("")
    out.append("---")
    out.append(
        "使用说明：partial/⚠ 条目引用前须人工核对；本表由机械核验生成，"
        "「核验一致」≠「支撑你的论点」——语义支撑请自行判断或用语境层"
        "（citation contexts）复核。复跑加 --refresh-cache 可强制重验。"
    )
    return "\n".join(out)


def export_ris(results: list, path: str) -> int:
    """v3.7.0 RIS 导出(Zotero/EndNote 通用,与 v1.9 BibTeX 导入构成回环)。
    收录策略与 GB/T 相同:verified + 元数据一致 partial。AU 每作者一行。"""
    n = 0
    out = []
    for r in results:
        dm = r.get("checks", {}).get("doi_metadata", {}) or {}
        if r["verdict"] == "verified":
            pass
        elif (
            r["verdict"] == "partial"
            and dm.get("adjust") == ""
            and dm.get("matched")
            and dm.get("csl")
        ):
            pass
        else:
            continue
        csl = dm.get("csl") or {}
        title = (csl.get("title") or r.get("title") or "").strip() or "untitled"
        out.append("TY  - " + ("JOUR" if csl.get("container") else "GEN"))
        out.append("TI  - " + title)
        for a in csl.get("authors") or []:
            out.append("AU  - " + a)
        if not csl.get("authors") and r.get("authors"):
            for a in re.split(r"[,，;；、]", str(r["authors"])):
                if a.strip():
                    out.append("AU  - " + a.strip())
        if csl.get("container"):
            out.append("JO  - " + csl["container"])
        if r.get("source"):
            out.append("PB  - " + str(r["source"])[:200])
        if csl.get("year") or r.get("year"):
            out.append("PY  - " + str(csl.get("year") or r.get("year")))
        if csl.get("volume"):
            out.append("VL  - " + csl["volume"])
        if csl.get("issue"):
            out.append("IS  - " + csl["issue"])
        if csl.get("page"):
            pg = str(csl["page"])
            if "-" in pg:
                sp, ep = pg.split("-", 1)
                out.append("SP  - " + sp.strip())
                out.append("EP  - " + ep.strip())
            else:
                out.append("SP  - " + pg)
        if r.get("doi"):
            out.append("DO  - " + str(r["doi"]))
        if r.get("url"):
            out.append("UR  - " + str(r["url"]))
        out.append("N1  - cite-holmes verified (" + r["verdict"] + ")")
        out.append("ER  - ")
        out.append("")
        n += 1
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    return n


def export_csv(results: list, path: str) -> None:
    """全量审计台账 CSV（utf-8-sig，Excel 直接打开不乱码）。单元格做公式注入中和。"""
    cols = [
        "index",
        "title",
        "verdict",
        "tier",
        "http_status",
        "needs_human_check",
        "year",
        "source",
        "url",
        "doi",
        "pmid",
        "arxiv",
        "note",
    ]
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in results:
            row = [_ROOT.csv_safe(str(r.get(c) if r.get(c) is not None else "")) for c in cols]
            w.writerow(row)


def export_audit(results: list, path: str, offline: bool, profile: str) -> None:
    """v1.9 透明工作底稿（auditjson）：每条引用的逐项检查明细，机器可读。
    供人工复核、机构审计与流程合规——回应"检测系统需要透明多源"的行业呼吁
    （arXiv 2607.22693：五家检测工具均不可无人监督运行，透明度是刚需）。"""
    doc = {
        "version": _ROOT.VERSION,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "offline": offline,
        "profile": profile,
        "checks_catalog": {
            "doi_metadata": "DOI.org CSL 元数据（标题/年份/期刊/作者交叉核验）",
            "retraction": "Crossref/Retraction Watch 撤稿库",
            "s2": "Semantic Scholar 第三源交叉确认（只确认不降级）",
            "s2_title": "Semantic Scholar 标题检索确认（无 DOI/PMID/arXiv 引用的正面信号，只确认不降级）",
            "arxiv_metadata": "arXiv 官方 API（标题/年份）",
            "arxiv_landing_fallback": "arXiv API 失败时官方着陆页标题比对（v1.11 确定性保卫）",
            "url": "可达性检查（HEAD→GET 降级）",
            "openalex": "OpenAlex 书目级存在性（只确认不降级）",
            "wayback": "Wayback Machine 存档对照（unreachable 时）",
            "doi_pmid_crosscheck": "DOI↔PMID 拼接伪造检测",
            "semantic_audit": "语义层工作底稿（v1.11，模型判定结构化透出；not_in_source/contradicted 封顶 partial）",
            "citation_contexts": "L3 引文语境层（v3.0.0，S2 citations contexts/intents——学界评价）",
            "l4_evidence_cascade": "L4 证据升级级联（v3.1.0 接入主流程：语义 not_in_source/unclear 且配置裁判端点时，升级官方摘要/全文段落检索+外置裁判；判定只加固不翻案）",
        },
        "results": [
            {
                "index": r.get("index"),
                "title": r.get("title"),
                "verdict": r.get("verdict"),
                "tier": r.get("tier"),
                "http_status": r.get("http_status"),
                "needs_human_check": bool(r.get("needs_human_check")),
                "checks": r.get("checks") or {},
                "semantic_audit": r.get("semantic_audit"),
                "citation_contexts": r.get("citation_contexts"),
                "triples": (r.get("semantic_audit") or {}).get("triples", []),
                "note": r.get("note", ""),
            }
            for r in results
        ],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)


def precheck_conclusion(sc: dict) -> str:
    """v1.9 投稿前结论（一行）：arXiv 自 2026-05 起对含幻觉/未核引用的投稿实施
    处罚（最长禁投一年；v1.11 据 Nature 2026-05-19 报道修正起始月份），ICML 2026
    等会议亦将幻觉引用列为桌拒理由——报告头部直接给出可否提交的结论。"""
    c = sc["counts"]
    parts = [f"{c[k]} 条 {k}" for k in ("invalid", "unreachable", "unverified") if c[k]]
    if parts:
        return (
            "⚠️ 投稿前结论：不建议直接提交——存在 "
            + " / ".join(parts)
            + "，先完成人工复核（arXiv 自 2026-05 起、ICML 2026 等会议已对"
            "含幻觉/未核引用的投稿实施处罚）"
        )
    if c["partial"]:
        return (
            f"🟡 投稿前结论：可提交，但建议先处理 {c['partial']} 条 partial"
            "（降级使用项，正文引用需注明保留意见）"
        )
    return "✅ 投稿前结论：全部 verified——可进入投稿流程"


def usage_line(cc) -> str:
    """v5.0.0 学界用法一句话（报告与综述工作台共用）：S2 引文语境的用法分布
    （方法学/背景/结果）+高影响引用数+第一条例引摘句。增强信号，绝不参与判定；
    无数据返回空串（调用方整段不渲染）。"""
    if not isinstance(cc, dict) or not isinstance(cc.get("samples"), list) or not cc.get("samples"):
        return ""
    intents = {}
    for s in cc.get("samples", []):
        for it in s.get("intents") or []:
            intents[it] = intents.get(it, 0) + 1
    parts = [
        f"{_ROOT._INTENTS_ZH.get(k, k)}×{v}"
        for k, v in sorted(intents.items(), key=lambda kv: -kv[1])
    ]
    seg = []
    if parts:
        seg.append("用法分布 " + "/".join(parts))
    n_inf = sum(1 for s in cc.get("samples", []) if s.get("influential"))
    if n_inf:
        seg.append(f"高影响引用 {n_inf}")
    s0 = (cc.get("samples") or [{}])[0]
    quote = re.sub(r"\s+", " ", str(s0.get("context") or ""))[:100]
    ct = str(s0.get("citing_title") or "")[:40]
    if quote:
        seg.append("例引「" + quote + "」" + (f"——{ct}" if ct else ""))
    return "；".join(seg)


# v5.9.0 引文语境分歧信号：对比/质疑句式模式（中英）。S2 intents 只有
# background/methodology/result 三分类（官方口径），不标注争议性——
# 对比型语境（SciCite 分类学的 compare_or_contrast 方向）由本地启发式补位，
# 零新增外呼、零新增依赖。词边界与否定词排除按对抗审计 P3 收口：
# (?<!not )\bunlike\b 不吃 "not unlike"（双否=赞同），\brefut(e[ds]?|ing)\b
# 不吃 "irrefutable"（强赞同），(?<!不)但 不吃「不但」夸赞句式，
# 挑战(?!性) 不吃「极具挑战性」；fail(s|ed|ing)? to 补齐
# "failed to generalize" 类漏报。「相反数」类数学词在引用语境近乎不出现
# （审计判定为可接受误报，不设窄补丁）。
def context_signal(cc) -> str:
    """v5.9.0 引文语境分歧信号（advisory 展示层）：对 S2 抽样语境跑
    对比/质疑句式启发式扫描，命中达到保守阈值时提示「学界表述存在分歧」。
    阈值设计：命中 ≥50% 抽样——3 条抽样仅 1 条含转折词属学术写作常态，
    不报（避免把常规转折误渲染成学术争议）；抽样即语境（1/1、1/2 命中）。
    纯呈现层信号：绝不改判定、
    不挂复核旗（宪法同 v5.0 usage_line——存在性佐证与判定分离）；启发式
    必有漏报误报，双向如实声明于文档。无命中返回空串（调用方不渲染——
    老输出逐字节不变）。"""
    if not isinstance(cc, dict) or not isinstance(cc.get("samples"), list):
        return ""
    samples = cc.get("samples") or []
    if not samples:
        return ""
    hits = sum(1 for s in samples if _ROOT._CONTRAST_RE.search(str(s.get("context") or "")))
    if hits * 2 < len(samples):  # ≥50% 门槛：3 抽样仅 1 条转折属学术写作常态不报
        return ""
    return (
        f"分歧信号 {hits}/{len(samples)}：抽样语境含对比/质疑型表述——"
        "学界对该文结论存在不同声音，引用前建议人工复核原文语境"
    )


def render_md(
    results: list, offline: bool, profile: str = "general", context_check: dict = None
) -> str:
    sc = compute_scorecard(results)
    c = sc["counts"]
    lines = [
        render_bluf(results, sc),
        "",
        "# 引用机械验证报告",
        f"- 验证器：verify_refs.py v{_ROOT.VERSION} · 模式：{'offline（未联网）' if offline else 'online'}"
        + (" · 医学信源预设" if profile == "medical" else ""),
    ]
    if profile == "medical":
        lines.append(
            "- ⚠️ 免责声明：本报告仅为信源机械核验，不构成证据分级结论或医疗建议；"
            "预印本/社区层来源不得支撑医学结论。"
        )
    lines.append(f"- {precheck_conclusion(sc)}")

    lines += [
        "",
        "## CiteScore 置信度评分",
        f"### **{sc['score']} / 100 · {sc['grade']} 级**",
        "",
        f"- 总计 {sc['total']} 条：✅verified {c['verified']} · 🟡partial {c['partial']} · "
        f"⚠️unreachable {c['unreachable']} · ❌invalid {c['invalid']} · ⏸unverified {c['unverified']}",
        "- 计分：verified +10 / partial +4 / unreachable 0 / unverified −2 / invalid −8，"
        "满分 = 10 × 条数，归一化 0-100",
    ]
    _oa_ran = [r for r in results if ((r.get("checks") or {}).get("open_access") or {}).get("ran")]
    if _oa_ran:
        _n_oa = sum(1 for r in _oa_ran if r["checks"]["open_access"].get("is_oa"))
        lines.append(
            f"- 开放获取：{_n_oa}/{len(_oa_ran)} 条可免费读取"
            "（Unpaywall；--mailto 启用查询——纯数据富集不改判定）"
        )
        lines.append("")
    else:  # 审计 P1-1：无 OA 路径保持与 v5.4 逐字节一致（无条件空行不丢）
        lines.append("")
    lines += [
        "| # | 标题 | 层级 | HTTP | 判定 | 说明 |",
        "|---|---|---|---|---|---|",
    ]
    for r in results:
        title = _ROOT.md_cell(r["title"], 48)
        # 含 Wayback 存档链的备注放宽截断（存档 URL 普遍 >90 字符，截断即废链）
        note = _ROOT.md_cell(r["note"], 200 if "web.archive.org" in (r.get("note") or "") else 90)
        lines.append(
            f"| {r['index']} | {title} | {r['tier']} | "
            f"{r['http_status'] or '-'} | {_ROOT.VERDICT_ZH[r['verdict']]} | {note} |"
        )
    flagged = [
        r for r in results if r["needs_human_check"] or r["verdict"] in ("invalid", "unverified")
    ]
    if flagged:
        lines += ["", "## 待人工复核", ""]
        for r in flagged:
            lim = 200 if "web.archive.org" in (r.get("note") or "") else 110
            act = {
                "invalid": "建议：删除或更换信源",
                "unreachable": "建议：人工打开原链复核",
                "unverified": "建议：在线环境重跑验证",
            }.get(r["verdict"], "建议：按备注复核")
            lines.append(
                f"- #{r['index']} {_ROOT.md_cell(r['title'], 60)} → {r['verdict']}"
                f"（{act}）：{_ROOT.md_cell(r['note'], lim)}"
            )
    # v1.11 语义层判定区：仅当引用带结构化 semantic 字段时输出（无则与 v1.10
    # 输出逐字节一致，老消费者零感知）。机械层只做结构化透出与封顶，判定由模型做出。
    sem_rows = [r for r in results if r.get("semantic_audit")]
    if sem_rows:
        lines += [
            "",
            "## 语义层判定（模型在研究流程中做出，机械层结构化透出）",
            "",
            "| # | support | 论断（claim） | 原文摘句 |",
            "|---|---|---|---|",
        ]
        for r in sem_rows:
            sa = r["semantic_audit"]
            lines.append(
                f"| {r['index']} | {_ROOT.md_cell(sa.get('support'), 16)} | "
                f"{_ROOT.md_cell(sa.get('claim'), 60)} | "
                f"{_ROOT.md_cell(sa.get('quote'), 60)} |"
            )
        lines += [
            "",
            "support 取值：supported 支撑 / partial 部分支撑 / not_in_source "
            "来源未包含 / contradicted 相矛盾 / unclear 无法判定；"
            "not_in_source 与 contradicted 的条目已封顶 partial 并转人工复核。",
        ]
    # v5.0.0 学界用法区（S2 引文语境；无数据整段不渲染——老输出逐字节不变）
    usage_rows = [r for r in results if usage_line(r.get("citation_contexts"))]
    if usage_rows:
        lines += [
            "",
            "## 学界用法（引文语境）",
            "",
            "后续文献如何使用该论文——语境是增强信号，绝不改变判定；覆盖率低属诚实边界。",
            "| # | 被引 | 学界用法 |",
            "|---|---|---|",
        ]
        for r in usage_rows:
            _cc = r.get("citation_contexts") or {}
            lines.append(
                f"| {r['index']} | {_cc.get('cited_by', '—')} | "
                f"{_ROOT.md_cell(usage_line(_cc), 130)} |"
            )
    # v5.9.0 分歧信号（advisory；有信号才渲染——无信号老输出逐字节不变）。
    # 审计 P2：独立于 usage_rows 门扫全量——usage_line 空而信号非空的行
    # （如首样本 contexts[0]==""）不再静默丢失，与 kit 渲染器口径一致。
    _sig_rows = [(r, context_signal(r.get("citation_contexts"))) for r in results]
    _sig_rows = [(r, s) for r, s in _sig_rows if s]
    if _sig_rows:
        lines += [
            "",
            "⚠ 分歧信号（启发式 advisory，绝不改变判定）：",
            *[f"- #{r['index']} {s}" for r, s in _sig_rows],
        ]
    lines += [
        "",
        "## 能力边界矩阵",
        "",
        "- ✅ 机械层已抓伪造类型：" + "；".join(capability_matrix()["caught"]),
        "- 🧠 仍需语义层把关：" + "；".join(capability_matrix()["semantic"]),
        "- 🚫 不支持的输入：" + "；".join(capability_matrix()["unsupported"]),
        "",
        "## 判定说明",
        "",
        "- `verified`：可达 + 权威层(official/journal/preprint/media) + 字段完整 —— 可支撑正文结论",
        "- `partial`：可达但社区/博客层来源，或字段缺失 —— 降级使用，结论需注明",
        "- `unreachable`：抓取失败（404/超时/反爬）—— 不等于不存在，需人工打开复核",
        "- `invalid`：无 URL/DOI 或格式错误 —— 不得进入报告",
        "- 语义验证（来源是否支持论断）由模型完成，本报告只覆盖机械层",
        "",
    ]
    # v3.8.0 上下文核验区(--check-document 时呈现)
    if context_check:
        lines += [
            "",
            "## 上下文核验（正文 in-text 引用）",
            "",
            f"- 正文引用 {context_check['n_citations']} 处：未绑定 "
            f"{context_check['n_unbound']}，锚词不足 {context_check['n_low_anchor']}"
            f"（阈值 {context_check['anchor_threshold']}）",
        ]
        if context_check.get("n_listed"):
            _u = context_check.get("uncited_refs") or []
            _us = (
                f"（条目 {'、'.join(str(i) for i in _u[:10])}" f"{'…' if len(_u) > 10 else ''}）"
                if _u
                else ""
            )
            lines.append(
                f"- 引用覆盖 {context_check['coverage']:.0%}：清单 "
                f"{context_check['n_listed']} 条中 {context_check['n_uncited']} 条"
                f"未在正文引用{_us}——漏引或冗列建议（写作规范提示，非真伪判定）"
            )
        for c in context_check["citations"]:
            if not c["bound"]:
                lines.append(f"- ⚠️ {c['marker']} 未绑定——正文引用了清单外的编号/条目")
            elif c["anchor"] == "low":
                lines.append(
                    f"- ⚠️ {c['marker']} 锚词率 {c['anchor_rate']}"
                    f"（疑似错配引文：引文句与被引标题内容词重叠过低）→ 人工复核"
                )
        lines += ["", "- 锚词率低≠错引：是语义层人工复核候选（句子是否真被支撑由模型判定）"]
    _pairs = _ROOT.collect_clone_pairs(results)  # v3.10 克隆引用对区块（有对才出现）
    if _pairs:
        lines += ["", "## 克隆引用对（同题不同 DOI / 同 DOI 不同题）", ""]
        for p in _pairs:
            kind = (
                "同一标题挂多个不同 DOI——至少一个标识为编造或错引"
                if p["kind"] == "clone_doi"
                else "同一 DOI 挂不同标题——拼接变体，两条判定已各自独立核验"
            )
            lines.append(f"- #{p['a']} ↔ #{p['b']}（相似度 {p['sim']}）：{kind}；以元数据核验为准")
        lines.append("")
    _prof = profile_bibliography(results)  # v3.11 清单画像区块（有旗标才出现）
    if _prof["flags"]:
        lines += [
            "",
            "## 清单画像（批量伪造指纹筛查）",
            "",
            "> 逐条核验抓单条伪造，画像抓整批伪装——旗标是人工抽查建议，不是判定。",
        ]
        for f in _prof["flags"]:
            lines.append(f"- **{f['kind']}**：{f['detail']}")
        lines.append("")
    # v3.7.0 求星合规铺设:交付物尾注(每报告一次,低调一行;家族任务 10-06)
    lines += [
        "",
        "> 本文档由 cite-holmes 生成（[GitHub](https://github.com/docsor1212/cite-holmes) · "
        "[SkillHub](https://skillhub.cn/skills/indiv-sorsor/cite-holmes)）· 觉得有用欢迎 Star / 收藏",
        "",
    ]
    return "\n".join(lines)


def render_html(
    results: list, offline: bool, profile: str = "general", context_check: dict = None
) -> str:
    """v1.7：自包含单文件 HTML 报告——零外链（无外部 CSS/JS/字体）、移动端可读，
    用作给导师/编辑的存档分享件（与 BibTeX/CSV 台账并列的第三种交付物）。
    动态内容全部经 html_escape；备注中的 URL 转为可点击链接。"""
    sc = compute_scorecard(results)
    c = sc["counts"]
    e = html_escape
    vcls = {
        "verified": "v-ok",
        "partial": "v-part",
        "unreachable": "v-unreach",
        "invalid": "v-bad",
        "unverified": "v-unk",
    }

    def linkify(note: str) -> str:
        s = e(str(note or ""))
        return re.sub(
            r"(https?://[^\s<\"]+)", lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>', s
        )

    def _chain(r: dict) -> str:
        """v2.0.0 证据链微可视化:基于 checks 明细生成检查路径图标行。"""
        c = r.get("checks") or {}
        seg = []
        if c.get("doi_metadata"):
            seg.append(("DOI.org" + (" ✓" if c["doi_metadata"].get("matched") else " ?")))
        if c.get("arxiv_metadata"):
            seg.append("arXiv ✓" if c["arxiv_metadata"].get("matched") else "arXiv ?")
        if c.get("s2"):
            seg.append("S2 ✓" if c["s2"].get("matched") else "S2 ·")
        if c.get("retraction"):
            # v4.1.0 分档展示：撤稿族⚠/EoC⚠/更正ℹ/检查未完成✗（失败不冒充干净）
            r = c["retraction"]
            if r.get("retracted"):
                seg.append("撤稿⚠")
            elif r.get("nature") == "expression_of_concern":
                seg.append("EoC⚠")
            elif r.get("nature") == "correction":
                seg.append("更正ℹ")
            elif r.get("check_failed"):
                seg.append("撤稿检查✗")
            else:
                seg.append("撤稿库 ✓")
        if c.get("pubmed_reverse"):
            # v4.1.0：反查三态（命中✓/未命中·/传输失败✗）——失败不冒充查无
            pr = c["pubmed_reverse"]
            if pr.get("network_error"):
                seg.append("反查✗")
            elif pr.get("matched"):
                seg.append("反查✓")
            else:
                seg.append("反查·")
        if c.get("openalex"):
            seg.append("OpenAlex ✓" if c["openalex"].get("confirmed") else "OpenAlex ·")
        if c.get("url"):
            seg.append("可达 ✓" if c["url"].get("reachable") else "可达 ✗")
        if c.get("wayback"):
            seg.append("存档 ·")
        return " → ".join(seg)

    rows = []
    for r in results:
        chain = _chain(r)
        chain_html = f"<br><span class='chain'>{e(chain)}</span>" if chain else ""
        rows.append(
            f"<tr><td>{r['index']}</td>"
            f"<td>{e(str(r.get('title') or ''))}</td>"
            f"<td>{e(str(r.get('tier') or ''))}</td>"
            f"<td>{r.get('http_status') if r.get('http_status') is not None else '-'}</td>"
            f"<td class='{vcls[r['verdict']]}'><b>{_ROOT.VERDICT_ZH[r['verdict']]}</b></td>"
            f"<td class='note'>{linkify(r.get('note'))}{chain_html}</td></tr>"
        )

    actions = {
        "invalid": "建议：删除或更换信源",
        "unreachable": "建议：人工打开原链复核",
        "unverified": "建议：在线环境重跑验证",
    }
    review = []
    for r in results:
        if r.get("needs_human_check") or r["verdict"] in ("invalid", "unverified"):
            act = actions.get(r["verdict"], "建议：按备注复核")
            review.append(
                f"<li>#{r['index']} {e(str(r.get('title') or ''))} → "
                f"<b>{r['verdict']}</b>（{act}）：{linkify(r.get('note'))}</li>"
            )
    review_html = ("<h2>待人工复核</h2><ul>" + "".join(review) + "</ul>") if review else ""

    cap = capability_matrix()
    cap_html = (
        f"<h2>能力边界矩阵</h2>"
        f"<p>✅ <b>机械层已抓伪造类型</b>：{e('；'.join(cap['caught']))}</p>"
        f"<p>🧠 <b>仍需语义层把关</b>：{e('；'.join(cap['semantic']))}</p>"
        f"<p>🚫 <b>不支持的输入</b>：{e('；'.join(cap['unsupported']))}</p>"
    )

    # v1.11 语义层判定区（仅当引用带结构化 semantic 字段时输出）
    sem_rows = [r for r in results if r.get("semantic_audit")]
    if sem_rows:
        sem_trs = "".join(
            f"<tr><td>{r['index']}</td>"
            f"<td>{e(str(r['semantic_audit'].get('support') or ''))}</td>"
            f"<td>{e(str(r['semantic_audit'].get('claim') or ''))}</td>"
            f"<td>{e(str(r['semantic_audit'].get('quote') or ''))}</td></tr>"
            for r in sem_rows
        )
        sem_html = (
            f"<h2>语义层判定</h2>"
            f"<p class='meta'>模型在研究流程中做出，机械层结构化透出；"
            f"not_in_source / contradicted 条目已封顶 partial 并转人工复核。</p>"
            f"<table><tr><th>#</th><th>support</th><th>论断（claim）</th>"
            f"<th>原文摘句</th></tr>{sem_trs}</table>"
        )
    else:
        sem_html = ""

    # v5.6.0 HTML 学界用法节（对齐 md 层；无数据整段不渲染——老输出不变）
    # v5.9.0 审计 P2：行集合以 usage_line or context_signal 双门取全量，
    # 信号不因 usage_line 空而静默丢失（与 md/kit 渲染器口径一致）
    usage_rows_h = [
        r
        for r in results
        if usage_line(r.get("citation_contexts")) or context_signal(r.get("citation_contexts"))
    ]
    if usage_rows_h:
        _trs = ""
        for r in usage_rows_h:
            _u = usage_line(r.get("citation_contexts"))
            _s = context_signal(r.get("citation_contexts"))  # 并入学界用法单元格
            _cell = "；".join(x for x in (_u, _s) if x)
            _trs += (
                f"<tr><td>{r['index']}</td>"
                f"<td>{e(str((r.get('citation_contexts') or {}).get('cited_by', '—')))}</td>"
                f"<td>{e(_cell)}</td></tr>"
            )
        usage_html = (
            f"<h2>学界用法（引文语境）</h2>"
            f"<p class='meta'>后续文献如何使用该论文——语境是增强信号，"
            f"绝不改变判定；覆盖率低属诚实边界。</p>"
            f"<table><tr><th>#</th><th>被引</th><th>学界用法</th>"
            f"</tr>{_trs}</table>"
        )
    else:
        usage_html = ""

    # v5.6.0 审计 P2-3：HTML 侧 OA 汇总行（对齐 md 层；无数据不渲染）
    _oa_ran_h = [
        r for r in results if ((r.get("checks") or {}).get("open_access") or {}).get("ran")
    ]
    if _oa_ran_h:
        _n_oa_h = sum(1 for r in _oa_ran_h if r["checks"]["open_access"].get("is_oa"))
        _oa_html = (
            f"<p>开放获取：{_n_oa_h}/{len(_oa_ran_h)} 条可免费读取"
            "（Unpaywall；--mailto 启用——纯数据富集不改判定）</p>"
        )
    else:
        _oa_html = ""
    # v5.6.0 审计 P2-1：空占位条件化——旧版（无 usage 节）字节契约保持
    mid_html = "\n".join(x for x in (sem_html, usage_html) if x) + "\n"

    med = (
        (
            "<p class='disclaim'>⚠️ 免责声明：本报告仅为信源机械核验，不构成证据分级结论"
            "或医疗建议；预印本/社区层来源不得支撑医学结论。</p>"
        )
        if profile == "medical"
        else ""
    )
    pcls = (
        "disclaim"
        if sc["counts"]["invalid"] or sc["counts"]["unreachable"] or sc["counts"]["unverified"]
        else "preok"
    )
    pre = f"<p class='{pcls}'>{e(precheck_conclusion(sc))}</p>"
    bluf = render_bluf(results, sc)
    bluf_v = html_escape("\n".join(l for l in bluf.splitlines() if not l.startswith("---")))
    cc_html_block = ""
    if context_check:
        rows_cc = []
        for item_cc in context_check["citations"]:  # v3.8.0:变量名避开 f-string 后文的 c
            if not item_cc["bound"]:
                state = "⚠️ 未绑定（清单外条目）"
            elif item_cc["anchor"] == "low":
                state = f"⚠️ 锚词率 {item_cc['anchor_rate']}（疑似错配引文，人工复核）"
            else:
                state = f"锚词率 {item_cc['anchor_rate']}"
            rows_cc.append(
                f"<li>#{item_cc.get('ref_index') or '-'} {item_cc['marker']} — {state}<br>"
                f"<span class='note'>{item_cc['sentence'][:160]}</span></li>"
            )
        cc_html_block = (
            "<div style='margin-top:20px;padding:12px;border:1px solid #e5e5e5;border-radius:6px;'>"
            "<h3 style='margin:0 0 8px 0;'>上下文核验（正文 in-text 引用）</h3>"
            f"<p>共 {context_check['n_citations']} 处：未绑定 {context_check['n_unbound']}，"
            f"锚词不足 {context_check['n_low_anchor']}（阈值 {context_check['anchor_threshold']}）。"
            "锚词率低≠错引，是语义层人工复核候选。</p><ul>" + "".join(rows_cc) + "</ul></div>"
        )
    _pairs = _ROOT.collect_clone_pairs(results)  # v3.10 克隆引用对区块（有对才出现）
    clone_html_block = ""
    if _pairs:
        rows_cl = []
        for p in _pairs:
            kind = (
                "同一标题挂多个不同 DOI——至少一个标识为编造或错引"
                if p["kind"] == "clone_doi"
                else "同一 DOI 挂不同标题——拼接变体，两条判定已各自独立核验"
            )
            rows_cl.append(
                f"<li>#{p['a']} ↔ #{p['b']}（相似度 {p['sim']}）：{kind}；以元数据核验为准</li>"
            )
        clone_html_block = (
            "<div style='margin-top:20px;padding:12px;border:1px solid #f0d9d9;"
            "border-radius:6px;background:#fffafa;'>"
            "<h3 style='margin:0 0 8px 0;'>克隆引用对（同题不同 DOI / 同 DOI 不同题）</h3>"
            "<ul>" + "".join(rows_cl) + "</ul></div>"
        )
    _prof = profile_bibliography(results)  # v3.11 清单画像区块（有旗标才出现）
    prof_html_block = ""
    if _prof["flags"]:
        rows_pf = [f"<li><b>{f['kind']}</b>：{e(f['detail'])}</li>" for f in _prof["flags"]]
        prof_html_block = (
            "<div style='margin-top:20px;padding:12px;border:1px solid #e5e5e5;"
            "border-radius:6px;'>"
            "<h3 style='margin:0 0 8px 0;'>清单画像（批量伪造指纹筛查）</h3>"
            "<p>逐条核验抓单条伪造，画像抓整批伪装——旗标是人工抽查建议，不是判定。</p>"
            "<ul>" + "".join(rows_pf) + "</ul></div>"
        )
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>引用机械验证报告 · CiteScore {sc['score']}/{sc['grade']}</title>
<style>
body{{font-family:system-ui,-apple-system,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
margin:0 auto;padding:16px;max-width:960px;color:#1c2733;background:#fbfaf7;line-height:1.55}}
h1{{font-size:1.3em}} .score{{font-size:2.6em;font-weight:700}}
.v-ok{{color:#1a7f37}} .v-part{{color:#9a6700}} .v-unreach{{color:#b45309}}
.v-bad{{color:#c1341b}} .v-unk{{color:#57606a}}
.bluf{{background:#eef6ff;padding:10px 12px;border-radius:6px;font-size:.85em;white-space:pre-wrap;margin:8px 0}}
.chain{{color:#57606a;font-size:.78em;opacity:.85}}
.preok{{color:#1a7f37;background:#e9f7ee;padding:8px 12px;border-radius:6px}}
table{{border-collapse:collapse;width:100%;font-size:.88em;background:#fff}}
td,th{{border:1px solid #d8d2c4;padding:6px 8px;vertical-align:top;text-align:left}}
td.note{{word-break:break-all}} a{{color:#0b5394;word-break:break-all}}
.disclaim{{color:#9a6700;background:#fdf6dd;padding:8px 12px;border-radius:6px}}
.meta{{color:#57606a}} footer{{margin-top:24px;color:#57606a;font-size:.85em;
border-top:1px solid #d8d2c4;padding-top:8px}}
</style></head><body>
<h1>引用机械验证报告</h1>
<!-- cite-holmes BLUF machine-readable
{bluf}
-->
<pre class="bluf">{bluf_v}</pre>
<p class="score">{sc['score']}<span style="font-size:.45em;color:#57606a"> / 100 · {sc['grade']} 级</span></p>
<p class="meta">验证器 verify_refs.py v{_ROOT.VERSION} · 模式：{'offline（未联网）' if offline else 'online'}
{' · 医学信源预设' if profile == 'medical' else ''}<br>
总计 {sc['total']} 条：✅verified {c['verified']} · 🟡partial {c['partial']} ·
⚠️unreachable {c['unreachable']} · ❌invalid {c['invalid']} · ⏸unverified {c['unverified']}</p>
{_oa_html}
{med}
{pre}
<table><tr><th>#</th><th>标题</th><th>层级</th><th>HTTP</th><th>判定</th><th>说明</th></tr>
{''.join(rows)}</table>
{review_html}
{mid_html}{cap_html}
<h2>判定说明</h2>
<ul>
<li><b>verified</b>：可达 + 权威层 + 字段完整——可支撑正文结论</li>
<li><b>partial</b>：可达但社区/博客层，或字段/期刊/作者存疑——降级使用</li>
<li><b>unreachable</b>：抓取失败——不等于不存在，需人工打开复核</li>
<li><b>invalid</b>：无 URL/DOI、编号不存在或格式错误——不得进入报告</li>
</ul>
<footer>语义验证（来源是否支持论断）由模型完成，本报告只覆盖机械层；
指向真实可信页面的精心伪造仍需人工判断。cite-holmes · Cite Holmes</footer>
{cc_html_block}
{clone_html_block}
{prof_html_block}
<footer style="margin-top:24px;padding-top:12px;border-top:1px solid #eee;color:#9aa0a6;font-size:12px;text-align:center;">
本文档由 cite-holmes 生成 · <a href="https://github.com/docsor1212/cite-holmes" style="color:#9aa0a6;">GitHub</a> · <a href="https://skillhub.cn/skills/indiv-sorsor/cite-holmes" style="color:#9aa0a6;">SkillHub</a> · 觉得有用欢迎 Star / 收藏
</footer>
</body></html>"""


_DOCTOR_PROBES = [
    ("DOI.org 解析", "https://doi.org/10.3866/PKU.WHXB201112303"),
    ("Crossref API", "https://api.crossref.org/works?rows=0&mailto=doctor%40cite-holmes"),
    (
        "PubMed E-utilities",
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        "esearch.fcgi?db=pubmed&retmode=json&retmax=0&term=cite+holmes+doctor",
    ),
    ("arXiv API", "https://export.arxiv.org/api/query?search_query=all:cite&max_results=1"),
    ("OpenAlex", "https://api.openalex.org/works?per-page=1&select=id"),
    (
        "Semantic Scholar",
        "https://api.semanticscholar.org/graph/v1/paper/"
        "DOI:10.3866/PKU.WHXB201112303?fields=title",
    ),
    ("Wayback 存档", "https://archive.org/wayback/available?url=example.com"),
]


# ═══ v3.14 --grill 对抗审查:对已核验报告做「审稿人预演」 ═══

_GRILL_BY_VERDICT = {
    "verified": [
        "该文献在你核验之后是否可能被撤稿/更正？——投稿前用撤稿库复查一次（--refresh-cache 重跑）",
        "引用句声称的结论强度是否超过了该文献实际支持的范围？（机械层只证明来源存在且一致，"
        "「这句话是否被支撑」请对照原文逐句确认——必要时用 --check-document 做锚词核验）",
        "你引用的是这一篇，还是同刊同年的相似题名？核对卷期页与 DOI 是否逐字一致",
    ],
    "partial": [
        "降级原因（见注记/错误码）是否直接影响你引用的那句话？若只影响其他部分，"
        "在正文中明确标注保留意见范围",
        "能否找到一个更强的替代来源替换它？（partial 来源长期留在关键结论上是风险敞口）",
    ],
    "unreachable": [
        "报告附带的 Wayback 存档链里，存档内容与你声称的内容一致吗？打开对照过吗？",
        "更换网络（--cn/--proxy）重跑后仍不可达吗？——不可达连续两轮就该换信源",
    ],
    "invalid": [
        "标识符是否为一位之差的抄写错误？按标题在注册库检索过正确的 ID 吗？",
        "若为编造：溯源到正文哪一句产生的它？——同一句附近的其他引用需要连坐复查",
    ],
    "unverified": [
        "联网重跑的阻塞是什么？离线 partial 不能作为投稿依据（ADR-0003）",
    ],
}

_GRILL_LIST_LEVEL = [
    "清单画像/克隆对旗标（若有）逐条作答了吗？——旗标是审稿人第一眼会问的问题单",
    "CiteScore 与投稿结论基于本次核验时刻——距投稿超过一周建议 --refresh-cache 重跑一次",
    "「待人工复核」区的条目是否每条都有了结论（处理/替换/删除）？——带着未决条目投稿是最大风险",
]


def grill_report(results: list) -> list:
    """v3.14 对抗审查问题单（审稿人预演，纯模板零网络）：对已核验的每条引用
    生成「最强挑战问题」——逐条作答后报告才具备投稿说服力。只出问题不出
    判定（与 ADR-0005 同向：这是自查工具，不是二次审判）。返回
    [{index, verdict, title, questions}]。"""
    out = []
    for r in results:
        qs = list(
            _GRILL_BY_VERDICT.get(
                r.get("verdict"),
                [
                    "该条判定异常（非五态），请重跑确认",
                ],
            )
        )
        # v6.9.0 F70 reviewer 机制化：错误码驱动针对性问题（与 F63 注册表
        # 同源——每码的 grill 问题注册在 ERROR_CODE_META；旧码先过别名）。
        # 只追加问题不改判定（ADR-0005 同向）。
        codes = [_ERR_CODE_ALIAS.get(c, c)
                 for c in (r.get("error_codes") or derive_error_codes(r))]
        for c in codes:
            q = (ERROR_CODE_META.get(c) or {}).get("grill")
            if q and q not in qs:
                qs.append(q)
        note = str(r.get("note") or "")
        if "克隆引用对" in note:
            qs.append("该条处于克隆引用对中——与配对条目孰真孰假，元数据核验结论是什么？")
        if "正式发表" in note:
            qs.append("预印本升级提示处理了吗？引用是否已换成注记中的期刊版 DOI？")
        if "跨语言" in note:
            qs.append("跨语言桥接未命中/命中——登记原题与你的引文是同一篇吗？人工确认了吗？")
        out.append(
            {
                "index": r.get("index"),
                "verdict": r.get("verdict"),
                "title": str(r.get("title") or "")[:80],
                "questions": qs,
            }
        )
    return out


def render_grill_md(items: list, meta: dict) -> str:
    """v3.14 对抗审查问题单渲染（md）。meta 含 score/grade。"""
    n_q = sum(len(x["questions"]) for x in items)
    bluf = (
        "---\nverdict: 对抗审查问题单就绪——逐条作答后再投稿\n"
        f"key_numbers: {len(items)} 条引用 · {n_q} 个挑战问题 · 判定不变\n"
        "blocker: 无（问题单是自查工具）\n"
        "next_action: 按清单逐条作答，未决条目投稿前处理\n"
        f"cite_holmes_version: {_ROOT.VERSION}\n---"
    )
    lines = [
        bluf,
        "",
        "# 对抗审查问题单（审稿人预演）",
        f"- 生成：verify_refs.py v{_ROOT.VERSION} · 来源报告 CiteScore "
        f"{meta.get('score', '?')}/100（{meta.get('grade', '?')} 级）",
        "- 用法：逐条作答。答不上来的条目就是你投稿前要处理的事——问题单"
        "不改变任何判定（自查工具，非二次审判）。",
        "",
    ]
    cur = None
    for it in items:
        if it["verdict"] != cur:
            cur = it["verdict"]
            lines.append(f"## {_ROOT.VERDICT_ZH.get(cur, cur)}")
        lines.append(f"### #{it['index']} {it['title']}")
        for q in it["questions"]:
            lines.append(f"- [ ] {q}")
        lines.append("")
    lines += ["## 清单级追问", ""]
    for q in _GRILL_LIST_LEVEL:
        lines.append(f"- [ ] {q}")
    lines.append("")
    return "\n".join(lines)


# v3.12 --explain 错误码人话翻译表；v6.6.0 F63 起由 ERROR_CODE_META 派生
# （单一来源；旧码经别名映射兼容读取）
_ERR_CODE_ZH = {c: m["zh"] for c, m in ERROR_CODE_META.items()}


def explain_ref(r: dict) -> str:
    """v3.12 单条判定链人话解释（--explain N）：判定语义 → 依据步骤 →
    错误码翻译 → 注记要点 → 完整度 → 建议动作。纯静态，零网络；
    与 MCP explain_verdict 同源语义（本版为 CLI 超集：含错误码/克隆对/
    预印本/完整度等 v3.10+ 新信号）。"""
    v = r.get("verdict")
    base = {
        "verified": (
            "来源存在、处于权威层级、字段完整，且通过官方注册库交叉核验",
            "可支撑正文结论；引用时保留原始链接与判定时间",
        ),
        "partial": (
            "来源可达但存在降级因素（社区层级/字段缺失/元数据存疑/撤稿/语义否定）",
            "降级使用：正文引用注明保留意见，或先人工复核再升级",
        ),
        "unreachable": (
            "本次抓取失败（404/超时/反爬），不等于不存在",
            "先开报告附带的 Wayback 存档链对照；关键来源反复失败则更换信源",
        ),
        "invalid": (
            "标识符不存在、指向错误论文或拼接伪造——机械层确凿判死",
            "不得引用；从清单删除或更换信源",
        ),
        "unverified": ("未执行检查（离线模式或跳过）", "联网环境重跑以获得真实判定"),
    }.get(v)
    if base is None:
        return f"无法解释：未知判定 {v!r}"
    why, action = base
    lines = [f"== 第 {r.get('index')} 条：{str(r.get('title') or '')[:60]}", f"判定：{v} —— {why}"]
    steps = []
    c = r.get("checks") or {}
    dm = c.get("doi_metadata") or {}
    if dm.get("matched"):
        steps.append("DOI.org 注册元数据比对一致（标题/年份）")
    elif r.get("doi") and dm:
        steps.append("DOI.org 注册元数据未确认（获取失败或比对未通过）")
    if (c.get("arxiv_metadata") or {}).get("matched"):
        steps.append("arXiv 官方 API 元数据比对一致")
    if (c.get("s2") or {}).get("matched"):
        steps.append("Semantic Scholar 第三源交叉确认")
    if (c.get("retraction") or {}).get("retracted"):
        steps.append("⚠️ 撤稿库命中——见错误码")
    if (c.get("openalex") or {}).get("confirmed"):
        steps.append("OpenAlex 书目级存在性确认")
    u = c.get("url") or {}
    if u.get("reachable") is True:
        steps.append(f"来源页可达（HTTP {u.get('status')}）")
    if (c.get("wayback") or {}).get("archive_found"):
        steps.append("Wayback 存档对照可用")
    lines.append("依据：" + ("；".join(steps) if steps else "无可用检查记录（离线/跳过）"))
    codes = r.get("error_codes") or derive_error_codes(r)
    if codes:
        codes = [_ERR_CODE_ALIAS.get(x, x) for x in codes]  # 旧拼写码兼容
        zh = [_ERR_CODE_ZH.get(x, x) for x in codes]
        lines.append("错误码：" + "；".join(f"{x}（{z}）" for x, z in zip(codes, zh)))
    note = str(r.get("note") or "").strip()
    if note:
        lines.append("注记：" + (note[:300] + ("…" if len(note) > 300 else "")))
    comp = r.get("completeness")
    if isinstance(comp, dict) and comp.get("score") is not None:
        extra = f"（缺：{'、'.join(comp['missing'])}）" if comp.get("missing") else ""
        lines.append(f"导出完整度：{comp['score']}/100{extra}")
    lines.append(f"建议：{action}")
    return "\n".join(lines)


def run_doctor(net: bool = False, timeout: float = 6.0, cache_path: str = "") -> int:
    """v3.10 --doctor 环境自检：先做零外呼体检（版本/缓存目录/配置键/运行
    形态），--net 时加测各学术注册库连通性与延迟。三态 PASS/WARN/FAIL；
    FAIL 存在退出码 1（可入 CI 健康门）。doctor 只诊断不治疗——修复建议
    给到操作层，绝不静默改配置。"""
    checks = []  # (name, status, detail)
    checks.append(
        ("引擎版本", "PASS", f"verify_refs.py v{_ROOT.VERSION} · Python {sys.version.split()[0]}")
    )
    # 缓存目录可写（持久缓存 v1.12 的唯一落盘依赖；写失败会静默停用——doctor 把它显性化）
    cp = os.path.expanduser(cache_path or "~/.cache/cite-holmes/cache.sqlite3")
    try:
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        probe = cp + ".doctor_probe"
        with open(probe, "w") as f:
            f.write("ok")
        os.remove(probe)
        checks.append(("缓存目录", "PASS", os.path.dirname(cp)))
    except Exception as e:
        checks.append(
            (
                "缓存目录",
                "WARN",
                f"不可写（{type(e).__name__}）——持久缓存将静默停用，复跑会全量外呼",
            )
        )
    # 配置键状态（只报状态不改行为；键值绝不回显）
    env_keys = [
        ("OPENALEX_API_KEY", "OpenAlex（2026 起生产调用需 key，无 key 每日 100 credits）"),
        ("NCBI_API_KEY", "PubMed E-utilities（无 key 3 req/s 限速）"),
        ("S2_API_KEY", "Semantic Scholar（无 key 共享池限流）"),
        ("CITE_HOLMES_PROXY", "代理"),
        ("ALL_PROXY", "系统代理"),
    ]
    for env, desc in env_keys:
        v = os.environ.get(env)
        if v:
            checks.append(("配置键", "INFO", f"{env} 已设置（{desc}）"))
        else:
            checks.append(("配置键", "INFO", f"{env} 未设置——{desc}"))
    # 输出编码形态（Windows GBK 控制台历史故障面）
    enc = getattr(sys.stdout, "encoding", "") or ""
    checks.append(
        (
            "输出编码",
            "PASS" if enc.lower().replace("-", "") == "utf8" else "INFO",
            f"stdout={enc or '未知'}（非 UTF-8 控制台下特殊字符按 replace 降级显示）",
        )
    )
    if net:
        print("── 注册库连通性探针（--net）──")
        for name, url in _DOCTOR_PROBES:
            t0 = time.time()
            status, detail = "FAIL", ""
            try:
                req = urllib.request.Request(
                    url, headers={"User-Agent": f"cite-holmes/{_ROOT.VERSION}; +doctor"}
                )
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    code = resp.code
                ms = (time.time() - t0) * 1000
                if code == 200:
                    status = "PASS" if ms <= 2000 else "WARN"
                    detail = f"HTTP 200 · {ms:.0f}ms" + ("" if ms <= 2000 else "（慢>2s）")
                else:
                    status, detail = "WARN", f"HTTP {code} · {ms:.0f}ms"
            except urllib.error.HTTPError as e:
                ms = (time.time() - t0) * 1000
                if e.code in (403, 429):
                    status, detail = "WARN", f"HTTP {e.code}（可达但限流/需 key）· {ms:.0f}ms"
                else:
                    status, detail = "WARN", f"HTTP {e.code} · {ms:.0f}ms"
            except Exception as e:
                detail = f"{type(e).__name__}（不可达/超时 {timeout}s）——该源核验将走降级路径"
            checks.append((f"探针·{name}", status, detail))
    n_fail = sum(1 for _, s, _ in checks if s == "FAIL")
    n_warn = sum(1 for _, s, _ in checks if s == "WARN")
    print("== cite-holmes doctor ==")
    for name, s, detail in checks:
        mark = {"PASS": "✅", "WARN": "⚠️ ", "INFO": "ℹ️ ", "FAIL": "❌"}[s]
        print(f"  {mark} [{s:4s}] {name}: {detail}")
    if n_fail:
        print(f"verdict: FAIL（{n_fail} 项 FAIL / {n_warn} 项 WARN）——先修复 FAIL 再跑批")
    elif n_warn:
        print(f"verdict: usable with caveats（{n_warn} 项 WARN）——可跑批，注意降级提示")
    else:
        print("verdict: all clear——环境就绪，可直接跑批")
    if net:  # v5.0.0 国内直连建议（评测 domestic 弱项定向：可达源统计+决策提示）
        _pc = [s for n, s, _ in checks if n.startswith("探针·")]
        if _pc:
            _ok = sum(1 for s in _pc if s == "PASS")
            if _ok == len(_pc):
                _adv = "全部注册库直连可达——无需代理，直接跑批"
            elif _ok >= 2:
                _adv = (
                    f"{_ok}/{len(_pc)} 源直连可用——DOI/PubMed 主通路在列时小批量可直连；"
                    "完整覆盖建议 --proxy，或 --cn（超时抬升 + DOI.org 三败自动回源 Crossref）"
                )
            else:
                _adv = (
                    "直连可用源不足——建议配置 --proxy（或 HTTPS_PROXY 环境变量）后重跑本自检；"
                    "探针明细显示「可达但限流/需 key」时优先配 S2_API_KEY/OPENALEX_API_KEY"
                    "（代理解不了缺 key）；磁盘缓存 7 天 TTL，重跑只补漏不重复付费"
                )
            print("── 国内直连建议 ──")
            print(f"  {_adv}")
    return 1 if n_fail else 0
