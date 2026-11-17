#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pan-downloader — 远程 NAS / 私有存储（SSH、rclone、WebDAV、SMB、S3、mount）子模块。"""
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


import os
import re
import shlex
import subprocess
import tarfile
import tempfile
from datetime import datetime
from pathlib import Path

# 共享工具函数从 engine 懒加载（engine 的命令为懒代理，运行期才 import 本模块，避免循环引用）。
from pancli.engine import *  # noqa: F401,F403
from pancli.engine import _read_stdin_secret  # noqa: F401

REMOTE_KINDS = ("ssh", "rclone", "webdav", "smb", "s3", "mount")


def normalize_remote_kind(value):
    kind = str(value or "").strip().lower()
    aliases = {
        "sftp": "ssh",
        "synology": "ssh",
        "fnos": "ssh",
        "nas": "ssh",
        "ftp": "rclone",
        "nfs": "mount",
        "local-mount": "mount",
    }
    kind = aliases.get(kind, kind)
    return kind if kind in REMOTE_KINDS else ""


def remote_entry(cfg, name):
    name = str(name or "").strip()
    if not name:
        return None
    entry = (cfg.get("remotes") or {}).get(name)
    return entry if isinstance(entry, dict) else None


def validate_remote_profile(name, entry):
    """返回 (normalized_profile, missing)；只校验配置，不触碰网络。"""
    entry = dict(entry or {})
    kind = normalize_remote_kind(entry.get("kind"))
    entry["kind"] = kind
    entry["name"] = str(name or entry.get("name") or "").strip()
    missing = []
    if not entry["name"]:
        missing.append("remote 名称")
    if not kind:
        missing.append("kind（ssh/rclone/webdav/smb/s3/mount）")
    if kind == "ssh":
        for key, label in (("host", "host"), ("user", "user"), ("root", "root")):
            if not str(entry.get(key) or "").strip():
                missing.append(label)
    elif kind == "mount":
        if not str(entry.get("root") or "").strip():
            missing.append("root（本机挂载路径，Windows 示例 Z:\\下载）")
    elif kind in ("rclone", "webdav", "smb", "s3"):
        for key, label in (("remote_name", "remote_name（rclone 配置名）"), ("root", "root")):
            if not str(entry.get(key) or "").strip():
                missing.append(label)
    return entry, missing


def remote_ssh_argv(profile, command):
    host = str(profile["host"]).strip()
    user = str(profile["user"]).strip()
    destination = "%s@%s" % (user, host)
    argv = ["ssh", "-o", "BatchMode=yes"]
    port = str(profile.get("port") or "").strip()
    if port:
        argv += ["-p", port]
    argv += [destination, command]
    return argv


def remote_scp_argv(profile, source, destination):
    host = str(profile["host"]).strip()
    user = str(profile["user"]).strip()
    argv = ["scp", "-q", "-o", "BatchMode=yes"]
    port = str(profile.get("port") or "").strip()
    if port:
        argv += ["-P", port]
    argv += [str(source), "%s@%s:%s" % (user, host, destination)]
    return argv


def remote_display(profile):
    if profile.get("kind") == "ssh":
        return "ssh://%s@%s:%s%s" % (
            profile.get("user", ""), profile.get("host", ""), profile.get("port", "22"), profile.get("root", "")
        )
    if profile.get("kind") == "mount":
        return str(profile.get("root") or "")
    return "%s:%s" % (str(profile.get("remote_name") or "").rstrip(":"), profile.get("root", ""))


def remote_rclone_destination(profile, task_name):
    remote = str(profile.get("remote_name") or "").strip()
    if not remote:
        return ""
    remote = remote.rstrip(":") + ":"
    root = str(profile.get("root") or "").strip().replace("\\", "/").strip("/")
    path = "/".join([p for p in (root, sanitize(task_name)) if p])
    return remote + "/" + path if path else remote


def remote_task_name(drive_name, url):
    return "%s-%s" % (datetime.now().strftime("%Y%m%d"), url_slug(url))


