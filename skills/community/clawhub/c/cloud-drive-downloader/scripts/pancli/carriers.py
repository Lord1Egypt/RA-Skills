#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pan-downloader — 下载载具 / 任务控制 / 目录 / 通知 / 直链 / 转存子模块。"""
from __future__ import annotations

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


import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

# 共享工具函数从 engine 懒加载（engine 的命令为懒代理，运行期才 import 本模块，避免循环引用）。
from pancli.engine import *  # noqa: F401,F403
from pancli.report import _atomic_write_json  # noqa: F401

COMPANY_DEST_MARKERS = ("/volumes/办公", "/volumes/拓展", "/mnt/办公", "/mnt/拓展", r"\\办公", r"\\拓展", "公司知识库")


def is_company_destination(dst):
    low = str(dst or "").lower()
    return any(m in low for m in COMPANY_DEST_MARKERS)


def scan_transfer_dest_guard(cfg, dst, allow_flag):
    if not is_company_destination(dst):
        return ""
    if allow_flag:
        return ""
    if bool((cfg.get("transfer") or {}).get("allow_company_dest")):
        return ""
    return "目标目录命中公司数据红线（只下载不上传默认不开放）：%s；确认允许请加 --allow-company-dest" % dst


def _transfer_args(cfg, args, kind):
    tcfg = cfg.get("transfer", {}) or {}
    transfers = getattr(args, "transfers", None) or tcfg.get("default_transfers", 4)
    checkers = getattr(args, "checkers", None) or tcfg.get("default_checkers", 8)
    return int(transfers), int(checkers)


def run_transfer_sync(kind, args):
    cfg = load_config()
    dst = args.dst
    guard = scan_transfer_dest_guard(cfg, dst, bool(getattr(args, "allow_company_dest", False)))
    if guard:
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "kind": kind, "error": guard, "missing": []}, ensure_ascii=False, indent=2))
        else:
            print("❌ %s" % guard)
        return 4
    if kind == "sync" and not getattr(args, "delete", False):
        msg = "sync 会删除目标多余文件，必须显式加 --delete + --apply"
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "kind": kind, "error": msg, "missing": []}, ensure_ascii=False, indent=2))
        else:
            print("❌ %s" % msg)
        return 3
    rclone = find_engine_binary("rclone", cfg)
    if not rclone:
        msg = "未安装 rclone。跨盘转存/同步依赖 rclone（brew install rclone），先用 pan.py doctor 确认"
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "kind": kind, "error": msg, "missing": ["rclone"]}, ensure_ascii=False, indent=2))
        else:
            print("❌ %s" % msg)
        return 2
    transfers, checkers = _transfer_args(cfg, args, kind)
    argv = [rclone, "copy" if kind == "transfer" else "sync",
            args.src, dst, "--transfers", str(transfers), "--checkers", str(checkers)]
    apply_run = bool(getattr(args, "apply", False))
    if not apply_run:
        argv.append("--dry-run")
    if getattr(args, "json", False):
        print(json.dumps({"ok": True, "kind": kind, "dry_run": not apply_run,
                          "rclone": rclone, "command": argv, "src": args.src, "dst": dst,
                          "transfers": transfers, "checkers": checkers}, ensure_ascii=False, indent=2))
    else:
        print("命令：" + " ".join(mask_argv(argv)))
        print("目标：%s" % dst)
        print("模式：%s" % ("dry-run（未实际执行；确认后加 --apply）" if not apply_run else "实际执行"))
    if not apply_run:
        return 0
    log_line("%s rclone=%s src=%s dst=%s" % (kind.upper(), rclone, args.src, dst))
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=0)
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("❌ rclone 执行失败：%s" % exc)
        return 127
    out = (proc.stdout or "").strip() + ("\n" + (proc.stderr or "").strip() if proc.stderr else "")
    if out:
        print(out[:2000])
    if proc.returncode == 0:
        print("✅ %s 完成：%s -> %s" % (kind, args.src, dst))
    return proc.returncode


def cmd_transfer(args):
    return run_transfer_sync("transfer", args)


def cmd_sync(args):
    return run_transfer_sync("sync", args)



