"""
analysis-toolkit 配置面板 — 单一入口。

启动：
    python serve_config.py              # 端口 8822
    python serve_config.py 8800         # 自定义端口

打开 http://127.0.0.1:{port} 即可查看和修改场景-报告关联。
页面数据和算子清单实时从注册表读取，配置变更直接写入 JSON 模板。
"""
import json, os, sys, html as html_mod, inspect, socket, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# 切换到 skill 根目录，确保 scripts.* 可导入
_SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(_SKILL_DIR)
sys.path.insert(0, os.path.dirname(_SKILL_DIR))

# 文件锁路径（防止并发写模板 JSON）
_LOCK_FILE = os.path.join(_SKILL_DIR, "scripts", "output", ".write_lock")


def _acquire_lock(timeout=5):
    """获取文件锁（阻塞等待，最多 timeout 秒）"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            fd = os.open(_LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            return fd
        except FileExistsError:
            time.sleep(0.1)
    raise TimeoutError(f"无法获取文件锁（{timeout}s 超时），其他进程正在写模板文件")


def _release_lock(fd):
    """释放文件锁"""
    os.close(fd)
    try:
        os.remove(_LOCK_FILE)
    except OSError:
        pass
_TEMPLATE_DIRS = {
    "default": os.path.join(_SKILL_DIR, "pipeline", "templates", "default"),
    "reports":  os.path.join(_SKILL_DIR, "pipeline", "templates", "reports"),
}


# ═══════════════════════════════════════════════════════
# API 处理
# ═══════════════════════════════════════════════════════

def _read_template(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _write_template(path, data):
    """写模板 JSON（带文件锁，防止并发写入）"""
    fd = _acquire_lock()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    finally:
        _release_lock(fd)

def handle_save_config(body):
    try:
        config = json.loads(body)
    except json.JSONDecodeError as e:
        return {"status": "error", "message": f"JSON解析失败: {e}"}
    saved, errors = 0, []
    for scene_name, report_name in config.items():
        path = os.path.join(_TEMPLATE_DIRS["default"], f"{scene_name}.json")
        if not os.path.exists(path):
            path = os.path.join(_SKILL_DIR, "pipeline", "templates", "user", f"{scene_name}.json")
        if not os.path.exists(path):
            errors.append(f"未找到场景: {scene_name}")
            continue
        try:
            data = _read_template(path)
            if report_name:
                data["default_report"] = report_name
            else:
                data.pop("default_report", None)
            _write_template(path, data)
            saved += 1
        except TimeoutError as e:
            errors.append(f"{scene_name}: 文件锁超时，请稍后重试")
            break
        except Exception as e:
            errors.append(f"{scene_name}: {e}")
    return {"status": "ok", "saved": saved, "errors": errors}

def handle_get_config():
    from scripts.pipeline.registry import list_templates, load_template
    scenarios = list_templates(template_type="scenario")
    result = []
    for s in scenarios:
        pipe = load_template(s["name"])
        result.append({"name": s["name"], "description": s.get("description",""),
                        "steps": s["steps"], "default_report": pipe.default_report or ""})
    return {"status": "ok", "scenarios": result}


# ═══════════════════════════════════════════════════════
# HTML 生成（实时从注册表读取）
# ═══════════════════════════════════════════════════════

def _esc(t):
    return html_mod.escape(str(t))

def _build_page():
    from scripts.pipeline.registry import list_templates, load_template
    from scripts.operations.registry import get_operator_registry

    scenarios = list_templates(template_type="scenario")
    reports   = list_templates(template_type="report")
    report_names = [r["name"] for r in reports]

    # 场景表
    srows = ""
    for s in scenarios:
        pipe = load_template(s["name"])
        cur = pipe.default_report or ""
        opts = '<option value="">(无报告)</option>'
        for rn in report_names:
            sel = ' selected' if rn == cur else ''
            opts += f'<option value="{_esc(rn)}"{sel}>{_esc(rn)}</option>'
        desc = _esc(s.get("description",""))[:80]
        badge_cls = "badge-ok" if cur else "badge-none"
        badge_txt = "已配对" if cur else "未配置"
        srows += f"""
        <tr><td class="sn">{_esc(s['name'])}</td>
            <td class="sd">{desc}</td>
            <td class="ss">{s['steps']}</td>
            <td><select class="rs" data-n="{_esc(s['name'])}">{opts}</select></td>
            <td><span class="badge {badge_cls}">{badge_txt}</span></td></tr>"""

    # 算子清单
    reg = get_operator_registry()
    ops = reg.list_all()
    cat_labels = {"statistics":"统计","uncertainty":"不确定度","total_error":"总误差","viz":"可视化"}
    cat_order  = ["statistics","uncertainty","total_error","viz"]
    grouped = {}
    for op in ops:
        grouped.setdefault(op.get("category","general"), []).append(op)

    osections = ""
    for cat in cat_order:
        items = grouped.get(cat, [])
        if not items:
            continue
        rows = ""
        for op in items:
            f = _esc(op.get("formula","") or "")
            d = _esc(op.get("description",""))[:60]
            s = _esc(op.get("signature","") or "")
            rows += f"<tr><td class='on'><code>{_esc(op['name'])}</code></td><td class='of'>{f or '<span style=color:#bbb>—</span>'}</td><td class='od'>{d}</td><td class='os'><code>{s or '—'}</code></td></tr>"
        osections += f"""<div class="oc"><h3 onclick="tc(this)" class="ch">📂 {cat_labels.get(cat,cat)} ({len(items)}个)<span class="ti">▼</span></h3><div class="cb"><table class="ot"><thead><tr><th>算子</th><th>公式</th><th>说明</th><th>签名</th></tr></thead><tbody>{rows}</tbody></table></div></div>"""

    # 统计卡片
    sc = len(scenarios)
    rc = len(reports)
    oc = len(ops)
    reports_json = json.dumps(report_names, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang=zh-CN>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>analysis-toolkit 配置面板</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f0f2f5;color:#2c3e50;padding:24px}}
.c{{max-width:1100px;margin:0 auto}}
h1{{font-size:22px;font-weight:600;margin-bottom:4px}}
h2{{font-size:17px;font-weight:600;margin:24px 0 12px;padding-bottom:8px;border-bottom:2px solid #378ADD}}
.st{{color:#7f8c8d;font-size:13px;margin-bottom:20px}}
.card{{background:#fff;border-radius:10px;padding:20px;margin-bottom:16px;border:1px solid #e8ecf1}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{background:#f0f2f5;padding:10px 14px;text-align:left;font-weight:600;border-bottom:2px solid #ddd}}
td{{padding:10px 14px;border-bottom:1px solid #eee;vertical-align:middle}}
tr:hover td{{background:#f8f9fc}}
.sn{{font-weight:600}}
.sd{{color:#7f8c8d;font-size:12px;max-width:260px}}
.ss{{text-align:center;color:#95a5a6}}
select.rs{{padding:5px 10px;border:1px solid #d5d9e0;border-radius:6px;font-size:13px;background:#fff;min-width:150px;cursor:pointer}}
select.rs:focus{{outline:none;border-color:#378ADD}}
.badge{{display:inline-block;padding:3px 10px;border-radius:10px;font-size:11px;font-weight:500}}
.badge-ok{{background:#EAF3DE;color:#27500A}}
.badge-none{{background:#FCEBEB;color:#791F1F}}
.bar{{display:flex;gap:10px;margin-top:14px;align-items:center}}
.btn{{padding:8px 20px;border:none;border-radius:6px;font-size:13px;cursor:pointer;font-weight:500}}
.btn-p{{background:#378ADD;color:#fff}}
.btn-p:hover{{background:#2a7bd4}}
.btn-s{{background:#f0f2f5;color:#555;border:1px solid #d5d9e0}}
.h{{font-size:12px;color:#95a5a6}}
.oc{{margin-bottom:8px}}
.ch{{font-size:14px;font-weight:600;padding:10px 14px;background:#f8f9fc;border-radius:8px;cursor:pointer;user-select:none}}
.ch:hover{{background:#eef0f5}}
.ti{{float:right;font-size:11px;transition:transform .2s}}
.ch.cd .ti{{transform:rotate(-90deg)}}
.cb{{overflow:hidden;transition:max-height .3s}}
.cb.cd{{max-height:0}}
.ot th{{background:#f0f2f5;padding:8px 12px;text-align:left;font-weight:600;border-bottom:2px solid #ddd}}
.ot td{{padding:7px 12px;border-bottom:1px solid #f0f0f0}}
.on code{{background:#f0f2f5;padding:2px 6px;border-radius:4px;font-size:12px}}
.of{{color:#7f8c8d;font-family:monospace;font-size:12px}}
.od{{color:#95a5a6;font-size:11px}}
.os code{{color:#95a5a6;font-size:11px}}
.sb{{width:100%;padding:8px 14px;border:1px solid #d5d9e0;border-radius:8px;font-size:13px;margin-bottom:12px}}
.sb:focus{{outline:none;border-color:#378ADD}}
.sr{{display:flex;gap:12px;margin-bottom:16px}}
.scard{{flex:1;background:#fff;border-radius:8px;padding:14px 16px;border:1px solid #e8ecf1;text-align:center}}
.scard-num{{font-size:24px;font-weight:600;color:#2c3e50}}
.scard-lbl{{font-size:11px;color:#95a5a6;margin-top:4px}}
#toast{{position:fixed;bottom:30px;right:30px;padding:12px 24px;border-radius:8px;font-size:13px;opacity:0;transition:opacity .3s;pointer-events:none;z-index:2000}}
#toast.show{{opacity:1}}
.toast-ok{{background:#27500A;color:#fff}}
.toast-warn{{background:#633806;color:#fff}}
</style>
<div class=c>
<h1>🧪 analysis-toolkit 配置面板</h1>
<p class=st>场景-报告关联配置 · 算子注册表总览 · 实时生成</p>
<div class=sr>
<div class=scard><div class=scard-num>{sc}</div><div class=scard-lbl>场景模板</div></div>
<div class=scard><div class=scard-num>{rc}</div><div class=scard-lbl>报告模板</div></div>
<div class=scard><div class=scard-num>{oc}</div><div class=scard-lbl>已注册算子</div></div>
</div>
<div class=card>
<h2>📋 场景 → 报告关联配置</h2>
<table><thead><tr><th>场景</th><th>功能</th><th>步骤</th><th>关联报告</th><th>状态</th></tr></thead>
<tbody>{srows}</tbody></table>
<div class=bar id=save-bar>
<button class="btn btn-p" onclick=sv()>💾 保存配置</button>
<button class="btn btn-s" onclick=ex()>📦 导出配置</button>
<button class="btn btn-s" onclick=rs()>↻ 重置</button>
<span class=h>💡 保存直接写入 JSON 模板</span>
</div>
<div class=bar id=done-bar style=display:none>
<button class="btn btn-p" onclick=dn() style="background:#059669">✅ 完成配置（关闭服务）</button>
<span class=h>配置已保存，点击关闭服务和本页面</span>
</div></div>
<div class=card>
<h2>🔧 算子注册表 ({oc} 个)</h2>
<input type=text class=sb id=op-s placeholder="搜索算子名称或公式..." oninput=fo(this.value)>
<div id=ol>{osections}</div>
</div></div>
<div id=modal-ov style=display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.4);z-index:1000 onclick=cm()></div>
<div id=modal style=display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#fff;border-radius:12px;padding:24px;width:520px;z-index:1001>
<span style=float:right;cursor:pointer;font-size:20px;color:#aaa onclick=cm()>&times;</span>
<h3 style=margin-bottom:12px>📦 场景-报告配置 JSON</h3>
<p style=font-size:13px;color:#7f8c8d;margin-bottom:12px>复制后粘贴到文件，或直接下载：</p>
<textarea id=cj style=width:100%;height:220px;font-size:12px;font-family:monospace;padding:10px;border:1px solid #d5d9e0;border-radius:6px;resize:vertical readonly></textarea>
<div style=display:flex;gap:10px;margin-top:12px>
<button class="btn btn-p" onclick=cp()>📋 复制</button>
<button class="btn btn-s" onclick=dw()>⬇ 下载</button>
<button class="btn btn-s" onclick=cm()>关闭</button>
</div></div>
<div id=toast></div>
<script>
var rl={reports_json};
function tc(e){{e.classList.toggle('cd');e.nextElementSibling.classList.toggle('cd')}}
function fo(k){{var kw=k.toLowerCase();document.querySelectorAll('.oc').forEach(function(c){{var v=0;c.querySelectorAll('.ot tbody tr').forEach(function(r){{var m=false;r.querySelectorAll('td').forEach(function(d){{if(d.textContent.toLowerCase().indexOf(kw)!==-1)m=true}});r.style.display=m?'':'none';if(m)v++}});c.style.display=v>0||kw===''?'':'none'}})}}
function gc(){{var s=document.querySelectorAll('.rs'),c={{}};s.forEach(function(e){{c[e.dataset.n]=e.value}});return c}}
function sv(){{var c=gc(),b=document.querySelector('.btn-p');b.textContent='⏳ 保存中...';b.disabled=true;fetch('/api/save_config',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(c)}}).then(function(r){{return r.json()}}).then(function(d){{if(d.status==='ok'){{st('✅ 已保存 ('+d.saved+' 个场景)','ok');document.querySelectorAll('.rs').forEach(function(e){{var bg=e.closest('tr').querySelector('.badge');bg.className='badge '+(e.value?'badge-ok':'badge-none');bg.textContent=e.value?'已配对':'未配置'}});document.getElementById('save-bar').style.display='none';document.getElementById('done-bar').style.display='flex'}}else{{st('❌ 保存失败','warn')}}}}).catch(function(){{st('⚠️ 保存失败','warn')}}).finally(function(){{b.textContent='💾 保存配置';b.disabled=false}})}}
function dn(){{document.getElementById('done-bar').querySelector('.btn-p').textContent='⏳ 关闭中...';fetch('/api/done').then(function(r){{return r.json()}}).then(function(d){{if(d.ok){{st('✅ 服务已关闭，可关闭此页面','ok');document.getElementById('done-bar').style.display='none'}}else{{st('❌ 关闭失败','warn')}}}})}}function ex(){{document.getElementById('cj').value=JSON.stringify(gc(),null,2);document.getElementById('modal-ov').style.display='block';document.getElementById('modal').style.display='block'}}
function cm(){{document.getElementById('modal-ov').style.display='none';document.getElementById('modal').style.display='none'}}
function cp(){{var t=document.getElementById('cj');t.select();document.execCommand('copy');st('📋 已复制','ok')}}
function dw(){{var b=new Blob([JSON.stringify(gc(),null,2)],{{type:'application/json'}}),a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='scenario_report_config.json';a.click();st('⬇ 已下载','ok')}}
function rs(){{if(!confirm('确认清空所有场景的默认报告？'))return;document.querySelectorAll('.rs').forEach(function(e){{e.value='';var bg=e.closest('tr').querySelector('.badge');bg.className='badge badge-none';bg.textContent='未配置'}});st('↻ 已重置','ok')}}
function st(m,t){{var o=document.getElementById('toast');o.textContent=m;o.className='show '+(t==='ok'?'toast-ok':'toast-warn');setTimeout(function(){{o.classList.remove('show')}},2500)}}
</script>"""


