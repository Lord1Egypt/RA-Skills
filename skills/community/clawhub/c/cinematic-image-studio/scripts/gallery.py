#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
输出目录 · 样图库 gallery.py

扫描 `assets/output/*/提示词.json` + `styles/` 风格卡 + `styles/_索引.md`，生成：

  1. `assets/output/_缩略图/<项目>/<id>.webp`  —— 480px 宽缩略图（cwebp / sips）
  2. `assets/output/index.html`               —— 单文件样图库：列表 + 点开看原图 + 提示词
  3. `assets/output/README.md`                —— 项目索引 + 全库样图覆盖表

零外部依赖；缩略图工具优先 `cwebp`，退回 macOS `sips`（jpeg）。

用法：
  python3 scripts/gallery.py                 # 全量重建（增量生成缩略图）
  python3 scripts/gallery.py --force-thumbs  # 强制重生成缩略图
"""
import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time


SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STYLES_DIR = os.path.join(SKILL_ROOT, "styles")
OUTPUT_ROOT = os.path.join(SKILL_ROOT, "assets", "output")
THUMB_ROOT = os.path.join(OUTPUT_ROOT, "_缩略图")
IMG_EXTS = (".png", ".jpg", ".jpeg", ".webp")
THUMB_WIDTH = 480
THUMB_QUALITY = "78"


# ---------------------------------------------------------------- 解析
def parse_index():
    """从 _索引.md 取：编号 -> {name, one, ratio, status, group}"""
    path = os.path.join(STYLES_DIR, "_索引.md")
    out, group = {}, ""
    if not os.path.isfile(path):
        return out
    for line in open(path, "r", encoding="utf-8"):
        m = re.match(r"^##\s+([一二三四五六七八九十]+)、(.+?)\s*$", line)
        if m:
            group = f"{m.group(1)}、{m.group(2).strip()}".split("（")[0].strip()
            continue
        if line.startswith("## "):
            group = ""
            continue
        m = re.match(r"^\|\s*(\d\d)\s*\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|", line)
        if m and group:
            out[m.group(1)] = {
                "name": m.group(2).strip(),
                "one": m.group(3).strip(),
                "ratio": m.group(4).strip(),
                "group": group,
            }
    return out


def parse_cards():
    """编号 -> {display, ratio, desc}"""
    out = {}
    for fn in sorted(os.listdir(STYLES_DIR)):
        if not re.match(r"^\d\d-.*\.md$", fn) or fn.startswith("_"):
            continue
        num = fn[:2]
        text = open(os.path.join(STYLES_DIR, fn), "r", encoding="utf-8").read()
        fm = text.split("---", 2)[1] if text.startswith("---") else ""
        disp = re.search(r"^displayName:\s*(.+?)\s*$", fm, re.M)
        ratio = re.search(r'^defaultRatio:\s*"?([^"\n]+)"?\s*$', fm, re.M)
        desc = ""
        dm = re.search(r"^description:\s*>\s*\n((?:[ \t]+.*\n?)+)", fm, re.M)
        if dm:
            desc = " ".join(x.strip() for x in dm.group(1).strip().splitlines())
        out[num] = {
            "file": fn,
            "display": disp.group(1).strip() if disp else fn[:-3],
            "ratio": ratio.group(1).strip() if ratio else "",
            "desc": desc,
        }
    return out


def parse_test_subjects():
    """编号 -> 建议测试主体"""
    path = os.path.join(STYLES_DIR, "_测试主体.md")
    out = {}
    if not os.path.isfile(path):
        return out
    for line in open(path, "r", encoding="utf-8"):
        m = re.match(r"^\|\s*(\d\d)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|", line)
        if m:
            out[m.group(1)] = m.group(3).strip()
    return out


def find_images(project_path):
    found = {}
    for dirpath, _d, files in os.walk(project_path):
        for fn in files:
            stem, ext = os.path.splitext(fn)
            if ext.lower() in IMG_EXTS:
                found.setdefault(stem, os.path.join(dirpath, fn))
    return found


# ---------------------------------------------------------------- 缩略图
def thumb_tool():
    if shutil.which("cwebp"):
        return "cwebp"
    if shutil.which("sips"):
        return "sips"
    return ""


def make_thumb(src, dst_base, force=False):
    """返回缩略图相对 assets/output 的路径（webp 或 jpg）；失败返回 ''。"""
    tool = thumb_tool()
    if not tool:
        return ""
    for ext in (".webp", ".jpg"):
        cand = dst_base + ext
        if os.path.isfile(cand) and not force:
            if os.path.getmtime(cand) >= os.path.getmtime(src):
                return os.path.relpath(cand, OUTPUT_ROOT)
    os.makedirs(os.path.dirname(dst_base), exist_ok=True)
    if tool == "cwebp":
        dst = dst_base + ".webp"
        cmd = ["cwebp", "-quiet", "-q", THUMB_QUALITY,
               "-resize", str(THUMB_WIDTH), "0", src, "-o", dst]
    else:
        dst = dst_base + ".jpg"
        cmd = ["sips", "-Z", str(THUMB_WIDTH), "-s", "format", "jpeg", src, "--out", dst]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (OSError, subprocess.CalledProcessError):
        return ""
    return os.path.relpath(dst, OUTPUT_ROOT) if os.path.isfile(dst) else ""


# ---------------------------------------------------------------- 采集
def collect(force_thumbs=False):
    """支持两种布局：
    ① 合并库：`assets/output/提示词.json` + `图片/<id>.png`（当前默认）
    ② 旧的多项目：`assets/output/<项目>/提示词.json` + `图片/<kind>/<id>.png`
    """
    index = parse_index()
    cards = parse_cards()
    subjects = parse_test_subjects()
    items = []

    sources = []  # (默认项目名, 提示词.json, 图片根目录, 是否用 row.project)
    root_pj = os.path.join(OUTPUT_ROOT, "提示词.json")
    if os.path.isfile(root_pj):
        sources.append(("合并库", root_pj, os.path.join(OUTPUT_ROOT, "图片"), True))
    for name in sorted(os.listdir(OUTPUT_ROOT)):
        ppath = os.path.join(OUTPUT_ROOT, name)
        pj = os.path.join(ppath, "提示词.json")
        if os.path.isdir(ppath) and not name.startswith("_") and os.path.isfile(pj):
            sources.append((name, pj, ppath, False))

    for default_project, pj, img_root, use_row_project in sources:
        data = json.load(open(pj, "r", encoding="utf-8"))
        rows = data.get("rows", [])
        imgs = find_images(img_root)
        for r in rows:
            rid = r.get("id", "")
            kind = r.get("kind", "")
            project = (r.get("project") or default_project) if use_row_project else default_project
            num_m = re.match(r"^(\d\d)-", kind) or re.match(r"^(\d\d)-", project)
            num = num_m.group(1) if num_m else ""
            src = imgs.get(rid)
            style = index.get(num, {})
            card = cards.get(num, {})
            subject = rid[len(kind) + 1:] if kind and rid.startswith(kind + "-") else ""
            subject = subject or subjects.get(num, "")
            thumb_base = os.path.join(THUMB_ROOT, rid) if use_row_project \
                else os.path.join(THUMB_ROOT, project, rid)
            items.append({
                "id": rid,
                "project": project,
                "number": num,
                "kind": kind,
                "style": style.get("name") or card.get("display", kind),
                "one": style.get("one", ""),
                "group": style.get("group", "未分组"),
                "ratio": (style.get("ratio") or card.get("ratio") or ""),
                "size": r.get("size", ""),
                "subject": subject,
                "prompt": r.get("prompt", ""),
                "image": os.path.relpath(src, OUTPUT_ROOT) if src else "",
                "thumb": make_thumb(src, thumb_base, force_thumbs) if src else "",
                "api": r.get("api", ""),
                "apiModel": r.get("model", ""),
                "apiAt": r.get("api_at", ""),
                "apiEst": bool(r.get("api_estimated")),
            })

    # 去重：同一 id 优先保留有图的
    best = {}
    for it in items:
        key = it["id"]
        if key not in best or (not best[key]["image"] and it["image"]):
            best[key] = it
    items = sorted(best.values(), key=lambda x: (x["number"] or "99", x["project"], x["id"]))

    # 项目摘要（按 row.project 聚合，合并库也能看出每批的来源）
    counts = {}
    for it in items:
        p = counts.setdefault(it["project"], {"name": it["project"], "rows": 0, "done": 0})
        p["rows"] += 1
        p["done"] += 1 if it["image"] else 0
    for p in counts.values():
        p["pending"] = p["rows"] - p["done"]
    projects = sorted(counts.values(), key=lambda x: x["name"])
    return items, projects, index


# ---------------------------------------------------------------- HTML
CSS = """
:root{
  --bg:#0e0f11; --panel:#15171a; --panel2:#1b1e22; --line:#2a2e34;
  --text:#ececec; --muted:#9aa0a8; --dim:#6e747c;
  --accent:#d8b46a; --accent2:#c8563f; --ok:#5fbf8a; --warn:#d9a441;
  --radius:14px; --shadow:0 12px 40px rgba(0,0,0,.45);
}
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--text);
  font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
  -webkit-font-smoothing:antialiased}
