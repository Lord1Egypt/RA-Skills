#!/usr/bin/env python3
import argparse
import base64
import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
LEVELS = ["口供", "旁证", "物证", "银票", "血书"]


def esc(value):
    return html.escape(str(value or ""), quote=True)


def clamp_score(value):
    try:
        n = int(round(float(value)))
    except Exception:
        n = 0
    return max(0, min(100, n))


def slug(text):
    value = re.sub(r"[\\/:*?\"<>|\\s]+", "-", str(text or "baoqingtian-case")).strip("-")
    return value[:48] or "baoqingtian-case"


def image_data(name):
    path = ASSETS / name
    mime = "image/png"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def pick_theme(case):
    explicit = case.get("theme")
    if explicit in {"black", "gray", "white"}:
        return explicit
    ruling = str(case.get("ruling_level") or case.get("verdict_tag") or "")
    score = clamp_score(case.get("score", 0))
    if "不予" in ruling or score < 45:
        return "black"
    if "开工" in ruling or score >= 80:
        return "white"
    return "gray"


def metric_rows(metrics):
    rows = []
    for item in (metrics or [])[:4]:
        name = esc(item.get("name", ""))
        score = clamp_score(item.get("score", 0))
        rows.append(
            f'<div class="bar"><span>{name}</span><i><b style="width:{score}%"></b></i><em>{score}</em></div>'
        )
    return "\n".join(rows)


def ladder_html(level):
    idx = LEVELS.index(level) if level in LEVELS else 0
    parts = []
    for i, name in enumerate(LEVELS):
        cls = "step current" if i == idx else ("step on" if i < idx else "step")
        parts.append(f'<div class="{cls}"><u></u><span>{esc(name)}</span></div>')
    return "\n".join(parts)


def problem_rows(problems):
    nums = ["壹", "贰", "叁"]
    rows = []
    for i, item in enumerate((problems or [])[:3]):
        rows.append(
            '<div class="problem-row">'
            f'<span class="idx">{nums[i]}</span>'
            f'<b>{esc(item.get("title", ""))}</b>'
            f'<p>{esc(item.get("desc", ""))}</p>'
            "</div>"
        )
    return "\n".join(rows)


def task_items(tasks):
    return "\n".join(f"<li>{esc(task)}</li>" for task in (tasks or [])[:3])


def detail_markdown(case):
    d = case.get("detailed") or {}
    lines = [
        f"# 包青天判词：{case.get('case_title', '未名案')}",
        "",
        f"## 立案等级",
        "",
        d.get("ruling") or case.get("ruling_level", ""),
        "",
        "## 伪需求嫌疑",
        "",
        d.get("pseudo_demand_risk", ""),
        "",
        "## 关键死因",
        "",
    ]
    for i, item in enumerate(d.get("key_deaths") or [], 1):
        lines.append(f"{i}. {item}")
    lines += [
        "",
        "## 最强证据",
        "",
        d.get("strongest_evidence", ""),
        "",
        "## 最大缺口",
        "",
        d.get("biggest_gap", ""),
        "",
        "## 准予 / 不准予翻案",
        "",
        d.get("appeal", ""),
        "",
        "## 七日补证任务",
        "",
    ]
    for i, item in enumerate(d.get("seven_day_tasks") or case.get("tasks") or [], 1):
        lines.append(f"{i}. {item}")
    return "\n".join(lines).strip() + "\n"


def detail_html(markdown_text):
    blocks = []
    for raw in markdown_text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("# "):
            blocks.append(f"<h1>{esc(line[2:])}</h1>")
        elif line.startswith("## "):
            blocks.append(f"<h2>{esc(line[3:])}</h2>")
        elif re.match(r"^\\d+\\.\\s+", line):
            blocks.append(f"<p class=\"ordered\">{esc(line)}</p>")
        else:
            blocks.append(f"<p>{esc(line)}</p>")
    return "\n".join(blocks)


