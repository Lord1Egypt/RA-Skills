#!/usr/bin/env python3
"""
plan_generator.py — 志愿方案生成器

将分类结果渲染为HTML报告。支持省份规则、梯度可视化、风险提示。

用法:
  python plan_generator.py --profile user_profile.json \
    --classified classified.json --province-rules province_rules.json \
    --template assets/report_template.html --output gaokao_plan_2026.html
"""

import json
import argparse
from pathlib import Path
from datetime import datetime


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_province_rule(rules: dict, province: str) -> dict:
    """获取省份填报规则"""
    return rules.get(province.lower(), rules.get(province, {}))


def build_risk_distribution_html(strategy: dict) -> str:
    """生成冲稳保分布的HTML"""
    reach = strategy["reach_count"]
    match_c = strategy["match_count"]
    safety = strategy["safety_count"]
    total = reach + match_c + safety

    if total == 0:
        return ""

    reach_pct = reach / total * 100
    match_pct = match_c / total * 100
    safety_pct = safety / total * 100

    return f"""
    <div class="distribution-bar">
      <div class="bar-segment bar-reach" style="width:{reach_pct}%">
        <span>{'🚀' if reach_pct > 5 else ''}冲 {reach}个 ({reach_pct:.0f}%)</span>
      </div>
      <div class="bar-segment bar-match" style="width:{match_pct}%">
        <span>{'✅' if match_pct > 10 else ''}稳 {match_c}个 ({match_pct:.0f}%)</span>
      </div>
      <div class="bar-segment bar-safety" style="width:{safety_pct}%">
        <span>{'🛡️' if safety_pct > 10 else ''}保 {safety}个 ({safety_pct:.0f}%)</span>
      </div>
    </div>
    """


def build_plan_table_html(plan: list[dict], risk_filter: str = None) -> str:
    """生成志愿表格HTML"""
    rows = []
    for item in plan:
        if risk_filter and item.get("risk_level") != risk_filter:
            continue

        rank = item.get("volunteer_rank", "-")
        uni = item.get("university_name", "-")
        group = item.get("major_group_name", "-")
        prob = item.get("admission_probability", 0)
        risk = item.get("risk_level", "-")
        hist_ranks = item.get("hist_min_ranks", [])
        majs = ", ".join(item.get("majors_in_group", [])) or "-"
        note = item.get("note", "")

        prob_text = f"{prob * 100:.0f}%"
        prob_class = "prob-high" if prob >= 0.8 else ("prob-mid" if prob >= 0.5 else "prob-low")
        risk_icon = {"冲": "🚀", "稳": "✅", "保": "🛡️"}.get(risk, "")

        hist_text = str(hist_ranks[-1]) if hist_ranks else "-"

        rows.append(f"""
        <tr class="risk-{risk}">
          <td class="col-rank">{rank}</td>
          <td class="col-school">{uni}</td>
          <td class="col-group">{group}</td>
          <td class="col-majors">{majs}</td>
          <td class="col-hist">{hist_text}</td>
          <td class="col-prob"><span class="{prob_class}">{prob_text}</span></td>
          <td class="col-risk">{risk_icon} {risk}</td>
          <td class="col-note">{note}</td>
        </tr>
        """)

    return "\n".join(rows)