def build_ssh_remote_plan(profile, url, pwd="", to=None, path=None, tier=None, engine=None, live=False):
    """远程执行模式：在 SSH 设备上调用已部署的 pan.py，文件直接落到远程磁盘。"""
    plan = {
        "ok": True,
        "drive": "remote-ssh",
        "drive_name": profile.get("name") or "远程设备",
        "engine": "ssh",
        "tier": tier or "",
        "target": remote_display(profile),
        "steps": [],
        "missing": [],
        "warnings": [],
        "reference": str(SKILL_DIR / "references/21-远程NAS与私有存储.md"),
        "remote_kind": "ssh-execute",
        "remote_name": profile.get("name", ""),
    }
    deploy_dir = str(profile.get("deploy_dir") or ".pan-downloader").strip().strip("/")
    python_bin = str(profile.get("python") or "python3").strip()
    remote_root = str(profile.get("root") or "").strip()
    task_name = remote_task_name(profile.get("name") or "remote", url)
    remote_target = str(to or ("%s/网盘下载/%s" % (remote_root.rstrip("/"), task_name)))
    script = "%s/scripts/pan.py" % deploy_dir
    cmd = "cd %s && %s %s get %s --to %s" % (
        shlex.quote(remote_root), shlex.quote(python_bin), shlex.quote(script),
        shlex.quote(url), shlex.quote(remote_target),
    )
    if live:
        cmd += " --live"
    if pwd:
        cmd += " --pwd " + shlex.quote(pwd)
    if path:
        cmd += " --path " + shlex.quote(path)
    if tier:
        cmd += " --tier " + shlex.quote(tier)
    if engine:
        cmd += " --engine " + shlex.quote(engine)
    cmd += " --force"
    plan["steps"].append({
        "engine": "ssh",
        "argv": remote_ssh_argv(profile, cmd),
        "cwd": str(SKILL_DIR),
        "note": "在远程设备执行 pan.py，下载直接落到 %s（需要预先把 SSH 密钥/agent 配置好）" % remote_target,
    })
    plan["target"] = remote_target
    return plan


def build_remote_sink_plan(profile, url, pwd="", to=None, path=None, tier=None, engine=None, cfg=None):
    """远程落地模式：本机取文件，再通过 rclone 写入 NAS/私有存储。"""
    cfg = cfg or load_config()
    profile = dict(profile)
    name = profile.get("name") or "remote"
    remote_task = remote_task_name(name, url)
    if profile.get("kind") == "mount":
        mount_root = Path(os.path.expanduser(str(profile.get("root") or "")))
        target = Path(to) if to else mount_root / "网盘下载" / remote_task
        local_plan = build_plan(url, pwd=pwd, to=str(target), cfg=cfg, engine=engine, tier=tier, path=path)
        local_plan["remote_kind"] = "mounted-target"
        local_plan["remote_name"] = name
        local_plan["reference"] = str(SKILL_DIR / "references/21-远程NAS与私有存储.md")
        return local_plan

    staging_root = str((cfg.get("remote") or {}).get("staging_root") or "").strip()
    staging = Path(os.path.expanduser(staging_root)) if staging_root else STATE_DIR / "remote-staging" / sanitize(name)
    staging_task = staging / remote_task
    local_plan = build_plan(url, pwd=pwd, to=str(staging_task), cfg=cfg, engine=engine, tier=tier, path=path)
    local_plan["remote_kind"] = "rclone-upload"
    local_plan["remote_name"] = name
    local_plan["staging"] = str(staging_task)
    local_plan["reference"] = str(SKILL_DIR / "references/21-远程NAS与私有存储.md")
    destination = remote_rclone_destination(profile, remote_task)
    if destination:
        local_plan["target"] = destination
    binary = find_engine_binary("rclone", cfg)
    if not binary:
        local_plan["missing"].append("rclone")
    if not destination:
        local_plan["missing"].append("remote_name")
    if binary and destination:
        try:
            conn = int((cfg.get("http") or {}).get(
                "max_connections_vip" if local_plan.get("tier") == "vip" else "max_connections_free", 1
            ))
        except (TypeError, ValueError):
            conn = 1
        conn = max(1, conn)
        argv = [
            binary, "copy", "--progress", "--transfers", str(conn),
            "--checkers", str(max(1, min(conn * 2, 8))),
            str(staging_task), destination,
        ]
        local_plan["steps"].append({
            "engine": "rclone",
            "argv": argv,
            "note": "把 %s 上传到远程存储 %s（tier=%s）" % (staging_task, destination, local_plan.get("tier", "free")),
        })
    return local_plan