def notify_webhook_url(cfg, channel):
    key = str(((cfg.get("notify") or {}).get(channel + "_secret") or "")).strip() or ("notify." + channel)
    value = keychain_get(key)
    return value, key

def build_notify_payload(channel, title, body, chat_id=""):
    content = (title + "\n" + body).strip()
    if channel == "work_weixin":
        return json.dumps({"msgtype": "text", "text": {"content": content}}, ensure_ascii=False)
    if channel == "bark":
        return json.dumps({"title": title, "body": body}, ensure_ascii=False)
    if channel == "telegram":
        return json.dumps({"chat_id": chat_id, "text": content}, ensure_ascii=False)
    if channel == "discord":
        return json.dumps({"content": content}, ensure_ascii=False)
    if channel == "feishu":
        return json.dumps({"msg_type": "text", "content": {"text": content}}, ensure_ascii=False)
    return json.dumps({"title": title, "body": body}, ensure_ascii=False)




# ---------------------------------------------------------------- 子命令







def cmd_notify_send(args):
    cfg = load_config()
    url, ref = notify_webhook_url(cfg, args.channel)
    if args.channel == "telegram" and not getattr(args, "chat_id", ""):
        msg = "telegram 需要 --chat-id"
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "channel": "telegram", "error": msg}, ensure_ascii=False, indent=2))
        else:
            print("❌ %s" % msg)
        return 1
    payload = build_notify_payload(args.channel, args.title, args.body, getattr(args, "chat_id", "") or "")
    if not url:
        msg = "未配置 %s webhook：请先在本机运行 pan secret set notify.%s --stdin 保存地址" % (args.channel, args.channel)
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "channel": args.channel, "error": msg}, ensure_ascii=False, indent=2))
        else:
            print("❌ %s" % msg)
        return 1
    if getattr(args, "json", False):
        print(json.dumps({"ok": True, "channel": args.channel, "send": bool(args.send),
                          "masked": True, "payload": json.loads(payload)}, ensure_ascii=False, indent=2))
    else:
        print("通知：%s｜发送：%s｜标题：%s" % (args.channel, "是(--send)" if args.send else "否(dry-run；加 --send)", args.title))
    if not args.send:
        return 0
    tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    tmp.write(payload); tmp.close(); Path(tmp.name).chmod(0o600)
    cfg_curl = "url = %s\n-H = \"Content-Type: application/json\"\n--data = \"@%s\"\n" % (json.dumps(url), tmp.name)
    log_line("NOTIFY channel=%s send=1 ref=%s" % (args.channel, ref))
    try:
        proc = subprocess.run(["curl", "-sS", "--config", "-"], input=cfg_curl,
                              capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        Path(tmp.name).unlink(missing_ok=True)
        print("❌ 通知发送失败：%s" % exc)
        return 127
    Path(tmp.name).unlink(missing_ok=True)
    if proc.returncode != 0:
        print("❌ 通知发送失败 exit=%s %s" % (proc.returncode, (proc.stderr or proc.stdout or "").strip()[:300]))
        return proc.returncode
    print("✅ 通知已发送：%s" % args.channel)
    return 0




def _wait_schedule(at, cfg=None, dry_run=False):
    """定时/低峰骨架：按 HH:MM 计算到点等待秒数并阻塞等待；返回是否真的等待过。
    显式命令级 --at 优先；未指定则回退配置 http.schedule_at；dry_run/JSON 不等待。"""
    at = (at or "").strip()
    if not at and cfg:
        at = ((cfg.get("http") or {}).get("schedule_at") or "").strip()
    if not at or dry_run:
        return 0
    try:
        hh, mm = (at.split(":", 1) + [""])[:2]
        hh = hh.strip()
        mm = (mm or "").strip()
        if not (hh.isdigit() and mm.isdigit()):
            return 0
        target = datetime.now().replace(hour=int(hh), minute=int(mm), second=0, microsecond=0)
    except (ValueError, TypeError):
        return 0
    now = datetime.now()
    if target <= now:
        return 0
    seconds = int((target - now).total_seconds())
    print("⏳ 已排到 %02d:%02d 开始，当前 %s；%d 秒后自动下载（可直接关掉窗口？不行，需保持终端或后台运行）。" % (
        target.hour, target.minute, now.strftime("%H:%M"), seconds))
    try:
        time.sleep(seconds)
    except KeyboardInterrupt:
        return 0
    return seconds



def cmd_get(args):
    if getattr(args, "remote", None):
        from pancli.remote import cmd_remote_get as _cmd_remote_get
        return _cmd_remote_get(args)
    if getattr(args, "generic_direct", False) and is_http_url(args.url):
        return cmd_direct(args)
    cfg = load_config()
    plan = build_plan(args.url, pwd=args.pwd or "", to=args.to, cfg=cfg,
                      engine=args.engine, tier=args.tier, path=args.path,
                      classify=getattr(args, "classify", None))
    if not plan.get("ok"):
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "error": plan.get("error", "")}, ensure_ascii=False, indent=2))
        else:
            print("❌ %s" % plan.get("error"))
        return 1
    if getattr(args, "json", False):
        print(json.dumps(public_plan(plan), ensure_ascii=False, indent=2))
    else:
        print("网盘：%s｜引擎：%s｜账号：%s｜目录：%s" % (plan["drive_name"], plan["engine"], plan["tier"], plan["target"]))
        for step in plan["steps"]:
            print("  - %s" % step.get("note", ""))
        for warn in plan.get("warnings", []):
            print("  ⚠️ %s" % warn)
        if plan["missing"]:
            print("缺少依赖：")
            for item in plan["missing"]:
                print("  - %s" % item)
            print("安装/配置说明：%s" % plan["reference"])
    # 预演本身不执行外部命令，缺依赖也先把计划完整展示出来；实际下载才拦截。
    if plan["missing"] and not args.dry_run and not args.force:
        return 2
    if not args.dry_run and not getattr(args, "json", False):
        _wait_schedule(getattr(args, "at", ""), cfg, dry_run=False)
    if args.dry_run:
        if not getattr(args, "json", False):
            Path(plan["target"]).mkdir(parents=True, exist_ok=True)
            run_plan(plan, timeout=cfg.get("http", {}).get("timeout", 0), dry_run=True)
            print("DRY-RUN 完成：未执行实际下载（去掉 --dry-run 执行）")
        return 0
    http_cfg = cfg.get("http") or {}
    auto_web = (
        not getattr(args, "no_web", False)
        and not getattr(args, "json", False)
        and not getattr(args, "events", False)
        and sys.stdout.isatty()
        and bool(http_cfg.get("auto_web", True))
    )
    web_info = None
    if auto_web:
        try:
            from pancli.web import ensure_web_ui as _ensure_web_ui
            web_info = _ensure_web_ui(cfg, open_browser=True)
        except Exception as exc:
            web_info = {"ok": False, "error": str(exc)}
        if web_info.get("ok"):
            print("实时状态：%s/live（下载位置可在页面复制）" % web_info.get("url", ""))
        else:
            print("⚠️ Web UI 未启动，下载继续：%s" % (web_info.get("error") or "未知原因"))
    Path(plan["target"]).mkdir(parents=True, exist_ok=True)
    log_line("TASK drive=%s engine=%s tier=%s target=%s url=%s" % (plan["drive"], plan["engine"], plan["tier"], plan["target"], args.url))
    from pancli.report import TaskControl as _TaskControl
    tc = _TaskControl(cfg, plan, url=args.url, args={
        "url": args.url, "to": args.to or "", "engine": args.engine or "",
        "tier": args.tier or plan.get("tier", ""), "path": getattr(args, "path", "") or "",
        "pwd": args.pwd or "",
    })
    tc.register()
    wish_live = bool(getattr(args, "live", False)) or bool(http_cfg.get("live_status", False)) or bool(auto_web)
    live = None
    if wish_live:
        try:
            interval = float((cfg.get("http") or {}).get("live_interval", 1.0))
        except (TypeError, ValueError):
            interval = 1.0
        if plan.get("engine") == "http" and is_http_url(args.url):
            plan["total_bytes"] = probe_http_total_bytes(args.url, cfg)
        from pancli.report import LiveMonitor as _LiveMonitor
        live = _LiveMonitor(cfg, plan, url=args.url, interval=interval)
        live.start()
    rc = 1
    try:
        split = resolve_split_count(cfg, args)
        if split <= 1 and plan.get("engine") == "http" and is_http_url(args.url):
            # F1（v0.20.0）：用户没显式要分片时，测速自动决策——单连接被限且支持 Range 就切分片。
            try:
                from pancli.engine import auto_split_decision as _auto_split
                _n, _why = _auto_split(args.url, cfg)
                if _n > 1:
                    split = _n
                    log_line("AUTO_SPLIT n=%d why=%s" % (_n, _why))
                    if not getattr(args, "json", False):
                        print("自动分片：%d 段（%s）" % (_n, _why), flush=True)
            except Exception as _exc:
                log_line("AUTO_SPLIT skip error=%s" % _exc)
        if split and split > 1 and plan.get("engine") == "http" and is_http_url(args.url):
            target_file = Path(plan["target"]) / filename_from_url(args.url)
            started = datetime.now()
            from pancli.docker import run_curl_split as _run_curl_split
            _rc, _results, _note = _run_curl_split(args.url, target_file, split, cfg, emit_events=bool(getattr(args, "events", False)), live=live, task_control=tc)
            if _rc is not None:
                finished = datetime.now()
                from pancli.report import write_download_report as _wdr
                report_path = _wdr(cfg, plan, _results, started, finished, ok=(_rc == 0), url=args.url)
                if report_path:
                    print("报告：%s" % report_path)
                if _rc == 0:
                    print("✅ %s" % _note)
                    from pancli.report import run_completion_hook as _rch
                    hook_msg = _rch(cfg, plan, report_path, url=args.url)
                    if hook_msg:
                        print("完成钩子：%s" % hook_msg)
                else:
                    print("❌ %s" % _note)
                rc = _rc
                if live is not None:
                    live.stop(ok=(rc == 0))
                tc.finish(ok=(rc == 0), rc=rc)
                return rc
        started = datetime.now()
        emit_events = bool(getattr(args, "events", False))
        rc, results = run_plan_detailed(plan, timeout=cfg.get("http", {}).get("timeout", 0), dry_run=False, emit_events=emit_events, live=live, task_control=tc)
        finished = datetime.now()
        from pancli.report import write_download_report as _wdr, report_remediation as _rr
        report_path = _wdr(cfg, plan, results, started, finished, ok=(rc == 0), url=args.url)
        if report_path:
            print("报告：%s" % report_path)
        if rc != 0:
            _hint = _rr(results)
            if _hint:
                print("⚠️ 需要处理：%s" % _hint)
        if rc == 0:
            print("✅ 下载完成：%s" % plan["target"])
            from pancli.report import run_completion_hook as _rch
            hook_msg = _rch(cfg, plan, report_path, url=args.url)
            if hook_msg:
                print("完成钩子：%s" % hook_msg)
        return rc
    finally:
        if live is not None:
            live.stop(ok=(rc == 0))
        tc.finish(ok=(rc == 0), rc=rc)