# ═══════════════════════════════════════════════════════
# HTTP 服务
# ═══════════════════════════════════════════════════════

class ConfigHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/config":
            self._json(handle_get_config())
        elif parsed.path in ("/", "/index.html"):
            html = _build_page()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length else "{}"
        if parsed.path == "/api/save_config":
            result = handle_save_config(body)
        elif parsed.path == "/api/done":
            # 创建关闭标志
            try:
                flag = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".serve_done")
                with open(flag, "w") as f:
                    f.write("done")
                result = {"status": "ok", "ok": True, "message": "服务将关闭"}
            except Exception as e:
                result = {"status": "error", "ok": False, "message": str(e)}
        else:
            result = {"status": "error", "message": "未知路径"}
        self._json(result)

    def _json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def log_message(self, fmt, *args):
        print(f"[Config] {args[0]} {args[1]}")

def find_available_port(start=8822, end=8922):
    """扫描可用端口"""
    for port in range(start, end + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("127.0.0.1", port))
            s.close()
            return port
        except OSError:
            continue
    return None

def main():
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 else None
    port = port_arg if port_arg else find_available_port()
    if port is None:
        print("❌ 8822-8922 端口均不可用，请指定端口: python serve_config.py <port>")
        sys.exit(1)

    done_flag = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".serve_done")
    if os.path.exists(done_flag):
        os.remove(done_flag)

    server = HTTPServer(("0.0.0.0", port), ConfigHandler)
    print(f"配置面板: http://127.0.0.1:{port}")
    if port_arg is None and port != 8822:
        print(f"  (端口 {port} 自动分配，保存后请使用此地址)")
    print("  保存配置 → 点击「完成配置」关闭服务")
    print("  Ctrl+C 强制停止")

    try:
        while True:
            server.timeout = 1.0
            server.handle_request()
            if os.path.exists(done_flag):
                print("\n配置完成，服务已关闭")
                break
    except KeyboardInterrupt:
        print("\n服务已停止")
    finally:
        server.server_close()
        if os.path.exists(done_flag):
            os.remove(done_flag)

if __name__ == "__main__":
    main()