def build_report_html(profile: dict, classified: dict, province_rule: dict,
                      template_path: str = None) -> str:
    """生成完整HTML报告"""
    strategy = classified.get("strategy", {})
    plan = classified.get("plan", [])
    warnings = classified.get("warnings", [])
    total = classified.get("total_volunteers", 0)

    # 读模板
    if template_path and Path(template_path).exists():
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    else:
        template = DEFAULT_TEMPLATE

    # 计算统计
    score = profile.get("score", 0)
    rank = profile.get("rank", 0)
    province_name = profile.get("province_name", province_rule.get("name", profile.get("province", "")))
    subject = profile.get("subject", "")
    batch_line = profile.get("batch_line", 0)

    # 填充模板
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    report = template
    report = report.replace("{{TITLE}}", f"2026年高考志愿填报方案")
    report = report.replace("{{SUBTITLE}}", f"{province_name} | {subject} | {score}分 | 位次{rank}")
    report = report.replace("{{GENERATED_TIME}}", now)

    # 位置分析
    line_delta = score - batch_line if batch_line else 0
    report = report.replace("{{SCORE_DELTA}}", f"+{line_delta}" if line_delta >= 0 else str(line_delta))
    report = report.replace("{{BATCH_LINE}}", str(batch_line))
    report = report.replace("{{RANK_PERCENTILE}}", "前3%" if rank < 10000 else ("前10%" if rank < 30000 else "-"))

    # 梯度分布
    report = report.replace("{{DISTRIBUTION_BAR}}", build_risk_distribution_html(strategy))

    # 冲刺表
    report = report.replace("{{REACH_TABLE}}", build_plan_table_html(plan, "冲"))
    report = report.replace("{{REACH_COUNT}}", str(strategy.get("reach_count", 0)))

    # 稳妥表
    report = report.replace("{{MATCH_TABLE}}", build_plan_table_html(plan, "稳"))
    report = report.replace("{{MATCH_COUNT}}", str(strategy.get("match_count", 0)))

    # 保底表
    report = report.replace("{{SAFETY_TABLE}}", build_plan_table_html(plan, "保"))
    report = report.replace("{{SAFETY_COUNT}}", str(strategy.get("safety_count", 0)))

    # 总志愿数
    report = report.replace("{{TOTAL_VOLUNTEERS}}", str(total))
    report = report.replace("{{TOTAL_COUNT}}", str(len([p for p in plan if p.get("university_name", "").startswith("[") is False])))

    # 填报规则
    batch_rules = province_rule.get("batches", {}).get("undergrad", {})
    rule_model = province_rule.get("model", "院校+专业")
    rule_parallel = "是" if batch_rules.get("parallel", True) else "否"
    rule_adjust = "是（" + batch_rules.get("adjustment_scope", "组内调剂") + "）" if batch_rules.get("allow_adjustment") else "否"
    report = report.replace("{{RULE_MODEL}}", rule_model)
    report = report.replace("{{RULE_PARALLEL}}", rule_parallel)
    report = report.replace("{{RULE_ADJUST}}", rule_adjust)

    # 策略说明
    report = report.replace("{{STRATEGY_HINT}}", batch_rules.get("strategy_hint",
        f"总志愿数 {total} 个，建议按冲稳保 18:45:37 比例分配"))

    # 风险警告
    warnings_html = ""
    if warnings:
        for w in warnings:
            warnings_html += f'<li>{w}</li>\n'
    else:
        warnings_html = '<li>未检测到明显风险，请结合个人情况复核</li>'
    report = report.replace("{{WARNINGS}}", warnings_html)

    return report


