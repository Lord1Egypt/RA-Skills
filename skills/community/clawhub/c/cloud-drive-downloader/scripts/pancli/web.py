"""网盘通 Web/Agent 一站式服务子模块（从 engine.py 拆分，命令入口由 engine 懒加载）。"""
# 自动继承 engine 的全部共享工具（SKILL_DIR、配置、日志、下载调度等）

try:
    import os as _boot_os, sys as _boot_sys
    _boot_here = _boot_os.path.dirname(_boot_os.path.abspath(__file__))
    _boot_parent = _boot_os.path.dirname(_boot_here)
    for _boot_dir in (_boot_here, _boot_parent):
        if _boot_dir not in _boot_sys.path:
            _boot_sys.path.insert(0, _boot_dir)
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

from pancli.engine import *  # noqa: F401,F403
from pancli.engine import _probe_link_checks, fast_login_gate, login_gate_for_url, engine_catalog_payload, route_link_payload, _config_stat_key, CONFIG_PATH  # noqa: F401
from pancli.report import _atomic_write_json, LIVE_FILE_NAME, TASK_FILE_NAME, read_task_records, web_state_root  # noqa: F401
import html as _html
import re as _re
import struct as _struct  # noqa: F401
import urllib.request as _urlrequest
import webbrowser
import zlib as _zlib  # noqa: F401


