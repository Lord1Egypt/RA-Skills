#!/usr/bin/env python3
"""
rule_editor.py - Zero-code visual rule editor (BidHunter v1.5, A10 + rule editor).

A lightweight local HTTP server (Python stdlib only, no pip install) that lets
non-technical users edit qual_rules.json in a browser, load industry templates,
live-test a title against the rules, and validate before saving.

Usage:
  python3 rule_editor.py [--port 8080] [--rules <path/to/qual_rules.json>]
  Then open http://localhost:8080

Features:
  - Edit entities (name + capability keywords), red_alerts, region priority
  - Load industry template (能源/建筑/IT/市政) as a starting point
  - Live-test: paste a title, see verdict + score instantly
  - Validate rules health before saving
  - Save back to qual_rules.json (atomic write + backup)
"""
import os
import sys
import json
import argparse
import subprocess
import shutil
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RULES_PATH = os.path.join(SCRIPT_DIR, "qual_rules.json")
PORT = 8080

# ---- Industry template presets (A10) ----
TEMPLATES = {
    "能源": {
        "name": "能源行业模板",
        "entities": {
            "energy_eng": {"name": "能源工程主体", "capabilities": ["电力", "电气", "油气", "管道", "新能源", "光伏", "风电", "储能", "输变电", "自动化"]},
            "energy_svc": {"name": "能源服务主体", "capabilities": ["运维", "检修", "调试", "安装", "设备", "系统集成"]},
        },
        "red_alerts": ["建筑施工", "消防", "危险品", "爆破", "特种设备", "压力容器", "劳务派遣", "医疗器械"],
        "region_priority": {"high": ["天津", "青岛", "深圳"], "note": "按需修改"},
    },
    "建筑": {
        "name": "建筑工程模板",
        "entities": {
            "build_main": {"name": "建筑工程主体", "capabilities": ["土建", "施工", "装修", "幕墙", "钢结构", "市政", "道路", "桥梁"]},
            "build_deco": {"name": "装饰装修主体", "capabilities": ["装修", "装饰", "设计", "展示", "标识"]},
        },
        "red_alerts": ["消防", "爆破", "劳务派遣", "医疗器械", "房地产开发", "勘探"],
        "region_priority": {"high": ["北京", "上海", "广州"], "note": "按需修改"},
    },
    "IT": {
        "name": "IT软件模板",
        "entities": {
            "it_dev": {"name": "软件开发主体", "capabilities": ["软件", "系统", "平台", "开发", "运维", "云", "数据", "信息化", "网络安全"]},
            "it_equip": {"name": "IT设备主体", "capabilities": ["设备", "器材", "集成", "自动化", "信息技术"]},
        },
        "red_alerts": ["劳务派遣", "电信", "互联网信息服务", "测绘"],
        "region_priority": {"high": ["杭州", "深圳", "成都"], "note": "按需修改"},
    },
    "市政": {
        "name": "市政公用模板",
        "entities": {
            "municipal": {"name": "市政公用主体", "capabilities": ["市政", "道路", "桥梁", "给排水", "环卫", "绿化", "照明", "公园"]},
        },
        "red_alerts": ["建筑施工", "消防", "爆破", "劳务派遣", "危险品"],
        "region_priority": {"high": ["成都", "重庆", "武汉"], "note": "按需修改"},
    },
}


def load_rules(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rules(path, data):
    backup = path + ".bak"
    if os.path.exists(path):
        shutil.copy2(path, backup)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def run_validate(path):
    r = subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, "qual_check.py"),
                        "--validate-rules", path], capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def run_test(title, rules_tmp):
    import tempfile
    tmp = os.path.join(tempfile.gettempdir(), ".editor_test_rules.json")
    save_rules(tmp, rules_tmp)
    # build a one-line cache
    cache = os.path.join(tempfile.gettempdir(), ".editor_test_cache.jsonl")
    with open(cache, "w", encoding="utf-8") as f:
        f.write(json.dumps({"title": title, "url": "", "id": "test"}) + "\n")
    r = subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, "qual_check.py"),
                        cache, tmp], capture_output=True, text=True)
    try:
        out = json.loads(r.stdout.strip().splitlines()[-1])
        return {"verdict": out.get("verdict"), "score": out.get("score"),
                "level": out.get("score_level"), "reason": out.get("reason"),
                "matched": out.get("matched_capabilities", [])}
    except Exception:
        return {"verdict": "error", "reason": r.stderr[:200]}


