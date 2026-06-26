"""
A/B 测试显著性分析 - data-auto-analyzer 模式 C
比例型：Z 检验（两比例差异）；均值型：Welch's T 检验（独立样本）
浅色主题 · 卡片阴影 · 可折叠。用法见 references/ab_test_guide.md
"""
import sys
import os
import argparse
import math
import warnings
warnings.filterwarnings("ignore")

import numpy as np
from scipy import stats as sp_stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (load_file, to_numeric_safe, resolve_output_path,
                     render_page, json_dumps, html_escape)


# ───────────── 比例型 Z 检验 ─────────────
def z_test_proportions(a_success, a_total, b_success, b_total, alpha=0.05):
    p1 = a_success / a_total if a_total > 0 else 0
    p2 = b_success / b_total if b_total > 0 else 0
    p_pool = (a_success + b_success) / (a_total + b_total) if (a_total + b_total) > 0 else 0
    se_pool = math.sqrt(p_pool * (1 - p_pool) * (1/a_total + 1/b_total)) if a_total > 0 and b_total > 0 else 0
    se_unpool = math.sqrt(p1*(1-p1)/a_total + p2*(1-p2)/b_total) if a_total > 0 and b_total > 0 else 0
    if se_pool == 0:
        z, p_value = 0, 1.0
    else:
        z = (p2 - p1) / se_pool
        p_value = 2 * (1 - sp_stats.norm.cdf(abs(z)))
    diff = p2 - p1
    z_crit = sp_stats.norm.ppf(1 - alpha/2)
    ci_lower, ci_upper = diff - z_crit * se_unpool, diff + z_crit * se_unpool
    significant = p_value < alpha
    if p_value < 0.01:
        confidence, confidence_level = "极显著", 99
    elif p_value < 0.05:
        confidence, confidence_level = "显著", 95
    elif p_value < 0.1:
        confidence, confidence_level = "边缘显著", 90
    else:
        confidence, confidence_level = "不显著", None
    effect_size = abs(p2 - p1) if abs(p2 - p1) > 0 else 0.01
    required_n_per_group = math.ceil((2 * (sp_stats.norm.ppf(0.975) + sp_stats.norm.ppf(0.80))**2
                                       * p_pool * (1 - p_pool)) / (effect_size**2)) if effect_size > 0 else None
    return {
        "type": "rate",
        "a_success": a_success, "a_total": a_total, "a_rate": p1,
        "b_success": b_success, "b_total": b_total, "b_rate": p2,
        "diff": diff, "relative_lift": (p2 - p1) / p1 * 100 if p1 > 0 else 0,
        "z": z, "p_value": p_value, "ci_lower": ci_lower, "ci_upper": ci_upper,
        "significant": significant, "confidence": confidence, "confidence_level": confidence_level,
        "required_n_per_group": required_n_per_group, "winner": "B" if p2 > p1 else ("A" if p2 < p1 else "tie"),
    }


# ───────────── 均值型 T 检验 ─────────────
def t_test_means(a_values, b_values, alpha=0.05):
    a_values = np.array(a_values, dtype=float); a_values = a_values[~np.isnan(a_values)]
    b_values = np.array(b_values, dtype=float); b_values = b_values[~np.isnan(b_values)]
    if len(a_values) < 2 or len(b_values) < 2:
        return {"error": "每组至少需要 2 个有效样本"}
    t_stat, p_value = sp_stats.ttest_ind(a_values, b_values, equal_var=False)
    m1, m2 = a_values.mean(), b_values.mean()
    s1, s2 = a_values.std(ddof=1), b_values.std(ddof=1)
    n1, n2 = len(a_values), len(b_values)
    df_w = (s1**2/n1 + s2**2/n2)**2 / ((s1**2/n1)**2/(n1-1) + (s2**2/n2)**2/(n2-1)) if (n1 > 1 and n2 > 1) else 1
    se_diff = math.sqrt(s1**2/n1 + s2**2/n2)
    t_crit = sp_stats.t.ppf(1 - alpha/2, df_w)
    diff = m2 - m1
    ci_lower, ci_upper = diff - t_crit * se_diff, diff + t_crit * se_diff
    if p_value < 0.01:
        confidence, level = "极显著", 99
    elif p_value < 0.05:
        confidence, level = "显著", 95
    elif p_value < 0.1:
        confidence, level = "边缘显著", 90
    else:
        confidence, level = "不显著", None
    return {
        "type": "mean",
        "a_n": int(n1), "a_mean": float(m1), "a_std": float(s1),
        "b_n": int(n2), "b_mean": float(m2), "b_std": float(s2),
        "diff": float(diff), "relative_lift": (m2 - m1) / m1 * 100 if m1 != 0 else 0,
        "t": float(t_stat), "p_value": float(p_value),
        "ci_lower": float(ci_lower), "ci_upper": float(ci_upper),
        "significant": p_value < alpha, "confidence": confidence, "confidence_level": level,
        "winner": "B" if m2 > m1 else ("A" if m2 < m1 else "tie"),
    }