def build_remote_plan(profile, url, pwd="", to=None, path=None, tier=None, engine=None, cfg=None):
    cfg = cfg or load_config()
    profile, missing = validate_remote_profile(profile.get("name", ""), profile)
    if missing:
        return {
            "ok": False,
            "error": "远程配置缺少：" + "、".join(missing),
            "missing": missing,
        }
    if profile["kind"] == "ssh":
        return build_ssh_remote_plan(profile, url, pwd=pwd, to=to, path=path, tier=tier, engine=engine, live=bool(profile.get("live", False)))
    return build_remote_sink_plan(profile, url, pwd=pwd, to=to, path=path, tier=tier, engine=engine, cfg=cfg)


def create_remote_deploy_archive():
    """打包技能文本与脚本，不含 config.json、凭据、缓存和用户数据。"""
    fd, tmp_name = tempfile.mkstemp(prefix="pan-downloader-deploy-", suffix=".tar.gz")
    os.close(fd)
    archive = Path(tmp_name)
    include = [SKILL_DIR / "SKILL.md", SKILL_DIR / "config.example.json", SKILL_DIR / "agents", SKILL_DIR / "references", SKILL_DIR / "scripts", SKILL_DIR / "docker"]
    with tarfile.open(archive, "w:gz") as tar:
        for source in include:
            if source.is_file():
                tar.add(source, arcname=source.name)
            elif source.is_dir():
                for item in sorted(source.rglob("*")):
                    if item.is_file() and "__pycache__" not in item.parts and item.name not in ("config.json",):
                        tar.add(item, arcname=str(item.relative_to(SKILL_DIR)))
    return archive


def remote_web_access(profile, port=0, web_host="", local_port=0):
    """构造远程 Web 控制页访问信息；不出网，只返回 URL 与隧道命令。"""
    port = int(port or 0) or int(profile.get("web_port") or 0) or 17890
    local_port = int(local_port or 0) or port
    web_host = (web_host or profile.get("web_host") or "127.0.0.1").strip() or "127.0.0.1"
    host = str(profile.get("host") or "NAS").strip()
    user = str(profile.get("user") or "").strip()
    if web_host in ("0.0.0.0", "::"):
        url = "http://%s:%d/" % (host, port)
    else:
        url = "http://127.0.0.1:%d/" % port
    tunnel = ""
    if user:
        ssh_port = (" -p %s" % profile.get("port")) if str(profile.get("port") or "").strip() else ""
        tunnel = "ssh%s -L %d:127.0.0.1:%d %s@%s" % (ssh_port, local_port, port, user, host)
    return {
        "web_port": port,
        "web_host": web_host,
        "url": url,
        "tunnel": tunnel,
        "local_url": ("http://127.0.0.1:%d/" % local_port) if tunnel else "",
        "guide": (
            "局域网直接打开：%s；外网/本机仅监听 127.0.0.1 时，另开终端执行：%s 后打开 http://127.0.0.1:%d/，保持隧道终端运行。" % (url, tunnel, local_port)
            if tunnel else ("远程 Web 已启动（127.0.0.1:%d）。如需局域网访问，重新部署时用 --web-host 0.0.0.0，或在本机保持 SSH 反向隧道。" % port)
        )
    }