def render_html(case):
    theme = pick_theme(case)
    dark_logo = image_data("bao-dark.png")
    light_logo = image_data("bao-light.png")
    logo = light_logo if theme == "black" else dark_logo
    evidence_level = case.get("evidence_level", "口供")
    score = clamp_score(case.get("score", 0))
    detail_md = detail_markdown(case)
    case_no = case.get("case_no", "案卷 · 001")

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(case.get("case_title", "包青天判牍"))} · 包青天判牍</title>
<style>
:root {{
  --page:#e5e5e5; --seal:#a8302d; --seal-dark:#7d211e; --seal-paper:#f0dfc4;
  --serif:"Songti SC","STSong","Noto Serif SC","Source Han Serif SC","SimSun",serif;
  --sans:"PingFang SC","Hiragino Sans GB","Microsoft YaHei",system-ui,sans-serif;
  --mono:"SFMono-Regular","Menlo","Consolas",monospace;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--page); color:#1a1a1a; font-family:var(--sans); -webkit-font-smoothing:antialiased; }}
.wrap {{ min-height:100vh; padding:28px 18px 54px; display:flex; flex-direction:column; align-items:center; gap:28px; }}
.card {{
  --bg:#cbcac5; --ink:#1c1c1b; --muted:#56564f; --line:rgba(25,25,25,.15);
  --line-strong:rgba(25,25,25,.36); --track:rgba(25,25,25,.16); --surface:rgba(255,255,255,.40);
  position:relative; width:min(466px, calc(100vw - 32px)); aspect-ratio:466/828; padding:24px 28px 22px;
  overflow:hidden; background:var(--bg); color:var(--ink); border:1px solid var(--line-strong);
  box-shadow:0 18px 46px rgba(0,0,0,.13); font-family:var(--serif);
}}
.card.black {{ --bg:#181818; --ink:#ededeb; --muted:#9b9b97; --line:rgba(237,237,235,.15); --line-strong:rgba(237,237,235,.30); --track:rgba(237,237,235,.14); --surface:rgba(255,255,255,.06); }}
.card.white {{ --bg:#fafaf8; --ink:#161616; --muted:#6b6b66; --line:rgba(22,22,22,.12); --line-strong:rgba(22,22,22,.30); --track:rgba(22,22,22,.11); --surface:rgba(255,255,255,.70); }}
.card:after {{ content:""; position:absolute; inset:18px; border:1px solid var(--line); pointer-events:none; }}
.wm {{ position:absolute; top:-14px; left:50%; transform:translateX(-46%); width:300px; opacity:.12; pointer-events:none; }}
.seal {{ position:absolute; top:18px; right:30px; width:54px; height:62px; display:grid; grid-template-columns:1fr 1fr; grid-template-rows:1fr 1fr; place-items:center; background:var(--seal); border:2px solid var(--seal-dark); box-shadow:inset 0 0 0 1.5px var(--seal-dark); color:var(--seal-paper); font-weight:700; font-size:18px; line-height:1; transform:rotate(-4deg); z-index:3; }}
.scene,.title,.metrics,.ladder,.mirror,.remedy,.foot,.rule,.label {{ position:relative; z-index:1; }}
.scene {{ height:46px; display:flex; align-items:center; justify-content:space-between; }}
.brand {{ display:flex; align-items:center; gap:10px; }}
.brand img {{ width:34px; height:34px; object-fit:contain; }}
.brand b {{ display:block; font-size:18px; line-height:1; }}
.brand span {{ display:block; margin-top:5px; color:var(--muted); font-family:var(--mono); font-size:7.5px; letter-spacing:.1em; }}
.case-no {{ min-width:90px; padding:6px 10px 5px; border:1px solid var(--line-strong); font-family:var(--mono); font-size:10px; text-align:center; background:var(--surface); }}
.title {{ margin-top:18px; }}
.title h1 {{ margin:0; font-size:37px; line-height:1.05; font-weight:800; letter-spacing:.01em; }}
.subtitle {{ margin-top:7px; color:var(--muted); font-size:14px; line-height:1.5; }}
.verdict {{ margin-top:12px; display:flex; align-items:center; gap:10px; min-height:25px; font-size:11px; }}
.tag {{ padding:5px 9px 4px; border:1px solid var(--line-strong); font-weight:700; line-height:1; }}
.black .tag {{ background:var(--seal); border-color:var(--seal-dark); color:var(--seal-paper); }}
.white .tag {{ background:var(--ink); border-color:var(--ink); color:var(--bg); }}
.verdict-text {{ color:var(--muted); font-family:var(--mono); }}
.verdict-text b {{ color:var(--ink); }}
.rule {{ height:1px; margin:13px 0; background:var(--line); }}
.label {{ display:flex; justify-content:space-between; align-items:baseline; margin-bottom:8px; color:var(--muted); font-family:var(--mono); font-size:9px; letter-spacing:.06em; }}
.label b {{ color:var(--ink); font-family:var(--serif); font-size:11px; font-weight:500; }}
.metrics {{ display:grid; grid-template-columns:124px 1fr; gap:22px; align-items:center; }}
.gauge {{ position:relative; width:116px; height:116px; border-radius:50%; background:conic-gradient(var(--seal) {score}%, var(--track) 0); }}
.gauge:before {{ content:""; position:absolute; inset:7px; border-radius:50%; background:var(--bg); }}
.gauge div {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; }}
.gauge strong {{ display:block; font-size:42px; line-height:.86; }}
.gauge small {{ display:block; margin-top:7px; color:var(--muted); font-family:var(--mono); font-size:8px; }}
.bars {{ display:grid; gap:10px; }}
.bar {{ display:grid; grid-template-columns:72px 1fr 26px; gap:10px; align-items:center; font-size:12px; }}
.bar span {{ color:var(--muted); }}
.bar i {{ height:5px; background:var(--track); display:block; }}
.bar b {{ height:100%; background:var(--ink); display:block; }}
.bar em {{ font-family:var(--mono); font-size:11px; font-style:normal; text-align:right; }}
.ladder {{ display:grid; grid-template-columns:repeat(5,1fr); height:45px; }}
.step {{ position:relative; padding-top:19px; text-align:center; color:var(--muted); font-size:11px; }}
.step:before {{ content:""; position:absolute; top:7px; left:0; right:0; height:1px; background:var(--line-strong); }}
.step u {{ position:absolute; top:2px; left:50%; width:10px; height:10px; transform:translateX(-50%); border:1px solid var(--ink); border-radius:50%; background:var(--bg); }}
.step.on u {{ background:var(--ink); }}
.step.current {{ color:var(--ink); font-weight:700; }}
.step.current u {{ top:0; width:14px; height:14px; border-color:var(--seal); background:var(--seal); box-shadow:0 0 0 4px rgba(168,48,45,.18); }}
.mirror {{ display:grid; }}
.problem-row {{ display:grid; grid-template-columns:24px 92px 1fr; gap:10px; align-items:baseline; min-height:32px; padding:7px 0; border-bottom:1px solid var(--line); }}
.problem-row:last-child {{ border-bottom:0; }}
.idx {{ color:var(--muted); font-style:italic; font-size:16px; }}
.problem-row b {{ font-size:15px; }}
.problem-row p {{ margin:0; color:var(--muted); font-size:12px; line-height:1.45; }}
.remedy {{ display:grid; grid-template-columns:1.08fr .92fr; gap:20px; margin-top:2px; }}
.judgement {{ padding-left:11px; border-left:2px solid var(--seal); }}
.red-label,.task-title {{ color:var(--seal); font-size:9px; letter-spacing:.06em; font-family:var(--mono); }}
.judgement p {{ margin:7px 0 0; font-size:16px; line-height:1.55; font-weight:700; }}
.tasks ul {{ margin:8px 0 0; padding:0; list-style:none; }}
.tasks li {{ position:relative; padding-left:12px; margin-top:5px; color:var(--ink); font-size:12px; line-height:1.45; }}
.tasks li:before {{ content:"·"; position:absolute; left:0; top:0; font-weight:700; }}
.foot {{ position:absolute; left:28px; right:28px; bottom:22px; display:flex; justify-content:space-between; align-items:flex-end; z-index:2; }}
.source {{ color:var(--muted); font-size:9px; }}
.url {{ margin-top:5px; font-family:var(--mono); font-size:11px; font-weight:700; }}
.closing {{ color:var(--muted); font-size:11px; line-height:1.5; text-align:right; }}
.closing b {{ display:block; color:var(--ink); font-size:13px; }}
.detail {{ width:min(720px, calc(100vw - 32px)); background:rgba(255,255,255,.42); border:1px solid rgba(71,73,75,.2); padding:28px; font-family:var(--serif); line-height:1.78; }}
.detail h1 {{ margin:0 0 18px; font-size:30px; }}
.detail h2 {{ margin:26px 0 8px; font-size:20px; }}
.detail p {{ margin:7px 0; color:#373737; }}
.detail .ordered {{ padding-left:1em; }}
@media (max-width:520px) {{ .wrap {{ padding:16px 8px 36px; }} .card {{ padding:20px 22px; }} .title h1 {{ font-size:32px; }} .problem-row {{ grid-template-columns:22px 82px 1fr; }} }}
</style>
</head>
<body>
<main class="wrap">
  <article class="card {theme}">
    <img class="wm" src="{logo}" alt="">
    <div class="seal"><span>包</span><span>拯</span><span>之</span><span>印</span></div>
    <div class="scene">
      <div class="brand"><img src="{logo}" alt=""><div><b>包青天</b><span>IDEA COURT · 需求判牍</span></div></div>
      <div class="case-no">{esc(case_no)}</div>
    </div>
    <section class="title">
      <h1>{esc(case.get("case_title", ""))}</h1>
      <div class="subtitle">{esc(case.get("subtitle", ""))}</div>
      <div class="verdict"><span class="tag">{esc(case.get("verdict_tag", ""))}</span><span class="verdict-text">判词 <b>{esc(case.get("verdict", ""))}</b></span></div>
    </section>
    <div class="rule"></div>
    <div class="label">准生指数 · 四维评分 <b>{esc(case.get("evidence_label", "证据力：" + str(evidence_level)))}</b></div>
    <section class="metrics">
      <div class="gauge"><div><strong>{score}</strong><small>准生指数</small></div></div>
      <div class="bars">{metric_rows(case.get("metrics"))}</div>
    </section>
    <div class="rule"></div>
    <section class="ladder">{ladder_html(evidence_level)}</section>
    <div class="rule"></div>
    <div class="label">照妖镜 · 三大死因</div>
    <section class="mirror">{problem_rows(case.get("problems"))}</section>
    <div class="rule"></div>
    <section class="remedy">
      <div class="judgement"><div class="red-label">本案判语</div><p>{esc(case.get("judgement", ""))}</p></div>
      <div class="tasks"><div class="task-title">七日翻案</div><ul>{task_items(case.get("tasks"))}</ul></div>
    </section>
    <footer class="foot">
      <div><div class="source">包青天.skill · 需求判牍</div><div class="url">b.caojuege.com</div></div>
      <div class="closing"><b>不杀热情，只杀幻想</b>先指出问题，再指出活路</div>
    </footer>
  </article>
  <section class="detail">{detail_html(detail_md)}</section>
</main>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Render Baoqingtian verdict HTML and Markdown.")
    parser.add_argument("--case-json", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--basename")
    args = parser.parse_args()

    case_path = Path(args.case_json)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    case = json.loads(case_path.read_text(encoding="utf-8"))
    base = slug(args.basename or case.get("case_title") or "包青天判牍")

    html_text = render_html(case)
    md_text = detail_markdown(case)
    html_path = out_dir / f"{base}-判牍卡.html"
    md_path = out_dir / f"{base}-判词.md"
    html_path.write_text(html_text, encoding="utf-8")
    md_path.write_text(md_text, encoding="utf-8")

    print(str(html_path))
    print(str(md_path))


if __name__ == "__main__":
    main()