def generate_conclusion(result, a_name="A", b_name="B", metric_name="指标", higher_is_better=True):
    if "error" in result:
        return result["error"]
    if result["type"] == "rate":
        lift = result["relative_lift"]; winner = result["winner"]
        if not result["significant"]:
            return f"两组 {metric_name} 无显著差异（p={result['p_value']:.4f}），不能证明哪个版本更好。建议扩大样本继续观察。"
        if winner == "B":
            winner_name, loser_name = b_name, a_name
        else:
            winner_name, loser_name = a_name, b_name; lift = -lift
        level_txt = f"置信度 {result['confidence_level']}%"
        return f"【{winner_name}】优于【{loser_name}】：{metric_name}相对提升 {abs(lift):.2f}%，差异{result['confidence']}（{level_txt}），建议采用【{winner_name}】。"
    else:
        if not result["significant"]:
            return f"两组 {metric_name} 均值无显著差异（p={result['p_value']:.4f}），建议扩大样本继续观察。"
        winner = result["winner"]
        winner_mean = result["b_mean"] if winner == "B" else result["a_mean"]
        loser_mean = result["a_mean"] if winner == "B" else result["b_mean"]
        winner_name = b_name if winner == "B" else a_name
        loser_name = a_name if winner == "B" else b_name
        if higher_is_better:
            action = f"建议采用【{winner_name}】"
        else:
            winner_name, loser_name = loser_name, winner_name
            winner_mean, loser_mean = loser_mean, winner_mean
            action = f"建议采用【{winner_name}】（成本更低）"
        level_txt = f"置信度 {result['confidence_level']}%"
        return f"【{winner_name}】（均值 {winner_mean:.4f}）优于【{loser_name}】（均值 {loser_mean:.4f}），差异{result['confidence']}（{level_txt}），{action}。"