def build_remote_deploy_plan(profile, archive_path, web_port=0, web_host=None, web_reports_dir=""):
    """把无凭据技能包部署到 SSH 设备；可选 --web-port 后台启动常驻 Web 控制页。"""
    profile, missing = validate_remote_profile(profile.get("name", ""), profile)
    if missing:
        return {"ok": False, "error": "远程配置缺少：" + "、".join(missing), "steps": []}
    if profile.get("kind") != "ssh":
        return {"ok": False, "error": "remote deploy 只支持 kind=ssh；WebDAV/SMB/S3 请直接用 rclone", "steps": []}
    deploy_dir = str(profile.get("deploy_dir") or ".pan-downloader").strip().strip("/")
    remote_dir = str(profile.get("root") or "").rstrip("/") + "/" + deploy_dir
    remote_root = str(profile.get("root") or "").rstrip("/") or ""
    remote_archive = "/tmp/pan-downloader-deploy-%s.tar.gz" % os.getpid()
    mkdir_cmd = "mkdir -p %s" % shlex.quote(remote_dir)
    extract_cmd = "tar -xzf %s -C %s && rm -f %s" % (
        shlex.quote(remote_archive), shlex.quote(remote_dir), shlex.quote(remote_archive)
    )
    steps = [
        {"engine": "ssh", "argv": remote_ssh_argv(profile, mkdir_cmd), "cwd": str(SKILL_DIR), "note": "创建远程技能目录 %s" % remote_dir},
        {"engine": "scp", "argv": remote_scp_argv(profile, archive_path, remote_archive), "cwd": str(SKILL_DIR), "note": "上传无凭据的部署包"},
        {"engine": "ssh", "argv": remote_ssh_argv(profile, extract_cmd), "cwd": str(SKILL_DIR), "note": "在远程设备解压技能脚本"},
    ]
    try:
        web_port = int(web_port or profile.get("web_port") or 0)
    except (TypeError, ValueError):
        web_port = 0
    web_host = (web_host or profile.get("web_host") or "127.0.0.1").strip() or "127.0.0.1"
    web_info = remote_web_access(profile, port=web_port or 0, web_host=web_host)
    if web_port > 0:
        reports_dir = str(web_reports_dir or remote_root or ".").strip() or "."
        python_bin = str(profile.get("python") or "python3").strip() or "python3"
        name_slug = re.sub(r"[^A-Za-z0-9_.@-]", "_", str(profile.get("name") or "remote"))
        start_cmd = (
            "cd %s && nohup %s scripts/pan.py serve --host %s --port %d --reports-dir %s "
            "</dev/null >/tmp/pan-remote-web-%s.log 2>&1 & echo started"
        ) % (
            shlex.quote(remote_dir), shlex.quote(python_bin), shlex.quote(web_host),
            web_port, shlex.quote(reports_dir), name_slug,
        )
        steps.append({
            "engine": "ssh",
            "argv": remote_ssh_argv(profile, start_cmd),
            "cwd": str(SKILL_DIR),
            "note": "在远程设备后台启动常驻 Web 控制页（scripts/pan.py serve），报告目录=%s，日志 /tmp/pan-remote-web-%s.log" % (reports_dir, name_slug),
        })
    return {
        "ok": True,
        "drive": "remote-deploy",
        "drive_name": profile.get("name", ""),
        "engine": "ssh",
        "tier": "free",
        "target": remote_dir,
        "steps": steps,
        "missing": [],
        "warnings": (["远程设备首次使用仍需在设备本机配置网盘凭据；本工具不会上传本机 config 或密码。"] +
                     (["远程 Web 页面已随部署启动：%s" % web_info["url"]] if web_port > 0 else [])),
        "reference": str(SKILL_DIR / "references/21-远程NAS与私有存储.md"),
        "web_port": web_port,
        "web_host": web_host,
        "web_url": web_info["url"] if web_port > 0 else "",
        "web_guide": web_info["guide"] if web_port > 0 else "",
    }



