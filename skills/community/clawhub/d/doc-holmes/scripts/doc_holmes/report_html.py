#!/usr/bin/env python3
"""v2.1.0：自包含 HTML 可视化批量报告（report.html）。

render_html(result) -> str；零外部依赖（内联 CSS），统计卡片 + 级别分布 +
逐文件状态表（状态着色、失败原因、续传/回滚标记）。中文界面。
"""

from __future__ import annotations

import html
import json
import os

GITHUB_URL = "https://github.com/docsor1212/doc-holmes"
SH_URL = "https://skillhub.cn/skills/indiv-sorsor/doc-holmes"

_STATUS_COLOR = {"success": "#16a34a", "failed": "#dc2626", "timeout": "#d97706",
                 "skipped": "#64748b"}


def _esc(v) -> str:
    return html.escape(str(v if v is not None else "-"))


def render_html(result, glossary_note: str = "") -> str:
    entries = [e for e in result.entries if "watchdog" not in e]
    tiers = {"A": 0, "B": 0, "C": 0}
    for e in entries:
        t = e.get("tier")
        if t in tiers:
            tiers[t] += 1
    rows = []
    for e in entries:
        st = e.get("status", "?")
        st = st if st in _STATUS_COLOR else "unknown"
        color = _STATUS_COLOR.get(st, "#334155")
        note = e.get("error") or e.get("reason") or ""
        ldp = e.get("large_doc_policy") or {}
        flags = []
        if ldp.get("part_pages"):
            flags.append("分段%s/段" % ldp["part_pages"])
        if ldp.get("glossary_skipped"):
            flags.append("跳过术语")
        if e.get("rolled_back"):
            flags.append("已回滚")
        # v2.10.0：与 report.md 备注列同款的质量热点/种子标记
        low = (e.get("ocr") or {}).get("low_conf_pages") or []
        if low:
            flags.append("低置信页:" + ",".join(str(x) for x in low[:8])
                         + ("…" if len(low) > 8 else ""))
        seeded = (e.get("glossary_seeding") or {}).get("seeded") or []
        if seeded:
            flags.append("种子术语%d" % len(seeded))
        flag_s = "；".join(flags)
        rows.append(
            "<tr class='r-%s'><td>%s</td><td>%s</td><td>%s</td><td>%ss</td>"
            "<td>%s</td><td>%s</td></tr>"
            % (st, _esc(e.get("path")), _esc(e.get("tier", "-")),
               ("<span style='color:%s;font-weight:600'>%s</span>" % (color, _esc(st))),
               _esc(e.get("duration_s", "-")), _esc(flag_s), _esc(note[:120])))
    glossary_s = ("<p class='note'>%s</p>" % _esc(glossary_note)) if glossary_note else ""
    return """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>doc-holmes 批量翻译报告</title><style>
body{font-family:"PingFang SC","Microsoft YaHei",system-ui,sans-serif;margin:24px;color:#0f172a}
h1{font-size:20px} .cards{display:flex;gap:12px;margin:16px 0}
.card{border-radius:10px;padding:12px 18px;color:#fff;min-width:90px}
.card h2{margin:0;font-size:26px}.card p{margin:4px 0 0;font-size:12px;opacity:.9}
.c-total{background:#334155}.c-ok{background:#16a34a}.c-fail{background:#dc2626}
.c-to{background:#d97706}.c-skip{background:#64748b}
table{border-collapse:collapse;width:100%;font-size:13px;margin-top:8px}
th,td{border:1px solid #e2e8f0;padding:6px 10px;text-align:left;word-break:break-all}
th{background:#f1f5f9}.meta{color:#64748b;font-size:12px}.note{color:#92400e;font-size:12px}
</style></head><body>
<h1>doc-holmes 批量翻译报告</h1>
<p class="meta">输出目录：__OUT__　时间：__SPAN__</p>
<div class="cards">
<div class="card c-total"><h2>__TOTAL__</h2><p>总计</p></div>
<div class="card c-ok"><h2>__OK__</h2><p>成功</p></div>
<div class="card c-fail"><h2>__FAIL__</h2><p>失败</p></div>
<div class="card c-to"><h2>__TO__</h2><p>超时</p></div>
<div class="card c-skip"><h2>__SKIP__</h2><p>跳过/续传</p></div>
</div>
<p class="note">体检分级分布：A 级 __TA__ ｜ B 级 __TB__ ｜ C 级 __TC__（C 级为预览质量，不可用于正式用途）</p>
__GLOSSARY__
<table><tr><th>文件</th><th>级别</th><th>状态</th><th>耗时</th><th>策略标记</th><th>备注</th></tr>
__ROWS__
</table>
<p class="meta">由 doc-holmes 生成；翻译为 AI 辅助，正式用途前请人工复核。</p>
<footer style="margin-top:24px;padding-top:12px;border-top:1px solid #eee;color:#9aa0a6;font-size:12px;text-align:center;">
本文档由 doc-holmes 生成 · <a href="__GH__" style="color:#9aa0a6;">GitHub</a> · <a href="__SH__" style="color:#9aa0a6;">SkillHub</a> · 觉得有用欢迎 Star / 收藏
</footer>
</body></html>""".replace("__TOTAL__", str(result.total)).replace("__OK__", str(result.success)
        ).replace("__FAIL__", str(result.failed)).replace("__TO__", str(result.timeout)
        ).replace("__SKIP__", str(result.skipped)).replace("__TA__", str(tiers["A"])
        ).replace("__TB__", str(tiers["B"])).replace("__TC__", str(tiers["C"])
        ).replace("__OUT__", _esc(result.outdir)).replace("__SPAN__", _esc(
            "%s ~ %s" % (result.started_at, result.finished_at))
        ).replace("__ROWS__", "\n".join(rows)).replace("__GLOSSARY__", glossary_s
        ).replace("__GH__", GITHUB_URL).replace("__SH__", SH_URL)


def write_html(result, outdir: str, glossary_note: str = "") -> str:
    path = os.path.join(outdir, "report.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(render_html(result, glossary_note=glossary_note))
    return path
