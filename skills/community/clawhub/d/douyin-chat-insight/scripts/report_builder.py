"""Single-page HTML / Markdown / JSON report builders."""
from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Set

ALLOWED_FORMATS: Set[str] = {"html", "md", "json"}


def write_reports(result: dict, output_dir: Path, formats: List[str] | None = None) -> Dict[str, str]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    formats = [f.lower() for f in (formats or ["html", "md", "json"])]
    unknown = [f for f in formats if f not in ALLOWED_FORMATS]
    if unknown:
        raise ValueError(f"不支持的 formats: {unknown}; 允许 {sorted(ALLOWED_FORMATS)}")
    # clear stale latest pointers so missing formats don't leave old files
    for name in ("latest.json", "latest.md", "latest.html"):
        lp = output_dir / name
        if lp.exists():
            try:
                lp.unlink()
            except OSError:
                pass
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    conv_name = (result.get("conversation") or {}).get("name") or "chat"
    if result.get("status") == "inventory":
        conv_name = "inventory"
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in conv_name)[:40]
    base = f"{safe}_{stamp}"
    paths = {}
    if "json" in formats:
        p = output_dir / f"{base}.json"
        p.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        paths["json"] = str(p)
    if "md" in formats:
        p = output_dir / f"{base}.md"
        p.write_text(render_markdown(result), encoding="utf-8")
        paths["md"] = str(p)
    if "html" in formats:
        p = output_dir / f"{base}.html"
        p.write_text(render_html(result), encoding="utf-8")
        paths["html"] = str(p)
    if "json" in paths:
        (output_dir / "latest.json").write_text(Path(paths["json"]).read_text(encoding="utf-8"), encoding="utf-8")
    if "md" in paths:
        (output_dir / "latest.md").write_text(Path(paths["md"]).read_text(encoding="utf-8"), encoding="utf-8")
    if "html" in paths:
        (output_dir / "latest.html").write_text(Path(paths["html"]).read_text(encoding="utf-8"), encoding="utf-8")
    return paths


def render_markdown(result: dict) -> str:
    if result.get("status") == "inventory":
        from inventory import format_inventory_text
        return format_inventory_text(result)
    c = result.get("conversation") or {}
    s = result.get("scope") or {}
    b = result.get("blocks") or {}
    lines = [
        f"# 聊天价值洞察 · {c.get('name','')}",
        "",
        f"- 类型: {c.get('type')} / 平台: {c.get('platform') or '—'}",
        f"- 范围: 消息 {s.get('messages_analyzed')}（正文 {s.get('prose_messages')} / 分享类 {s.get('share_like_messages')}）",
        f"- 时段: {s.get('date_start') or '—'} → {s.get('date_end') or '—'}",
        f"- 人物过滤: {s.get('person_filter') or '（全部）'}",
        f"- 群主/主理人别名: {', '.join(s.get('owner_aliases_used') or []) or '—'}",
        "",
        "> " + (result.get("meta") or {}).get("note", ""),
        "",
        "## 一、硬事实（带原话）",
        "",
    ]
    facts = b.get("hard_facts") or []
    if not facts:
        lines.append("_（未抽到启发式硬事实）_")
    for i, f in enumerate(facts, 1):
        lines.append(f"{i}. **{f.get('fact','')}**")
        lines.append(f"   - 出处: {f.get('sender')} · {f.get('ts') or '—'}")
    lines += ["", "## 二、未闭合矛盾", ""]
    cons = b.get("open_contradictions") or []
    if not cons:
        lines.append("_（未发现明显极性矛盾候选）_")
    for i, x in enumerate(cons, 1):
        lines.append(f"### {i}. {x.get('theme','')}")
        a, bb = x.get("side_a") or {}, x.get("side_b") or {}
        lines.append(f"- A `{a.get('sender')}`: {a.get('quote')}")
        lines.append(f"- B `{bb.get('sender')}`: {bb.get('quote')}")
        lines.append(f"- 状态: {x.get('status')} — {x.get('note','')}")
    lines += ["", "## 三、需求侧原话墙（非主理人）", ""]
    dem = b.get("demand_quotes") or []
    if not dem:
        lines.append("_（需求墙为空：可能全是主理人发言，或过滤过严）_")
    for d in dem:
        lines.append(f"- **{d.get('sender')}** ({d.get('ts') or '—'}): 「{d.get('quote')}」")
    lines += ["", "## 四、可执行动作（必须指回上文）", ""]
    acts = b.get("actions") or []
    if not acts:
        lines.append("_（无动作候选）_")
    for i, a in enumerate(acts, 1):
        lines.append(f"{i}. **[{a.get('priority','P2')}] {a.get('action')}**")
        lines.append(f"   - 为什么: {a.get('why')}")
        lines.append(f"   - 指回: {', '.join(a.get('refs') or [])}")
    opt = result.get("optional_enhancements") or {}
    if opt:
        lines += ["", "## 可选增强（抖音链接 / ASR）", ""]
        lines.append(f"- 状态: {opt.get('status')}")
        lines.append(f"- 核心需要百炼: **否**（cloud_asr_required_for_core={opt.get('cloud_asr_required_for_core')})")
        lines.append(f"- 检测到链接/样本数: {opt.get('douyin_links_detected')} / 分享类消息 {opt.get('share_like_messages')}")
        lines.append(f"- 本机 Key 探测: {opt.get('dashscope_key_present')}")
        lines.append(f"- 说明: {opt.get('user_guidance_zh')}")
        lines.append(f"- 配置指导: `{opt.get('guide_path')}`")
    lines += ["", "## 质量自审", ""]
    for q in result.get("quality_checklist") or []:
        lines.append(f"- [ ] {q}")
    lines.append("")
    return "\n".join(lines)