def _remote_public(entry):
    return {
        "name": entry.get("name", ""),
        "kind": entry.get("kind", ""),
        "host": entry.get("host", ""),
        "port": entry.get("port", ""),
        "user": entry.get("user", ""),
        "root": entry.get("root", ""),
        "remote_name": entry.get("remote_name", ""),
        "python": entry.get("python", ""),
        "deploy_dir": entry.get("deploy_dir", ""),
        "web_port": entry.get("web_port", ""),
        "web_host": entry.get("web_host", ""),
        "credential_ref": entry.get("credential_ref", ""),
        "description": entry.get("description", ""),
    }


def cmd_remote_add(args):
    cfg = load_config()
    remotes = cfg.setdefault("remotes", {})
    name = str(args.name or "").strip()
    if not re.fullmatch(r"[A-Za-z0-9._@-]{1,80}", name):
        print("❌ remote 名称只允许字母、数字、点、下划线、@ 和连字符")
        return 1
    entry = remotes.setdefault(name, {})
    if args.kind:
        entry["kind"] = normalize_remote_kind(args.kind) or args.kind
    for attr, key in (
        ("host", "host"), ("port", "port"), ("user", "user"), ("root", "root"),
        ("remote_name", "remote_name"), ("python", "python"), ("deploy_dir", "deploy_dir"),
        ("web_port", "web_port"), ("web_host", "web_host"),
        ("description", "description"),
    ):
        value = getattr(args, attr, None)
        if value is not None:
            entry[key] = value
    if args.credential_ref:
        try:
            entry["credential_ref"] = normalize_secret_ref(args.credential_ref)
        except ValueError as exc:
            print("❌ %s" % exc)
            return 1
    if args.credential_stdin:
        try:
            entry["credential_ref"] = credential_store("remote." + name, _read_stdin_secret())
        except (OSError, EOFError, ValueError, RuntimeError) as exc:
            print("❌ 凭据未保存：%s" % exc)
            return 1
    profile, missing = validate_remote_profile(name, entry)
    if missing:
        print("⚠️ 已保存，但配置不完整：%s" % "、".join(missing))
    path = save_config(cfg)
    print("已保存 remote.%s：%s" % (name, path))
    return 0


def cmd_remote_list(args):
    cfg = load_config()
    rows = []
    for name, entry in sorted((cfg.get("remotes") or {}).items()):
        profile, missing = validate_remote_profile(name, entry)
        row = _remote_public(profile)
        row["ready"] = not missing
        row["missing"] = missing
        rows.append(row)
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    elif not rows:
        print("尚未登记远程设备。示例：pan remote add nas --kind ssh --host 192.168.1.10 --user lis --root /volume1")
    else:
        for row in rows:
            print("%s %-18s %-8s %s" % ("✅" if row["ready"] else "⚠️", row["name"], row["kind"], row["host"] or row["remote_name"] or row["root"]))
    return 0


def cmd_remote_remove(args):
    cfg = load_config()
    remotes = cfg.setdefault("remotes", {})
    if args.name not in remotes:
        print("❌ 未找到 remote：%s" % args.name)
        return 1
    remotes.pop(args.name, None)
    path = save_config(cfg)
    print("✅ 已移除 remote.%s：%s" % (args.name, path))
    return 0


def _remote_checks(profile):
    checks = []
    kind = profile.get("kind")
    if kind == "ssh":
        checks.append(("ssh", find_engine_binary("ssh", {}) or "未安装（远程执行需要）"))
        checks.append(("scp", find_engine_binary("scp", {}) or "未安装（远程部署需要）"))
        checks.append(("认证方式", "SSH key/agent（BatchMode=yes，禁止把远程密码放进命令行）"))
    elif kind == "mount":
        root = Path(os.path.expanduser(str(profile.get("root") or "")))
        checks.append(("挂载路径", "%s（%s）" % (root, "可写" if root.exists() and os.access(str(root), os.W_OK) else "不可用或未挂载")))
    else:
        checks.append(("rclone", find_engine_binary("rclone", {}) or "未安装（远程落地需要）"))
        checks.append(("rclone remote", str(profile.get("remote_name") or "未配置")))
    return checks


