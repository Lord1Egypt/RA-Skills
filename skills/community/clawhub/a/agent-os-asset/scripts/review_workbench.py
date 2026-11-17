#!/usr/bin/env python3
"""Render the reusable static Agent Asset review workbench / 渲染可复用的静态 Agent Asset review workbench。"""

from __future__ import annotations

from collections import Counter
import html
import json
from pathlib import Path
import shutil
from typing import Any


DECISION_OPTIONS = ["review", "keep", "delete", "archive_only", "generate_asset", "metadata_only"]


def shell_quote(value: str) -> str:
    return "'" + value.replace("'", "'\\''") + "'"


def is_absolute_path(value: str) -> bool:
    return Path(value).is_absolute()


def display_path(root: Path, value: str) -> str:
    path = Path(value)
    return path.as_posix() if path.is_absolute() else (root / path).as_posix()


def original_directories(root: Path, row: dict[str, Any]) -> list[str]:
    def full_relative(value: str) -> str:
        path = Path(value)
        if path.is_absolute():
            try:
                value = path.resolve(strict=False).relative_to(root.resolve()).as_posix()
            except ValueError:
                return path.as_posix()
        return f"{root.name}/{str(value).lstrip('/')}"

    explicit = [full_relative(str(value)) for value in row.get("original_directories", []) if value]
    if explicit:
        return explicit
    paths = [str(value) for value in row.get("source_paths", []) if value]
    if not paths:
        return []
    if row.get("asset_type") == "code_project":
        return [full_relative(path) for path in paths[:1]]
    return [full_relative(str(Path(path).parent) if Path(path).parent.as_posix() != "." else ".") for path in paths]


def normalized_rows(root: Path, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for index, raw in enumerate(rows, start=1):
        row = dict(raw)
        row["review_index"] = index
        row["original_directories"] = original_directories(root, row)
        output.append(row)
    return output


def summary(rows: list[dict[str, Any]]) -> dict[str, int]:
    statuses = Counter(str(row.get("index_status", "candidate")) for row in rows)
    return {
        "assets": len(rows),
        "candidate": statuses["candidate"],
        "final": statuses["final"],
        "excluded": statuses["excluded"],
        "pii": sum(str(row.get("privacy", "")) == "pii" for row in rows),
    }


def shortcut_available() -> bool:
    executable = shutil.which("shortcuts")
    if not executable:
        return False
    try:
        import subprocess

        result = subprocess.run([executable, "list"], text=True, capture_output=True, check=False, timeout=3)
    except (OSError, subprocess.SubprocessError):
        return False
    return result.returncode == 0 and "OpenAgentAssetFile" in result.stdout.splitlines()


def static_apply_command(root: Path, scope: str, adapter_path: Path, pipeline_path: Path) -> str:
    downloads = Path.home() / "Downloads"
    return "\n".join(
        [
            f"cd {shell_quote(root.as_posix())}",
            (
                f"latest_decisions=$(find {shell_quote(downloads.as_posix())} "
                "-maxdepth 1 -name 'asset-decisions*.json' -type f -print0 | xargs -0 ls -t | head -n 1)"
            ),
            (
                f"python3 {shell_quote(pipeline_path.as_posix())} --root {shell_quote(root.as_posix())} "
                f"--scope {shell_quote(scope)} --cleanup-tool {shell_quote(adapter_path.as_posix())} "
                '--stage apply --decisions "$latest_decisions" --execute-decisions'
            ),
        ]
    )


def render_workbench(
    *,
    root: Path,
    scope: str,
    rows: list[dict[str, Any]],
    adapter_path: Path,
    pipeline_path: Path,
    shortcut_available: bool,
) -> str:
    assets = normalized_rows(root, rows)
    payload = {
        "root": root.as_posix(),
        "scope": scope,
        "assets": assets,
        "summary": summary(assets),
        "shortcut_available": shortcut_available,
        "static_apply_command": static_apply_command(root, scope, adapter_path, pipeline_path),
    }
    json_payload = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "\\u003c!--")
    title = html.escape(f"Agent Asset Review Workbench · {scope}")
    shortcut_label = "Open via Shortcut / 通过快捷指令打开" if shortcut_available else ""
    return HTML_TEMPLATE.replace("__TITLE__", title).replace("__PAYLOAD__", json_payload).replace("__SHORTCUT_LABEL__", shortcut_label)