def build_html(result, a_name, b_name, metric_name, higher_is_better):
    conclusion = generate_conclusion(result, a_name, b_name, metric_name, higher_is_better)
    is_rate = result.get("type") == "rate"
    sig = result.get("significant")

    concl_html = f'<div class="info-box {"green" if sig else "yellow"}" style="font-size:1rem">{"✅" if sig else "⚠️"} {html_escape(conclusion)}</div>'

    def card(label, val, sub=""):
        return f'<div class="card"><div class="label">{html_escape(label)}</div><div class="value">{val}</div><div class="sub">{html_escape(sub)}</div></div>'

    winner = result.get("winner")
    wname = a_name if winner == "A" else (b_name if winner == "B" else "持平")
    cards = card("p 值", f'{result["p_value"]:.4f}', "p<0.05 视为显著")
    cards += card("显著性", result["confidence"], f'置信度 {result["confidence_level"]}%' if result.get("confidence_level") else "未达显著")
    cards += card("胜出方", str(wname), f'相对提升 {result.get("relative_lift", 0):.2f}%' if winner != "tie" else "")
    cards += card("差异 95% CI", f'[{result["ci_lower"]:.4f}, {result["ci_upper"]:.4f}]', "不含 0 即显著")
    overview = f'<div class="cards">{cards}</div>'

    if is_rate:
        a_val, b_val = f'{result["a_rate"]*100:.3f}%', f'{result["b_rate"]*100:.3f}%'
        a_sub = f'{result["a_success"]:.0f} / {result["a_total"]:.0f}'
        b_sub = f'{result["b_success"]:.0f} / {result["b_total"]:.0f}'
        av, bv, unit = result["a_rate"]*100, result["b_rate"]*100, "%"
    else:
        a_val, b_val = f'{result["a_mean"]:.4f}', f'{result["b_mean"]:.4f}'
        a_sub = f'n={result["a_n"]} · σ={result["a_std"]:.4f}'
        b_sub = f'n={result["b_n"]} · σ={result["b_std"]:.4f}'
        av, bv, unit = result["a_mean"], result["b_mean"], ""
    cmp_html = (f'<div class="cards">{card("【"+a_name+"】"+metric_name, a_val, a_sub)}'
                f'{card("【"+b_name+"】"+metric_name, b_val, b_sub)}</div>'
                f'<div class="chart-card" style="margin-top:16px"><div class="chart-box" id="c-ab" style="height:340px"></div></div>')

    if is_rate:
        rows = [("A 比例", f'{result["a_rate"]*100:.4f}%'), ("B 比例", f'{result["b_rate"]*100:.4f}%'),
                ("绝对差异", f'{result["diff"]*100:.4f} pp'), ("相对提升", f'{result["relative_lift"]:.2f}%'),
                ("Z 统计量", f'{result["z"]:.4f}'), ("p 值", f'{result["p_value"]:.6f}'),
                ("差异 95% CI", f'[{result["ci_lower"]:.4f}, {result["ci_upper"]:.4f}]'),
                ("达 95% 置信所需样本/组", str(result.get("required_n_per_group") or "—"))]
    else:
        rows = [("A 均值", f'{result["a_mean"]:.4f}'), ("B 均值", f'{result["b_mean"]:.4f}'),
                ("绝对差异", f'{result["diff"]:.4f}'), ("相对提升", f'{result["relative_lift"]:.2f}%'),
                ("t 统计量", f'{result["t"]:.4f}'), ("p 值", f'{result["p_value"]:.6f}'),
                ("差异 95% CI", f'[{result["ci_lower"]:.4f}, {result["ci_upper"]:.4f}]'),
                ("A 样本数", str(result["a_n"])), ("B 样本数", str(result["b_n"]))]
    tbl = ('<div class="table-wrap"><div class="table-container"><table class="dt"><tbody>'
           + ''.join(f'<tr><td style="color:var(--text-secondary)">{html_escape(k)}</td><td class="num">{html_escape(v)}</td></tr>' for k, v in rows)
           + '</tbody></table></div></div>')

    test_type = "比例型（Z 检验）" if is_rate else "均值型（Welch's T 检验）"
    sections = [
        {"id": "sec-cc", "nav": "结论", "title": "结论", "html": concl_html},
        {"id": "sec-ov", "nav": "关键", "title": "关键结果", "html": overview},
        {"id": "sec-ab", "nav": "对比", "title": "A/B 对比", "html": cmp_html},
        {"id": "sec-st", "nav": "明细", "title": "统计明细", "html": tbl},
    ]
    chart = "const AB=" + json_dumps({"a": a_name, "b": b_name, "av": av, "bv": bv, "unit": unit, "metric": metric_name}) + ";" + r"""
const EC={text:'#5a6478',axis:'#e3e7ef',split:'#eef1f6'};
const ch=echarts.init(document.getElementById('c-ab'));window.__charts.push(ch);
ch.setOption({backgroundColor:'transparent',tooltip:{trigger:'axis',backgroundColor:'#fff',borderColor:'#e9ecf2',textStyle:{color:'#1d2433'}},
 grid:{top:30,bottom:40,left:64,right:20},
 xAxis:{type:'category',data:[AB.a,AB.b],axisLabel:{color:EC.text},axisLine:{lineStyle:{color:EC.axis}}},
 yAxis:{type:'value',name:AB.metric+(AB.unit?'('+AB.unit+')':''),nameTextStyle:{color:EC.text},axisLabel:{color:EC.text},splitLine:{lineStyle:{color:EC.split}}},
 series:[{type:'bar',barMaxWidth:90,data:[{value:+AB.av.toFixed(4),itemStyle:{color:'#3b6cff',borderRadius:[6,6,0,0]}},{value:+AB.bv.toFixed(4),itemStyle:{color:'#10b981',borderRadius:[6,6,0,0]}}],label:{show:true,position:'top',color:EC.text,formatter:p=>p.value+AB.unit}}]});
"""
    return render_page("A/B 测试报告", f"{metric_name} · {test_type}", sections, chart)