def cmd_remote_check(args):
    cfg = load_config()
    entry = remote_entry(cfg, args.name)
    if entry is None:
        print("❌ 未找到 remote：%s" % args.name)
        return 1
    profile, missing = validate_remote_profile(args.name, entry)
    if missing:
        if args.json:
            print(json.dumps({"name": args.name, "ready": False, "missing": missing}, ensure_ascii=False, indent=2))
        else:
            print("❌ remote.%s 配置不完整：%s" % (args.name, "、".join(missing)))
        return 1
    checks = _remote_checks(profile)
    probe = ""
    if getattr(args, "probe", False):
        if profile["kind"] == "ssh":
            cmd = "python3 --version && mkdir -p %s" % shlex.quote(str(profile.get("root") or ""))
            try:
                proc = subprocess.run(remote_ssh_argv(profile, cmd), capture_output=True, text=True, timeout=20)
                probe = "成功：%s" % ((proc.stdout or proc.stderr or "").strip().splitlines()[-1] if (proc.stdout or proc.stderr) else "远程响应正常")
                if proc.returncode != 0:
                    probe = "失败：SSH/远程 Python 不可用（exit=%s）" % proc.returncode
            except (OSError, subprocess.TimeoutExpired) as exc:
                probe = "失败：%s" % exc
        elif profile["kind"] != "mount":
            destination = remote_rclone_destination(profile, "")
            try:
                proc = subprocess.run(["rclone", "lsd", destination], capture_output=True, text=True, timeout=20)
                probe = "成功：%s" % ((proc.stdout or proc.stderr or "").strip().splitlines()[-1] if (proc.stdout or proc.stderr) else "远端响应正常")
                if proc.returncode != 0:
                    probe = "失败：rclone 远端不可用（exit=%s）" % proc.returncode
            except (OSError, subprocess.TimeoutExpired) as exc:
                probe = "失败：%s" % exc
    result = {"name": args.name, "kind": profile.get("kind"), "ready": True, "checks": checks, "probe": probe}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("remote.%s（%s）" % (args.name, profile.get("kind")))
        for name, value in checks:
            print("  %-14s %s" % (name, value))
        if probe:
            print("  探测            %s" % probe)
    return 0 if not probe.startswith("失败") else 1


def cmd_remote_deploy(args):
    cfg = load_config()
    entry = remote_entry(cfg, args.name)
    if entry is None:
        print("❌ 未找到 remote：%s" % args.name)
        return 1
    profile, missing = validate_remote_profile(args.name, entry)
    if missing:
        print("❌ remote.%s 配置不完整：%s" % (args.name, "、".join(missing)))
        return 1
    profile["name"] = args.name
    archive = None
    try:
        archive = create_remote_deploy_archive()
        plan = build_remote_deploy_plan(
            profile, archive,
            web_port=getattr(args, "web_port", 0) or 0,
            web_host=getattr(args, "web_host", None),
            web_reports_dir=getattr(args, "web_reports_dir", None) or "",
        )
        if not plan.get("ok"):
            print("❌ %s" % plan.get("error"))
            return 1
        if args.dry_run:
            run_plan(plan, dry_run=True)
            print("DRY-RUN 完成：未上传部署包")
            return 0
        if args.json:
            print(json.dumps(public_plan(plan), ensure_ascii=False, indent=2))
            return 0
        rc = run_plan(plan, dry_run=False)
        if rc == 0:
            print("✅ 已部署到 remote.%s：%s" % (args.name, plan["target"]))
        return rc
    finally:
        if archive:
            try:
                archive.unlink()
            except OSError:
                pass