def write_workbench(
    *,
    root: Path,
    scope_path: Path,
    scope: str,
    rows: list[dict[str, Any]],
    adapter_path: Path,
    pipeline_path: Path,
) -> Path:
    output = scope_path / "cleanup-asset-review-workbench.html"
    output.write_text(
        render_workbench(
            root=root,
            scope=scope,
            rows=rows,
            adapter_path=adapter_path,
            pipeline_path=pipeline_path,
            shortcut_available=shortcut_available(),
        ),
        encoding="utf-8",
    )
    return output


HTML_TEMPLATE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="review-token" content="">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root { --paper:#f4f0e8; --panel:#fffdf8; --ink:#172b3a; --muted:#64727c; --line:#d9d2c6; --blue:#155d7a; --gold:#a26716; --red:#a43832; --green:#196c45; --shadow:0 10px 28px rgba(35,48,57,.10); --w-index:54px; --w-select:64px; --w-decision:156px; --w-pii:116px; }
* { box-sizing:border-box; } body { margin:0; color:var(--ink); background:linear-gradient(90deg,rgba(21,93,122,.04) 1px,transparent 1px) 0 0/28px 28px,var(--paper); font:14px/1.45 ui-rounded,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif; }
header { padding:28px clamp(18px,4vw,54px) 22px; background:var(--ink); color:#fff; border-bottom:4px solid var(--gold); } h1 { margin:0; font-size:clamp(23px,3vw,34px); letter-spacing:.02em; } .subtitle { margin-top:7px; color:#c8d6dc; } main { padding:20px clamp(18px,4vw,54px) 42px; }
.stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(120px,1fr)); gap:10px; margin-bottom:14px; } .stat { padding:12px 14px; background:var(--panel); border:1px solid var(--line); border-radius:12px; box-shadow:var(--shadow); } .stat b { display:block; margin-top:2px; font:700 25px/1.1 ui-monospace,"SFMono-Regular",monospace; color:var(--blue); } .muted { color:var(--muted); font-size:12px; }
.toolbar { position:sticky; top:0; z-index:8; display:flex; flex-wrap:wrap; gap:9px; align-items:end; padding:11px 12px; margin:0 -4px 14px; background:rgba(255,253,248,.96); border:1px solid var(--line); border-radius:12px; box-shadow:var(--shadow); backdrop-filter:blur(10px); } input,select,button,textarea { font:inherit; } input:not(.row-select),select,button { min-height:34px; border:1px solid #bdb6ac; border-radius:7px; padding:6px 9px; background:#fffefa; color:var(--ink); } input:not(.row-select) { min-width:230px; flex:1 1 250px; } button { cursor:pointer; font-weight:650; } button:hover { border-color:var(--blue); background:#eaf3f4; } .primary { background:var(--blue); color:white; border-color:var(--blue); } .danger { color:var(--red); } .toolbar-section { display:flex; gap:7px; align-items:end; flex-wrap:wrap; } .toolbar-label { color:var(--muted); font-size:11px; font-weight:800; letter-spacing:.05em; padding:0 2px 8px; } .toolbar-divider { align-self:stretch; width:1px; background:var(--line); margin:0 2px; } .filter-control { display:grid; gap:2px; color:var(--muted); font-size:11px; font-weight:750; } .filter-control select { min-width:112px; }
.table-shell { max-height:calc(100vh - 276px); overflow:auto; position:relative; border:1px solid var(--line); border-radius:12px; box-shadow:var(--shadow); background:var(--panel); overscroll-behavior:contain; scrollbar-gutter:stable both-edges; } table { width:100%; min-width:1750px; table-layout:fixed; border-collapse:separate; border-spacing:0; } col.col-index { width:var(--w-index); } col.col-select { width:var(--w-select); } col.col-decision { width:var(--w-decision); } col.col-pii { width:var(--w-pii); } col.col-suggestion { width:235px; } col.col-type { width:100px; } col.col-directory { width:270px; } col.col-title { width:340px; } col.col-actions { width:205px; } col.col-insights { width:270px; } th,td { padding:9px 10px; border-bottom:1px solid #ebe5db; vertical-align:top; text-align:left; background:var(--panel); } th { position:sticky; top:0; z-index:3; background:#e5edf0; color:#123649; font-size:12px; } tr:hover td { background:#f9f5ed; }
.frozen-index,.frozen-select,.frozen-decision,.frozen-pii { position:sticky; z-index:4; box-shadow:1px 0 0 #d7d0c4; } th.frozen-index,th.frozen-select,th.frozen-decision,th.frozen-pii { z-index:6; background:#dce8ec; } .frozen-index { left:0; width:var(--w-index); } .frozen-select { left:var(--w-index); width:var(--w-select); } .frozen-decision { left:calc(var(--w-index) + var(--w-select)); width:var(--w-decision); } .frozen-pii { left:calc(var(--w-index) + var(--w-select) + var(--w-decision)); width:var(--w-pii); } tbody tr:hover .frozen-index,tbody tr:hover .frozen-select,tbody tr:hover .frozen-decision,tbody tr:hover .frozen-pii { background:#f9f5ed; }
.frozen-select { text-align:center; } .selection-control { display:grid; place-items:center; width:100%; min-height:30px; cursor:pointer; } .row-select { appearance:auto; -webkit-appearance:checkbox; width:20px; height:20px; min-width:20px; min-height:20px; margin:0; padding:0; display:block; flex:none; accent-color:var(--blue); cursor:pointer; }
code { font:12px/1.35 ui-monospace,"SFMono-Regular",monospace; overflow-wrap:anywhere; } .path-full { display:block; max-width:260px; color:#334b59; } .pill { display:inline-block; padding:2px 8px; border-radius:999px; background:#e5edf0; color:#123649; font-size:12px; } .suggestion { min-width:0; } .decision-pill { display:inline-block; padding:2px 8px; border-radius:999px; background:#e5edf0; font-weight:750; } .decision-pill.keep { background:#dff2e7; color:var(--green); } .decision-pill.generate_asset { background:#fff0cd; color:#7c4c00; } .decision-pill.archive_only { background:#eee7f5; color:#634188; } .decision-pill.delete { background:#f8dedb; color:var(--red); } .suggestion-meta { color:var(--muted); font-size:11px; margin-left:5px; } .suggestion-reason { margin-top:5px; display:-webkit-box; -webkit-box-orient:vertical; -webkit-line-clamp:2; overflow:hidden; } .evidence { margin-top:5px; color:var(--muted); font-size:11px; } .evidence summary { cursor:pointer; color:var(--blue); font-weight:700; } .evidence ul { padding-left:16px; margin:5px 0 0; }
.asset-actions { display:grid; gap:5px; } .action-row { display:flex; align-items:center; gap:5px; min-width:0; } .action-label { flex:0 0 38px; color:var(--muted); font-size:11px; font-weight:800; } .file-link,.copy-open { display:inline-block; margin:0; padding:4px 6px; border:1px solid #bdd1d8; border-radius:6px; background:#f4fafb; color:var(--blue); text-decoration:none; font-size:12px; } .file-link.source { color:var(--green); } .file-link.semantic { color:var(--gold); } .file-link.shortcut { color:#6a3e78; } .copy-open { cursor:pointer; color:var(--ink); background:#fffefa; }
.summary,.insights { display:-webkit-box; -webkit-box-orient:vertical; -webkit-line-clamp:3; overflow:hidden; } textarea { width:100%; min-height:180px; margin-top:14px; border:1px solid var(--line); border-radius:10px; padding:10px; background:#152631; color:#e6f2f5; font:12px/1.4 ui-monospace,"SFMono-Regular",monospace; }
@media (max-width:700px) { header { padding:22px 18px; } main { padding:16px 12px 28px; } .toolbar { top:0; border-radius:0; margin:0 -12px 12px; } th { top:0; } }
</style>
</head>
<body>
<header><h1>Agent Asset Review Workbench / Agent Asset 审查工作台</h1><div class="subtitle">Independent asset review ledger; static pages only download or copy commands, while localhost mode may save and apply / 独立资产审查台账；静态页面只下载或复制命令，localhost 模式才允许保存和执行。</div></header>
<main>
  <section id="stats" class="stats"></section>
  <div class="toolbar">
    <input id="search" placeholder="Search title/path/summary/insight" aria-label="Search assets">
    <div class="toolbar-section"><span class="toolbar-label">Filters / 筛选</span>
      <label class="filter-control"><span>Status / 状态</span><select id="filterStatus" aria-label="Filter index status"><option value="">All / 全部</option><option value="candidate">candidate</option><option value="final">final</option><option value="excluded">excluded</option></select></label>
      <label class="filter-control"><span>Suggestion / 建议</span><select id="filterSuggestion" aria-label="Filter suggestion"><option value="">All / 全部</option></select></label>
      <label class="filter-control"><span>Decision</span><select id="filterDecision" aria-label="Filter decision"><option value="">All / 全部</option></select></label>
      <label class="filter-control"><span>PII</span><select id="filterPii" aria-label="Filter PII"><option value="">All / 全部</option><option value="unknown">unknown</option><option value="pii">PII</option><option value="non_pii">non-PII</option></select></label>
      <label class="filter-control"><span>File type / 文件类型</span><select id="filterFileType" aria-label="Filter file type"><option value="">All / 全部</option></select></label>
    </div>
    <span class="toolbar-divider"></span>
    <div class="toolbar-section"><span class="toolbar-label">Batch / 批量</span>
      <label class="filter-control"><span>Decision</span><select id="batchDecision" aria-label="Batch decision"><option value="">No change / 不改</option></select></label>
      <label class="filter-control"><span>PII</span><select id="batchPii" aria-label="Batch PII"><option value="">No change / 不改</option><option value="unknown">unknown</option><option value="pii">PII</option><option value="non_pii">non-PII</option></select></label>
      <button id="selectVisible">Select all / 全选</button><button id="invertVisible">Invert / 反选</button><button id="clearSelection">Clear selection / 清空选择</button><button id="applySelected" class="primary">Apply to selected / 应用到已选</button>
    </div>
    <span class="toolbar-divider"></span>
    <div class="toolbar-section"><button id="saveJson">Download decisions.json / 下载 decisions.json</button><button id="executeDecisions" class="danger">Download and copy command / 下载并复制命令</button><span id="selectionCount" class="muted"></span><span id="openStatus" class="muted"></span></div>
  </div>
  <div class="table-shell"><table><colgroup><col class="col-index"><col class="col-select"><col class="col-decision"><col class="col-pii"><col class="col-suggestion"><col class="col-type"><col class="col-directory"><col class="col-title"><col class="col-actions"><col class="col-insights"></colgroup><thead><tr><th class="frozen-index">No. / 编号</th><th class="frozen-select">Select / 选择</th><th class="frozen-decision">Decision / 决策</th><th class="frozen-pii">PII</th><th>Suggestion / 建议</th><th>File type / 文件类型</th><th>Original directory / 材料原始目录</th><th>Title / Summary</th><th>Original + Agent</th><th>Insights / 洞察</th></tr></thead><tbody id="rows"></tbody></table></div>
  <textarea id="exportBox" readonly aria-label="decisions JSON preview"></textarea>
</main>
<script id="asset-data" type="application/json">__PAYLOAD__</script>
<script>
const DATA = JSON.parse(document.getElementById('asset-data').textContent);
const OPTIONS = ['review','keep','delete','archive_only','generate_asset','metadata_only'];
const decisions = new Map(), piiLabels = new Map(), selected = new Set(); let query = '', statusFilter = '', suggestionFilter = '', decisionFilter = '', piiFilter = '', fileTypeFilter = '';
const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const isStatic = () => location.protocol === 'file:';
const isAbsolute = path => String(path || '').startsWith('/');
const absolutePath = path => isAbsolute(path) ? String(path) : `${String(DATA.root || '').replace(/\/$/,'')}/${String(path || '').replace(/^\//,'')}`;
const fileUrl = path => `file://${absolutePath(path).split('/').map(encodeURIComponent).join('/')}`;
const quoteShell = value => `'${String(value).replaceAll("'", "'\\''")}'`;
const openCommand = path => `open ${quoteShell(absolutePath(path))}`;
const defaultDecision = row => row.review_decision || row.suggested_decision || (row.index_status === 'final' ? 'keep' : 'review');
const defaultPii = row => row.review_pii_label || row.suggested_pii_label || row.privacy || 'unknown';
const effectiveDecision = row => decisions.get(row.asset_id) || defaultDecision(row);
const effectivePii = row => piiLabels.get(row.asset_id) || defaultPii(row);
const sourceTypes = row => [...new Set((row.source_formats || []).filter(Boolean).map(value => String(value).toLowerCase()))];
const visibleRows = () => DATA.assets.filter(row => (!query || JSON.stringify(row).toLowerCase().includes(query)) && (!statusFilter || row.index_status === statusFilter) && (!suggestionFilter || row.suggested_decision === suggestionFilter) && (!decisionFilter || effectiveDecision(row) === decisionFilter) && (!piiFilter || effectivePii(row) === piiFilter) && (!fileTypeFilter || sourceTypes(row).includes(fileTypeFilter)));
function copyText(value) { if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(value); const box=document.createElement('textarea'); box.value=value; box.style.cssText='position:fixed;left:-9999px'; document.body.appendChild(box); box.select(); document.execCommand('copy'); box.remove(); return Promise.resolve(); }
function suggestion(row) { if (!row.suggested_decision) return '<span class="muted">no suggestion</span>'; const reason=row.suggestion_reason||row.reason||''; const signals=row.suggestion_signals||[]; const evidence=signals.length ? `<details class="evidence"><summary>Evidence / 证据 ${signals.length}</summary><ul>${signals.map(item=>`<li>${esc(item)}</li>`).join('')}</ul></details>` : ''; return `<div class="suggestion"><span class="decision-pill ${esc(row.suggested_decision)}">${esc(row.suggested_decision)}</span><span class="suggestion-meta">${esc(row.suggestion_confidence||'')} ${row.suggestion_score ? '· '+esc(row.suggestion_score) : ''}</span><div class="suggestion-reason" title="${esc(reason)}">${esc(reason)}</div>${evidence}</div>`; }
function actionRow(path,label,kind) { if (!path) return ''; const shortcut = DATA.shortcut_available ? `<a class="file-link shortcut" href="shortcuts://run-shortcut?name=OpenAgentAssetFile&input=text&text=${encodeURIComponent(absolutePath(path))}">__SHORTCUT_LABEL__</a>` : ''; return `<div class="action-row"><span class="action-label">${esc(label)}</span><a href="${esc(fileUrl(path))}" target="_blank" rel="noopener" class="file-link ${esc(kind)} open-file" data-path="${esc(path)}">Open / 打开</a>${shortcut}<button type="button" class="copy-open" data-command="${esc(openCommand(path))}">Copy / 复制</button></div>`; }
function paths(row) { const source=(row.source_paths||[]).map((value,index)=>actionRow(value,index ? 'Source / 源'+(index+1) : 'Original / 原始','source')).join(''); const semantic=(row.semantic_paths||[]).map((value,index)=>actionRow(value,index ? 'Agent '+(index+1) : 'Agent','semantic')).join(''); const ledger=row.member_ledger_path ? actionRow(row.member_ledger_path,'Members / 成员','semantic') : ''; return `<div class="asset-actions">${source || ''}${semantic || ''}${ledger}${!source && !semantic && !ledger ? '<span class="muted">no files</span>' : ''}</div>`; }
function selectDecision(row) { const value=effectiveDecision(row); return `<select class="decision" data-id="${esc(row.asset_id)}">${OPTIONS.map(option=>`<option value="${option}" ${option===value?'selected':''}>${option}</option>`).join('')}</select>`; }
function selectPii(row) { const value=effectivePii(row); return `<select class="pii" data-id="${esc(row.asset_id)}">${['unknown','pii','non_pii'].map(option=>`<option value="${option}" ${option===value?'selected':''}>${option}</option>`).join('')}</select>`; }
function fileType(row) { const formats=[...(row.source_formats||[])].filter(Boolean); return `<span class="pill">${esc([...new Set(formats.map(value=>String(value).toUpperCase()))].join(' / ') || '—')}</span>`; }
function renderStats() { document.getElementById('stats').innerHTML=Object.entries(DATA.summary).map(([key,value])=>`<div class="stat"><span class="muted">${esc(key)}</span><b>${esc(value)}</b></div>`).join(''); }
function decisionRows() { return DATA.assets.map(row=>({review_index:row.review_index,asset_id:row.asset_id,path:row.path||'',source_paths:row.source_paths||[],semantic_paths:row.semantic_paths||[],decision:effectiveDecision(row),asset_mode:effectiveDecision(row),pii_label:effectivePii(row),category:row.review_decision?'user_review':(row.suggested_decision?'kb_review_suggestion':''),reason:row.review_reason||row.suggestion_reason||row.reason||''})); }
function jsonExport() { return JSON.stringify({scope:DATA.scope,decisions:decisionRows()},null,2); }
function updateExport() { document.getElementById('exportBox').value=jsonExport(); }
function renderRows() { const rows=visibleRows(); document.getElementById('rows').innerHTML=rows.map(row=>{const bundle=row.asset_type==='data_bundle' ? `<span class="muted">Members / 成员 ${esc(row.member_count||0)} · ${esc(Object.entries(row.format_counts||{}).map(([k,v])=>`${k}=${v}`).join(', '))}</span>` : ''; return `<tr><td class="frozen-index"><b>${esc(row.review_index)}</b></td><td class="frozen-select"><label class="selection-control" title="Select / 选择 ${esc(row.title||row.asset_id)}"><input class="row-select" type="checkbox" aria-label="Select asset / 选择资产 ${esc(row.title||row.asset_id)}" data-id="${esc(row.asset_id)}" ${selected.has(row.asset_id)?'checked':''}></label></td><td class="frozen-decision">${selectDecision(row)}</td><td class="frozen-pii">${selectPii(row)}</td><td>${suggestion(row)}</td><td>${fileType(row)}</td><td>${(row.original_directories||[]).map(value=>`<code class="path-full" title="${esc(value)}">${esc(value)}</code>`).join('<br>') || '<span class="muted">unknown</span>'}</td><td><b>${esc(row.title||'')}</b><div class="summary">${esc(row.summary||'')}</div>${bundle}</td><td>${paths(row)}</td><td><div class="insights">${(row.insights||[]).map(esc).join('<br>')}</div></td></tr>`;}).join(''); document.getElementById('selectionCount').textContent=`${selected.size} selected · ${rows.length}/${DATA.assets.length} visible`; updateExport(); }
function downloadDecisions() { const blob=new Blob([jsonExport()],{type:'application/json'}); const anchor=document.createElement('a'); anchor.href=URL.createObjectURL(blob); anchor.download='asset-decisions.json'; anchor.click(); setTimeout(()=>URL.revokeObjectURL(anchor.href),0); }
async function postJson(path, payload) { const token=document.querySelector('meta[name="review-token"]')?.content; if(!token)throw new Error('Open through the local review server or use static downloads / 请通过本地工作台服务打开，或使用静态下载模式'); const response=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json','X-Review-Token':token},body:payload===undefined?jsonExport():JSON.stringify(payload)}); const text=await response.text(); let data={}; try { data=JSON.parse(text); } catch (_) { data={error:text}; } if (!response.ok) throw new Error(data.error||text); return data; }
function updateModeLabels() { const save=document.getElementById('saveJson'), execute=document.getElementById('executeDecisions'); if (isStatic()) { save.textContent='Download decisions.json / 下载 decisions.json'; execute.textContent='Download and copy command / 下载并复制命令'; } else { save.textContent='Save decisions.json / 保存 decisions.json'; execute.textContent='Apply review results / 执行 review 结果'; } }
function appendOptions(id, values) { const select=document.getElementById(id); values.forEach(value=>select.append(new Option(value,value))); }
document.getElementById('search').addEventListener('input', event=>{query=event.target.value.toLowerCase();renderRows();});
appendOptions('filterSuggestion', [...new Set(DATA.assets.map(row=>row.suggested_decision).filter(Boolean))]);
appendOptions('filterDecision', OPTIONS);
appendOptions('filterFileType', [...new Set(DATA.assets.flatMap(sourceTypes))].sort());
appendOptions('batchDecision', OPTIONS);
document.getElementById('filterStatus').addEventListener('change', event=>{statusFilter=event.target.value;renderRows();});
document.getElementById('filterSuggestion').addEventListener('change', event=>{suggestionFilter=event.target.value;renderRows();});
document.getElementById('filterDecision').addEventListener('change', event=>{decisionFilter=event.target.value;renderRows();});
document.getElementById('filterPii').addEventListener('change', event=>{piiFilter=event.target.value;renderRows();});
document.getElementById('filterFileType').addEventListener('change', event=>{fileTypeFilter=event.target.value;renderRows();});
document.getElementById('selectVisible').onclick=()=>{visibleRows().forEach(row=>selected.add(row.asset_id));renderRows();}; document.getElementById('invertVisible').onclick=()=>{visibleRows().forEach(row=>selected.has(row.asset_id)?selected.delete(row.asset_id):selected.add(row.asset_id));renderRows();}; document.getElementById('clearSelection').onclick=()=>{selected.clear();renderRows();}; document.getElementById('applySelected').onclick=()=>{const decision=document.getElementById('batchDecision').value, pii=document.getElementById('batchPii').value; DATA.assets.filter(row=>selected.has(row.asset_id)).forEach(row=>{if(decision)decisions.set(row.asset_id,decision);if(pii)piiLabels.set(row.asset_id,pii);});renderRows();};
document.addEventListener('change', event=>{const node=event.target; if(node.classList.contains('row-select')) { node.checked?selected.add(node.dataset.id):selected.delete(node.dataset.id); renderRows(); } if(node.classList.contains('decision')) { decisions.set(node.dataset.id,node.value); renderRows(); } if(node.classList.contains('pii')) { piiLabels.set(node.dataset.id,node.value); renderRows(); }});
document.addEventListener('click', event=>{const copy=event.target.closest('.copy-open'); if(copy){event.preventDefault();copyText(copy.dataset.command).then(()=>document.getElementById('openStatus').textContent='Copied open command / 已复制 open 命令');return;} const link=event.target.closest('.open-file'); if(!link || isStatic())return; event.preventDefault(); postJson('/__open',{path:link.dataset.path}).then(()=>document.getElementById('openStatus').textContent='Opened / 已打开').catch(()=>document.getElementById('openStatus').textContent='Open failed; copy the open command / 打开失败；请复制 open 命令');});
document.getElementById('saveJson').onclick=()=>{if(isStatic()){downloadDecisions();document.getElementById('openStatus').textContent='Downloaded decisions.json / 已下载 decisions.json';return;}postJson('/__save_decisions').then(data=>document.getElementById('openStatus').textContent=`saved: ${data.path||''}`).catch(error=>document.getElementById('openStatus').textContent=error.message);};
document.getElementById('executeDecisions').onclick=()=>{if(isStatic()){downloadDecisions();copyText(DATA.static_apply_command).then(()=>document.getElementById('openStatus').textContent='Downloaded JSON and copied the apply command / 已下载 JSON，并复制执行命令');return;}if(!confirm('Apply current review results? delete moves files to system Trash. / 执行当前 review 结果？delete 会移动到系统 Trash。'))return;postJson('/__apply_decisions').then(data=>{const apply=data.apply||{};const postIndex=apply.post_apply_index||{};const indexText=postIndex.status?` · index ${postIndex.status}`:'';document.getElementById('openStatus').textContent=`Applied and rewrote workbench / 已执行并回写 workbench${indexText}`;if(apply.workbench)window.setTimeout(()=>window.location.reload(),450);}).catch(error=>document.getElementById('openStatus').textContent=error.message);};
renderStats(); renderRows(); updateModeLabels();
</script>
</body>
</html>'''