body{padding-bottom:80px}
a{color:inherit}
.wrap{max-width:1560px;margin:0 auto;padding:0 28px}
header{padding:34px 0 18px;border-bottom:1px solid var(--line);
  background:radial-gradient(1200px 220px at 12% -40%,rgba(216,180,106,.18),transparent 70%)}
h1{font-size:26px;margin:0 0 8px;letter-spacing:.04em;font-weight:650}
h1 em{font-style:normal;color:var(--accent)}
.sub{color:var(--muted);font-size:13px;line-height:1.7}
.sub b{color:var(--text);font-weight:600}
.sub .dot{margin:0 8px;color:var(--dim)}
.toolbar{position:sticky;top:0;z-index:20;background:rgba(14,15,17,.9);
  backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.toolbar .wrap{display:flex;gap:14px;align-items:center;padding-top:14px;padding-bottom:14px;flex-wrap:wrap}
.search{flex:1 1 260px;display:flex;align-items:center;gap:9px;background:var(--panel);
  border:1px solid var(--line);border-radius:10px;padding:9px 13px}
.search input{flex:1;background:none;border:0;outline:0;color:var(--text);font-size:14px}
.search svg{opacity:.5}
select{background:var(--panel);color:var(--text);border:1px solid var(--line);
  border-radius:10px;padding:10px 12px;font-size:13px;outline:0}
.count{color:var(--muted);font-size:13px;white-space:nowrap}
.count b{color:var(--accent);font-weight:600}
.chips{display:flex;gap:7px;flex-wrap:wrap;padding:12px 0 0}
.chip{border:1px solid var(--line);background:var(--panel);color:var(--muted);
  padding:6px 12px;border-radius:999px;font-size:12.5px;cursor:pointer;transition:.16s}
.chip:hover{border-color:#4a505a;color:var(--text)}
.chip.on{background:var(--accent);border-color:var(--accent);color:#1a1508;font-weight:600}
.grid{column-width:330px;column-gap:20px;padding:26px 0 10px}
/* ⚠ .card 上不要加 transform：多列(column-width)中间元素一旦带 transform，
   WebKit 会破坏分栏分段，导致 hover 时邻列卡片整张不绘制（丢图）。
   抬升效果改用 border-color + box-shadow + 背景微亮；图片缩放(scale)不受影响。 */
.card{display:block;width:100%;margin:0 0 20px;break-inside:avoid;
  background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);
  overflow:hidden;cursor:pointer;transition:border-color .18s,box-shadow .18s,background .18s;
  text-align:left;padding:0;color:inherit;font:inherit;position:relative}
.card:hover{border-color:#5b6169;background:#181b1f;
  box-shadow:0 14px 34px rgba(0,0,0,.55),0 0 0 1px rgba(216,180,106,.16)}
.thumb{position:relative;background:var(--panel2);overflow:hidden;min-height:120px}
.thumb img{width:100%;height:auto;display:block;transition:transform .5s}
.card:hover .thumb img{transform:scale(1.04)}
.thumb.portrait{min-height:0}
.badge{position:absolute;left:12px;top:12px;background:rgba(10,10,11,.74);
  border:1px solid rgba(255,255,255,.18);backdrop-filter:blur(6px);
  color:#fff;font-size:11.5px;letter-spacing:.06em;padding:4px 8px;border-radius:6px}
.state{position:absolute;right:12px;top:12px;font-size:11px;padding:4px 9px;border-radius:999px;
  backdrop-filter:blur(6px);border:1px solid rgba(255,255,255,.16);background:rgba(10,10,11,.7)}
.state.ok{color:#9be3bd}.state.pending{color:#f0c979}
.body{padding:14px 15px 16px}
.name{font-size:15px;font-weight:600;margin-bottom:5px;letter-spacing:.01em}
.one{font-size:12.5px;color:var(--muted);line-height:1.6;min-height:40px}
.meta{display:flex;gap:8px;flex-wrap:wrap;margin-top:11px;font-size:11.5px;color:var(--dim)}
.meta span{border:1px solid var(--line);border-radius:6px;padding:3px 7px;background:#131518}
.meta .api{border-color:rgba(216,180,106,.32);color:#cbb079;background:rgba(216,180,106,.07)}
.meta .api.ark{border-color:rgba(95,191,138,.30);color:#8fd3ae;background:rgba(95,191,138,.07)}
.meta .api.newapi{border-color:rgba(122,162,247,.30);color:#9dbaf8;background:rgba(122,162,247,.07)}
.meta .api.none{border-color:var(--line);color:#5c626a;background:#131518}
/* 出图 API 角标：贴在缩略图左下角，每张图都有（无记录的历史图标「未标注」） */
/* ⚠ 不要给 .api-chip 加 backdrop-filter：WebKit 下多列(column-width)分段里、
   贴着缩略图底边的绝对定位元素带 backdrop-filter 会整块不绘制（标签看不见）。
   改用更实的半透明底保证可读性。 */
.api-chip{position:absolute;left:12px;bottom:12px;display:inline-flex;align-items:center;gap:6px;
  font-size:11px;letter-spacing:.04em;padding:4px 9px;border-radius:999px;
  background:rgba(10,10,11,.84);border:1px solid rgba(255,255,255,.22);
  color:#d6d9dd;max-width:calc(100% - 24px);overflow:hidden;
  white-space:nowrap;text-overflow:ellipsis}
.api-chip::before{content:"";width:6px;height:6px;border-radius:50%;background:#6e747c;flex:none}
.api-chip.ark{color:#9be3bd;border-color:rgba(95,191,138,.42)}
.api-chip.ark::before{background:#5fbf8a}
.api-chip.newapi{color:#a9c4ff;border-color:rgba(122,162,247,.42)}
.api-chip.newapi::before{background:#7aa2f7}
.api-chip.tool{color:#f0c979;border-color:rgba(217,164,65,.42)}
.api-chip.tool::before{background:#d9a441}
.api-chip.none{color:#8b9199}
.api-chip.none::before{background:#6e747c}
/* 推定标签（历史图按尺寸反推）：虚线边 + 稍低不透明度 */
.api-chip.est{border-style:dashed}
.api-chip.est::before{opacity:.55}
.empty{display:none;padding:80px 0;text-align:center;color:var(--dim)}
/* lightbox */
.lb{position:fixed;inset:0;z-index:80;display:none;background:rgba(6,7,8,.94);
  backdrop-filter:blur(10px)}
.lb.on{display:grid;grid-template-columns:1fr 400px}
.lb-stage{position:relative;display:flex;align-items:center;justify-content:center;padding:44px 30px}
.lb-stage img{max-width:100%;max-height:calc(100vh - 88px);border-radius:8px;
  box-shadow:0 30px 90px rgba(0,0,0,.7)}
.lb-close{position:absolute;right:20px;top:16px;background:rgba(255,255,255,.08);
  border:1px solid rgba(255,255,255,.16);color:#fff;width:38px;height:38px;border-radius:50%;
  font-size:18px;cursor:pointer;z-index:3}
.lb-nav{position:absolute;top:50%;transform:translateY(-50%);background:rgba(0,0,0,.45);
  border:1px solid rgba(255,255,255,.30);color:#fff;width:46px;height:68px;border-radius:10px;
  font-size:24px;line-height:1;cursor:pointer;z-index:3;backdrop-filter:blur(6px)}
.lb-nav:hover{background:rgba(216,180,106,.30);border-color:var(--accent)}
.lb-nav.prev{left:16px}.lb-nav.next{right:16px}
.lb-nav:disabled{opacity:.2;cursor:default}
.lb-side{background:var(--panel);border-left:1px solid var(--line);overflow-y:auto;padding:26px 24px}
.lb-side h2{font-size:19px;margin:8px 0 6px;line-height:1.35}
.lb-kicker{font-size:11.5px;letter-spacing:.12em;color:var(--accent);text-transform:uppercase}
.lb-one{color:var(--muted);font-size:13px;line-height:1.75;margin:10px 0 18px}
.kv{display:grid;grid-template-columns:74px 1fr;gap:7px 10px;font-size:12.5px;
  border-top:1px solid var(--line);padding-top:16px}
.kv dt{color:var(--dim)}.kv dd{margin:0;color:var(--text);word-break:break-all}
.prompt-head{display:flex;align-items:center;justify-content:space-between;margin:22px 0 8px}
.prompt-head span{font-size:12px;color:var(--dim);letter-spacing:.08em}
.btn{background:var(--panel2);border:1px solid var(--line);color:var(--text);font-size:12px;
  padding:6px 11px;border-radius:7px;cursor:pointer}
.btn:hover{border-color:var(--accent);color:var(--accent)}
pre.prompt{white-space:pre-wrap;word-break:break-word;background:#0f1113;border:1px solid var(--line);
  border-radius:10px;padding:14px;font-size:12px;line-height:1.75;color:#cfd3d8;
  max-height:44vh;overflow:auto;margin:0;font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.placeholder{display:flex;align-items:center;justify-content:center;height:100%;
  color:#4d535b;font-size:13px;letter-spacing:.1em;
  background:repeating-linear-gradient(45deg,#15171a,#15171a 12px,#181b1f 12px,#181b1f 24px)}
footer{color:var(--dim);font-size:12px;padding:34px 0;border-top:1px solid var(--line);margin-top:30px}
@media(max-width:900px){
  .lb.on{grid-template-columns:1fr;grid-template-rows:1fr auto}
  .lb-side{max-height:46vh;border-left:0;border-top:1px solid var(--line)}
  .grid{column-width:240px;column-gap:14px}
  .wrap{padding:0 16px}
}
"""

JS = """
const DATA = __DATA__;
const GROUPS = __GROUPS__;
const PROJECTS = __PROJECTS__;
let state = {q:"", group:"", project:"", api:"", pending:false, view:[]};

const $ = s => document.querySelector(s);
const esc = s => s.replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

/* 出图 API 标签：ark / newapi / tool / 空(历史未标注) */
const API_LABEL = {ark:"ARK", newapi:"NewAPI", tool:"宿主工具"};
function apiName(it){
  if(!it.api) return "未标注";
  return API_LABEL[it.api] || it.api;
}
function apiShort(model){
  if(!model) return "";
  return model.replace(/^doubao-/, "").replace(/-\d{6}$/, "");
}
function apiText(it){
  const n = apiName(it), m = apiShort(it.apiModel);
  const base = m ? `${n} · ${m}` : n;
  return it.apiEst ? base + "（推定）" : base;
}
/* 缩略图角标：直接显示模型名（seedream-5-0-pro / gpt-image-2-c），点色代表渠道 */
function apiChip(it){
  if(!it.image) return `<span class="api-chip none">待出图</span>`;
  if(!it.api) return `<span class="api-chip none" title="无出图记录">未标注</span>`;
  const cls = it.api + (it.apiEst ? " est" : "");
  const label = apiShort(it.apiModel) || apiName(it);
  const tip = it.apiEst
    ? `推定：按图片尺寸反推（${esc(it.apiModel || it.api)}），未记录原始调用`
    : `出图 API：${apiText(it)}`;
  return `<span class="api-chip ${esc(cls)}" title="${esc(tip)}">${esc(label)}</span>`;
}
function apiTag(it){ return ""; }

function ratioClass(r){
  const t = (r||"").replace(/\s/g,"");
  return (t==="9:16"||t==="3:4") ? "portrait" : "";
}
function renderChips(){
  const g = $("#groups");
  g.innerHTML = ['<button class="chip on" data-group="">全部风格</button>']
    .concat(GROUPS.map(x=>`<button class="chip" data-group="${esc(x)}">${esc(x)}</button>`)).join("");
  g.querySelectorAll(".chip").forEach(el=>el.onclick=()=>{
    g.querySelectorAll(".chip").forEach(e=>e.classList.remove("on"));
    el.classList.add("on"); state.group = el.dataset.group; apply();
  });
}
function apply(){
  const q = state.q.trim().toLowerCase();
  state.view = DATA.filter(it=>{
    if(state.project && it.project!==state.project) return false;
    if(state.group && it.group!==state.group) return false;
    if(state.api){
      if(state.api === "none" ? !!it.api : (it.api||"") !== state.api) return false;
    }
    if(state.pending && it.image) return false;
    if(q){
      const hay = [it.id,it.style,it.one,it.subject,it.kind,it.group,
                   apiText(it)].join(" ").toLowerCase();
      if(!hay.includes(q)) return false;
    }
    return true;
  });
  const grid = $("#grid"); grid.innerHTML = state.view.map((it,i)=>card(it,i)).join("");
  grid.querySelectorAll(".card").forEach(el=>{
    el.onclick = ()=>openLb(+el.dataset.i);
  });
  $("#count").innerHTML = `共 <b>${state.view.length}</b> / ${DATA.length} 张样图`;
  $("#empty").style.display = state.view.length ? "none" : "block";
}
function card(it,i){
  const thumb = it.thumb
    ? `<img loading="lazy" src="${it.thumb}" alt="${esc(it.style + ' · ' + (it.subject||''))}">`
    : `<div class="placeholder">待出图</div>`;
  const state = it.image
    ? `<span class="state ok">已出图</span>`
    : `<span class="state pending">⏳ 待出</span>`;
  const subj = it.subject ? `<span>主体 · ${esc(it.subject)}</span>` : "";
  return `<button class="card" data-i="${i}">
    <div class="thumb ${ratioClass(it.ratio)}">
      ${thumb}
      <span class="badge">${esc(it.number||"—")} · ${esc(it.ratio||it.size)}</span>
      ${state}
      ${apiChip(it)}
    </div>
    <div class="body">
      <div class="name">${esc(it.style)}</div>
      <div class="one">${esc(it.one||"")}</div>
      <div class="meta">${subj}<span>${esc(it.project)}</span>${apiTag(it)}</div>
    </div>
  </button>`;
}
let idx = -1;
function openLb(i){
  idx = i; const it = state.view[i]; if(!it) return;
  $("#lb").classList.add("on");
  const img = $("#lbImg");
  if(it.image){ img.src = it.image; img.style.display="block"; }
  else { img.removeAttribute("src"); img.style.display="none"; }
  $("#lbNum").textContent = `第 ${i+1} / ${state.view.length} 张 · ${it.number||""}`;
  $("#lbTitle").textContent = it.style;
  $("#lbOne").textContent = it.one || "";
  $("#lbMeta").innerHTML = [
    ["编号", it.number || "—"],
    ["风格卡", "styles/" + it.kind + ".md"],
    ["测试主体", it.subject || "—"],
    ["画幅 / 尺寸", (it.ratio||"—") + " · " + (it.size||"—")],
    ["批次", it.project],
    ["出图 API", it.image ? apiText(it) : "（待出）"],
    ["出图时间", it.apiAt || "—"],
    ["文件", it.image || "（待出）"],
  ].map(([k,v])=>`<dt>${k}</dt><dd>${esc(v)}</dd>`).join("");
  $("#lbPrompt").textContent = it.prompt || "";
  $("#lbPrev").disabled = i<=0; $("#lbNext").disabled = i>=state.view.length-1;
  $("#lbOpen").href = it.image || "#";
  document.body.style.overflow = "hidden";
}
function closeLb(){ $("#lb").classList.remove("on"); document.body.style.overflow=""; idx=-1; }
function step(d){ const n = idx + d; if(n>=0 && n<state.view.length){ openLb(n); } }
$("#lbClose").onclick = closeLb;
$("#lbPrev").onclick = ()=>step(-1);
$("#lbNext").onclick = ()=>step(1);
$("#lb").onclick = e => { if(e.target.id==="lb") closeLb(); };
document.addEventListener("keydown", e=>{
  if(!$("#lb").classList.contains("on")) return;
  if(e.key==="Escape") closeLb();
  if(e.key==="ArrowLeft") step(-1);
  if(e.key==="ArrowRight") step(1);
});
$("#q").oninput = e => { state.q = e.target.value; apply(); };
$("#proj").onchange = e => { state.project = e.target.value; apply(); };
$("#apiSel").onchange = e => { state.api = e.target.value; apply(); };
$("#pend").onchange = e => { state.pending = e.target.checked; apply(); };
$("#copy").onclick = async ()=>{
  const t = $("#lbPrompt").textContent;
  try{ await navigator.clipboard.writeText(t); $("#copy").textContent="已复制"; }
  catch(e){ const r=document.createRange(); r.selectNodeContents($("#lbPrompt"));
    getSelection().removeAllRanges(); getSelection().addRange(r); document.execCommand("copy");
    $("#copy").textContent="已复制"; }
  setTimeout(()=>$("#copy").textContent="复制提示词", 1400);
};
$("#proj").innerHTML = ['<option value="">全部批次</option>']
  .concat(PROJECTS.map(p=>`<option value="${esc(p.name)}">${esc(p.name)}（${p.done}/${p.rows}）</option>`)).join("");
const API_OPTS = [["","全部 API"],["ark","ARK（火山·Seedream）"],["newapi","NewAPI（中转·gpt-image）"],
                  ["tool","宿主工具 generate_image"],["none","未标注（无记录）"]];
$("#apiSel").innerHTML = API_OPTS.map(([v,t])=>`<option value="${v}">${t}</option>`).join("");
renderChips(); apply();
const hm = location.hash.match(/^#(\d+)$/);
if(hm){ const i = +hm[1]-1; if(i>=0 && i<state.view.length) openLb(i); }
"""


def build_html(items, projects, index):
    total = len(items)
    with_img = sum(1 for x in items if x["image"])
    groups = []
    for x in items:
        if x["group"] not in groups:
            groups.append(x["group"])
    cn_order = {c: i for i, c in enumerate("一二三四五六七八九十", 1)}
    groups.sort(key=lambda g: cn_order.get(g[:1], 99))

    def js_dump(obj):
        return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")

    groups_json = js_dump(groups)
    projects_json = js_dump(projects)
    data_json = js_dump(items)
    js = JS.replace("__DATA__", data_json).replace("__GROUPS__", groups_json) \
           .replace("__PROJECTS__", projects_json)
    today = time.strftime("%Y-%m-%d %H:%M")
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>风格样图库 · cinematic-image-studio</title>
<style>{CSS}</style>
</head>
<body>
<header>
  <div class="wrap">
    <h1>风格样图库 <em>cinematic-image-studio</em></h1>
    <div class="sub">
      <b>{len(index)}</b> 张风格卡<span class="dot">·</span><b>{total}</b> 条提示词<span class="dot">·</span>
      <b>{with_img}</b> 张成图<span class="dot">·</span><b>{total - with_img}</b> 张待出
      <span class="dot">·</span>点击卡片看原图与完整提示词
      <span class="dot">·</span>更新于 {today}
    </div>
  </div>
</header>
<div class="toolbar">
  <div class="wrap">
    <label class="search">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
      <input id="q" placeholder="搜风格 / 主体 / 批次…">
    </label>
    <select id="proj"></select>
    <select id="apiSel"></select>
    <label class="count" style="display:flex;gap:7px;align-items:center;cursor:pointer">
      <input type="checkbox" id="pend"> 只看待出
    </label>
    <div class="count" id="count"></div>
  </div>
  <div class="wrap"><div class="chips" id="groups"></div></div>
</div>
<main class="wrap">
  <div class="grid" id="grid"></div>
  <div class="empty" id="empty">没有匹配的样图</div>
  <footer>
    由 <code>scripts/gallery.py</code> 生成 · 原图保持在 <code>assets/output/&lt;项目&gt;/图片/</code> ·
    缩略图在 <code>_缩略图/</code>（可随时重建）
  </footer>
</main>
<div class="lb" id="lb">
  <div class="lb-stage">
    <button class="lb-close" id="lbClose" title="关闭">✕</button>
    <button class="lb-nav prev" id="lbPrev" title="上一张">‹</button>
    <img id="lbImg" alt="">
    <button class="lb-nav next" id="lbNext" title="下一张">›</button>
  </div>
  <aside class="lb-side">
    <div class="lb-kicker" id="lbNum"></div>
    <h2 id="lbTitle"></h2>
    <p class="lb-one" id="lbOne"></p>
    <dl class="kv" id="lbMeta"></dl>
    <div class="prompt-head">
      <span>PROMPT</span>
      <div style="display:flex;gap:8px">
        <a class="btn" id="lbOpen" target="_blank" rel="noopener">原图</a>
        <button class="btn" id="copy">复制提示词</button>
      </div>
    </div>
    <pre class="prompt" id="lbPrompt"></pre>
  </aside>
</div>
<script>{js}</script>
</body>
</html>
"""


def build_readme(items, projects, index):
    with_img = sum(1 for x in items if x["image"])
    lines = [
        "# 样图库 · 索引",
        "",
        f"> 由 `scripts/gallery.py` 生成于 {time.strftime('%Y-%m-%d %H:%M')}；"
        f"共 **{len(items)}** 条提示词 / **{with_img}** 张成图（全部图片平铺在 `图片/`）。",
        "> 浏览：双击 `index.html`（列表 + 点开看原图与提示词）。",
        "> 出图 API：卡片缩略图左下角角标（`ARK` / `NewAPI` / `宿主工具` / `未标注` 历史图），"
        "顶部「全部 API」下拉可按渠道筛选；详情页显示具体模型与出图时间。",
        "> 历史图（早期未记录调用）由 `scripts/backfill_api.py` 按图片尺寸规格回填，"
        "`提示词.json` 里标 `api_estimated: true`，界面上以**虚线边框 + 详情「（推定）」**区分。",
        "",
        "## 一、批次来源",
        "",
        "| 批次 | 提示词 | 成图 | 待出 | 说明 |",
        "|---|---:|---:|---:|---|",
    ]
    notes = {
        "01-全库样图": "一风格一张的横向比稿（全库覆盖）",
        "02-厚涂52-53": "国潮厚涂 52 / 53 风格样图",
        "03-现代年轻审美": "58–65 现代年轻审美（Gen Z · 社媒）",
        "04-影像技术与材质实验": "66–75 影像技术与材质实验（蓝晒/红外/移轴/高速/故障…）",
        "51-天庭仙境-墨青": "51 卡的墨青变体（单张）",
        "51-天庭仙境-月白青瓷": "51 卡的月白青瓷变体（单张）",
    }
    for p in projects:
        lines.append(f"| `{p['name']}` | {p['rows']} | {p['done']} | {p['pending']} | "
                     f"{notes.get(p['name'], '')} |")
    lines += ["", f"## 二、全库样图覆盖（{len(index)} 张风格卡）", "",
              "| # | 风格 | 样图数 | 状态 |", "|---|---|---:|---|"]
    count_by_num = {}
    for x in items:
        if x["number"]:
            count_by_num[x["number"]] = count_by_num.get(x["number"], 0) + (1 if x["image"] else 0)
    for num in sorted(index):
        n = count_by_num.get(num, 0)
        if 54 <= int(num) <= 57:
            state = "— MV 专用（3:4，本库不出图）"
        else:
            state = "✅ 已出样图" if n else "⏳ 待出"
        lines.append(f"| {num} | {index[num]['name']} | {n} | {state} |")
    lines += [
        "",
        "## 三、目录约定",
        "",
        "```",
        "assets/output/",
        "├── index.html          # 样图库浏览页（列表 + 原图 + 提示词）",
        "├── README.md           # 本文件",
        "├── 提示词.json         # 全部提示词（每行带 project 批次）",
        "├── 提示词.md           # 人读版（提示词独立成块，可整段复制）",
        "├── 图片/               # ★ 全部输出图片（平铺，文件名 = id）",
        "└── _缩略图/            # 480px webp（可删，重建用 gallery.py）",
        "```",
        "",
        "- **kind** = 风格卡文件名去 `.md`；**id** = `kind-主体`；图片名 = `id`。",
        "- 出图：`python3 scripts/generate.py --project . --yes`（写入 `图片/`）。",
        "- 刷新人读版 / 本页：`python3 scripts/export_md.py && python3 scripts/gallery.py`。",
        "",
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force-thumbs", action="store_true")
    args = ap.parse_args()

    items, projects, index = collect(args.force_thumbs)
    if not items:
        print("[!] 没有找到任何 提示词.json")
        return 1
    os.makedirs(THUMB_ROOT, exist_ok=True)

    html_path = os.path.join(OUTPUT_ROOT, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(build_html(items, projects, index))
    readme_path = os.path.join(OUTPUT_ROOT, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(build_readme(items, projects, index))

    with_img = sum(1 for x in items if x["image"])
    missing_thumb = sum(1 for x in items if x["image"] and not x["thumb"])
    print(f"[+] {html_path}  ({len(items)} 条 / {with_img} 张图)")
    print(f"[+] {readme_path}")
    print(f"[+] 缩略图目录: {THUMB_ROOT}" + (f"  [!] {missing_thumb} 张缩略图生成失败" if missing_thumb else ""))
    print(f"[i] 缩略图工具: {thumb_tool() or '未找到 cwebp / sips（仅生成列表，不生成缩略图）'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