def render_html(result: dict) -> str:
    if result.get("status") == "inventory":
        from inventory import format_inventory_text
        body = f"<pre>{html.escape(format_inventory_text(result))}</pre>"
        title = "会话概况"
    else:
        c = result.get("conversation") or {}
        s = result.get("scope") or {}
        b = result.get("blocks") or {}
        title = html.escape(str(c.get("name") or "chat"))
        parts = [
            f"<header><h1>聊天价值洞察</h1><p class='sub'>{title}</p>",
            f"<p class='meta'>类型 {html.escape(str(c.get('type')))} · 消息 {s.get('messages_analyzed')} · "
            f"{html.escape(str(s.get('date_start') or '—'))} → {html.escape(str(s.get('date_end') or '—'))}</p>",
            f"<p class='note'>{html.escape((result.get('meta') or {}).get('note',''))}</p></header>",
            _sec("一、硬事实（带原话）", _facts_html(b.get("hard_facts") or [])),
            _sec("二、未闭合矛盾", _cons_html(b.get("open_contradictions") or [])),
            _sec("三、需求侧原话墙", _dem_html(b.get("demand_quotes") or [])),
            _sec("四、可执行动作", _act_html(b.get("actions") or [])),
            _opt_html(result.get("optional_enhancements") or {}),
            _sec("质量自审", "<ul>" + "".join(f"<li>☐ {html.escape(q)}</li>" for q in (result.get("quality_checklist") or [])) + "</ul>"),
        ]
        body = "\n".join(parts)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Douyin Chat Insight — {html.escape(str(title))}</title>
<style>
:root {{ --bg:#0f1419; --card:#1a2332; --text:#e7ecf3; --muted:#8b9bb4; --accent:#5b9fd4; --line:#2a3548; --good:#3ddc97; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Noto Sans SC",sans-serif;
  background:var(--bg); color:var(--text); line-height:1.55; }}