def read_report_summary(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return {"path": str(path), "ok": data.get("ok"), "engine": data.get("engine"),
            "drive": data.get("drive"), "target": data.get("target"),
            "finished": data.get("finished"), "elapsed": data.get("elapsed")}


def serve_reports_json(reports_dir, limit=50):
    base = Path(reports_dir)
    out = []
    if base.exists():
        for p in sorted(base.glob("**/下载报告.json"))[:limit]:
            item = read_report_summary(p)
            if item:
                out.append(item)
    return out


def serve_live_json(reports_dir, limit=50):
    """扫描实时速度状态文件（下载速度.live.json），返回最近 limit 个。"""
    base = Path(reports_dir)
    out = []
    if not base.exists():
        return out
    files = sorted(base.glob("**/%s" % LIVE_FILE_NAME), key=lambda p: p.stat().st_mtime, reverse=True)
    for f in files[:limit]:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        data["path"] = str(f)
        data["mtime"] = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%dT%H:%M:%S%z")
        out.append(data)
    return out


def _task_id(target):
    import hashlib
    return hashlib.sha1(str(target).encode("utf-8")).hexdigest()[:12]


def _web_ui_status_ok(port, timeout=0.35, expected_reports_dir=""):
    """检测本地 Web UI 是否已经就绪；失败时静默返回 False。"""
    try:
        with _urlrequest.urlopen("http://127.0.0.1:%d/api/status" % int(port), timeout=timeout) as resp:
            if int(getattr(resp, "status", 0) or 0) != 200:
                return False
            if expected_reports_dir:
                body = json.loads(resp.read().decode("utf-8") or "{}")
                got = str(body.get("reports_dir") or "")
                if got and os.path.realpath(got) != os.path.realpath(str(expected_reports_dir)):
                    return False
            return True
    except Exception:
        return False


def ensure_web_ui(cfg=None, open_browser=True):
    """确保本地 Web UI 已启动，并可选打开 /live 页面。

    该函数只负责启动/复用状态服务，不参与下载执行；端口被占用或被系统禁止时
    返回错误字典，由调用方降级继续下载，绝不因 Web UI 失败中断下载。
    """
    cfg = cfg or load_config()
    http = cfg.get("http") or {}
    if not bool(http.get("auto_web", True)):
        return {"ok": False, "reused": False, "started": False, "port": 0,
                "url": "", "reports_dir": "", "browser_opened": False,
                "error": "配置已关闭自动 Web UI（http.auto_web=false）"}
    dep = cfg.get("deployment") or {}
    try:
        requested_port = int(dep.get("web_port") or http.get("web_port") or 17890)
    except (TypeError, ValueError):
        requested_port = 17890
    requested_port = max(1, min(65535, requested_port))
    reports_dir = str(web_state_root(cfg))
    candidates = []
    for port in range(requested_port, min(65536, requested_port + 6)):
        if port not in candidates:
            candidates.append(port)

    def _ready_result(port, reused=False, browser_opened=False):
        url = "http://127.0.0.1:%d" % port
        return {"ok": True, "reused": bool(reused), "started": not bool(reused),
                "port": port, "url": url, "reports_dir": reports_dir,
                "browser_opened": bool(browser_opened), "error": ""}

    last_error = ""
    for port in candidates:
        if _web_ui_status_ok(port, expected_reports_dir=reports_dir):
            opened = False
            if open_browser:
                try:
                    opened = bool(webbrowser.open("http://127.0.0.1:%d/live" % port, new=1))
                except Exception as exc:
                    last_error = "Web UI 已运行，但浏览器打开失败：%s" % exc
                if not opened:
                    print("⚠️ 浏览器自动打开失败（沙箱/LaunchServices 限制），请手动访问：%s" % ("http://127.0.0.1:%d/live" % port), file=sys.stderr)
            return _ready_result(port, reused=True, browser_opened=opened)

        argv = [sys.executable, str(SKILL_DIR / "scripts" / "pan.py"), "serve",
                "--host", "127.0.0.1", "--port", str(port), "--reports-dir", reports_dir]
        try:
            proc = subprocess.Popen(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                    start_new_session=True)
        except OSError as exc:
            last_error = "端口 %d 启动失败：%s" % (port, exc)
            continue
        ready = False
        for _ in range(12):
            if _web_ui_status_ok(port, expected_reports_dir=reports_dir):
                ready = True
                break
            if proc.poll() is not None:
                last_error = "端口 %d 启动失败（进程退出码 %s）" % (port, proc.returncode)
                break
            time.sleep(0.1)
        if ready:
            opened = False
            if open_browser:
                try:
                    opened = bool(webbrowser.open("http://127.0.0.1:%d/live" % port, new=1))
                except Exception as exc:
                    last_error = "Web UI 已启动，但浏览器打开失败：%s" % exc
                if not opened:
                    print("⚠️ 浏览器自动打开失败（沙箱/LaunchServices 限制），请手动访问：%s" % ("http://127.0.0.1:%d/live" % port), file=sys.stderr)
            return _ready_result(port, reused=False, browser_opened=opened)
        if proc.poll() is None:
            try:
                proc.terminate()
            except OSError:
                pass
        if not last_error:
            last_error = "端口 %d 启动超时" % port
    return {"ok": False, "reused": False, "started": False, "port": 0,
            "url": "", "reports_dir": reports_dir, "browser_opened": False,
            "error": last_error or "未找到可用端口"}


def _redact_task_url(url):
    """任务 API 不返回提取码等 URL 敏感参数。"""
    text = str(url or "")
    return _re.sub(r"(?i)([?&](?:pwd|password|passcode|token|access_token|secret)=)[^&#]*", r"\1***", text)


def serve_unified_tasks(reports_dir, limit=100, state=None):
    """统一任务中心：实时任务 + 历史报告 + 任务控制记录汇总成一张任务表。"""
    control = serve_task_controls(reports_dir, limit=limit * 2)
    tasks = []
    # 实时任务（优先以 live 文件为准）
    live = serve_live_json(reports_dir, limit=limit)
    for item in live:
        st = item.get("state", "")
        ctl = control.get(_task_id(item.get("target", "")))
        if ctl and ctl.get("state") in ("paused", "cancelled"):
            st = ctl["state"]
        if state and st != state:
            continue
        tasks.append({
            "id": _task_id(item.get("target", "")),
            "source": "live",
            "state": st,
            "drive": item.get("drive", ""),
            "drive_name": item.get("drive_name", ""),
            "engine": item.get("engine", ""),
            "tier": item.get("tier", ""),
            "url": _redact_task_url(item.get("url", "")),
            "target": item.get("target", ""),
            "current_step": item.get("current_step", ""),
            "speed_kbps": item.get("speed_kbps"),
            "avg_speed_kbps": item.get("avg_speed_kbps"),
            "bytes_done": item.get("bytes_done", 0),
            "total_bytes": item.get("total_bytes", 0),
            "percent": item.get("percent"),
            "eta_seconds": item.get("eta_seconds"),
            "files_total": item.get("files_total", 0),
            "files_done": item.get("files_done", 0),
            "files_failed": item.get("files_failed", 0),
            "current_file": item.get("current_file", ""),
            "local_path": item.get("local_path", "") or item.get("target", ""),
            "file_bytes": item.get("file_bytes", 0),
            "file_size": item.get("file_size", 0),
            "file_percent": item.get("file_percent"),
            "status_text": item.get("status_text", ""),
            "started": item.get("started", ""),
            "updated": item.get("updated", "") or item.get("mtime", ""),
            "finished": item.get("updated", "") if st in ("done", "failed", "cancelled") else "",
            "elapsed": item.get("elapsed", 0),
            "ok": st not in ("failed", "cancelled"),
        })
    # 历史报告（不在 live 里重复/或已结束的兜底）
    seen = {t["target"] for t in tasks}
    reports = serve_reports_json(reports_dir, limit=limit)
    for r in reports:
        if r.get("target") in seen:
            continue
        st = "done" if r.get("ok") else "failed"
        if state and st != state:
            continue
        tasks.append({
            "id": _task_id(r.get("target", "")),
            "source": "report",
            "state": st,
            "drive": r.get("drive", ""),
            "drive_name": "",
            "engine": r.get("engine", ""),
            "tier": "",
            "url": "",
            "target": r.get("target", ""),
            "current_step": "",
            "speed_kbps": None,
            "avg_speed_kbps": None,
            "bytes_done": 0,
            "total_bytes": 0,
            "percent": 100 if r.get("ok") else 0,
            "eta_seconds": None,
            "files_total": 0,
            "files_done": 0,
            "files_failed": 0 if r.get("ok") else 1,
            "current_file": "",
            "local_path": r.get("target", ""),
            "file_bytes": 0,
            "file_size": 0,
            "file_percent": None,
            "status_text": "已完成" if r.get("ok") else "失败",
            "started": "",
            "updated": r.get("finished", ""),
            "finished": r.get("finished", ""),
            "elapsed": r.get("elapsed", 0),
            "ok": bool(r.get("ok")),
        })
    # 任务控制记录兜底（paused/cancelled/done/failed 等不在 live/报告中的）
    seen = {t["target"] for t in tasks}
    for tid, rec in sorted(control.items(), key=lambda kv: str(kv[1].get("updated") or ""), reverse=True):
        if rec.get("target") in seen:
            continue
        st = rec.get("state") or "running"
        if state and st != state:
            continue
        tasks.append({
            "id": tid,
            "source": "task",
            "state": st,
            "drive": rec.get("drive", ""),
            "drive_name": rec.get("drive_name", ""),
            "engine": rec.get("engine", ""),
            "tier": rec.get("tier", ""),
            "url": _redact_task_url(rec.get("url", "")),
            "target": rec.get("target", ""),
            "current_step": rec.get("current_step", ""),
            "speed_kbps": None,
            "avg_speed_kbps": None,
            "bytes_done": 0,
            "total_bytes": 0,
            "percent": 100 if st == "done" else 0,
            "eta_seconds": None,
            "files_total": 0,
            "files_done": 0,
            "files_failed": 1 if st == "failed" else 0,
            "current_file": rec.get("current_step", ""),
            "local_path": rec.get("target", ""),
            "file_bytes": 0,
            "file_size": 0,
            "file_percent": None,
            "status_text": rec.get("current_step", ""),
            "started": rec.get("started", ""),
            "updated": rec.get("updated", ""),
            "finished": rec.get("finished", ""),
            "elapsed": 0,
            "ok": st not in ("failed", "cancelled"),
        })
    # 去掉内部用路径字段后返回
    for t in tasks:
        t.pop("_control_path", None)
    # 去语气归一：live 优先，报告/控制记录排后
    tasks.sort(key=lambda t: (t.get("updated") or ""), reverse=True)
    return tasks[:limit]


def _spawn_retry_task(rec):
    """按任务控制记录里的参数重新拉起一个 get 子进程；返回 (pid, 错误)。"""
    url = rec.get("url", "")
    if not url:
        return "", "任务记录缺少 url，无法重试"
    args = rec.get("args") or {}
    argv = [sys.executable, str(SKILL_DIR / "scripts" / "pan.py"), "get", url, "--live",
            "--to", str(args.get("to") or ""), "--engine", str(args.get("engine") or ""),
            "--tier", str(args.get("tier") or "")]
    if args.get("pwd"):
        argv += ["--pwd", str(args["pwd"])]
    if args.get("path"):
        argv += ["--path", str(args["path"])]
    try:
        proc = subprocess.Popen(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                start_new_session=True)
    except OSError as exc:
        return "", "启动重试失败：%s" % exc
    return str(proc.pid), ""


def serve_task_controls(reports_dir, limit=200):
    """递归收集 reports_dir 下所有任务控制记录（按 target 去重）。"""
    base = Path(reports_dir)
    out = {}
    if base.exists():
        for f in sorted(base.glob("**/" + TASK_FILE_NAME), key=lambda p: p.stat().st_mtime, reverse=True):
            recs = read_task_records(f)
            for k, v in recs.items():
                out.setdefault(k, dict(v))
                out[k]["_control_path"] = str(f)
            if len(out) >= limit:
                break
    return out


def _locate_task_control(reports_dir, task_id):
    base = Path(reports_dir)
    if not base.exists():
        return None, {}
    for f in base.glob("**/" + TASK_FILE_NAME):
        recs = read_task_records(f)
        if task_id in recs:
            return f, recs[task_id]
    return None, {}


def _apply_task_action(reports_dir, task_id, action):
    """对任务控制记录执行 pause/resume/delete/retry；返回 (ok, message)。"""
    path, rec = _locate_task_control(reports_dir, task_id)
    if not path or not rec:
        return False, "未找到任务 %s" % task_id
    if "_control_path" in rec:
        rec.pop("_control_path", None)
    recs = read_task_records(path)
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
    if action == "pause":
        if rec.get("state") != "running":
            return False, "只有运行中的任务可以暂停（当前：%s）" % rec.get("state")
        rec["state"] = "paused"
    elif action == "resume":
        if rec.get("state") != "paused":
            return False, "只有已暂停的任务可以继续（当前：%s）" % rec.get("state")
        rec["state"] = "running"
    elif action == "delete":
        if rec.get("state") == "running":
            rec["state"] = "cancelled"
            rec["updated"] = now
            rec["finished"] = rec.get("finished") or now
            _atomic_write_json(path, {"schema": 1, "tasks": recs})
            return True, "已发送取消并删除标记"
        recs.pop(task_id, None)
        _atomic_write_json(path, {"schema": 1, "tasks": recs})
        return True, "已删除任务记录"
    elif action == "retry":
        if rec.get("state") not in ("done", "failed", "cancelled"):
            return False, "仅已结束（done/failed/cancelled）任务可重试"
        pid, err = _spawn_retry_task(rec)
        if err:
            return False, err
        new_rec = dict(rec)
        new_rec["state"] = "running"
        new_rec["pid"] = pid
        new_rec["started"] = now
        new_rec["updated"] = now
        new_rec["finished"] = ""
        new_rec["rc"] = None
        recs[task_id] = new_rec
        _atomic_write_json(path, {"schema": 1, "tasks": recs})
        return True, "已重新启动下载（新 PID %s）；若原链接需要提取码，请用 `pan task show %s` 查看后补充 --pwd" % (pid, task_id)
    rec["updated"] = now
    recs[task_id] = rec
    _atomic_write_json(path, {"schema": 1, "tasks": recs})
    return True, "任务已%s" % action


def _spawn_download_task(url, pwd="", to="", engine="", tier="", path=""):
    """后台启动 pan get --live；返回 (pid, 错误)。供浏览器扩展 POST /api/download 调用。"""
    if not url or not url.strip():
        return "", "url 为空"
    argv = [sys.executable, str(SKILL_DIR / "scripts" / "pan.py"), "get", url.strip(), "--live", "--no-web"]
    if pwd:
        argv += ["--pwd", pwd]
    if to:
        argv += ["--to", to]
    if engine:
        argv += ["--engine", engine]
    if tier:
        argv += ["--tier", tier]
    if path:
        argv += ["--path", path]
    try:
        proc = subprocess.Popen(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                start_new_session=True)
    except OSError as exc:
        return "", "启动下载失败：%s" % exc
    return str(proc.pid), ""


def render_live_table(live):
    """把实时任务渲染成 /live 表格；供 HTTP 路由和离线自测共用。"""
    if not live:
        return '<div class="empty">暂无进行中的实时下载<br><span>普通终端执行 pan get 会自动打开本页；后台任务请加 --live</span></div>', "[]"
    shown = []
    rows = []
    for item in live[:8]:
        st = item.get("state", "")
        badge = st if st else "unknown"
        sp = item.get("speed_kbps")
        av = item.get("avg_speed_kbps")
        sps = ("%.1f" % float(sp)) if sp not in (None, "") else "-"
        avs = ("%.1f" % float(av)) if av not in (None, "") else "-"
        by = int(item.get("bytes_done") or 0)
        if by >= 1024 * 1024:
            btxt = "%.2f MB" % (by / 1048576.0)
        else:
            btxt = "%.2f KB" % (by / 1024.0)
        local_path = item.get("local_path") or item.get("target") or "-"
        current_file = item.get("current_file") or ""
        if current_file and local_path != "-" and current_file not in str(local_path):
            local_path = str(local_path).rstrip("/\\") + "/" + current_file
        local_path_text = _html.escape(str(local_path))
        local_path_attr = _html.escape(str(local_path), quote=True)
        eta = item.get("eta_seconds")
        ets = "-"
        if eta is not None:
            eta = float(eta)
            if eta <= 0:
                ets = "即将完成"
            elif eta < 60:
                ets = "约 %d 秒" % int(eta)
            elif eta < 3600:
                ets = "约 %d 分 %d 秒" % (int(eta // 60), int(eta % 60))
            else:
                ets = "约 %d 小时 %d 分" % (int(eta // 3600), int((eta % 3600) // 60))
        percent = item.get("percent")
        pct = ("%.1f%%" % float(percent)) if percent not in (None, "") else "-"
        detail = str(item.get("status_text") or "")
        active_shards = int(item.get("active_shards") or 0)
        batch_percent = item.get("batch_percent")
        if active_shards and batch_percent is not None:
            detail = ("%s · 当前批次 %.1f%%（%d 分片）" % (detail, float(batch_percent), active_shards)).strip(" ·")
        shown.append({
            "name": item.get("drive_name", ""), "step": item.get("current_step", ""),
            "speed": sps, "avg": avs, "done": btxt, "state": badge,
            "eta": ets, "path": str(local_path), "history": item.get("history", [])[:300],
            "total": item.get("total_bytes", 0), "percent": item.get("percent"),
            "detail": detail, "active_shards": active_shards,
        })
        detail_html = ("<div class=tip>%s</div>" % _html.escape(detail)) if detail else ""
        drive_name_html = _html.escape(str(item.get("drive_name", "")))
        current_step_html = _html.escape(str(item.get("current_step", "")))
        updated_html = _html.escape(str(item.get("updated", "")))
        rows.append(
            "<tr><td>%s</td><td>%s</td><td><span class=speed>%s KB/s</span></td>"
            "<td>%s KB/s</td><td>%s</td><td>%s</td><td>%s</td>"
            "<td><span class='badge %s'>%s</span>%s</td>"
            "<td class=mono>%s<button class=copy type=button data-path=\"%s\">复制路径</button></td>"
            "<td class=mono>%s</td></tr>" % (
                drive_name_html, current_step_html,
                sps, avs, btxt, pct, ets, badge, badge, detail_html, local_path_text,
                local_path_attr, updated_html))
    items_json = json.dumps(shown, ensure_ascii=False)
    table = ("<thead><tr><th>网盘</th><th>当前文件 / 步骤</th><th>实时速度</th>"
             "<th>平均速度</th><th>已下载</th><th>总进度</th><th>剩余时间</th><th>状态</th>"
             "<th>下载位置</th><th>更新时间</th></tr></thead>"
             "<tbody>%s</tbody>" % "".join(rows))
    body = table + '<div id="charts"></div>'
    return body, items_json


def serve_live_page_html(content, items_json="[]"):
    """渲染实时速度页 HTML（与任务中心同款深色风格），items_json 供前端画速度曲线。"""
    _json_esc = items_json.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e") \
        .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    return ("""<!doctype html><html lang=zh-CN><head><meta charset=utf-8>"""
            """<meta name=viewport content="width=device-width,initial-scale=1">"""
            """<meta http-equiv=refresh content=2><title>多网盘实时速度</title>"""
            """<link rel="manifest" href="/manifest.webmanifest">"""
            """<script>if('serviceWorker'in navigator){navigator.serviceWorker.register('/sw.js')}</script>"""
            """<style>
:root{--bg:#0f172a;--panel:#1e293b;--line:#334155;--text:#e2e8f0;--muted:#94a3b8;--acc:#38bdf8}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,"PingFang SC","Microsoft YaHei",system-ui,sans-serif}
.wrap{max-width:1100px;margin:0 auto;padding:24px 18px 40px}
header{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:16px}
header h1{font-size:20px;margin:0}
.nav a{color:var(--acc);text-decoration:none;font-size:13px;margin-left:12px}
.nav a:hover{text-decoration:underline}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden}
table{width:100%%;border-collapse:collapse;font-size:13px}
thead th{background:#0b1120;color:var(--muted);text-align:left;padding:10px 14px;border-bottom:1px solid var(--line);white-space:nowrap}
tbody td{padding:10px 14px;border-bottom:1px solid var(--line)}
tr:last-child td{border-bottom:none}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px}
.speed{color:#facc15;font-weight:600}
.badge{display:inline-block;padding:2px 9px;border-radius:999px;font-size:11px;font-weight:600}
.badge.running{background:#f59e0b;color:#1a1206}
.badge.done{background:#22c55e;color:#052e16}
.badge.failed{background:#ef4444;color:#fff}
.badge.paused{background:#64748b;color:#f1f5f9}
.empty{background:var(--panel);border:1px solid var(--line);border-radius:12px;color:var(--muted);text-align:center;padding:40px;font-size:15px;line-height:1.8}
.empty span{font-size:12px}
#charts{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px;margin:16px 0 4px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px 14px}
.card h4{margin:0 0 8px;font-size:14px}
.card canvas{width:100%%;height:140px;display:block}
.card .meta{font-size:12px;color:var(--muted);margin-top:6px;line-height:1.6}
.copy{background:#13233b;border:1px solid #334f78;color:#bfdbfe;border-radius:7px;padding:3px 8px;font-size:11px;cursor:pointer;margin-left:6px}.copy:hover{background:#1d3557}
.hint{color:var(--muted);font-size:12px;margin:0 0 10px}
</style></head><body><div class=wrap>
<header><h1>⚡ 多网盘实时速度</h1><div class=nav>
<a href=/guide>使用教程</a><a href=/login>登录</a><a href=/>任务中心</a><a href=/api/live>API 实时</a><a href=/api/status>API 状态</a>
</div></header>
<p class=hint>下载位置显示在任务行右侧，点击“复制路径”即可复制到剪贴板。</p>
<div class=panel><table>%(content)s</table><div id="CURVE_DATA" style="display:none">%(_json_esc)s</div></div>
<script>
function fallbackCopy(text, done) {
  const ta = document.createElement('textarea');
  ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
  document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove(); done();
}
document.addEventListener('click', e => {
  const b = e.target.closest('.copy');
  if (!b) return;
  const text = b.dataset.path || '';
  const done = () => { b.textContent = '已复制'; setTimeout(() => { b.textContent = '复制路径'; }, 1200); };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(done).catch(() => fallbackCopy(text, done));
  } else {
    fallbackCopy(text, done);
  }
});
(() => {
  const wrap = document.getElementById('charts');
  if (!wrap) return;
  let data = [];
  const el = document.getElementById('CURVE_DATA');
  try { data = JSON.parse(el ? el.textContent : '[]'); } catch (e) { data = []; }
  data.forEach((d, i) => {
    const his = d.history || [];
    const div = document.createElement('div');
    div.className = 'card';
    const h = document.createElement('h4');
    h.textContent = d.name || '';
    const canv = document.createElement('canvas');
    canv.width = 600; canv.height = 140;
    const meta = document.createElement('div');
    meta.className = 'meta';
    meta.textContent = '当前 ' + (d.speed || '') + ' KB/s · 平均 ' + (d.avg || '') + ' KB/s\n已下载 ' + (d.done || '') + ' · 剩余 ' + (d.eta || '') + (d.percent != null ? ' · ' + d.percent + '%%' : '');
    div.appendChild(h); div.appendChild(canv); div.appendChild(meta);
    wrap.appendChild(div);
    const cv = canv;
    const ctx = cv.getContext('2d');
    ctx.clearRect(0, 0, cv.width, cv.height);
    ctx.strokeStyle = '#475569'; ctx.lineWidth = 1;
    for (let gx = 0; gx <= 4; gx++) {
      const x = gx * cv.width / 4;
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, cv.height); ctx.stroke();
    }
    if (!his.length) return;
    let m = 0;
    his.forEach(pp => { m = Math.max(m, pp[1] || 0); });
    const top = Math.max(1, Math.ceil(m * 1.1 / 10) * 10);
    const grad = ctx.createLinearGradient(0, 0, 0, cv.height);
    grad.addColorStop(0, 'rgba(56,189,248,0.35)'); grad.addColorStop(1, 'rgba(56,189,248,0.02)');
    ctx.beginPath();
    his.forEach((pp, j) => {
      const x = cv.width * j / Math.max(1, his.length - 1);
      const y = cv.height - (cv.height - 16) * (pp[1] / top) - 8;
      if (j === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    });
    ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2; ctx.stroke();
    ctx.lineTo(cv.width, cv.height); ctx.lineTo(0, cv.height); ctx.closePath();
    ctx.fillStyle = grad; ctx.fill();
    ctx.fillStyle = '#94a3b8'; ctx.font = '11px sans-serif';
    ctx.fillText('峰值 ' + (m.toFixed ? m.toFixed(1) : m) + ' KB/s', 8, cv.height - 8);
  });
})();
setInterval(() => { if (!document.hidden) location.reload(); }, 10000);
</script>
</div></body></html>""" % {"content": content, "_json_esc": _json_esc})


def serve_guide_html():
    """内置「使用教程」页：新手打开网页即可看到完整操作说明。"""
    return """<!doctype html><html lang=zh-CN><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>网盘通 · 使用教程</title>
<link rel="manifest" href="/manifest.webmanifest">
<script>if('serviceWorker'in navigator){navigator.serviceWorker.register('/sw.js')}</script>
<style>
:root{--bg:#0f172a;--panel:#1e293b;--line:#334155;--text:#e2e8f0;--muted:#94a3b8;--acc:#38bdf8}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,"PingFang SC","Microsoft YaHei",system-ui,sans-serif}
.wrap{max-width:820px;margin:0 auto;padding:24px 18px 40px}
header{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:16px}
header h1{font-size:20px;margin:0}
.nav a{color:var(--acc);text-decoration:none;font-size:13px;margin-left:12px}
.nav a:hover{text-decoration:underline}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin-bottom:14px;line-height:1.8}
.card h3{margin:0 0 8px;font-size:15px}
.step{display:flex;gap:10px;align-items:flex-start;margin:7px 0}
.num{flex:0 0 22px;height:22px;border-radius:999px;background:var(--acc);color:#052e16;font-weight:700;font-size:13px;display:flex;align-items:center;justify-content:center}
code{background:#0b1120;border:1px solid var(--line);border-radius:6px;padding:1px 6px;font-size:12px}
a{color:var(--acc)}
.ok{color:#4ade80}.warn{color:#fbbf24}.tip{color:var(--muted);font-size:13px}
</style></head><body><div class=wrap>
<header><h1>📖 网盘通 · 使用教程</h1><div class=nav>
<a href=/>任务中心</a><a href=/test>测试连接</a><a href=/live>实时速度</a>
</div></header>

<div class=card><h3>3 秒学会：复制链接 → 粘贴 → 开始 → 看实时速度</h3>
<div class="step"><span class=num>1</span><div>复制你想下载的网盘分享链接（可带提取码）。</div></div>
<div class="step"><span class=num>2</span><div>回到 <a href=/>任务中心</a>，把链接粘贴到「粘贴链接开始下载」输入框。</div></div>
<div class="step"><span class=num>3</span><div>提取码可不填；目标目录可不填（默认 <code>下载 / Downloads/网盘下载</code>）。</div></div>
<div class="step"><span class=num>4</span><div>点「开始下载」，网页自动识别网盘类型并开始下载。</div></div>
<div class="step"><span class=num>5</span><div>打开 <a href=/live>实时速度</a> 页，可看当前速度、平均速度、已下载大小、剩余时间和速度曲线。</div></div>
</div>

<div class=card><h3>第一次用，先测一下</h3>
<div class="step"><span class=num>1</span><div>打开 <a href=/test>测试连接</a> 页。</div></div>
<div class="step"><span class=num>2</span><div>粘贴网盘链接（提取码留空也可以）。</div></div>
<div class="step"><span class=num>3</span><div>点「开始测试」，几秒内会告诉你这个网盘能不能连、缺什么。</div></div>
<p class=tip>测试只做本地检查，不会真下载，也不会向你选择的网盘发请求。</p>
</div>

<div class=card><h3>常见问题</h3>
<p><b>「提示登录过期」怎么办？</b> 部分网盘首次要官方扫码或网页登录一次，这是官方要求，工具不会绕过。</p>
<p><b>下载会更快吗？</b> 免费档按网盘官方限速执行，不能承诺更快；会员走本机并发调度。想提速看下一条。</p>
<p><b>非会员怎么提速？</b> 三招：①换赛道——让分享方用 123 云盘/夸克离线（见教程 <code>references/42-换赛道提速指南.md</code>）；②http 直链单连接被限时会自动切分片（v0.20.0）；③深夜下载用 <code>pan idle add &lt;链接&gt;</code> 排闲时队列（默认 0-8 点自动跑）。</p>
<p><b>密码安全吗？</b> 账号/Cookie/OAuth 凭据只存系统钥匙串，不存明文、不进聊天记录、不上传云端。</p>
<p><b>下载到哪了？</b> 默认 <code>下载 / Downloads/网盘下载</code>；可在「目标目录」填写 NAS、U盘等路径。</p>
<p><b>卡在某个网盘不会用？</b> 先用「测试连接」，再按它的建议补配置即可。</p>
</div>
</div></body></html>"""


def pwa_manifest_json():
    """Web 应用清单：让任务中心可被 Chrome/Safari 安装为独立窗口 PWA。"""
    m = {
        "name": "多网盘任务中心",
        "short_name": "pan 任务中心",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0f172a",
        "theme_color": "#0f172a",
        "lang": "zh-CN",
        "icons": [
            {"src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
            {"src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
        ]
    }
    return json.dumps(m, ensure_ascii=False)


def pwa_service_worker_js():
    """离线优先外壳：只缓存首页与实时速度页，读取时仍从服务器取最新数据。"""
    return ("""const CACHE = 'pan-pwa-v1';
const PAGES = ['/', '/live', '/test', '/guide'];
self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(PAGES)));
});
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((keys) =>
    Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))));
  self.clients.claim();
});
self.addEventListener('fetch', (e) => {
  e.respondWith(
    fetch(e.request).then((res) => {
      const clone = res.clone();
      if (e.request.method === 'GET') {
        caches.open(CACHE).then((c) => c.put(e.request, clone));
      }
      return res;
    }).catch(() => caches.match(e.request).then((hit) => hit || Response.error()))
  );
});
""")


def pwa_icon_png(size):
    """生成本地 PWA 图标 PNG（无需外部文件，尺寸 192/512）。"""
    import struct as _struct
    import zlib as _zlib

    def _chunk(t, d):
        c = _struct.pack('>I', len(d)) + t + d
        return c + _struct.pack('>I', _zlib.crc32(t + d) & 0xffffffff)

    w = h = size
    rows = []
    for y in range(h):
        row = bytearray([0])
        for x in range(w):
            dx = min(x, w - 1 - x); dy = min(y, h - 1 - y)
            r = int(size * 0.12)
            if dx < r and dy < r and ((r - dx) ** 2 + (r - dy) ** 2 > r * r):
                a = 0
            else:
                a = 255
            cy = y
            in_arrow = (0.45 * w <= x <= 0.55 * w and 0.30 * h <= cy <= 0.62 * h) or                        (0.42 * h <= cy <= 0.58 * h and 0.25 * w <= x <= 0.75 * w) or                        (cy >= 0.55 * h and cy <= int(0.62 * h) + (int(0.50 * w) - x))
            if in_arrow:
                c = (255, 255, 255, a)
            else:
                c = (40, 110, 210, a)
            row += bytes(c)
        rows.append(bytes(row))
    raw = b''.join(rows)
    ihdr = _chunk(b'IHDR', _struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
    return b'\x89PNG\r\n\x1a\n' + ihdr + _chunk(b'IDAT', _zlib.compress(raw)) + _chunk(b'IEND', b'')



def _human_error(text):
    """把常见失败转成人话；原始错误保留在 detail。"""
    raw = str(text or "")
    low = raw.lower()
    rules = [
        ("could not resolve host", "域名解析失败：可能是 NAS 容器 DNS 或外网不可用。"),
        ("connection refused", "连接被拒绝：目标服务/端口没有开启，或地址端口写错。"),
        ("timeout", "连接超时：网络慢、目标站点无响应或被防火墙拦截。"),
        ("no space left on device", "NAS/目标盘空间不足，请清理或换目录。"),
        ("authorization", "没有访问权限：先在 AList/网盘官方授权，或检查凭据。"),
        ("forbidden", "目标拒绝访问：链接可能已失效，或站点限制下载。"),
        ("password", "缺少或提取码错误，请重新输入。"),
        ("engine", "下载引擎未安装或未配置，先到快速诊断处理。"),
    ]
    for key, msg in rules:
        if key in low:
            return msg + "（原始信息：%s）" % (raw[:180] or "-")
    return raw or "未知错误。"


_DIAG_CACHE = {"key": None, "payload": {}, "expires": 0.0}
_DIAG_CACHE_TTL = 30.0


def diagnostics_payload(force=False):
    """Web 快速诊断：只读检测，不做绕过；结果缓存 30 秒，refresh=1 可强制刷新。"""
    now = time.time()
    try:
        st = CONFIG_PATH.stat()
        key = (str(CONFIG_PATH), st.st_mtime_ns, st.st_size, st.st_ino)
    except OSError:
        key = (str(CONFIG_PATH), -1, -1, -1)
    if not force and _DIAG_CACHE["key"] == key and now < _DIAG_CACHE["expires"]:
        out = copy.deepcopy(_DIAG_CACHE["payload"])
        out["cache_hit"] = True
        out["cache_ttl_seconds"] = _DIAG_CACHE_TTL
        return out
    import shutil as _sh
    import socket as _socket
    cfg = load_config()
    checks = []
    for name in ("curl", "aria2", "rclone"):
        binpath = find_engine_binary(name, cfg)
        checks.append({"name": name, "ok": bool(binpath), "detail": binpath or "未安装"})
    alist = ((cfg.get("engines") or {}).get("alist_url") or "").strip()
    checks.append({"name": "AList", "ok": bool(alist), "detail": alist or "未配置"})
    root = default_root(cfg)
    root_path = Path(root)
    if not root_path.exists() and Path("/data/download").exists():
        root_path = Path("/data/download")
    try:
        usage = _sh.disk_usage(root_path)
        free_gb = usage.free / 1024 ** 3
        checks.append({"name": "磁盘空间", "ok": free_gb >= 1, "detail": "%.1f GB 可用 / %s" % (free_gb, root_path)})
    except Exception as exc:
        checks.append({"name": "磁盘空间", "ok": False, "detail": _human_error(exc)})
    try:
        _socket.setdefaulttimeout(2.5)
        _socket.gethostbyname("www.baidu.com")
        checks.append({"name": "外网 DNS", "ok": True, "detail": "域名解析正常"})
    except Exception as exc:
        checks.append({"name": "外网 DNS", "ok": False, "detail": _human_error(exc)})
    out = {"ok": all(c["ok"] for c in checks), "checks": checks,
           "cache_hit": False, "cache_ttl_seconds": _DIAG_CACHE_TTL,
           "checked_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")}
    _DIAG_CACHE.update(key=key, payload=copy.deepcopy(out), expires=now + _DIAG_CACHE_TTL)
    return out


def runtime_payload():
    """通用运行时信息：所有 UI/Agent/插件都不再依赖固定主机或目录。"""
    cfg = load_config()
    dep = cfg.get("deployment") or {}
    port = int(dep.get("web_port") or 17890)
    mode = dep.get("mode") or ("docker" if (os.environ.get("PAN_CONFIG") or Path("/.dockerenv").exists()) else "local")
    root = str(default_root(cfg))
    dirs = dep.get("download_dirs")
    if not isinstance(dirs, dict) or not dirs:
        dirs = {"默认": root, "电影": str(Path(root) / "电影"), "音乐": str(Path(root) / "音乐"),
                "资料": str(Path(root) / "资料"), "临时": "/tmp"}
    return {
        "ok": True,
        "mode": mode,
        "mode_name": {"local": "本机", "nas_docker": "NAS Docker", "server_docker": "服务器 Docker", "docker": "Docker 容器"}.get(mode, mode),
        "web_host": dep.get("web_host") or "",
        "web_port": port,
        "api_url": dep.get("api_url") or "http://127.0.0.1:%d" % port,
        "download_root": root,
        "download_dirs": dirs,
        "services": {
            "alist": (cfg.get("engines") or {}).get("alist_url") or "",
            "rclone": (cfg.get("engines") or {}).get("rclone_remote") or "",
            "aria2": (cfg.get("engines") or {}).get("aria2_url") or "",
        },
    }


def recent_log_lines(limit=50):
    """读取最近关键日志；无权限或无文件时返回提示。"""
    p = Path(os.environ.get("PAN_LOG") or (SKILL_DIR / "pan.log"))
    if not p.exists():
        return ["暂无日志文件：%s" % p]
    try:
        return [x for x in p.read_text(errors="replace").splitlines()[-limit:]]
    except OSError as exc:
        return [_human_error(exc)]


def serve_settings_html():
    return """<!doctype html><html lang=zh-CN><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>网盘通 · 设置</title>
<style>:root{--bg:#0b1120;--panel:#111827;--line:#243244;--text:#e5edf8;--muted:#94a3b8;--acc:#38bdf8}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,PingFang SC,system-ui,sans-serif}.w{max-width:820px;margin:auto;padding:20px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;margin-bottom:14px}input,select{width:100%;padding:10px;border-radius:8px;border:1px solid var(--line);background:#020617;color:var(--text);margin-bottom:10px}button{width:100%;border:0;border-radius:8px;background:var(--acc);color:#06283d;font-weight:700;padding:11px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}@media(max-width:640px){.grid{grid-template-columns:1fr}}a{color:var(--acc);text-decoration:none}.msg{margin-top:8px;color:var(--muted)}</style></head><body><div class=w>
<h1>设置</h1><p><a href="/">← 返回控制台</a></p>
<div class=panel><label>AList 地址</label><input id=alist placeholder="http://127.0.0.1:5244"><label>rclone 远端</label><input id=remote placeholder="alist:"><label>默认下载目录</label><input id=root placeholder="/data/download"><div class=grid><label>并发数</label><input id=conn type=number min=1 max=16 value=4><label>通知钩子</label><input id=hook placeholder="可留空"></div><div class=grid><label>闲时窗口开始（HH:MM，配合 pan idle 用）</label><input id=idle_start type=time value="00:00"><label>闲时窗口结束</label><input id=idle_end type=time value="08:00"></div><button id=save>保存设置</button><div class=msg id=msg></div></div>
<script>fetch('/api/settings').then(r=>r.json()).then(d=>{const c=d.config||{};const e=c.engines||{};alist.value=e.alist_url||'';remote.value=e.rclone_remote||'';root.value=c.download_root||'';conn.value=(c.http||{}).max_connections_vip||4;hook.value=(c.http||{}).on_complete_hook||'';const w=(c.http||{}).idle_window||['00:00','08:00'];idle_start.value=w[0];idle_end.value=w[1]});save.onclick=async()=>{save.disabled=1;msg.textContent='保存中…';try{const r=await fetch('/api/settings',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({alist_url:alist.value,rclone_remote:remote.value,download_root:root.value,max_connections:Number(conn.value)||4,on_complete_hook:hook.value,idle_start:idle_start.value,idle_end:idle_end.value})});const j=await r.json();msg.textContent=j.ok?'✅ 已保存':'❌ '+(j.error||'失败')}catch(e){msg.textContent='❌ '+e}save.disabled=0};</script></div></body></html>"""


def serve_engines_html(url=""):
    """零客户端引擎桥说明页：不承诺绕过官方限制。"""
    cat = engine_catalog_payload(url)
    cards = "".join("""<article class=panel><div class=tag>%s</div><h2>%s</h2>
<p><b>默认兼容回退：</b>%s</p><p><b>零客户端桥：</b>%s</p></article>""" % (
        d["name"], d["drive"], d["default_engine"] or "-",
        " / ".join(x["label"] for x in d["zero_client"])
    ) for d in cat.get("drives", []))
    return """<!doctype html><html lang=zh-CN><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>网盘通 · 零客户端引擎桥</title>
<style>body{margin:0;background:#07111f;color:#e5edf8;font-family:-apple-system,PingFang SC,system-ui,sans-serif}.w{max-width:1180px;margin:auto;padding:20px}nav a{color:#38bdf8;text-decoration:none;margin-right:12px;font-size:13px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}.panel{background:#0f172a;border:1px solid #22314a;border-radius:16px;padding:16px}.tag{color:#38bdf8;font-size:12px}h2{margin:0 0 10px;font-size:18px}p,li{font-size:13px;line-height:1.6;color:#94a3b8}b{color:#e5edf8}</style></head><body><div class=w>
<header><h1>🧩 零客户端引擎桥</h1><nav><a href="/">任务中心</a><a href="/login">登录</a><a href="/live">进度</a><a href="/test">测试</a></nav></header>
<div class=panel style=margin-top:16px><h2>零客户端的含义</h2><p>不安装百度网盘、夸克、迅雷等桌面客户端；优先用官方网页生成直链，再交给浏览器插件捕获，或用 AList/OAuth/WebDAV 统一桥接。<b>不破解登录、签名、风控、限速或 DRM。</b>官方不给直链时，无法保证所有网盘都零客户端。</p></div>
<div class=grid style=margin-top:16px>__CARDS__</div>
<p style=margin-top:16px><a href=/api/engines>查看 JSON 引擎目录</a></p>
</div></body></html>""".replace("__CARDS__", cards)


def serve_login_html(drive=""):
    """统一登录/授权引导页：所有网盘共用“官方登录优先 + 状态页统一展示”。"""
    drive = str(drive or "").strip()
    notice = ""
    if drive:
        gate = login_gate_for_drive_key(drive)
        if gate.get("required"):
            notice = ('<div class="panel" style="border-color:#f59e0b;margin-top:16px"><b>当前：%s</b>'
                      '<p>%s — %s</p><p style="margin:8px 0 0"><a href="/test">登录后回测试页复核</a> · <a href="/">回任务中心</a></p></div>') % (
                      gate.get("drive_name", drive), gate.get("mode", ""), gate.get("message", ""))
    return """<!doctype html><html lang=zh-CN><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>网盘通 · 登录与授权</title>
<style>:root{--bg:#07111f;--panel:#0f172a;--line:#22314a;--text:#e5edf8;--muted:#94a3b8;--acc:#38bdf8}*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,PingFang SC,system-ui,sans-serif}.w{max-width:1180px;margin:auto;padding:20px}
header{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}nav a{color:var(--acc);text-decoration:none;margin-right:12px;font-size:13px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:16px}
h2{margin:0 0 10px;font-size:18px}p,li{font-size:13px;line-height:1.6;color:var(--muted)}b{color:var(--text)}
ul{padding-left:18px;margin:8px 0 0}.tag{font-size:12px;color:var(--acc);margin-bottom:4px}
</style></head><body><div class=w>
<header><h1>🔐 登录与授权</h1><nav><a href="/">任务中心</a><a href="/live">实时进度</a><a href="/test">测试连接</a><a href="/settings">设置</a><a href="/guide">教程</a></nav></header>
__LOGIN_NOTICE__
<div class="panel" style="margin-top:16px"><h2>铁律</h2>
<ul><li><b>官方登录优先</b>：扫码、OAuth、浏览器授权 > 手工 Cookie > 账号密码。</li>
<li><b>不在聊天里粘贴密码、Cookie、BDUSS、STOKEN、Token。</b></li>
<li><b>需要 Cookie 时</b>：只在本机浏览器/终端复制进系统凭据库或工具自己的配置，不发给 Agent。</li>
<li><b>不绕过</b>验证码、风控、限速、会员限制、DRM。</li>
<li><b>下载状态必须显示在 Web UI</b> 的任务中心和 /live，不再用聊天轮询刷屏。</li></ul></div>
<div class=grid style="margin-top:16px">
<article class=panel><div class=tag>百度网盘</div><h2>优先扫码登录</h2><p>用百度 App 扫码完成 BaiduPCS-Go 登录；避免复制 BDUSS/STOKEN。分享文件先转存到自己网盘，再走统一任务中心。</p><ul><li>支持：扫码、浏览器登录</li><li>禁止：聊天粘贴 Cookie、密码</li><li>状态：任务中心 / /live</li></ul></article>
<article class=panel><div class=tag>阿里云盘</div><h2>OAuth 优先</h2><p>优先官方开放平台 OAuth；个人快速使用可挂 AList 后扫码授权。不要把 refresh_token 发进聊天。</p><ul><li>支持：OAuth、扫码</li><li>凭据：AList/系统凭据库</li></ul></article>
<article class=panel><div class=tag>夸克 / 115 / 123 / 移动 / 天翼 / 迅雷</div><h2>AList 驱动优先</h2><p>优先在 AList 中按驱动提示完成扫码、OAuth 或 Cookie 授权。Cookie 只写进 AList/系统凭据库。</p><ul><li>支持：扫码、OAuth、Cookie</li><li>凭据：AList/系统凭据库</li></ul></article>
<article class=panel><div class=tag>OneDrive / Google Drive / Dropbox / SharePoint</div><h2>OAuth</h2><p>统一走官方 OAuth；不要账号密码交给 Agent。rclone/AList/官方 CLI 都应在系统凭据库或自身配置里保管 Token。</p><ul><li>支持：OAuth</li><li>凭据：rclone/AList/官方 CLI</li></ul></article>
<article class=panel><div class=tag>坚果云 / WebDAV</div><h2>应用密码</h2><p>使用坚果云的应用密码而不是账号密码，保存在系统凭据库或 rclone 配置中。</p><ul><li>支持：WebDAV 应用密码</li><li>凭据：系统凭据库/rclone</li></ul></article>
<article class=panel><div class=tag>其他网盘</div><h2>官方通道优先</h2><p>优先官方客户端/CLI 或公开直链；仅当工具明确要求 Cookie/Token 时，才在本机完成凭据写入。禁止把敏感值发到聊天。</p><ul><li>支持：官方客户端、CLI、直链</li><li>凭据：系统凭据库</li></ul></article>
</div>
<p style="margin-top:16px;color:var(--muted);font-size:12px">遇到平台限制时，只报告真实原因；不破解、不伪造登录态、不绕过限速或风控。</p>
</div></body></html>""".replace("__LOGIN_NOTICE__", notice)

def serve_logs_html():
    rows = "".join("<div class=log>%s</div>" % x.replace("&", "&amp;").replace("<", "&lt;") for x in recent_log_lines(50))
    return """<!doctype html><html lang=zh-CN><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>网盘通 · 日志</title><style>body{background:#0b1120;color:#e5edf8;font-family:ui-monospace,Menlo,monospace;margin:0;padding:20px}a{color:#38bdf8;text-decoration:none}.box{background:#020617;border:1px solid #243244;border-radius:10px;padding:12px;white-space:pre-wrap;overflow:auto;max-height:80vh}.log{padding:3px 0;border-bottom:1px solid #16212f;font-size:12px}</style></head><body><h1>最近日志</h1><p><a href="/">← 返回控制台</a></p><div class=box>%s</div></body></html>""" % (rows or "<div class=log>暂无日志</div>")


def serve_home_html(tasks):
    """极简自动下载控制台：投递即开始，前端 10 秒无刷新轮询；提交后立即回执受理与耗时。"""
    return r"""<!doctype html><html lang=zh-CN><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>网盘通 · 零客户端下载</title>
<link rel="manifest" href="/manifest.webmanifest">
<script>if('serviceWorker'in navigator){navigator.serviceWorker.register('/sw.js')}</script>
<style>
:root{--bg:#07111f;--panel:#0f172a;--line:#22314a;--text:#e5edf8;--muted:#94a3b8;--acc:#38bdf8;--ok:#4ade80;--bad:#f87171}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,"PingFang SC","Microsoft YaHei",system-ui,sans-serif}
.w{max-width:1180px;margin:auto;padding:20px}header{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:14px}
h1{font-size:21px;margin:0}small{color:var(--muted);font-weight:400}nav a{color:var(--acc);text-decoration:none;margin-left:12px;font-size:13px}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:16px;margin-bottom:14px}
.drop{font-size:17px;padding:15px;border:1px dashed #3b82f6;border-radius:12px}.drop:focus{outline:2px solid var(--acc);outline-offset:1px}
.msg{min-height:22px;color:var(--muted);font-size:13px;margin:8px 2px 0}.msg.ok{color:var(--ok)}.msg.bad{color:var(--bad)}
.adv{margin-top:10px;color:var(--muted);font-size:12px}.adv summary{cursor:pointer}.adv-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:8px}
label{display:block;color:var(--muted);font-size:12px;margin-bottom:4px}input,select{width:100%;background:#020617;border:1px solid var(--line);color:var(--text);border-radius:9px;padding:9px}
.tasks{display:grid;gap:10px}.task{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:13px}
.top,.stats,.ops{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font-size:12px;color:var(--muted)}
.name{font-size:15px;margin:6px 0;word-break:break-all}.bar{height:9px;background:#1e293b;border-radius:99px;overflow:hidden}.bar i{display:block;height:100%;background:linear-gradient(90deg,#38bdf8,#22c55e);width:0;transition:width .25s}
.stats{margin-top:8px}.path{margin-top:7px;color:var(--muted);font-size:12px;word-break:break-all}.ops{margin-top:8px}.ops a{color:var(--acc);text-decoration:none}
.pathline{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.pathline code{color:#dbeafe;font-size:11px;font-family:ui-monospace,Menlo,monospace}.copy{background:#13233b;border:1px solid #334f78;color:#bfdbfe;border-radius:7px;padding:3px 8px;font-size:11px;cursor:pointer}.copy:hover{background:#1d3557}
.state{font-weight:700}.state.running{color:#facc15}.state.done{color:var(--ok)}.state.failed,.state.cancelled{color:var(--bad)}.state.paused{color:#cbd5e1}
.empty{color:var(--muted);font-size:14px;text-align:center;padding:28px}.foot{color:var(--muted);font-size:12px;text-align:center;margin-top:18px}
@media(max-width:760px){.adv-grid{grid-template-columns:1fr}}
</style></head><body><div class=w>
<header><h1>⏬ 网盘通 <small id=runtime>零客户端下载 · 粘贴链接后自动开始</small></h1><nav><a href=/test>测试</a><a href=/live>速度</a><a href=/engines>引擎</a><a href=/settings>设置</a><a href=/logs>日志</a></nav></header>
<section class=panel>
<input class=drop id=url autocomplete=off placeholder="粘贴百度网盘/直链后自动开始（支持多行）">
<div id=msg class=msg>无需点击开始；链接中的 pwd 会自动识别。</div>
<details class=adv><summary>可选设置（默认已自动）</summary><div class=adv-grid>
<div><label>提取码</label><input id=pwd autocomplete=off placeholder="链接内已含时可留空"></div>
<div><label>下载目录</label><select id=to><option value="">默认目录</option></select></div>
<div><label>引擎</label><select id=engine><option value="">自动</option><option value=baiduweb>百度官方网页会话</option><option value=browser>浏览器直链桥</option></select></div>
</div></details>
</section>
<section><h2 style="font-size:16px;margin:4px 0 10px">任务中心</h2><div id=tasks class=tasks><div class=empty>暂无任务</div></div></section>
<div class=foot>状态由本地服务实时刷新；不在聊天里轮询进度。遇验证码/风控/会员/付费限制会安全失败。</div>
<script>
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function size(n){n=Number(n||0);if(!n)return '-';if(n>=1073741824)return (n/1073741824).toFixed(2)+' GB';if(n>=1048576)return (n/1048576).toFixed(2)+' MB';return (n/1024).toFixed(1)+' KB'}
function speed(n){if(n==null||n==='')return '-';n=Number(n);if(n>=1024)return (n/1024).toFixed(2)+' MB/s';return n.toFixed(1)+' KB/s'}
function eta(n){if(n==null||n==='')return '-';n=Number(n);if(n<=0)return '即将完成';if(n<60)return Math.round(n)+' 秒';if(n<3600)return Math.floor(n/60)+' 分 '+Math.round(n%60)+' 秒';return Math.floor(n/3600)+' 时 '+Math.floor((n%3600)/60)+' 分'}
function stateText(s){return ({running:'下载中',done:'已完成',failed:'失败',paused:'已暂停',cancelled:'已取消',unknown:'等待中'})[s]||s||'等待中'}
function taskHtml(t){
 const total=Number(t.files_total||0),done=Number(t.files_done||0),failed=Number(t.files_failed||0);
 let pct=Number(t.percent);if(!Number.isFinite(pct)){const tb=Number(t.total_bytes||0),bd=Number(t.bytes_done||0);pct=tb?bd*100/tb:0}
 pct=Math.max(0,Math.min(100,pct||0));
 const name=t.current_file||t.name||String(t.target||t.url||'任务').split('/').pop()||'任务';
 const count=total?(`${done}/${total} 已完成 · ${failed} 失败`):(t.state==='done'?'完成':'-');
 const ops=t.state==='running'?`<a href="/api/task/action?task=${encodeURIComponent(t.id)}&action=pause">暂停</a><a href="/api/task/action?task=${encodeURIComponent(t.id)}&action=delete">删除</a>`:t.state==='paused'?`<a href="/api/task/action?task=${encodeURIComponent(t.id)}&action=resume">继续</a><a href="/api/task/action?task=${encodeURIComponent(t.id)}&action=delete">删除</a>`:`<a href="/api/task/action?task=${encodeURIComponent(t.id)}&action=retry">重试</a><a href="/api/task/action?task=${encodeURIComponent(t.id)}&action=delete">删除</a>`;
 let loc=t.local_path||t.target||'-';const cf=t.current_file||'';if(cf&&loc&&!String(loc).includes(cf))loc=String(loc).replace(/[\\/]+$/,'')+'/'+cf;
 return `<article class=task><div class=top><span class="state ${esc(t.state||'')}">${esc(stateText(t.state))}</span><span>${esc(t.drive_name||t.drive||'直链')} · ${esc(t.engine||'-')}</span></div><div class=name>${esc(name)}</div><div class=bar><i style="width:${pct}%"></i></div><div class=stats><span>总进度 ${pct.toFixed(1)}% · ${size(t.bytes_done)} / ${size(t.total_bytes)}</span><span>${esc(count)}</span><span>${speed(t.speed_kbps)} · 剩余 ${eta(t.eta_seconds)}</span></div><div class=path>状态：${esc(t.status_text||stateText(t.state))}<div class=pathline><span>下载位置：</span><code>${esc(loc)}</code><button class=copy type=button data-path="${esc(loc)}">复制路径</button></div></div><div class=ops>${ops}</div></article>`;
}
async function copyPath(text,btn){try{await navigator.clipboard.writeText(text)}catch(e){const ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();document.execCommand('copy');ta.remove()}btn.textContent='已复制';setTimeout(()=>btn.textContent='复制路径',1200)}
document.getElementById('tasks').addEventListener('click',e=>{const b=e.target.closest('.copy');if(b)copyPath(b.dataset.path||'',b)});
async function loadTasks(){try{const j=await (await fetch('/api/tasks',{cache:'no-store'})).json();const list=j.tasks||[];document.getElementById('tasks').innerHTML=list.length?list.map(taskHtml).join(''):'<div class=empty>暂无任务</div>'}catch(e){}}
let lastSubmit='',submitting=false;
async function submitUrls(){
 const raw=document.getElementById('url').value.trim();const urls=raw.split(/\s+/).filter(x=>/^https?:\/\//i.test(x));
 if(!urls.length||submitting)return;const sig=urls.join('\n');if(sig===lastSubmit)return;submitting=true;lastSubmit=sig;
 const msg=document.getElementById('msg');msg.className='msg';msg.textContent='已受理，正在派发…（本地服务通常 <50ms 返回）';
 const t0=performance.now();
 try{const body={urls,pwd:document.getElementById('pwd').value.trim(),to:document.getElementById('to').value,engine:document.getElementById('engine').value};const j=await (await fetch('/api/download',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})).json();const ms=Math.round(j.dispatch_ms!=null?j.dispatch_ms:(performance.now()-t0));if(!j.ok){msg.className='msg bad';msg.textContent='投递失败：'+(j.error||j.message||'未知错误')}else{msg.className='msg ok';msg.textContent='已受理 '+urls.length+' 个任务（'+ms+'ms）· 实时进度见 '+(j.live_url||'/live');document.getElementById('url').value='';loadTasks()}}catch(e){msg.className='msg bad';msg.textContent='通信失败：'+e}finally{submitting=false}
}
const input=document.getElementById('url');let debounce=null;function schedule(){clearTimeout(debounce);debounce=setTimeout(submitUrls,120)}
input.addEventListener('paste',()=>setTimeout(submitUrls,0));input.addEventListener('input',schedule);input.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();submitUrls()}});
fetch('/api/runtime').then(r=>r.json()).then(r=>{document.getElementById('runtime').textContent='零客户端下载 · '+(r.mode_name||r.mode||'local');const to=document.getElementById('to');to.innerHTML='<option value="">默认目录</option>'+Object.entries(r.download_dirs||{}).map(([k,v])=>`<option value="${esc(v)}">${esc(k)}</option>`).join('')}).catch(()=>{});
loadTasks();setInterval(loadTasks,10000);
</script></div></body></html>"""

def serve_test_html():
    """独立「测试连接」页：粘贴链接→调用 /api/test→人话结果（不自动刷新，避免打断输入）。"""
    return """<!doctype html><html lang=zh-CN><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>多网盘 · 测试连接</title>
<link rel="manifest" href="/manifest.webmanifest">
<script>if('serviceWorker'in navigator){navigator.serviceWorker.register('/sw.js')}</script>
<style>
:root{--bg:#0f172a;--panel:#1e293b;--line:#334155;--text:#e2e8f0;--muted:#94a3b8;--acc:#38bdf8}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,"PingFang SC","Microsoft YaHei",system-ui,sans-serif}
.wrap{max-width:760px;margin:0 auto;padding:24px 18px 40px}
header{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:18px}
header h1{font-size:20px;margin:0}
.nav a{color:var(--acc);text-decoration:none;font-size:13px;margin-left:12px}
.nav a:hover{text-decoration:underline}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px}
form{display:grid;gap:10px;margin-bottom:6px}
input{background:#0b1120;border:1px solid var(--line);border-radius:8px;color:var(--text);padding:10px 12px;font-size:14px}
button{border:0;border-radius:8px;background:var(--acc);color:#052e16;font-size:14px;font-weight:600;padding:11px;cursor:pointer}
button:hover{opacity:.9}
.row{display:flex;justify-content:space-between;gap:12px;padding:9px 2px;border-bottom:1px solid var(--line);font-size:13px}
.row:last-child{border-bottom:none}
.row .name{white-space:nowrap}
.row .detail{color:var(--muted);text-align:right;word-break:break-all}
.ok{color:#4ade80}.bad{color:#f87171}
.sum{font-size:16px;font-weight:700;padding:10px 2px}
.empty{color:var(--muted);font-size:13px;padding:8px 2px}
</style></head><body><div class=wrap>
<header><h1>🧪 多网盘 · 测试连接</h1><div class=nav>
<a href=/guide>使用教程</a><a href=/>任务中心</a><a href=/live>实时速度</a>
</div></header>
<div class=panel>
<form id=testForm>
<input id=testUrl type=text placeholder="粘贴网盘分享链接或 HTTP 直链" required>
<input id=testPwd type=text placeholder="提取码（没有可留空）" autocomplete=off>
<button type=submit>开始测试</button>
</form>
<p style="color:var(--muted);font-size:12px;margin:6px 0 0">一次本地路由：识别网盘、登录/授权、依赖与配置、目标目录、提取码和零客户端桥。不会下载文件、不发请求到网盘页面。</p>
<div id=result></div>
</div>
<script>
document.getElementById('testForm').addEventListener('submit', async function (e) {
  e.preventDefault();
  const url = document.getElementById('testUrl').value.trim();
  if (!url) { return; }
  const pwd = document.getElementById('testPwd').value.trim();
  const out = document.getElementById('result');
  out.innerHTML = '<div class=empty>测试中…</div>';
  try {
    const qs = new URLSearchParams({ url: url });
    if (pwd) { qs.append('pwd', pwd); }
    const resp = await fetch('/api/route?' + qs.toString());
    const j = await resp.json();
    let html = '';
    const marks = [];
    (j.checks || []).forEach(function (c) {
      const mark = c.ok ? '✅' : '❌';
      marks.push(c.ok);
      html += '<div class="row"><span class="name ' + (c.ok ? 'ok' : 'bad') + '">' + mark + ' ' + (c.name || '') + '</span><span class="detail">' + (c.detail || '') + '</span></div>';
    });
    const allOk = marks.length > 0 && marks.every(Boolean);
    const next = j.next_action || '';
    let summary = allOk ? '✅ 可以开始下载' : '❌ 当前还不能直接下载';
    if (next === 'login' && j.login_url) { summary = '⚠️ 需要登录/授权：<a href="' + j.login_url + '">打开登录页</a>'; }
    html = '<div class="sum ' + (allOk ? 'ok' : 'bad') + '">' + summary + ' <small>' + (j.latency_ms || '-') + 'ms</small></div>' + html;
    out.innerHTML = html;
  } catch (err) {
    out.innerHTML = '<div class="row"><span class="name bad">❌ 通信失败</span><span class="detail">请确认本机服务已运行：python3 scripts/pan.py serve</span></div>';
  }
});
</script>
</div></body></html>"""





def bookmarklet_js():
    """生成书签栏一键投递脚本（拖到书签栏，在任何网页点一下即可把媒体链接投给本机/NAS pan serve）。"""
    return (
        "javascript:(function(){"
        "var d=document;var u='';"
        "var s=window.getSelection?String(window.getSelection()):'';"
        "if(/^https?:\/\//.test(s)){u=s;}else{"
        "var cands=[];d.querySelectorAll('a[href],video[src],source[src],audio[src]').forEach(function(el){"
        "var h=el.href||el.src||'';if(/^(https?:)?\/\//.test(h)){cands.push(h)}});"
        "if(cands.length){u=cands[0]}else{u=location.href}}"
        "u=prompt('投递到网盘通\n（回车确认，ESC 取消）',u);"
        "if(!u){return}"
        "var api=location.origin.replace(/:\\d+$/',':17890')+'/api/download';"
        "if(location.port==='17890'){api='/api/download'}"
        "fetch(api,{method:'POST',headers:{'Content-Type':'application/json'},"
        "body:JSON.stringify({url:u})}).then(function(r){return r.json()}).then(function(j){"
        "alert(j.ok?('✅ 已投递：'+(j.live_url||j.home_url||'')):('❌ '+(j.error||'失败')))"
        "}).catch(function(e){alert('❌ 连接失败：'+e)})})()"
    )


def cmd_serve(args):
    try:
        from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    except ImportError:
        print("❌ 当前环境无 http.server")
        return 1
    import threading
    import hmac as _hmac
    import secrets as _secrets
    cfg = load_config()
    reports_dir = os.path.expanduser(args.reports_dir) if args.reports_dir else str(web_state_root(cfg))
    host, port = args.host, int(args.port)

    # ---- 鉴权（修复：Web API 此前完全无鉴权，配合 --host 0.0.0.0 构成 LAN RCE 面）----
    LOOPBACK = {"127.0.0.1", "localhost", "::1"}
    is_loopback = host in LOOPBACK
    if not (cfg.get("web_auth_token") or "").strip():
        cfg["web_auth_token"] = _secrets.token_urlsafe(24)
        save_config(cfg)
    token = cfg["web_auth_token"]
    # PAN_NOAUTH=1 仅在回环绑定下允许关闭鉴权；非回环强制开启
    auth_enabled = True if not is_loopback else os.environ.get("PAN_NOAUTH") != "1"
    failed = {}  # ip -> [次数, 首次时间戳]；连败 10 次拉黑 5 分钟

    def _token_ok(provided: str) -> bool:
        return bool(provided) and _hmac.compare_digest(str(provided), token)

    def _client_allowed(ip: str) -> bool:
        import time as _time
        rec = failed.get(ip)
        if not rec:
            return True
        if _time.time() - rec[1] > 300:
            failed.pop(ip, None)
            return True
        return rec[0] < 10

    def _record_fail(ip: str) -> None:
        import time as _time
        rec = failed.get(ip)
        if rec and _time.time() - rec[1] <= 300:
            rec[0] += 1
        else:
            failed[ip] = [1, _time.time()]

    _TOKEN_SCRIPT = (
        '<script>(function(){var T=%r;var of=window.fetch;'
        'window.fetch=function(u,o){try{if(typeof u==="string"&&u.indexOf("/api/")===0)'
        '{u=u+(u.indexOf("?")>=0?"&":"?")+"token="+encodeURIComponent(T)}}catch(e){}'
        'return of(u,o)}})();</script>'
    ) % token

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _ip(self):
            return self.client_address[0] if self.client_address else "?"

        def _reject_auth(self):
            ip = self._ip()
            if not _client_allowed(ip):
                self.send_error(403, "temporarily blocked")
                return
            _record_fail(ip)
            try:
                self.send_response(401)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("WWW-Authenticate", 'Bearer realm="pan"')
                self.end_headers()
                self.wfile.write(json.dumps({"ok": False, "error": "unauthorized"}).encode("utf-8"))
            except OSError:
                pass

        def _authed(self) -> bool:
            """校验 Authorization: Bearer <token> 或 ?token=<token>。"""
            if not auth_enabled:
                return True
            q = urlparse(self.path).query
            provided = ""
            if q:
                provided = (dict(parse_qs(q)).get("token") or [""])[0]
            if not provided:
                provided = (self.headers.get("Authorization") or "").replace("Bearer ", "", 1).strip()
            if _token_ok(provided):
                return True
            self._reject_auth()
            return False

        def _json(self, obj):
            data = json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _html(self, text):
            if auth_enabled and "<script>" in text:
                # 注入 fetch 包装：页面内所有 /api/ 请求自动带上 token
                text = text.replace("<script>", _TOKEN_SCRIPT + "<script>", 1)
            data = text.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _raw(self, data, content_type):
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_POST(self):
            if not self._authed():
                return
            length = int(self.headers.get("Content-Length", 0) or 0)
            raw = b""
            if length:
                raw = self.rfile.read(length)
            try:
                body = json.loads(raw.decode("utf-8") or "{}")
            except (ValueError, UnicodeDecodeError):
                body = {}
            if self.path.startswith("/api/download"):
                urls = body.get("urls") or ([body.get("url")] if body.get("url") else [])
                if not isinstance(urls, list):
                    urls = [urls]
                urls = [str(x).strip() for x in urls if str(x).strip()]
                if not urls:
                    self._json({"ok": False, "error": "缺少下载链接", "human": "请先粘贴至少一个 HTTP/HTTPS 链接。"})
                    return
                _t0 = time.perf_counter()
                cfg_once = load_config()          # 整批只读一次配置，避免逐条深拷贝+重复读盘
                _pwd = body.get("pwd") or ""
                _to = body.get("to") or ""
                _engine = body.get("engine") or ""
                _tier = body.get("tier") or ""
                _path = body.get("path") or ""
                _confirm = bool(body.get("confirm_auth"))
                errors, queued = [], []
                # 登录门禁是纯本机毫秒级检查，必须同步做完：需要登录时要立刻回 /login。
                for url in urls[:100]:
                    auth = fast_login_gate(url, cfg_once)
                    if auth.get("blocking") and not _confirm:
                        errors.append({"url": url, "error": "login_required", "human": auth.get("message", "需要先完成官方登录/授权"),
                                       "login_url": auth.get("login_url", "/login"), "drive": auth.get("drive", "")})
                        continue
                    queued.append(url)

                def _dispatch_batch(url_list):
                    """分批派发下载进程；放到后台线程，HTTP 不再为 N 次 fork 买单。"""
                    for u in url_list:
                        _pid, _err = _spawn_download_task(u, pwd=_pwd, to=_to, engine=_engine, tier=_tier, path=_path)
                        if _err:
                            log_line("download dispatch failed: %s -> %s" % (_redact_task_url(u), _err))
                results, async_dispatch = [], False
                if len(queued) == 1:
                    # 单个链接同步派发：立即拿到真实 PID，浏览器插件/Agent 语义不变。
                    pid, err = _spawn_download_task(queued[0], pwd=_pwd, to=_to, engine=_engine, tier=_tier, path=_path)
                    if err:
                        errors.append({"url": queued[0], "error": err, "human": _human_error(err)})
                    else:
                        results.append({"url": queued[0], "pid": pid})
                elif queued:
                    # 多链接批量：先回执受理，下载进程在后台线程里派发，响应时间与链接数解耦。
                    threading.Thread(target=_dispatch_batch, args=(list(queued),), daemon=True).start()
                    results = [{"url": u, "pid": ""} for u in queued]
                    async_dispatch = True
                first_auth_error = next((e for e in errors if e.get("login_url")), {})
                dispatch_ms = round((time.perf_counter() - _t0) * 1000, 1)
                first_pid = next((r["pid"] for r in results if r.get("pid")), "")
                self._json({"ok": not errors, "message": "已受理 %d 个任务，失败 %d 个。" % (len(queued), len(errors)),
                            "results": results, "errors": errors,
                            "pid": first_pid, "accepted": len(queued), "queued": len(queued) if async_dispatch else 0,
                            "async": async_dispatch,
                            "accepted_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                            "dispatch_ms": dispatch_ms,
                            "live_url": "http://%s:%d/live" % (host, port),
                            "login_required": bool(first_auth_error), "login_url": first_auth_error.get("login_url", ""),
                            "home_url": "http://%s:%d/" % (host, port)})
            elif self.path.startswith("/api/settings"):
                cfg = load_config()
                cfg.setdefault("engines", {})["alist_url"] = str(body.get("alist_url") or "").strip()
                cfg.setdefault("engines", {})["rclone_remote"] = str(body.get("rclone_remote") or "").strip()
                cfg["download_root"] = str(body.get("download_root") or "").strip()
                cfg.setdefault("http", {})["max_connections_vip"] = max(1, min(16, int(body.get("max_connections") or 4)))
                # F2（v0.20.0）：闲时窗口，格式 HH:MM，跨午夜允许（如 22:00-06:00）
                idle_win = []
                for key in ("idle_start", "idle_end"):
                    v = str(body.get(key) or "").strip()
                    if v and len(v.split(":")) == 2 and all(x.isdigit() for x in v.split(":")):
                        idle_win.append("%02d:%02d" % (int(v.split(":")[0]) % 24, int(v.split(":")[1]) % 60))
                if len(idle_win) == 2:
                    cfg.setdefault("http", {})["idle_window"] = idle_win
                elif idle_win:
                    self._json({"ok": False, "error": "闲时窗口需要同时填开始和结束（HH:MM）"})
                    return
                hook_warn = ""
                if body.get("on_complete_hook"):
                    # 安全修复：on_complete_hook 会在下载完成后被执行（report.run_completion_hook），
                    # 不允许经 Web API 写入；如需使用请手工编辑配置文件并配置 hook_whitelist。
                    hook_warn = "on_complete_hook 出于安全考虑不接受 Web 修改，请手工编辑配置文件"
                save_config(cfg)
                self._json({"ok": True, "message": "设置已保存" if not hook_warn else "设置已保存；" + hook_warn,
                            "warning": hook_warn})
            elif self.path.startswith("/api/task/action"):
                q = dict(parse_qs(self.path.split("?", 1)[1])) if "?" in self.path else {}
                action = (body.get("action") or q.get("action") or [""])
                task = (body.get("task") or q.get("task") or [""])
                action = action[0] if isinstance(action, list) else action
                task = task[0] if isinstance(task, list) else task
                if action not in ("pause", "resume", "delete", "retry"):
                    self._json({"ok": False, "error": "未知操作"})
                elif not task:
                    self._json({"ok": False, "error": "缺少 task"})
                else:
                    ok, msg = _apply_task_action(reports_dir, task, action)
                    self._json({"ok": ok, "action": action, "task": task, "message": msg})
            else:
                self.send_error(404, "Not Found")

        def do_GET(self):
            if self.path.startswith("/api/") and not self._authed():
                return
            if self.path in ("/manifest.webmanifest", "/manifest.json"):
                self._raw(pwa_manifest_json().encode("utf-8"), "application/manifest+json; charset=utf-8")
            elif self.path in ("/bookmarklet.js", "/bookmarklet"):
                self._raw(bookmarklet_js().encode("utf-8"), "application/javascript; charset=utf-8")
            elif self.path == "/sw.js":
                self._raw(pwa_service_worker_js().encode("utf-8"), "application/javascript; charset=utf-8")
            elif self.path.startswith("/icons/icon-") and self.path.endswith(".png"):
                size = int("".join(ch for ch in self.path.split("-")[-1].split(".")[0] if ch.isdigit()) or 192)
                self._raw(pwa_icon_png(size), "image/png")
            elif self.path.startswith("/api/runtime"):
                self._json(runtime_payload())
            elif self.path.startswith("/api/engines"):
                q = dict(parse_qs(self.path.split("?", 1)[1])) if "?" in self.path else {}
                self._json(engine_catalog_payload((q.get("url") or [""])[0]))
            elif self.path.startswith("/api/diagnostics"):
                q = dict(parse_qs(self.path.split("?", 1)[1])) if "?" in self.path else {}
                self._json(diagnostics_payload(force=(q.get("refresh") or [""])[0] == "1"))
            elif self.path.startswith("/api/settings"):
                self._json({"ok": True, "config": load_config()})
            elif self.path.startswith("/api/reports"):
                self._json({"reports": serve_reports_json(reports_dir)})
            elif self.path.startswith("/api/route"):
                q = dict(parse_qs(self.path.split("?", 1)[1])) if "?" in self.path else {}
                url = (q.get("url") or [""])[0]
                if not url:
                    self._json({"ok": False, "error": "缺少 url 参数"})
                else:
                    self._json(route_link_payload(load_config(), url,
                                                  pwd=(q.get("pwd") or [""])[0],
                                                  engine=(q.get("engine") or [""])[0],
                                                  tier=(q.get("tier") or [""])[0],
                                                  path=(q.get("path") or [""])[0]))
            elif self.path.startswith("/api/test"):
                q = dict(parse_qs(self.path.split("?", 1)[1])) if "?" in self.path else {}
                url = (q.get("url") or [""])[0]
                if not url:
                    self._json({"ok": False, "error": "缺少 url 参数"})
                else:
                    rel = _probe_link_checks(load_config(), url,
                                             pwd=(q.get("pwd") or [""])[0],
                                             engine=(q.get("engine") or [""])[0],
                                             tier=(q.get("tier") or [""])[0],
                                             path=(q.get("path") or [""])[0])
                    self._json(rel)
            elif self.path.startswith("/api/tasks"):
                st = ""
                for part in self.path.split("?")[-1].split("&"):
                    if part.startswith("state="):
                        st = part.split("=", 1)[1]
                self._json({"tasks": serve_unified_tasks(reports_dir, limit=100, state=st or None)})
            elif self.path.startswith("/api/status"):
                self._json({"ok": True, "reports_dir": reports_dir,
                            "reports": len(serve_reports_json(reports_dir)),
                            "live": len(serve_live_json(reports_dir)),
                            "tasks": len(serve_unified_tasks(reports_dir))})
            elif self.path.startswith("/api/live"):
                self._json({"live": serve_live_json(reports_dir)})
            elif self.path.startswith("/api/task/action"):
                q = dict(parse_qs(self.path.split("?", 1)[1])) if "?" in self.path else {}
                action = (q.get("action") or [""])[0]
                task = (q.get("task") or [""])[0]
                if action not in ("pause", "resume", "delete", "retry"):
                    self._json({"ok": False, "error": "未知操作"})
                elif not task:
                    self._json({"ok": False, "error": "缺少 task 参数"})
                else:
                    ok, msg = _apply_task_action(reports_dir, task, action)
                    self._json({"ok": ok, "action": action, "task": task, "message": msg})
            elif self.path.startswith("/api/tasks") or self.path.startswith("/api/task-json"):
                st = ""
                for part in self.path.split("?")[-1].split("&"):
                    if part.startswith("state="):
                        st = part.split("=", 1)[1]
                self._json({"tasks": serve_unified_tasks(reports_dir, limit=100, state=st or None)})
            elif self.path in ("/live", "/live.html"):
                live = serve_live_json(reports_dir)
                body, items_json = render_live_table(live)
                self._html(serve_live_page_html(body, items_json=items_json))
            elif urlparse(self.path).path in ("/login", "/login.html"):
                q = dict(parse_qs(urlparse(self.path).query))
                drive = (q.get("drive") or [""])[0]
                self._html(serve_login_html(drive))
            elif urlparse(self.path).path in ("/engines", "/engines.html"):
                q = dict(parse_qs(urlparse(self.path).query))
                self._html(serve_engines_html((q.get("url") or [""])[0]))
            elif self.path in ("/test", "/test.html"):
                self._html(serve_test_html())
            elif self.path in ("/settings", "/settings.html"):
                self._html(serve_settings_html())
            elif self.path in ("/logs", "/logs.html"):
                self._html(serve_logs_html())
            elif self.path in ("/guide", "/guide.html"):
                self._html(serve_guide_html())
            elif self.path in ("/", "/index.html"):
                self._html(serve_home_html(serve_unified_tasks(reports_dir)))
            else:
                self.send_error(404, "Not Found")

    try:
        httpd = ThreadingHTTPServer((host, port), Handler)
    except OSError as exc:
        print("❌ 启动失败 %s:%s：%s" % (host, port, exc))
        return 1
    print("Web 控制台：http://%s:%s/（含任务投递/设置等写接口，已启用 token 鉴权）" % (host, port), flush=True)
    if auth_enabled:
        print("鉴权已启用：API 请求需携带 token（Authorization: Bearer <token> 或 ?token=…）", flush=True)
        print("带 token 入口：http://%s:%s/?token=%s" % (host, port, token), flush=True)
        if not is_loopback:
            print("⚠️ 监听在非回环地址 %s：token 强制启用；on_complete_hook 禁止经 Web 修改" % host, flush=True)
    else:
        print("⚠️ PAN_NOAUTH=1：鉴权已关闭（仅回环绑定允许）。请勿在此模式下暴露到局域网。", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0