# 默认HTML模板
DEFAULT_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{TITLE}}</title>
<style>
  :root {
    --reach: #e74c3c;
    --match: #f39c12;
    --safety: #27ae60;
    --bg: #f8f9fa;
    --card: #fff;
    --text: #2c3e50;
    --muted: #7f8c8d;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }
  .container { max-width: 1100px; margin: 0 auto; padding: 20px; }
  .header { background: linear-gradient(135deg, #1a1a2e, #16213e); color: #fff; padding: 30px 40px; border-radius: 12px; margin-bottom: 24px; }
  .header h1 { font-size: 28px; margin-bottom: 8px; }
  .header .subtitle { font-size: 16px; opacity: 0.85; }
  .header .meta { font-size: 13px; opacity: 0.6; margin-top: 8px; }
  .card { background: var(--card); border-radius: 10px; padding: 24px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
  .card h2 { font-size: 20px; margin-bottom: 16px; padding-bottom: 10px; border-bottom: 2px solid #eee; }
  .score-overview { display: flex; gap: 24px; flex-wrap: wrap; }
  .stat { flex: 1; min-width: 140px; text-align: center; padding: 16px; background: #f0f4ff; border-radius: 8px; }
  .stat .value { font-size: 28px; font-weight: 700; color: #1a56db; }
  .stat .label { font-size: 13px; color: var(--muted); margin-top: 4px; }
  .distribution-bar { display: flex; height: 40px; border-radius: 8px; overflow: hidden; margin: 16px 0; }
  .bar-segment { display: flex; align-items: center; justify-content: center; color: #fff; font-size: 13px; font-weight: 600; }
  .bar-reach { background: var(--reach); }
  .bar-match { background: var(--match); }
  .bar-safety { background: var(--safety); }
  table { width: 100%; border-collapse: collapse; font-size: 14px; }
  th { background: #f1f5f9; padding: 10px 8px; text-align: left; font-weight: 600; border-bottom: 2px solid #ddd; white-space: nowrap; }
  td { padding: 10px 8px; border-bottom: 1px solid #eee; }
  tr:hover { background: #f8fafc; }
  .risk-冲 { border-left: 3px solid var(--reach); }
  .risk-稳 { border-left: 3px solid var(--match); }
  .risk-保 { border-left: 3px solid var(--safety); }
  .col-rank { width: 40px; text-align: center; font-weight: 600; }
  .col-school { width: 150px; font-weight: 600; }
  .col-group { width: 130px; }
  .col-majors { max-width: 250px; overflow: hidden; text-overflow: ellipsis; }
  .col-hist { width: 70px; text-align: center; }
  .col-prob { width: 80px; text-align: center; font-weight: 600; }
  .col-risk { width: 70px; text-align: center; font-weight: 600; }
  .col-note { width: 100px; color: var(--muted); font-size: 12px; }
  .prob-high { color: var(--safety); }
  .prob-mid { color: var(--match); }
  .prob-low { color: var(--reach); }
  .warnings { background: #fff3cd; border: 1px solid #ffc107; border-radius: 8px; padding: 16px; }
  .warnings h3 { color: #856404; margin-bottom: 8px; }
  .warnings ul { margin-left: 20px; }
  .warnings li { margin-bottom: 4px; color: #856404; }
  .disclaimer { background: #e2e8f0; border-radius: 8px; padding: 16px; font-size: 13px; color: var(--muted); margin-top: 20px; }
  .rule-info { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; }
  .rule-item { padding: 12px; background: #f0f4ff; border-radius: 6px; }
  .rule-item .key { font-size: 12px; color: var(--muted); }
  .rule-item .val { font-size: 16px; font-weight: 600; }
  @media print { body { background: #fff; } .card { box-shadow: none; break-inside: avoid; } }
</style>
</head>
<body>
<div class="container">

  <!-- Header -->
  <div class="header">
    <h1>{{TITLE}}</h1>
    <div class="subtitle">{{SUBTITLE}}</div>
    <div class="meta">生成时间: {{GENERATED_TIME}} | AI辅助生成，仅供参考</div>
  </div>

  <!-- Score Overview -->
  <div class="card">
    <h2>📊 成绩定位</h2>
    <div class="score-overview">
      <div class="stat">
        <div class="value">{{SCORE_DELTA}}</div>
        <div class="label">线差 (批次线 {{BATCH_LINE}}分)</div>
      </div>
      <div class="stat">
        <div class="value">{{RANK_PERCENTILE}}</div>
        <div class="label">位次百分比</div>
      </div>
      <div class="stat">
        <div class="value">{{TOTAL_COUNT}}</div>
        <div class="label">匹配院校数</div>
      </div>
      <div class="stat">
        <div class="value">{{TOTAL_VOLUNTEERS}}</div>
        <div class="label">总志愿数</div>
      </div>
    </div>
    {{DISTRIBUTION_BAR}}
  </div>

  <!-- Province Rules -->
  <div class="card">
    <h2>📋 本省填报规则</h2>
    <div class="rule-info">
      <div class="rule-item">
        <div class="key">填报模式</div>
        <div class="val">{{RULE_MODEL}}</div>
      </div>
      <div class="rule-item">
        <div class="key">平行志愿</div>
        <div class="val">{{RULE_PARALLEL}}</div>
      </div>
      <div class="rule-item">
        <div class="key">专业调剂</div>
        <div class="val">{{RULE_ADJUST}}</div>
      </div>
    </div>
    <p style="margin-top:12px; font-size:14px; color:var(--muted);">
      💡 {{STRATEGY_HINT}}
    </p>
  </div>

  <!-- 冲刺志愿 -->
  <div class="card">
    <h2>🚀 冲刺志愿 ({{REACH_COUNT}}个 | 录取概率 30-50%)</h2>
    <p style="font-size:13px; color:var(--muted); margin-bottom:12px;">
      录取概率较低，可能有"捡漏"机会，不建议超过总志愿数的20%
    </p>
    <table>
      <thead><tr>
        <th>#</th><th>院校</th><th>专业组</th><th>包含专业</th><th>最低位次</th><th>录取概率</th><th>风险</th><th>备注</th>
      </tr></thead>
      <tbody>{{REACH_TABLE}}</tbody>
    </table>
  </div>

  <!-- 稳妥志愿 -->
  <div class="card">
    <h2>✅ 稳妥志愿 ({{MATCH_COUNT}}个 | 录取概率 50-80%)</h2>
    <p style="font-size:13px; color:var(--muted); margin-bottom:12px;">
      正常发挥大概率录取的主力志愿，应占总量40-50%
    </p>
    <table>
      <thead><tr>
        <th>#</th><th>院校</th><th>专业组</th><th>包含专业</th><th>最低位次</th><th>录取概率</th><th>风险</th><th>备注</th>
      </tr></thead>
      <tbody>{{MATCH_TABLE}}</tbody>
    </table>
  </div>

  <!-- 保底志愿 -->
  <div class="card">
    <h2>🛡️ 保底志愿 ({{SAFETY_COUNT}}个 | 录取概率 >80%)</h2>
    <p style="font-size:13px; color:var(--muted); margin-bottom:12px;">
      确保有学上的底线，应占30-40%，防止滑档
    </p>
    <table>
      <thead><tr>
        <th>#</th><th>院校</th><th>专业组</th><th>包含专业</th><th>最低位次</th><th>录取概率</th><th>风险</th><th>备注</th>
      </tr></thead>
      <tbody>{{SAFETY_TABLE}}</tbody>
    </table>
  </div>

  <!-- 风险提示 -->
  <div class="warnings">
    <h3>⚠️ 风险提示与建议</h3>
    <ul>
      {{WARNINGS}}
    </ul>
  </div>

  <!-- 免责声明 -->
  <div class="disclaimer">
    <strong>免责声明：</strong>本报告由AI辅助生成，数据基于公开信息和历史录取趋势分析，可能存在滞后或误差。
    志愿填报具有重大人生影响，请务必：
    1. 去各省教育考试院官网核实当年招生计划和投档线；
    2. 结合个人兴趣、职业规划、家庭条件等综合决策；
    3. 最终填报方案的决策权与责任在考生本人。
  </div>
</div>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="志愿方案生成器")
    parser.add_argument("--profile", type=str, required=True, help="用户画像JSON文件")
    parser.add_argument("--classified", type=str, required=True, help="分类结果JSON文件")
    parser.add_argument("--province-rules", type=str, default=None,
                        help="省份规则JSON文件路径")
    parser.add_argument("--template", type=str, default=None, help="HTML模板文件路径")
    parser.add_argument("--output", type=str, required=True, help="输出HTML文件路径")

    args = parser.parse_args()

    profile = load_json(args.profile)
    classified = load_json(args.classified)

    if args.province_rules and Path(args.province_rules).exists():
        rules = load_json(args.province_rules)
    else:
        rules = {}

    province = profile.get("province", "")
    province_rule = get_province_rule(rules, province)

    html = build_report_html(profile, classified, province_rule, args.template)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[plan_generator] 报告已生成: {args.output}")


if __name__ == "__main__":
    main()