.wrap {{ max-width:920px; margin:0 auto; padding:28px 20px 64px; }}
header {{ margin-bottom:28px; }}
h1 {{ font-size:1.6rem; margin:0 0 6px; letter-spacing:.02em; }}
h2 {{ font-size:1.1rem; margin:0 0 12px; color:var(--accent); border-bottom:1px solid var(--line); padding-bottom:8px; }}
.sub {{ color:var(--muted); margin:0; }}
.meta {{ color:var(--muted); font-size:.9rem; }}
.note {{ background:var(--card); border-left:3px solid var(--accent); padding:10px 14px; color:var(--muted); font-size:.88rem; }}
section {{ background:var(--card); border:1px solid var(--line); border-radius:12px; padding:18px 18px 8px; margin:16px 0; }}
ol,ul {{ padding-left:1.2rem; }}
li {{ margin:0 0 12px; }}
.quote {{ color:#cfe3ff; }}
.who {{ color:var(--muted); font-size:.85rem; }}
.badge {{ display:inline-block; background:#243247; color:var(--good); font-size:.75rem; padding:2px 8px; border-radius:999px; margin-right:6px; }}
pre {{ white-space:pre-wrap; background:var(--card); padding:16px; border-radius:12px; }}
footer {{ margin-top:28px; color:var(--muted); font-size:.8rem; }}
</style>
</head>
<body>
<div class="wrap">
{body}
<footer>douyin-chat-insight · single-page report · local-first · no IM login</footer>
</div>
</body>
</html>
"""


def _sec(title: str, inner: str) -> str:
    return f"<section><h2>{html.escape(title)}</h2>{inner}</section>"


def _facts_html(items: list) -> str:
    if not items:
        return "<p class='who'>（未抽到启发式硬事实）</p>"
    lis = []
    for f in items:
        lis.append(
            f"<li><div class='quote'>{html.escape(str(f.get('fact','')))}</div>"
            f"<div class='who'>出处: {html.escape(str(f.get('sender','')))} · {html.escape(str(f.get('ts') or '—'))}</div></li>"
        )
    return "<ol>" + "".join(lis) + "</ol>"


def _cons_html(items: list) -> str:
    if not items:
        return "<p class='who'>（未发现明显极性矛盾候选）</p>"
    blocks = []
    for x in items:
        a, b = x.get("side_a") or {}, x.get("side_b") or {}
        blocks.append(
            f"<div style='margin-bottom:14px'><strong>{html.escape(str(x.get('theme','')))}</strong>"
            f"<div class='who'>A {html.escape(str(a.get('sender','')))}: {html.escape(str(a.get('quote','')))}</div>"
            f"<div class='who'>B {html.escape(str(b.get('sender','')))}: {html.escape(str(b.get('quote','')))}</div>"
            f"<div class='who'>{html.escape(str(x.get('status','')))} — {html.escape(str(x.get('note','')))}</div></div>"
        )
    return "".join(blocks)


def _dem_html(items: list) -> str:
    if not items:
        return "<p class='who'>（需求墙为空）</p>"
    lis = []
    for d in items:
        lis.append(
            f"<li><strong>{html.escape(str(d.get('sender','')))}</strong> "
            f"<span class='who'>({html.escape(str(d.get('ts') or '—'))})</span> "
            f"<span class='quote'>「{html.escape(str(d.get('quote','')))}」</span></li>"
        )
    return "<ul>" + "".join(lis) + "</ul>"


def _act_html(items: list) -> str:
    if not items:
        return "<p class='who'>（无动作候选）</p>"
    lis = []
    for a in items:
        lis.append(
            f"<li><span class='badge'>{html.escape(str(a.get('priority','P2')))}</span>"
            f"<strong>{html.escape(str(a.get('action','')))}</strong>"
            f"<div class='who'>为什么: {html.escape(str(a.get('why','')))}</div>"
            f"<div class='who'>指回: {html.escape(', '.join(a.get('refs') or []))}</div></li>"
        )
    return "<ol>" + "".join(lis) + "</ol>"


def _opt_html(opt: dict) -> str:
    if not opt:
        return ""
    g = html.escape(str(opt.get("user_guidance_zh") or ""))
    st = html.escape(str(opt.get("status") or ""))
    guide = html.escape(str(opt.get("guide_path") or ""))
    inner = (
        f"<p class='who'>状态: {st} · 核心路径需要百炼: <strong>否</strong></p>"
        f"<p class='quote'>{g}</p>"
        f"<p class='who'>配置指导: {guide}</p>"
    )
    return _sec("可选增强（抖音链接 / ASR 端口）", inner)