def _task_reports_dir(args=None):
    cfg = load_config()
    if getattr(args, "reports_dir", None):
        return os.path.expanduser(args.reports_dir)
    from pancli.report import web_state_root as _web_state_root
    return str(_web_state_root(cfg))


def cmd_task(args):
    """pan task list|show|pause|resume|delete|retry <id> — 任务控制命令行入口。"""
    reports_dir = _task_reports_dir(args)
    sub = getattr(args, "task_cmd", "")

    def _json_or_text(obj, text_lines):
        if getattr(args, "json", False):
            print(json.dumps(obj, ensure_ascii=False, indent=2))
        else:
            print("\n".join(text_lines))

    if sub == "list":
        from pancli import web as _web; tasks = _web.serve_unified_tasks(reports_dir, limit=200, state=getattr(args, "state", None) or None)
        if getattr(args, "json", False):
            _json_or_text(tasks, [])
            return 0
        if not tasks:
            print("无任务（下载时执行 get 生成任务控制记录；历史报告也可在此看到）")
            return 0
        print("%-14s %-6s %-8s %-10s %-20s" % ("ID", "状态", "网盘", "引擎", "更新时间"))
        for t in tasks:
            print("%-14s %-6s %-8s %-10s %-20s" % (
                t["id"], t.get("state", ""), (t.get("drive_name") or t.get("drive") or ""),
                t.get("engine", ""), (t.get("updated") or "")))
        return 0

    if sub == "show":
        if not getattr(args, "id", None):
            print("❌ 缺少任务 ID")
            return 2
        path, rec = _locate_task_control(reports_dir, args.id)
        if not path or not rec:
            print("❌ 未找到任务：%s（可先 `pan task list` 查看）" % args.id)
            return 1
        rec.pop("_control_path", None)
        if getattr(args, "json", False):
            _json_or_text(rec, [])
        else:
            print(json.dumps(rec, ensure_ascii=False, indent=2))
        return 0

    if sub in ("pause", "resume", "delete", "retry"):
        if not getattr(args, "id", None):
            print("❌ 缺少任务 ID")
            return 2
        ok, msg = _apply_task_action(reports_dir, args.id, sub)
        print(("✅ " if ok else "❌ ") + msg)
        return 0 if ok else 1

    print("用法：pan task list|show|pause|resume|delete|retry <id>")
    return 2