# ---- Frontend (embedded) ----
PAGE = r"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>标讯猎手 · 规则编辑器</title>
<style>
*{{box-sizing:border-box}}body{{font-family:-apple-system,"PingFang SC",sans-serif;margin:0;background:#f1f5f9;color:#1e293b}}
header{{background:#0f172a;color:#fff;padding:14px 20px;font-size:16px;font-weight:700}}
.wrap{{max-width:980px;margin:16px auto;padding:0 16px}}
.card{{background:#fff;border-radius:10px;padding:16px 18px;margin-bottom:14px;box-shadow:0 1px 3px rgba(0,0,0,.08)}}
h3{{margin:0 0 10px;font-size:15px;color:#0f172a}}
.row{{margin-bottom:12px}}
label{{display:block;font-size:13px;color:#475569;margin-bottom:4px;font-weight:600}}
input[type=text],textarea{{width:100%;border:1px solid #cbd5e1;border-radius:6px;padding:8px;font-size:13px;font-family:inherit}}
textarea{{min-height:70px;resize:vertical}}
.ent{{border:1px solid #e2e8f0;border-radius:8px;padding:10px;margin-bottom:10px;background:#f8fafc}}
.ent .ename{{font-weight:700;margin-bottom:6px}}
button{{background:#2563eb;color:#fff;border:0;border-radius:6px;padding:8px 16px;font-size:13px;cursor:pointer;margin-right:8px}}
button.ghost{{background:#e2e8f0;color:#1e293b}}
button.green{{background:#16a34a}}
.tpl{{display:inline-block;background:#e0e7ff;color:#3730a3;border-radius:6px;padding:6px 12px;margin:0 6px 6px 0;cursor:pointer;font-size:13px}}
#result{{font-size:13px;white-space:pre-wrap;background:#f8fafc;border-radius:6px;padding:10px;min-height:40px}}
.badge{{display:inline-block;padding:2px 10px;border-radius:4px;color:#fff;font-size:12px;font-weight:600}}
.ok{{background:#16a34a}}.warn{{background:#d97706}}.err{{background:#dc2626}}
.hint{{font-size:12px;color:#64748b;margin-top:6px}}
</style></head><body>
<header>标讯猎手 · 规则编辑器 <span style="font-weight:400;font-size:12px;opacity:.7">（v1.5 零代码配规则）</span></header>
<div class="wrap">
  <div class="card">
    <h3>① 选行业模板起步（可选）</h3>
    <div id="tpls"></div>
    <div class="hint">点模板会把能力词/红警/地区预填到下方，你再按营业执照微调。</div>
  </div>
  <div class="card">
    <h3>② 投标主体与能力词</h3>
    <div id="entities"></div>
    <button class="ghost" onclick="addEnt()">+ 新增主体</button>
  </div>
  <div class="card">
    <h3>③ 红色预警（不可投类型）</h3>
    <div class="row"><label>逗号分隔</label><textarea id="red_alerts"></textarea></div>
  </div>
  <div class="card">
    <h3>④ 重点跟进地区</h3>
    <div class="row"><label>逗号分隔，如 天津,青岛,深圳</label><textarea id="region_high" style="min-height:40px"></textarea></div>
  </div>
  <div class="card">
    <h3>⑤ 保存前自检 & 实时试标</h3>
    <div class="row"><label>粘贴一条公告标题测试</label><input type="text" id="test_title" placeholder="如：天津港区视频制作服务项目招标公告"></div>
    <button onclick="testTitle()">试标</button>
    <button class="ghost" onclick="validateRules()">校验规则</button>
    <div id="result" style="margin-top:10px"></div>
  </div>
  <div class="card">
    <button class="green" onclick="saveRules()">💾 保存规则</button>
    <button class="ghost" onclick="location.reload()">放弃改动</button>
    <div class="hint">保存会覆盖 qual_rules.json 并自动备份上一份。</div>
  </div>
</div>
<script>
let RULES={{RULES_JSON}};
function esc(s){{return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;')}}
function renderEntities(){{
  const box=document.getElementById('entities');box.innerHTML='';
  for(const [id,e] of Object.entries(RULES.entities||{{}})){{
    const d=document.createElement('div');d.className='ent';
    d.innerHTML=`<div class="ename">主体ID: <input type="text" value="${{esc(id)}}" onchange="renameEnt(this,'${{esc(id)}}')" style="width:200px;display:inline-block"> 名称: <input type="text" value="${{esc(e.name)}}" data-k="name" style="width:240px;display:inline-block"></div>
    <div class="row"><label>能力词（逗号分隔）</label><textarea data-k="caps">${{esc((e.capabilities||[]).join(', '))}}</textarea></div>`;
    box.appendChild(d);
  }}
}}
function renameEnt(inp,oldId){{
  const v=inp.value.trim();if(!v||v===oldId)return;
  const e=RULES.entities[oldId];delete RULES.entities[oldId];RULES.entities[v]=e;inp.onchange=null;renderEntities();
}}
function addEnt(){{
  let i=1;while(RULES.entities['entity_'+i])i++;
  RULES.entities['entity_'+i]={{name:'新主体',capabilities:[]}};renderEntities();
}}
function collect(){{
  // entities
  const ents={{}};
  document.querySelectorAll('#entities .ent').forEach(d=>{{
    const id=d.querySelector('input').value.trim();
    const name=d.querySelector('[data-k=name]').value.trim();
    const caps=d.querySelector('[data-k=caps]').value.split(/[,\n]/).map(s=>s.trim()).filter(Boolean);
    if(id)ents[id]={{name:name,capabilities:caps}};
  }});
  RULES.entities=ents;
  RULES.red_alerts=document.getElementById('red_alerts').value.split(/[,\n]/).map(s=>s.trim()).filter(Boolean);
  RULES.region_priority=RULES.region_priority||{{}};
  RULES.region_priority.high=document.getElementById('region_high').value.split(/[,\n]/).map(s=>s.trim()).filter(Boolean);
  return RULES;
}}
function loadTpls(){{
  fetch('/api/templates').then(r=>r.json()).then(ts=>{{
    const box=document.getElementById('tpls');box.innerHTML='';
    ts.forEach(t=>{{const s=document.createElement('span');s.className='tpl';s.textContent=t;s.onclick=()=>applyTpl(t);box.appendChild(s);}});
  }});
}}
function applyTpl(name){{
  fetch('/api/template/'+encodeURIComponent(name)).then(r=>r.json()).then(t=>{{
    RULES.entities=t.entities;RULES.red_alerts=t.red_alerts;
    RULES.region_priority=RULES.region_priority||{{}};RULES.region_priority.high=t.region_priority.high;
    document.getElementById('red_alerts').value=(t.red_alerts||[]).join(', ');
    document.getElementById('region_high').value=(t.region_priority.high||[]).join(', ');
    renderEntities();
  }});
}}
function testTitle(){{
  const title=document.getElementById('test_title').value;if(!title)return;
  fetch('/api/test',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{title:title,rules:collect()}})
  }).then(r=>r.json()).then(d=>{{
    const col=d.verdict==='investable'?'ok':(d.verdict==='needs_review'?'warn':'err');
    document.getElementById('result').innerHTML=`<span class="badge ${{col}}">${{d.verdict}}</span> 评分:${{d.score}} ${{d.level||''}}<br>原因:${{esc(d.reason)}}<br>命中:${{(d.matched||[]).join(', ')}}`;
  }});
}}
function validateRules(){{
  fetch('/api/validate',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(collect())}})
  .then(r=>r.json()).then(d=>{{
    document.getElementById('result').innerHTML=d.ok?`<span class="badge ok">校验通过</span>`:`<span class="badge err">有问题</span><br>${{esc(d.msg)}}`;
  }});
}}
function saveRules(){{
  fetch('/api/rules',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(collect())}})
  .then(r=>r.json()).then(d=>{{
    document.getElementById('result').innerHTML=d.ok?`<span class="badge ok">已保存</span> ${{esc(d.msg)}}`:`<span class="badge err">保存失败</span> ${{esc(d.msg)}}`;
  }});
}}
// init
document.getElementById('red_alerts').value=(RULES.red_alerts||[]).join(', ');
document.getElementById('region_high').value=((RULES.region_priority&&RULES.region_priority.high)||[]).join(', ');
renderEntities();loadTpls();
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(obj, ensure_ascii=False).encode("utf-8"))

    def _send_html(self, html):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/" or u.path == "/index.html":
            try:
                rules = load_rules(RULES_PATH)
            except Exception as e:
                rules = {"entities": {}, "red_alerts": [], "region_priority": {"high": []},
                         "_note": "load failed: " + str(e)}
            html = PAGE.replace("{{RULES_JSON}}", json.dumps(rules, ensure_ascii=False))
            self._send_html(html)
        elif u.path == "/api/templates":
            self._send(200, list(TEMPLATES.keys()))
        else:
            self.send_error(404)

    def do_POST(self):
        u = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            data = json.loads(body)
        except Exception:
            data = {}
        if u.path == "/api/rules":
            try:
                save_rules(RULES_PATH, data)
                self._send(200, {"ok": True, "msg": "已写入 qual_rules.json（含备份）"})
            except Exception as e:
                self._send(200, {"ok": False, "msg": str(e)})
        elif u.path == "/api/validate":
            import tempfile
            tmp = os.path.join(tempfile.gettempdir(), ".editor_validate_rules.json")
            save_rules(tmp, data)
            ok, msg = run_validate(tmp)
            self._send(200, {"ok": ok, "msg": msg})
        elif u.path == "/api/test":
            res = run_test(data.get("title", ""), data.get("rules", {}))
            self._send(200, res)
        elif u.path.startswith("/api/template/"):
            name = u.path.split("/")[-1]
            import urllib.parse
            name = urllib.parse.unquote(name)
            t = TEMPLATES.get(name)
            self._send(200, t if t else {"error": "no such template"})
        else:
            self.send_error(404)

    def log_message(self, *a):
        pass


def main():
    global RULES_PATH, PORT
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--rules", default=RULES_PATH)
    args = ap.parse_args()
    RULES_PATH = os.path.abspath(args.rules)
    PORT = args.port
    print(f"规则编辑器已启动: http://localhost:{PORT}  (Ctrl+C 退出)")
    print(f"编辑目标: {RULES_PATH}")
    HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