def cmd_remote_web(args):
    cfg = load_config()
    entry = remote_entry(cfg, args.name)
    if entry is None:
        print("❌ 未找到 remote：%s" % args.name)
        return 1
    profile, missing = validate_remote_profile(args.name, entry)
    if missing:
        print("❌ remote.%s 配置不完整：%s" % (args.name, "、".join(missing)))
        return 1
    profile["name"] = args.name
    info = remote_web_access(profile, port=getattr(args, "port", 0) or 0,
                             web_host=getattr(args, "host", None) or "",
                             local_port=getattr(args, "local_port", 0) or 0)
    if getattr(args, "json", False):
        print(json.dumps({"name": args.name,
                          "kind": profile.get("kind", ""),
                          "web_port": info["web_port"],
                          "web_host": info["web_host"],
                          "url": info["url"],
                          "tunnel": info["tunnel"],
                          "local_url": info["local_url"],
                          "guide": info["guide"]}, ensure_ascii=False, indent=2))
    else:
        print("remote.%s：%s://%s（root=%s）" % (args.name, profile.get("kind", "ssh"), profile.get("host", ""), profile.get("root", "")))
        print("  Web 控制页：%s" % info["url"])
        if info["tunnel"]:
            print("  外网/本机访问（反向隧道）：")
            print("    %s" % info["tunnel"])
            print("  本地打开：%s（保持隧道终端运行）" % info["local_url"])
        else:
            print("  提示：remote add 时登记 host/user 后可生成 SSH 反向隧道命令。")
    return 0

def _plan_dirs(plan):
    if plan.get("remote_kind") == "ssh-execute":
        return []
    path = plan.get("staging") or plan.get("target")
    if path:
        return [Path(str(path))]
    return []


def cmd_remote_get(args):
    cfg = load_config()
    name = getattr(args, "name", None) or getattr(args, "remote", None)
    entry = remote_entry(cfg, name)
    if entry is None:
        print("❌ 未找到 remote：%s" % name)
        return 1
    profile, missing = validate_remote_profile(name, entry)
    if missing:
        print("❌ remote.%s 配置不完整：%s" % (name, "、".join(missing)))
        return 1
    profile["name"] = name
    if getattr(args, "live", False):
        profile["live"] = True
    plan = build_remote_plan(profile, args.url, pwd=args.pwd or "", to=getattr(args, "to", None),
                             path=getattr(args, "path", None), tier=getattr(args, "tier", None),
                             engine=getattr(args, "engine", None), cfg=cfg)
    if not plan.get("ok"):
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "error": plan.get("error", ""), "missing": plan.get("missing", [])}, ensure_ascii=False, indent=2))
        else:
            print("❌ %s" % plan.get("error"))
        return 1
    if getattr(args, "json", False):
        print(json.dumps(public_plan(plan), ensure_ascii=False, indent=2))
    else:
        print("远程：%s｜模式：%s｜引擎：%s｜目标：%s" % (name, plan.get("remote_kind", ""), plan.get("engine", ""), plan.get("target", "")))
        for step in plan.get("steps", []):
            print("  - %s" % step.get("note", ""))
        for warn in plan.get("warnings", []):
            print("  ⚠️ %s" % warn)
        if plan.get("missing"):
            print("缺少依赖：")
            for item in plan["missing"]:
                print("  - %s" % item)
    if plan.get("missing") and not args.dry_run and not getattr(args, "force", False):
        return 2
    if args.dry_run:
        if not getattr(args, "json", False):
            run_plan(plan, dry_run=True)
            print("DRY-RUN 完成：未执行远程操作")
        return 0
    for directory in _plan_dirs(plan):
        directory.mkdir(parents=True, exist_ok=True)
    log_line("REMOTE name=%s kind=%s engine=%s target=%s url=%s" % (name, plan.get("remote_kind", ""), plan.get("engine", ""), plan.get("target", ""), args.url))
    rc = run_plan(plan, timeout=cfg.get("http", {}).get("timeout", 0), dry_run=False)
    if rc == 0:
        print("✅ 远程下载完成：%s" % plan.get("target", ""))
    return rc