def main():
    parser = argparse.ArgumentParser(description="A/B 测试分析 模式 C")
    parser.add_argument("--inline", action="store_true", help="使用命令行参数直接输入数据")
    parser.add_argument("--file", help="Excel/CSV 文件路径")
    parser.add_argument("--a-success", type=float, help="A 组成功数")
    parser.add_argument("--a-total", type=float, help="A 组总数")
    parser.add_argument("--b-success", type=float, help="B 组成功数")
    parser.add_argument("--b-total", type=float, help="B 组总数")
    parser.add_argument("--group-col", help="分组列名")
    parser.add_argument("--metric-col", help="指标列名（均值型）")
    parser.add_argument("--success-col", help="成功次数列（比例型）")
    parser.add_argument("--total-col", help="总次数列（比例型）")
    parser.add_argument("--metric-type", choices=["rate", "mean"], help="指标类型：rate=比例, mean=均值")
    parser.add_argument("--a-name", default="A")
    parser.add_argument("--b-name", default="B")
    parser.add_argument("--metric-name", default="指标")
    parser.add_argument("--lower-is-better", action="store_true", help="指标越低越好（CPA/CPC 等成本指标）")
    parser.add_argument("--out", default="ab_result.html")
    args = parser.parse_args()
    higher_is_better = not args.lower_is_better

    if args.inline:
        if None in (args.a_success, args.a_total, args.b_success, args.b_total):
            print("❌ inline 模式需要 --a-success --a-total --b-success --b-total"); sys.exit(1)
        result = z_test_proportions(args.a_success, args.a_total, args.b_success, args.b_total)
        metric_name = args.metric_name if args.metric_name != "指标" else "转化率"
        print(f"\nA 组: {args.a_success}/{args.a_total} = {result['a_rate']*100:.3f}%")
        print(f"B 组: {args.b_success}/{args.b_total} = {result['b_rate']*100:.3f}%")
    elif args.file:
        if not os.path.exists(args.file):
            print(f"❌ 文件不存在: {args.file}"); sys.exit(1)
        df = load_file(args.file)
        if args.metric_type is None:
            print("❌ 从文件读取时必须指定 --metric-type (rate 或 mean)"); sys.exit(1)
        if args.metric_type == "rate":
            if not (args.group_col and args.success_col and args.total_col):
                print("❌ rate 模式需要 --group-col --success-col --total-col"); sys.exit(1)
            grouped = df.groupby(args.group_col).agg({args.success_col: "sum", args.total_col: "sum"})
            if len(grouped) != 2:
                print(f"❌ 分组列需要正好两组，当前: {list(grouped.index)}"); sys.exit(1)
            groups = list(grouped.index)
            result = z_test_proportions(
                float(grouped.loc[groups[0], args.success_col]), float(grouped.loc[groups[0], args.total_col]),
                float(grouped.loc[groups[1], args.success_col]), float(grouped.loc[groups[1], args.total_col]))
            args.a_name = str(groups[0]) if args.a_name == "A" else args.a_name
            args.b_name = str(groups[1]) if args.b_name == "B" else args.b_name
            metric_name = args.metric_name if args.metric_name != "指标" else args.success_col + " / " + args.total_col
        else:
            if not (args.group_col and args.metric_col):
                print("❌ mean 模式需要 --group-col --metric-col"); sys.exit(1)
            df[args.metric_col] = to_numeric_safe(df[args.metric_col])
            groups = df[args.group_col].dropna().unique()
            if len(groups) != 2:
                print(f"❌ 分组列需要正好两组，当前: {list(groups)}"); sys.exit(1)
            a_vals = df[df[args.group_col] == groups[0]][args.metric_col].dropna().values
            b_vals = df[df[args.group_col] == groups[1]][args.metric_col].dropna().values
            result = t_test_means(a_vals, b_vals)
            args.a_name = str(groups[0]) if args.a_name == "A" else args.a_name
            args.b_name = str(groups[1]) if args.b_name == "B" else args.b_name
            metric_name = args.metric_name if args.metric_name != "指标" else args.metric_col
    else:
        print("❌ 需要指定 --inline 或 --file"); sys.exit(1)

    if "error" in result:
        print(f"❌ {result['error']}"); sys.exit(1)

    print(f"\np 值: {result['p_value']:.6f}\n显著性: {result['confidence']}")
    print(f"结论: {generate_conclusion(result, args.a_name, args.b_name, metric_name, higher_is_better)}")

    html = build_html(result, args.a_name, args.b_name, metric_name, higher_is_better)
    out_path = resolve_output_path(args.out)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n✅ A/B 测试报告已生成（浅色主题）: {out_path}")


if __name__ == "__main__":
    main()
