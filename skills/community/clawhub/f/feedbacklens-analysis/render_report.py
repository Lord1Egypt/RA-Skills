#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FeedbackLens 报告渲染器（feedbacklens-analysis 技能内置）

把「评估结果 JSON」渲染成 HTML 报告。纯标准库，无第三方依赖，跨平台可用。

用法：
  # 1) 演示：读内置 demo_evaluation.json，一键出报告
  python render_report.py --demo --out demo-report.html

  # 2) 正式分析：读你自己的评估 JSON
  python render_report.py --evaluation evaluations/2026-09-16-my.json --out evaluations/2026-09-16-my.html

  # 3) 自定义模板（默认用同目录 report_template.html）
  python render_report.py --demo --template my_tpl.html --out out.html

设计原则：
- 只做「数据 → HTML」的机械渲染，不做任何分析判断。
- 对缺失字段自动降级补齐（见 _normalize），保证 JSON 不全也能出报告。
- 输出的 HTML 中不允许残留未替换的 {{占位符}}（脚本会自检并报错）。
"""

import argparse
import datetime
import html
import io
import json
import os
import sys

LEVEL_CLS = {"高": "high", "中": "mid", "低": "low"}
LEVEL_RANK = {"高": 3, "中": 2, "低": 1}


# ---------------------------------------------------------------- 数值工具
def _round(x):
    """标准四舍五入（Python 内置 round 是银行家舍入，不适合分值）。"""
    return int(x + 0.5) if x >= 0 else -int(-x + 0.5)


def _num(d, key, default=0):
    v = d.get(key, default)
    try:
        return float(v)
    except (TypeError, ValueError):
        return float(default)


# ---------------------------------------------------------------- 字段补齐
def _normalize(data):
    """补齐可推导字段，保证渲染不因字段缺失而失败。"""
    clusters = data.get("clusters") or []
    for c in clusters:
        freq = _num(c, "frequency_score")
        sev = _num(c, "severity_score")
        imp = _num(c, "impact_scope_score")
        c["frequency_score"] = _round(freq)
        c["severity_score"] = _round(sev)
        c["impact_scope_score"] = _round(imp)

        # 优先级分：缺失则按公式复算
        if "priority_score" not in c or c.get("priority_score") is None:
            c["priority_score"] = _round(freq * 0.3 + sev * 0.5 + imp * 0.2)
        else:
            c["priority_score"] = _round(_num(c, "priority_score"))

        # 优先级档：缺失则按分数推导 + 轻微兜底规则（严重性<40 强制低）
        if not c.get("priority_level"):
            if sev < 40:
                c["priority_level"] = "低"
            else:
                s = c["priority_score"]
                c["priority_level"] = "高" if s >= 70 else ("中" if s >= 40 else "低")
        if c["priority_level"] not in LEVEL_CLS:
            c["priority_level"] = "低"

        # 计分说明：缺失则自动生成
        if not c.get("priority_reason"):
            base = "频次 %d×0.3 + 严重性 %d×0.5 + 影响面 %d×0.2 = %d" % (
                c["frequency_score"], c["severity_score"],
                c["impact_scope_score"], c["priority_score"])
            if sev < 40 and c["priority_level"] == "低":
                c["priority_reason"] = base + "，且严重性 %d < 40 触发轻微兜底规则 → 低" % c["severity_score"]
            else:
                c["priority_reason"] = base + " → " + c["priority_level"]

        c["count"] = int(_num(c, "count", 0))
        c.setdefault("keywords", [])
        c.setdefault("quote", "")
        c.setdefault("description", "")
        c.setdefault("summary", "")

    # 建议：ROI / quick win 缺失则推导
    for g in (data.get("suggestions") or []):
        impact = _num(g, "impact_score")
        effort = _num(g, "effort_score")
        if "roi" not in g or g.get("roi") is None:
            g["roi"] = round(impact / effort, 2) if effort else 0.0
        else:
            g["roi"] = round(float(g["roi"]), 2)
        if g.get("is_quick_win") is None:
            g["is_quick_win"] = bool(g["roi"] >= 2 and effort <= 40)
        g.setdefault("what", "")
        g.setdefault("why", "")
        g.setdefault("how", "")
        g.setdefault("cluster", "")
        g["impact_score"] = _round(impact)
        g["effort_score"] = _round(effort)

    # 排序：簇按优先级降序（同级按档位），建议按 ROI 降序
    clusters.sort(key=lambda c: (-c["priority_score"], -LEVEL_RANK.get(c["priority_level"], 0)))
    (data.get("suggestions") or []).sort(key=lambda g: -g["roi"])
    return data


# ---------------------------------------------------------------- 渲染
def render(data, template_path, today=None):
    data = _normalize(data)
    tpl = io.open(template_path, encoding="utf-8").read()

    is_demo = bool(data.get("is_demo"))
    date = (today or datetime.date.today().isoformat())
    if not is_demo:
        date = data.get("date") or (str(data.get("timestamp", ""))[:10]) or date

    # ---- 条形图 ----
    bars = []
    for c in data["clusters"]:
        cls = LEVEL_CLS[c["priority_level"]]
        subs = ('<span>频次分 <b>%d</b></span><span>严重性分 <b>%d</b></span>'
                '<span>影响面分 <b>%d</b></span><span>反馈 <b>%d</b> 条</span>'
                % (c["frequency_score"], c["severity_score"], c["impact_scope_score"], c["count"]))
        bars.append(
            '<div class="bar-row">\n'
            '      <div class="top"><span class="label">%s</span>'
            '<span class="score %s">%d <span style="font-size:12px;font-weight:600;">· %s</span></span></div>\n'
            '      <div class="bar-track"><div class="bar-fill %s" data-w="%d"></div></div>\n'
            '      <div class="subs">%s</div>\n'
            '    </div>' % (html.escape(str(c["label"])), cls, c["priority_score"],
                            c["priority_level"], cls, c["priority_score"], subs))

    # ---- 聚类明细卡 ----
    cards = []
    for c in data["clusters"]:
        cls = LEVEL_CLS[c["priority_level"]]
        kws = "".join('<span class="kw">%s</span>' % html.escape(str(k)) for k in c.get("keywords", []))
        s = c.get("sentiment") or {}
        sent = ""
        if s:
            sent = ('<span>负面 <b>%d</b> / 中性 <b>%d</b> / 正面 <b>%d</b></span>'
                    % (int(_num(s, "negative")), int(_num(s, "neutral")), int(_num(s, "positive"))))
        cards.append(
            '<div class="cluster-card">\n'
            '    <div class="cluster-head"><span class="name">%s</span>'
            '<span class="badge %s">优先级 %d · %s</span></div>\n'
            '    <div style="font-size:13px;color:#6E6C64;margin-top:6px;">%s</div>\n'
            '    <div class="kws">%s</div>\n'
            '    <div class="quote">%s</div>\n'
            '    <div class="subs-grid"><span>频次分 <b>%d</b></span><span>严重性分 <b>%d</b></span>'
            '<span>影响面分 <b>%d</b></span><span>反馈 <b>%d</b> 条</span>%s</div>\n'
            '    <div style="margin-top:10px;font-size:12.5px;color:#4A4957;background:#F4F2FB;'
            'border-left:3px solid #4A3FBF;padding:8px 12px;border-radius:0 8px 8px 0;">'
            '<b>计分：</b>%s</div>\n'
            '    <div style="margin-top:8px;font-size:13px;color:#33323E;line-height:1.65;">%s</div>\n'
            '  </div>' % (html.escape(str(c["label"])), cls, c["priority_score"], c["priority_level"],
                           html.escape(str(c.get("description", ""))), kws,
                           html.escape(str(c.get("quote", ""))),
                           c["frequency_score"], c["severity_score"], c["impact_scope_score"],
                           c["count"], sent, html.escape(str(c["priority_reason"])),
                           html.escape(str(c.get("summary", "")))))

    # ---- 建议卡（已按 ROI 降序） ----
    sugs = []
    for i, g in enumerate(data.get("suggestions") or []):
        rk = ["r1", "r2", "r3"][i] if i < 3 else "rx"
        qw = '<span class="quickwin">⚡ 快速见效</span>' if g["is_quick_win"] else ""
        sugs.append(
            '<div class="sug-card">\n'
            '    <div class="sug-head"><span class="sug-rank %s">%d</span>'
            '<span class="ttl">%s</span>%s'
            '<span class="roi-tag">ROI %.2f</span></div>\n'
            '    <div class="sug-body">\n'
            '      <div><span class="lbl">改什么：</span>%s</div>\n'
            '      <div style="margin-top:6px;"><span class="lbl">为什么：</span>%s</div>\n'
            '      <div class="sug-how"><span class="lbl">怎么做：</span>%s</div>\n'
            '      <div style="margin-top:8px;font-size:12px;color:#6E6C64;">'
            '影响分 %d · 成本分 %d · 对应簇：%s</div>\n'
            '    </div>\n  </div>' % (rk, i + 1, html.escape(str(g.get("suggestion", ""))), qw, g["roi"],
                                    html.escape(str(g["what"])), html.escape(str(g["why"])),
                                    html.escape(str(g["how"])),
                                    g["impact_score"], g["effort_score"],
                                    html.escape(str(g["cluster"]))))

    out = (tpl.replace("{{TITLE}}", html.escape(str(data.get("title", "用户反馈分析报告"))))
              .replace("{{CONCLUSION}}", html.escape(str(data.get("overall_conclusion", ""))))
              .replace("{{INDUSTRY}}", html.escape(str(data.get("industry", "通用"))))
              .replace("{{TOTAL_COUNT}}", str(data.get("total_count", 0)))
              .replace("{{SOURCE_TYPE}}", html.escape(str(data.get("source_type", "通用"))))
              .replace("{{DATE}}", html.escape(date))
              .replace("{{BAR_ROWS}}", "\n    ".join(bars))
              .replace("{{CLUSTER_CARDS}}", "\n    ".join(cards))
              .replace("{{SUG_CARDS}}", "\n    ".join(sugs))
              # 报告 CTA 的 UTM：区分「看了演示」与「真跑了数据」两类来客
              .replace("{{UTM_CONTENT}}", "demo" if is_demo else "real_report"))

    # 信息缺失时兜底：结论为空则用最高优先级簇生成一句
    if not str(data.get("overall_conclusion", "")).strip() and data["clusters"]:
        top = data["clusters"][0]
        out = out.replace('<div class="conclusion"></div>',
                          '<div class="conclusion">最高优先级问题：%s（优先级分 %d · %s），%d 条反馈指向该问题。</div>'
                          % (html.escape(str(top["label"])), top["priority_score"],
                             top["priority_level"], top["count"]))

    # ---------------- 演示模式标识 ----------------
    if is_demo:
        n = data.get("total_count", 0)
        out = out.replace(
            '<span class="chip">来源：%s</span>' % html.escape(str(data.get("source_type", "通用"))),
            '<span class="chip">来源：%s</span>\n      '
            '<span class="chip" style="background:rgba(215,56,62,0.20);border-color:rgba(215,56,62,0.40);'
            'color:#FFD9DA;font-weight:650;">⚠ 示例数据 · 内置 %d 条样例</span>'
            % (html.escape(str(data.get("source_type", "通用"))), n))
        out = out.replace(
            '<div class="note">AI 生成的反馈分析结果，建议结合业务上下文人工复核</div>',
            '<div class="note">本页为<b>内置样例数据（%d 条）</b>的演示结果，非真实用户反馈；'
            'AI 生成的分析结论，建议结合业务上下文人工复核。</div>\n  '
            '<div class="note" style="margin-top:10px;color:#B02A30;font-weight:650;font-size:13px;">'
            '这是内置样例数据的结果。把你的真实反馈（粘贴文本 / CSV / Excel）给我，用同一套算法跑一遍 '
            '—— 免费、不限次数。</div>' % n)

    if "{{" in out:
        i = out.index("{{")
        raise ValueError("模板存在未替换占位符：%s" % out[i:i + 40])
    return out, data


# ---------------------------------------------------------------- CLI
def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    skill_dir = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="FeedbackLens 报告渲染器：评估 JSON → HTML 报告")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--demo", action="store_true", help="使用内置演示样例（demo_evaluation.json）")
    src.add_argument("--evaluation", help="评估结果 JSON 路径")
    ap.add_argument("--out", required=True, help="输出 HTML 路径")
    ap.add_argument("--template", default=os.path.join(skill_dir, "report_template.html"),
                    help="报告模板路径（默认用技能目录下的 report_template.html）")
    args = ap.parse_args()

    if args.demo:
        jp = os.path.join(skill_dir, "demo_evaluation.json")
    else:
        jp = args.evaluation
    if not os.path.exists(jp):
        sys.exit("找不到评估 JSON：%s" % jp)
    if not os.path.exists(args.template):
        sys.exit("找不到模板：%s" % args.template)

    data = json.load(io.open(jp, encoding="utf-8"))
    out_html, norm = render(data, args.template)

    od = os.path.dirname(os.path.abspath(args.out))
    if od and not os.path.isdir(od):
        os.makedirs(od)
    io.open(args.out, "w", encoding="utf-8").write(out_html)

    lv = {}
    for c in norm["clusters"]:
        lv[c["priority_level"]] = lv.get(c["priority_level"], 0) + 1
    print("报告已生成：%s" % args.out)
    print("  簇 %d 个（高 %d / 中 %d / 低 %d）｜建议 %d 条｜%d 字符"
          % (len(norm["clusters"]), lv.get("高", 0), lv.get("中", 0), lv.get("低", 0),
             len(norm.get("suggestions") or []), len(out_html)))
    print("  占位符自检：全部替换完成")
    if norm.get("is_demo"):
        print("  模式：演示（已自动加示例数据标识与转化引导）")


if __name__ == "__main__":
    main()