def cmd_dirs(args):
    cfg = load_config()
    the_root = default_root(cfg)
    example = task_dir(cfg, "百度网盘", "https://pan.baidu.com/s/1abcd")
    if getattr(args, "json", False):
        print(json.dumps({"default_root": str(the_root), "example_task_dir": str(example)}, ensure_ascii=False, indent=2))
    else:
        print("默认根目录：%s" % the_root)
        print("示例任务目录：%s" % example)
    return 0


def cmd_direct(args):
    """通用 HTTP/HTTPS 直链下载模块（覆盖整个 skill 的直链入口，见 scripts/http_downloader/）。

    只接受 http/https 直链，不解析网盘分享链接、不绕过鉴权、不搜索盗版资源。
    下载前必须确认用户对该文件拥有授权（非交互必须 --confirm-own-use）。
    """
    if not GENERIC_DIRECT_OK:
        print("❌ http_downloader 模块缺失：请确认 scripts/http_downloader/ 位于 pan.py 同级目录。")
        return 2
    url = getattr(args, "url", "") or ""
    scheme = (url.split(":", 1)[0] or "").lower() if url else ""
    if scheme not in ("http", "https"):
        print("❌ 仅支持 http/https 直链，收到: %s://" % (scheme or "未知"))
        return 2
    confirmed = bool(getattr(args, "confirm_own_use", False))
    if not confirmed:
        if sys.stdin.isatty():
            from http_downloader.compliance import confirm
            try:
                confirm(interactive=True)
            except Exception as e:
                print("❌ %s" % e)
                return 2
        else:
            print("❌ 非交互模式必须添加 --confirm-own-use，表示你已确认对该文件拥有下载/使用授权。")
            print(COMPLIANCE_NOTICE or "")
            return 2
    try:
        rep = HTTPDownloader(
            url,
            getattr(args, "to", None) or ".",
            split=getattr(args, "split", 0) or 1,
            retries=getattr(args, "retries", 3) or 3,
            timeout=getattr(args, "timeout", 30) or 30,
            sha256=getattr(args, "sha256", "") or None,
            md5=getattr(args, "md5", "") or None,
        ).download(confirmed=True)
    except Exception as e:
        print("❌ %s" % e)
        return 1
    if getattr(args, "json", False):
        print(json.dumps({"ok": True, "file": str(rep.dest), "bytes": rep.bytes_downloaded,
                          "elapsed_sec": rep.elapsed_sec, "chunks": rep.chunks,
                          "verified": rep.verified, "sha256": rep.sha256},
                         ensure_ascii=False, indent=2))
    else:
        mb = rep.bytes_downloaded / 1048576.0
        print("✅ %s: %.1f MiB，%.1fs，分片=%d" % (rep.filename, mb, rep.elapsed_sec, rep.chunks))
        print("   位置: %s" % rep.dest)
    return 0




