"""成本 / 观测报表（轻量，零依赖）。

- render_text：CLI 表格（日 / 周 / 月报、各家花费、成功率、P95 延迟）。
- render_html：自包含 HTML 报表（内联 CSS，无外部依赖），可浏览器打开。
- budget_alert：月预算超阈值的中文告警（可选推企微）。
- v2.7.0 新增：双轨计算——档案价估算 vs 实测回填。
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _esc(s):
    """HTML 转义，防止厂商名等字段注入到导出的 HTML 报表中。"""
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def render_text(agg, pricing=None):
    """渲染文本报表。
    
    pricing: dict 价格档案（可选），用于双轨计算。
    """
    lines = []
    lines.append("══════════════ 成本报表（%s） ══════════════" % agg["period"])
    lines.append("  总花费 : ¥%.4f" % agg["total_cost"])
    lines.append("  总调用 : %d 次" % agg["total_calls"])
    lines.append("  成功率 : %.1f%%" % agg["success_rate"])
    lines.append("  P95 延迟: %d ms" % agg["p95_ms"])
    lines.append("  输入/输出 token: %d / %d" % (agg["total_in"], agg["total_out"]))
    
    # v2.6 实测/估算分列
    if agg.get("measured_in", 0) or agg.get("est_in", 0):
        lines.append("  ┌ 实测 token: 入 %d / 出 %d" % (agg["measured_in"], agg["measured_out"]))
        lines.append("  └ 估算 token: 入 %d / 出 %d (标注 est)" % (agg["est_in"], agg["est_out"]))
    
    # v2.7.0 双轨：档案价估算 vs 实测
    if pricing:
        est_cost = _estimate_cost_from_pricing(agg, pricing)
        if est_cost is not None:
            lines.append("  ┌ 档案价估算花费: ¥%.4f" % est_cost)
            lines.append("  └ 实测回填花费: ¥%.4f" % agg["total_cost"])
            diff = agg["total_cost"] - est_cost
            if abs(diff) > 0.0001:
                tag = "↑" if diff > 0 else "↓"
                lines.append("  └ 差异: %s ¥%.4f (实测 %s 档案)" % (tag, abs(diff), "高于" if diff > 0 else "低于"))
    
    if agg["by_provider"]:
        lines.append("")
        lines.append("  各家花费：")
        for p, d in sorted(agg["by_provider"].items(), key=lambda x: -x[1]["cost"]):
            est_tag = " (%d 次估算)" % d.get("est_calls", 0) if d.get("est_calls") else ""
            lines.append("    - %-10s 花费 ¥%.4f  调用 %d 次%s" % (p, d["cost"], d["calls"], est_tag))
    else:
        lines.append("  （暂无调用记录）")
    lines.append("═══════════════════════════════════════════════")
    return "\n".join(lines)


def _estimate_cost_from_pricing(agg, pricing):
    """按档案价估算花费（v2.7.0 双轨计算）。"""
    if not pricing:
        return None
    total = 0.0
    for p, d in agg.get("by_provider", {}).items():
        model_name = d.get("model", "")
        if not model_name:
            for pname, pinfo in pricing.items():
                if pinfo.get("provider") == p:
                    model_name = pname
                    break
        if model_name and model_name in pricing:
            pinfo = pricing[model_name]
            cost = d.get("in", 0) / 1_000_000 * pinfo["in"] + d.get("out", 0) / 1_000_000 * pinfo["out"]
            total += cost
    return round(total, 4) if total > 0 else None


def render_html(agg, path):
    """渲染 HTML 报表（自包含，无外部依赖）。"""
    rows = ""
    for p, d in sorted(agg["by_provider"].items(), key=lambda x: -x[1]["cost"]):
        rows += (
            "<tr><td>%s</td><td>¥%.4f</td><td>%d</td><td>%d</td><td>%d</td></tr>"
            % (_esc(p), d["cost"], d["calls"], d["in"], d["out"])
        )
    html = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>国产大模型统一路由 - 成本报表</title>
<style>
body{font-family:-apple-system,"Microsoft YaHei",sans-serif;margin:32px;color:#222}
h1{font-size:20px}.card{background:#f7f8fa;border:1px solid #e5e7eb;border-radius:10px;padding:16px;margin:16px 0}
.metric{display:inline-block;min-width:140px;margin:8px}
.metric b{display:block;font-size:22px;color:#1a56db}
table{width:100%%;border-collapse:collapse;margin-top:8px}
th,td{border:1px solid #e5e7eb;padding:8px;text-align:left}
th{background:#f0f2f5}
</style></head><body>
<h1>国产大模型统一路由 · 成本报表（%s）</h1>
<div class="card">
  <div class="metric"><b>¥%.4f</b>总花费</div>
  <div class="metric"><b>%d</b>调用次数</div>
  <div class="metric"><b>%.1f%%</b>成功率</div>
  <div class="metric"><b>%d ms</b>P95 延迟</div>
</div>
<table><thead><tr><th>厂商</th><th>花费</th><th>调用</th><th>输入token</th><th>输出token</th></tr></thead>
<tbody>%s</tbody>
</table>
<p style="color:#888;font-size:12px">由 cn-llm-router 本地生成，数据仅存于本机 SQLite，不上传任何服务器。</p>
</body></html>
""" % (_esc(agg["period"]), agg["total_cost"], agg["total_calls"], agg["success_rate"], agg["p95_ms"], rows)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def budget_alert(exceeded, spent, budget):
    if not exceeded:
        return "✅ 本月花费 ¥%.4f，未超预算 ¥%.4f" % (spent, budget)
    return ("🔴 预算告警：本月已花费 ¥%.4f，已超过预算 ¥%.4f！"
            "建议切换 cheap 策略或检查路由配置。" % (spent, budget))


def maybe_push_wecom(webhook, text):
    """可选：把告警推送到企微机器人（webhook 来自本机 config.json，不进包）。"""
    if not webhook:
        return False
    import json
    import urllib.request
    try:
        data = json.dumps({"msgtype": "text", "text": {"content": text}}).encode("utf-8")
        req = urllib.request.Request(webhook, data=data,
                                     headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(req, timeout=10)
        return True
    except Exception:
        return False
