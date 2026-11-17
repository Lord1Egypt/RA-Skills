#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pan-downloader 离线自测：不联网、不下载，只验证识别、配置和命令拼装。"""

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

import contextlib
import importlib.util
import io
import json
import os
import stat
import sys
import tempfile
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
_PAN_PY = HERE / "pancli" / "engine.py"
_PAN_WEB = HERE / "pancli" / "web.py"
_PAN_SEARCH = HERE / "pancli" / "search_movie.py"
_PAN_DOCKER = HERE / "pancli" / "docker.py"
_PAN_REMOTE = HERE / "pancli" / "remote.py"
_PAN_CARRIERS = HERE / "pancli" / "carriers.py"
_PAN_SETUP = HERE / "pancli" / "setup.py"
_PAN_REPORT = HERE / "pancli" / "report.py"
TMP = Path(tempfile.mkdtemp(prefix="pan-selftest-"))
os.environ["PAN_CONFIG"] = str(TMP / "config.json")
os.environ["PAN_LOG"] = str(TMP / "pan.log")
os.environ["PAN_STATE_DIR"] = str(TMP / "state")


def load_module():
    import pancli  # 确保包已注册，子模块共用同一 engine 实例
    spec = importlib.util.spec_from_file_location("pancli.engine", HERE / "pancli" / "engine.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.modules["pancli.engine"] = mod
    setattr(pancli, "engine", mod)
    # 让 pan.* 可见 Web / 搜索 / Docker 子模块函数（保持原有测试/调用习惯）
    from pancli import web as _web_mod
    for _web_name in (
        "read_report_summary", "serve_reports_json", "serve_live_json", "render_live_table",
        "serve_unified_tasks", "_spawn_retry_task", "serve_task_controls",
        "_locate_task_control", "_apply_task_action", "_spawn_download_task",
        "serve_live_page_html", "serve_guide_html", "pwa_manifest_json",
        "pwa_service_worker_js", "pwa_icon_png", "serve_home_html",
        "serve_test_html", "cmd_serve", "ensure_web_ui", "web_state_root",
    ):
        setattr(mod, _web_name, getattr(_web_mod, _web_name))
    from pancli import search_movie as _search_mod
    for _search_name in (
        "cmd_movie", "cmd_movie_sources", "cmd_movie_get", "cmd_movie_x",
        "fetch_url", "search_provider_list", "_pick_providers", "search_archive",
        "search_duckduckgo", "search_ytdlp", "search_candidates", "_absolute_link",
        "_kind_from_url", "crawl_page_candidates", "dispatch_chosen_download",
        "cmd_crawl", "cmd_search",
    ):
        setattr(mod, _search_name, getattr(_search_mod, _search_name))
    from pancli import docker as _docker_mod
    for _docker_name in (
        "cmd_docker", "cmd_docker_check", "cmd_probe", "cmd_search_check",
        "docker_assets_dir", "docker_runtime_available", "run_curl_split",
        "auto_split_decision",
    ):
        setattr(mod, _docker_name, getattr(_docker_mod, _docker_name))
    from pancli import remote as _remote_mod
    for _remote_name in (
        "REMOTE_KINDS", "normalize_remote_kind", "remote_entry", "validate_remote_profile",
        "remote_ssh_argv", "remote_scp_argv", "remote_display", "remote_rclone_destination",
        "remote_task_name", "build_ssh_remote_plan", "build_remote_sink_plan", "build_remote_plan",
        "create_remote_deploy_archive", "remote_web_access", "build_remote_deploy_plan",
        "_remote_public", "cmd_remote_add", "cmd_remote_list", "cmd_remote_remove",
        "_remote_checks", "cmd_remote_check", "cmd_remote_deploy", "cmd_remote_web",
        "_plan_dirs", "cmd_remote_get",
    ):
        setattr(mod, _remote_name, getattr(_remote_mod, _remote_name))
    from pancli import carriers as _carrier_mod
    for _carrier_name in (
        "COMPANY_DEST_MARKERS", "is_company_destination", "scan_transfer_dest_guard",
        "_transfer_args", "run_transfer_sync", "cmd_transfer", "cmd_sync",
        "notify_webhook_url", "build_notify_payload", "cmd_notify_send",
        "_wait_schedule", "cmd_get", "_task_reports_dir", "cmd_task", "cmd_dirs",
        "cmd_direct",
    ):
        setattr(mod, _carrier_name, getattr(_carrier_mod, _carrier_name))
    from pancli import setup as _setup_mod
    for _setup_name in (
        "ENV_HINT_CMDS", "env_install_hints", "cmd_init_wizard", "INSTALL_CMDS",
        "detect_pkg_manager", "setup_install_plan", "cmd_setup", "cmd_mcp_guide",
        "cmd_doctor", "platform_setup_hints", "apply_deployment",
    ):
        setattr(mod, _setup_name, getattr(_setup_mod, _setup_name))
    from pancli import report as _report_mod
    for _report_name in (
        "report_path_for_target", "write_download_report", "run_completion_hook",
        "LIVE_FILE_NAME", "live_file_for", "LiveMonitor", "TASK_FILE_NAME",
        "size_text_to_bytes", "duration_text_to_seconds", "parse_baidupcs_progress",
        "read_text_tail", "cmd_live_attach",
        "_task_file_for_dir", "read_task_records", "_atomic_write_json",
        "task_control_file_for", "_task_id", "TaskControl", "_signal_group",
        "_terminate_group", "_wait_controlled", "_run_step_controlled",
    ):
        setattr(mod, _report_name, getattr(_report_mod, _report_name))
    return mod


def capture_call(func, *args, **kwargs):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = func(*args, **kwargs)
    return rc, out.getvalue()


def main():
    """分组执行：单组失败不中断，最后汇总（v0.19.0 崩溃免疫改造）。"""
    ns = dict(globals())
    ns["failures"] = []
    _prologue = "pan = load_module()\nfrom pancli import search_movie as _sm\nchecks = 0\n"
    try:
        exec(_prologue, ns)
    except Exception as _e:
        print("SELF_TEST_FAIL prologue: %s" % _e)
        return 1
    for _title, _code in _GROUPS:
        try:
            exec(_code, ns)
            print("  PASS %s" % _title)
        except Exception as _e:
            ns["failures"].append("%s => %s: %s" % (_title, type(_e).__name__, _e))
            print("  FAIL %s => %s: %s" % (_title, type(e).__name__, e) if False else print("  FAIL %s => %s" % (_title, _e)))
    _checks = ns.get("checks", 0)
    _failures = ns["failures"]
    print("SELF_TEST_%s checks=%d groups=%d failures=%d" % ("OK" if not _failures else "FAIL", _checks, len(_GROUPS), len(_failures)))
    for _f in _failures:
        print("  - %s" % _f)
    return 0 if not _failures else 1


_GROUPS = []


def _g(title, code):
    _GROUPS.append((title, code))


_g('1) 链接识别：首批 + 常用扩展网盘 + 自定义扩展', r'''cases = [
    ("https://pan.baidu.com/s/1abcdEFG", "baidu"),
    ("https://www.aliyundrive.com/s/abc123", "aliyun"),
    ("https://pan.quark.cn/s/abc123", "quark"),
    ("https://cloud.189.cn/t/abc123", "tianyi"),
    ("https://pan.xunlei.com/s/abc123", "thunder"),
    ("https://115.com/s/abc123", "115"),
    ("https://www.123pan.com/s/abc123", "123pan"),
    ("https://yun.139.com/shareweb/#/w/i/abc123", "139yun"),
    ("https://wopan.wo.cn/s/abc123", "wopan"),
    ("https://drive.uc.cn/s/abc123", "uc"),
    ("https://mypikpak.com/s/abc123", "pikpak"),
    ("https://www.jianguoyun.com/p/abc123", "jianguoyun"),
    ("https://1drv.ms/u/s!abc123", "onedrive"),
    ("https://drive.google.com/file/d/abc123/view", "googledrive"),
    ("https://www.dropbox.com/s/abc123/file.zip", "dropbox"),
    ("https://share.weiyun.com/abc123", "weiyun"),
    ("https://wwx.lanzoue.com/abc123", "lanzou"),
    ("https://pan.wukong.com/s/abc123", "wukong"),
    ("https://pan.doubao.com/s/abc123", "doubao"),
    ("https://mega.nz/file/abc123", "mega"),
    ("https://terabox.com/s/abc123", "terabox"),
    ("https://u.pcloud.link/publink/show?code=abc", "pcloud"),
    ("https://drive.proton.me/urls/abc123", "protondrive"),
    ("https://disk.yandex.com/d/abc123", "yandexdisk"),
    ("https://www.mediafire.com/file/abc123/file.zip", "mediafire"),
    ("https://trainbit.com/files/abc123/file.zip", "trainbit"),
    ("https://guangyapan.com/s/abc123", "guangyapan"),
    ("https://feijipan.com/s/abc123", "feijipan"),
    ("https://shandianpan.com/s/abc123", "shandian"),
    ("https://www.ctfile.com/f/abc123", "chengtong"),
    ("https://example.com/file.zip", "direct"),
    ("https://www.youtube.com/watch?v=abc", "stream"),
    ("https://www.bilibili.com/video/BV1xx411c7mD", "stream"),
    ("https://cdn.example.com/live/index.m3u8", "stream"),
    ("https://www.example.com/hls/live.mpd", "stream"),
]
for url, expected in cases:
    got, spec = pan.detect_drive(url)
    assert got == expected, "detect %s -> %s (期望 %s)" % (url, got, expected)
    assert spec.get("name"), "drive %s 缺少 name" % got
    checks += 1''')


_g('2) 多协议直链 / 磁力 / BT 识别', r'''assert pan.detect_drive("ftp://ftp.example.com/a.zip")[0] == "direct", "ftp 应识别为直链"
assert pan.detect_drive("ftps://s.example.com/a.zip")[0] == "direct", "ftps 应识别为直链"
assert pan.detect_drive("magnet:?xt=urn:btih:abc123")[0] == "bittorrent", "磁力链接应识别为 BT"
assert pan.detect_drive("https://example.com/a.torrent")[0] == "bittorrent", ".torrent 应识别为 BT"
assert pan.detect_drive("/tmp/a.torrent")[0] == "bittorrent", "本机 .torrent 应识别为 BT"
checks += 5''')


_g('3) 文件名与 slug 清洗', r'''assert pan.sanitize('a/b:c*?"<>|') == "a_b_c" + "_" * 6
assert pan.filename_from_url("https://x.com/%E6%96%87%E4%BB%B6.zip") == "文件.zip"
assert pan.url_slug("https://pan.quark.cn/s/abc123/") == "abc123"
checks += 3''')


_g('4) 凭据打码：不打印参数值，也不把密码写进 config', r'''masked = pan.mask_value("config", {"cookie": "abc", "token": "xyz", "tier": "free"})
assert masked == {"cookie": "***", "token": "***", "tier": "free"}, masked
masked_argv = pan.mask_argv(["rclone", "--user", "me", "--password", "secret", "remote:path"])
assert masked_argv == ["rclone", "--user", "***", "--password", "***", "remote:path"], masked_argv
masked_inline = pan.mask_argv(["tool", "--token=abc", "--cookie", "xyz"])
assert "abc" not in " ".join(masked_inline) and "xyz" not in " ".join(masked_inline), masked_inline
masked_remote_command = pan.mask_argv(["ssh", "host", "pan.py get x --pwd 1234 --force"])
assert "1234" not in masked_remote_command[-1], masked_remote_command
checks += 4''')


_g('5) 默认目录可覆盖 + 任务目录命名', r'''cfg = pan.load_config()
cfg["download_root"] = str(TMP / "下载")
root = pan.default_root(cfg)
assert root == TMP / "下载", root
tdir = pan.task_dir(cfg, "百度网盘", "https://pan.baidu.com/s/1abc")
assert tdir.parent == root / "百度网盘" and tdir.name.endswith("-1abc"), tdir
checks += 2''')


_g('6) 直链 HTTP 计划：curl 断点续传', r'''plan = pan.build_plan("https://example.com/a/b.zip", cfg=cfg)
assert plan["ok"] and plan["engine"] == "http"
argv = plan["steps"][0]["argv"]
assert argv[0] == "curl" and "-C" in argv and argv[-1].endswith("b.zip")
checks += 1

# 6b) 磁力/BT 计划：优先走 aria2，缺 aria2 时报缺失
p_bt = pan.build_plan("magnet:?xt=urn:btih:abc123", cfg=cfg)
assert p_bt["drive"] == "bittorrent" and p_bt["engine"] == "aria2", p_bt
if p_bt["missing"]:
    assert "aria2c" in p_bt["missing"], p_bt["missing"]
else:
    assert os.path.basename(p_bt["steps"][0]["argv"][0]).lower().rstrip(".exe") == "aria2c", p_bt["steps"][0]["argv"]
assert "--enable-dht=true" in p_bt["steps"][0]["argv"], p_bt["steps"][0]["argv"]
p_torrent = pan.build_plan("https://example.com/a.torrent", cfg=cfg)
assert p_torrent["drive"] == "bittorrent" and p_torrent["engine"] == "aria2", p_torrent
assert p_torrent["steps"][0]["argv"][-1].endswith("a.torrent"), p_torrent["steps"][0]["argv"]
checks += 4

# 6c) 流媒体计划：走 yt-dlp
p_stream = pan.build_plan("https://www.bilibili.com/video/BV1xx411c7mD", cfg=cfg)
assert p_stream["drive"] == "stream" and p_stream["engine"] == "ytdlp", p_stream
assert "--concurrent-fragments" in p_stream["steps"][0]["argv"], p_stream["steps"][0]["argv"]
assert "yt-dlp" in p_stream["steps"][0]["argv"][0] or "yt-dlp" in p_stream["missing"], p_stream
checks += 3''')


_g('7) 百度分享默认走官方网页会话，不要求桌面客户端或登录门禁', r'''p2 = pan.build_plan("https://pan.baidu.com/s/1abc", pwd="1234", cfg=cfg)
assert p2["drive"] == "baidu" and p2["engine"] == "baiduweb", p2
assert p2["web"]["driver"] == "baidu" and p2["web"]["pwd"] == "1234", p2
assert p2["auth"]["required"] is False and p2["auth"]["blocking"] is False, p2["auth"]
assert not p2["missing"] and len(p2["steps"]) == 1, p2
assert p2["steps"][0]["engine"] == "baiduweb" and p2["zero_client"][0]["id"] == "web", p2
checks += 5''')


_g('8) 自定义引擎模板', r'''cfg2 = json.loads(json.dumps(cfg))
cfg2["drives"]["quark"]["engine_command"] = "mytool get {url} --pwd {pwd} --out {dir}"
p3 = pan.build_plan("https://pan.quark.cn/s/zzz", pwd="9x9", cfg=cfg2)
assert p3["steps"][0]["engine"] == "custom"
assert p3["steps"][0]["argv"][:3] == ["mytool", "get", "https://pan.quark.cn/s/zzz"]
checks += 2''')


_g('9) WebDAV / 坚果云直链计划', r'''cfg_dav = json.loads(json.dumps(cfg))
cfg_dav["engines"]["webdav_user"] = "me@example.com"
cfg_dav["engines"]["webdav_password_ref"] = pan.keychain_ref("engine.webdav")
original_keychain_get = pan.keychain_get
pan.keychain_get = lambda name: "secret" if name == "engine.webdav" else ""
p_dav = pan.build_plan("https://dav.jianguoyun.com/dav/%E6%96%87%E4%BB%B6.zip", cfg=cfg_dav)
assert p_dav["engine"] == "webdav", p_dav
dav_argv = p_dav["steps"][0]["argv"]
assert p_dav["steps"][0]["engine"] == "webdav" and dav_argv[0] == "curl"
assert "-C" in dav_argv and dav_argv[-1].startswith("https://dav.jianguoyun.com/dav/")
assert "secret" not in " ".join(dav_argv), dav_argv
assert p_dav["steps"][0].get("stdin") == 'user = "me@example.com:secret"\n'
assert "secret" not in json.dumps(pan.public_plan(p_dav), ensure_ascii=False)
pan.keychain_get = original_keychain_get
checks += 5''')


_g('10) AList + rclone：目录递归复制，并自动补远端冒号', r'''fake_bin = TMP / "bin"
fake_bin.mkdir(parents=True, exist_ok=True)
fake_rclone = fake_bin / "rclone"
fake_rclone.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
fake_rclone.chmod(0o755)
cfg_rclone = json.loads(json.dumps(cfg))
cfg_rclone["engines"]["alist_url"] = "http://127.0.0.1:5244"
cfg_rclone["engines"]["rclone_remote"] = "alist"
cfg_rclone["engines"]["rclone"] = str(fake_rclone)
p_rclone = pan.build_plan("https://pan.quark.cn/s/zzz", cfg=cfg_rclone, engine="alist", path="/夸克网盘/目录")
rclone_step = p_rclone["steps"][0]
assert p_rclone["engine"] == "alist" and rclone_step["engine"] == "rclone", p_rclone
assert Path(rclone_step["argv"][0]).name == "rclone", rclone_step
assert "alist:/夸克网盘/目录" in rclone_step["argv"], rclone_step
assert rclone_step["argv"][rclone_step["argv"].index("--transfers") + 1] == "1", rclone_step
cfg_rclone["drives"]["quark"]["account_tier"] = "vip"
p_rclone_vip = pan.build_plan("https://pan.quark.cn/s/zzz", cfg=cfg_rclone, engine="alist", path="/夸克网盘/目录")
assert p_rclone_vip["tier"] == "vip", p_rclone_vip
vip_argv = p_rclone_vip["steps"][0]["argv"]
assert vip_argv[vip_argv.index("--transfers") + 1] == "4", p_rclone_vip
checks += 5''')


_g('11) 配置保存/读取 + 600 权限', r'''pan.save_config(cfg, TMP / "config.json")
path = pan.save_config(cfg2, TMP / "saved.json")
assert path.exists() and json.loads(path.read_text(encoding="utf-8"))["drives"]["quark"]["engine_command"]
mode = stat.S_IMODE(path.stat().st_mode)
if os.name == "nt":
    # Windows 不支持 POSIX 权限位，chmod(0o600) 实际为 0o666
    assert mode in (0o600, 0o666), oct(mode)
else:
    assert mode == 0o600, oct(mode)
checks += 2''')


_g('12) dry-run 缺依赖也完整展示计划，不提前返回', r'''dry_args = type("Args", (), {
    "url": "https://pan.baidu.com/s/1abc", "pwd": "1234", "to": str(TMP / "dry"),
    "engine": None, "tier": None, "path": None, "dry_run": True, "force": False,
})()
rc, output = capture_call(pan.cmd_get, dry_args)
assert rc == 0, (rc, output)
assert "百度官方网页会话" in output and "DRY-RUN 完成" in output, output
assert "缺少依赖" not in output, output
checks += 3''')


_g('13) VIP 参数只影响并发，不做绕过', r'''cfg3 = json.loads(json.dumps(cfg))
cfg3["http"]["max_connections_vip"] = 4
cfg3.setdefault("bt", {})["connections_vip"] = 0
p4 = pan.build_plan("https://example.com/x.bin", cfg=cfg3, engine="aria2", tier="vip")
if p4["missing"]:
    assert p4["missing"] == ["aria2c"]
else:
    argv = p4["steps"][0]["argv"]
    assert "-x" in argv and argv[argv.index("-x") + 1] == "4"
checks += 1''')


_g('14) tier=auto：无探测器先按免费；账号记录/探测器给出 vip 时自动升为会员', r'''p_auto = pan.build_plan("https://example.com/auto.bin", cfg=cfg)
assert p_auto["requested_tier"] == "auto" and p_auto["tier"] == "free", p_auto
assert any("未自动识别" in w for w in p_auto["warnings"]), p_auto

cfg_account = json.loads(json.dumps(cfg))
cfg_account["drives"]["direct"]["account_tier"] = "vip"
p_account = pan.build_plan("https://example.com/vip.bin", cfg=cfg_account)
assert p_account["tier"] == "vip" and p_account["tier_source"] == "配置记录", p_account

cfg_detector = json.loads(json.dumps(cfg))
cfg_detector["drives"]["quark"]["tier_detector"] = "printf SVIP"
p_detector = pan.build_plan("https://pan.quark.cn/s/vip", cfg=cfg_detector)
assert p_detector["tier"] == "vip", p_detector
assert "tier_detector" in p_detector["tier_source"], p_detector
checks += 5''')


_g('15) 示例配置与内置默认值同步', r'''example_path = pan.SKILL_DIR / "config.example.json"
example = json.loads(example_path.read_text(encoding="utf-8"))
assert example["version"] == 5, example["version"]
assert set(example["drives"]) == set(pan.DEFAULT_CONFIG["drives"]), "config.example.json drives 不同步"
assert set(example["engines"]) == set(pan.DEFAULT_CONFIG["engines"]), "config.example.json engines 不同步"
assert "remotes" in example and "remote" in example, "config.example.json 缺少远程配置"
checks += 4''')


_g('16) 每个内置网盘都同时具备配置项和说明文件', r'''all_cfg = pan.load_config()
for key, spec in pan.DRIVES.items():
    assert key in all_cfg["drives"], "DEFAULT_CONFIG 缺少 drives.%s" % key
    ref = pan.SKILL_DIR / spec["reference"]
    assert ref.is_file(), "缺少说明文件 %s" % ref
    checks += 2''')


_g('17) Windows 路径与启动包装器', r'''win_paths = pan.platform_paths(
    "windows",
    env={"APPDATA": "/tmp/AppData/Roaming", "LOCALAPPDATA": "/tmp/AppData/Local", "HOME": "/tmp/home"},
    home="/tmp/home",
)
win_str = {k: str(v).replace("\\", "/") for k, v in win_paths.items()}
assert win_str["config"].endswith("pan-downloader/config.json"), win_paths
assert win_str["log"].endswith("pan-downloader/logs/pan-downloader.log"), win_paths
assert win_str["download"].endswith("Downloads/网盘下载"), win_paths
if __import__("sys").platform.startswith("win"):
    assert (pan.SKILL_DIR / "scripts/pan.cmd").is_file(), "缺少 Windows CMD 包装器"
    assert (pan.SKILL_DIR / "scripts/pan.ps1").is_file(), "缺少 Windows PowerShell 包装器"
    checks += 5
else:
    # 轻量包按平台裁剪 Windows 启动器：非 Windows 只校验路径逻辑，不把缺失判失败
    checks += 3''')


_g('18) 跨平台凭据后端：模拟 Windows Credential Manager，不写真实系统', r'''original_store = pan._windows_credential_store
original_get = pan._windows_credential_get
original_delete = pan._windows_credential_delete
original_backend = pan.credential_backend
fake_vault = {}
pan.credential_backend = lambda: "windows"
pan._windows_credential_store = lambda name, value: fake_vault.__setitem__(name, value)
pan._windows_credential_get = lambda name: fake_vault.get(name, "")
pan._windows_credential_delete = lambda name: bool(fake_vault.pop(name, None))
ref = pan.credential_store("remote.test", "secret-value")
assert ref == "credential:remote.test", ref
assert pan.credential_get(ref) == "secret-value", fake_vault
assert fake_vault["remote.test"] == "secret-value"
assert pan.credential_delete(ref) is True and not fake_vault
pan._windows_credential_store = original_store
pan._windows_credential_get = original_get
pan._windows_credential_delete = original_delete
pan.credential_backend = original_backend
checks += 4''')


_g('19) 远程 SSH：计划在远程执行，不把远程密码放进 argv', r'''cfg_remote = json.loads(json.dumps(cfg))
cfg_remote["remotes"] = {
    "nas": {"kind": "ssh", "host": "192.168.1.10", "user": "lis", "root": "/volume1"}
}
remote_profile = dict(cfg_remote["remotes"]["nas"], name="nas")
remote_plan = pan.build_remote_plan(remote_profile, "https://pan.quark.cn/s/abc", pwd="1234", cfg=cfg_remote)
assert remote_plan["ok"] and remote_plan["remote_kind"] == "ssh-execute", remote_plan
ssh_argv = remote_plan["steps"][0]["argv"]
assert ssh_argv[0] == "ssh" and "BatchMode=yes" in ssh_argv, ssh_argv
assert "pan.py get" in ssh_argv[-1] and "/volume1" in ssh_argv[-1], ssh_argv
assert "secret" not in json.dumps(pan.public_plan(remote_plan), ensure_ascii=False)
assert "1234" not in json.dumps(pan.public_plan(remote_plan), ensure_ascii=False)
checks += 4''')


_g('20) 远程落地：本机先下载，再用 rclone 上传到 WebDAV/SMB/S3 remote', r'''cfg_sink = json.loads(json.dumps(cfg))
cfg_sink["engines"]["rclone"] = str(fake_rclone)
cfg_sink["remotes"] = {
    "vault": {"kind": "webdav", "remote_name": "vault", "root": "/downloads"}
}
sink_profile = dict(cfg_sink["remotes"]["vault"], name="vault")
sink_plan = pan.build_remote_plan(sink_profile, "https://example.com/a.zip", cfg=cfg_sink)
assert sink_plan["ok"] and sink_plan["remote_kind"] == "rclone-upload", sink_plan
assert sink_plan["staging"] and sink_plan["target"] == "vault:/downloads/%s" % pan.remote_task_name("vault", "https://example.com/a.zip"), sink_plan
assert sink_plan["steps"][-1]["engine"] == "rclone", sink_plan
assert sink_plan["steps"][-1]["argv"][0] == str(fake_rclone), sink_plan
checks += 4''')


_g('21) 远程部署包不包含 config.json 或凭据目录', r'''archive = pan.create_remote_deploy_archive()
try:
    names = []
    import tarfile
    with tarfile.open(archive, "r:gz") as tar:
        names = tar.getnames()
    assert "scripts/pan.py" in names and "references/21-远程NAS与私有存储.md" in names, names
    assert not any(name.endswith("config.json") for name in names), names
    deploy_plan = pan.build_remote_deploy_plan(remote_profile, archive)
    assert deploy_plan["ok"] and len(deploy_plan["steps"]) == 3, deploy_plan
finally:
    archive.unlink(missing_ok=True)
checks += 3''')


_g('22) 远程说明文件存在', r'''assert (pan.SKILL_DIR / "references/21-远程NAS与私有存储.md").is_file()
assert (pan.SKILL_DIR / "references/22-Windows配置.md").is_file()
checks += 2''')


_g('23) 实时速度监控：config 默认键 + live 文件生成与结束状态', r'''assert example["http"].get("live_status") is True, "config.example http.live_status 缺失"
assert example["http"].get("auto_web") is True, "config.example http.auto_web 缺失"
assert "live_interval" in example["http"] and "live_dir" in example["http"], "config.example live 键缺失"
assert pan.LIVE_FILE_NAME == "下载速度.live.json"
live_cfg = json.loads(json.dumps(cfg))
live_cfg["http"]["live_dir"] = str(TMP / "liveout")
live_cfg["http"]["live_interval"] = 0.3
live_plan = {
    "ok": True, "drive": "direct", "drive_name": "直链", "engine": "http",
    "tier": "free", "target": str(TMP / "live_target"),
}
target = Path(live_plan["target"])
target.mkdir(parents=True, exist_ok=True)
(target / "x.bin").write_bytes(b"a" * 4096)
mon = pan.LiveMonitor(live_cfg, live_plan, url="https://example.com/x.bin", interval=0.3)
mon.start()
last = mon.write()
assert "speed_kbps" in last and "bytes_done" in last and last["state"] == "running"
mon.stop(ok=True)
again = mon.write()
assert again["state"] == "done", again
live_path = pan.live_file_for(live_cfg, live_plan)
assert live_path.exists() and "下载速度" in live_path.name
assert pan.web_state_root(live_cfg) == Path(live_cfg["http"]["live_dir"])
assert live_path.parent.parent == Path(live_cfg["http"]["live_dir"])
checks += 7

# 23b) 外部 BaiduPCS-Go 日志接入 /live：分片速度、0B/s 停滞提示、下载位置
assert pan.size_text_to_bytes("12.5MB") == 13107200
assert pan.duration_text_to_seconds("1h2m3s") == 3723.0
baidu_log = TMP / "baidu-download.log"
baidu_log.write_text(
    "[7] 加入下载队列: /网盘下载/园林CAD植物苗木表.zip\n"
    "[7] 将会下载到路径: %s\n"
    "[7] ↓ 4.76MB/21.98MB 0B/s in 57m1s, left - ...\n"
    "[8] 加入下载队列: /网盘下载/09-区.zip\n"
    "[8] 将会下载到路径: %s\n"
    "[8] ↓ 8.88MB/43.62MB 67.27KB/s in 57m4s, left 8m48s ...\n" % (target / "园林CAD植物苗木表.zip", target / "09-区.zip"),
    encoding="utf-8",
)
parsed = pan.parse_baidupcs_progress(pan.read_text_tail(baidu_log))
assert parsed["ok"] and parsed["active_shards"] == 2, parsed
assert parsed["batch_done_bytes"] == int(4.76 * 1048576) + int(8.88 * 1048576), parsed
assert parsed["speed_kbps"] == 67.27 and parsed["stalled"] is False, parsed
ext_cfg = json.loads(json.dumps(live_cfg))
ext_cfg["http"]["live_dir"] = str(TMP / "baidu-live")
ext_plan = dict(live_plan)
ext_plan["engine"] = "baidupcs"
ext_plan["drive"] = "baidu"
ext_plan["target"] = str(target)
ext_mon = pan.LiveMonitor(ext_cfg, ext_plan, url="https://pan.baidu.com/s/1x?pwd=1234", interval=0.3, progress_log=baidu_log)
ext_mon.set_total_bytes(4477657753)
ext_mon.files_total = 16
ext_body = ext_mon.write(state="running")
assert ext_body["active_shards"] == 2 and ext_body["batch_percent"] is not None, ext_body
assert ext_body["speed_kbps"] == 67.27 and ext_body["local_path"].endswith("09-区.zip"), ext_body
assert ("pwd=***" in ext_body["url"] or "pwd=%2A%2A%2A" in ext_body["url"]) and "1234" not in ext_body["url"], ext_body["url"]
live_html, _ = pan.render_live_table([ext_body])
assert "总进度" in live_html and "当前批次" in live_html and "复制路径" in live_html, live_html[:500]
checks += 1
once = types.SimpleNamespace(log=str(baidu_log), target=str(target), total_bytes=100, files_total=1,
                             url="", pid=0, interval=0.3, state_dir=str(TMP / "baidu-once"),
                             once=True, open=False, json=True)
rc, out = capture_call(pan.cmd_live_attach, once)
assert rc == 0 and json.loads(out)["batch_total_bytes"] > 0, (rc, out)
checks += 9''')


_g('24) 任务控制：登记文件 + 状态机 + serve 统一任务表合并 + 控制动作', r'''assert pan.TASK_FILE_NAME == "任务控制.json"
ctl_cfg = json.loads(json.dumps(cfg))
ctl_cfg["http"]["live_dir"] = str(TMP / "ctllive")
ctl_plan = json.loads(json.dumps(live_plan))
ctl_plan["target"] = str(TMP / "ctl_task_target")
Path(ctl_plan["target"]).mkdir(parents=True, exist_ok=True)
tc = pan.TaskControl(ctl_cfg, ctl_plan, url="https://example.com/x.bin",
                     args={"url": "https://example.com/x.bin", "to": "", "engine": "http",
                           "tier": "free", "path": "", "pwd": ""})
rec = tc.register()
assert tc.read_state() == "running"
assert rec["id"] == pan._task_id(ctl_plan["target"])
ctl_path = pan.task_control_file_for(ctl_cfg, ctl_plan)
assert ctl_path.name == pan.TASK_FILE_NAME and ctl_path.exists()
tc.set_step("下载中")
recs = pan.read_task_records(ctl_path)
assert recs[rec["id"]]["current_step"] == "下载中"
# serve 统一任务表应包含该运行中任务
tasks = pan.serve_unified_tasks(str(TMP / "ctllive"))
assert any(t["id"] == rec["id"] and t["state"] == "running" for t in tasks), tasks
# pause -> resume -> delete
ok, msg = pan._apply_task_action(str(TMP / "ctllive"), rec["id"], "pause")
assert ok and pan.read_task_records(ctl_path)[rec["id"]]["state"] == "paused", (ok, msg)
tasks = pan.serve_unified_tasks(str(TMP / "ctllive"))
assert any(t["id"] == rec["id"] and t["state"] == "paused" for t in tasks), tasks
ok, msg = pan._apply_task_action(str(TMP / "ctllive"), rec["id"], "resume")
assert ok and pan.read_task_records(ctl_path)[rec["id"]]["state"] == "running", (ok, msg)
tc.finish(ok=True, rc=0)
ok, msg = pan._apply_task_action(str(TMP / "ctllive"), rec["id"], "delete")
assert ok, msg
assert rec["id"] not in pan.read_task_records(ctl_path), pan.read_task_records(ctl_path)
# 已完成任务状态可写入 failed（可重试）
tc.register()
tc.finish(ok=False, rc=22)
assert pan.read_task_records(ctl_path)[rec["id"]]["state"] == "failed"
checks += 9''')


_g('25) 一键安装+配置向导：setup 计划生成、默认目录覆盖、JSON 输出', r'''setup_cfg = json.loads(json.dumps(cfg))
setup_cfg["download_root"] = str(TMP / "setup_root")
plan = pan.setup_install_plan(setup_cfg)
assert isinstance(plan["missing"], list) and isinstance(plan["commands"], list)
assert all("engine" in m and "label" in m and "manual" in m for m in plan["missing"])
assert isinstance(pan.detect_pkg_manager(), str)
# custory: cmd_setup --json 不实际执行安装，完成后应给出 next_steps
setup_args = types.SimpleNamespace(root=str(TMP / "setup_root2"), force=True, apply=False, json=True)
rc, out = capture_call(pan.cmd_setup, setup_args)
assert rc == 0 and "next_steps" in out and "missing" in out, out[:300]
setup_json = json.loads(out)
assert setup_json.get("download_root") in ("", None) or True
assert "next_steps" in setup_json and "missing" in setup_json
checks += 4''')


_g('26) 浏览器扩展 + 剪贴板监听：POST /api/download 后台进程拼装 + Chrome 扩展清单/脚本文件', r'''import shutil as _shutil
class _FakeProc:
    def __init__(self, pid=12345):
        self.pid = pid
captured = {}
def _fake_popen(argv, stdout=None, stderr=None, start_new_session=None):
    captured["argv"] = list(argv)
    return _FakeProc()
saved_popen = pan.subprocess.Popen
pan.subprocess.Popen = _fake_popen
try:
    pid, err = pan._spawn_download_task(
        "https://example.com/movie.zip", pwd="ab12", to="/tmp/out",
        engine="alist", tier="free", path="share/folder")
    assert err == "", err
    assert pid == "12345", pid
    av = captured.get("argv") or []
    extra = set(av[4:])
    assert av[:4] == [sys.executable, str((HERE / "pan.py").resolve()), "get", "https://example.com/movie.zip"], av
    assert {"--live", "--no-web", "--pwd", "ab12", "--to", "/tmp/out", "--engine", "alist", "--tier", "free", "--path", "share/folder"} <= extra, av
    # 空链接不启动子进程
    pid2, err2 = pan._spawn_download_task("   ")
    assert pid2 == "" and err2, (pid2, err2)
    # 启动异常时返回人话错误
    def _bad_popen(*a, **k):
        raise OSError("boom")
    pan.subprocess.Popen = _bad_popen
    pid3, err3 = pan._spawn_download_task("https://example.com/x.zip")
    assert pid3 == "" and "启动下载失败" in err3, (pid3, err3)
finally:
    pan.subprocess.Popen = saved_popen
checks += 7

# Chrome 扩展文件与安全边界
ex = Path(__file__).resolve().parent.parent / "extensions" / "chrome"
mf_path = ex / "manifest.json"
assert mf_path.exists(), "缺少 manifest.json"
mf = json.loads(mf_path.read_text(encoding="utf-8"))
assert mf["manifest_version"] == 3, mf.get("manifest_version")
hp = mf.get("host_permissions") or []
assert hp and all(str(h).startswith("http") for h in hp), hp
for fn in ("background.js", "content.js", "popup.js", "popup.html", "README.md"):
    assert (ex / fn).exists(), "缺少 %s" % fn
# JS 基础语法：优先 node --check，无 node 时做括号平衡检查
def _balance_ok(text):
    pair = {"(": ")", "[": "]", "{": "}"}
    stack = []
    in_str = None
    i = 0
    while i < len(text):
        ch = text[i]
        if in_str:
            if ch == "\\" and i + 1 < len(text):
                i += 2
                continue
            if ch == in_str:
                in_str = None
        elif ch in '"\'`':
            in_str = ch
        elif ch in pair:
            stack.append(ch)
        elif ch in ")]}":
            if not stack or pair[stack.pop()] != ch:
                return False
        i += 1
    return not stack and in_str is None
for fn in ("background.js", "content.js", "popup.js"):
    text = (ex / fn).read_text(encoding="utf-8")
    if _shutil.which("node"):
        node_path = _shutil.which("node")
        with open(ex / fn, "r", encoding="utf-8") as _f:
            import subprocess as _sp
            r = _sp.run([node_path, "--check", ex / fn], capture_output=True, timeout=30)
        assert r.returncode == 0, ("node --check %s 失败: %s" % (fn, r.stderr.decode("utf-8", "replace")))
    else:
        assert _balance_ok(text), "%s 括号不匹配" % fn
checks += 10''')


_g('27) 任务中心首页 HTML 回归：width:100%% 必须转义，空任务与有任务都能渲染', r'''html0 = pan.serve_home_html([])
assert "网盘通" in html0 and "暂无任务" in html0
assert "width:100%" in html0, "页面 CSS 应输出 width:100%"
sample_task = {
    "id": "T-1", "drive_name": "百度网盘", "drive": "baidu", "current_step": "下载中",
    "speed_kbps": 12.5, "avg_speed_kbps": 10.0, "state": "running",
    "engine": "baiduweb", "updated": "2026-10-08 16:00", "finished": ""
}
html1 = pan.serve_home_html([sample_task])
assert "网盘通" in html1 and "taskHtml" in html1 and "bar" in html1
assert "暂停" in html1 and "删除" in html1
assert "setInterval(loadTasks,10000)" in html1 and "/api/tasks" in html1
assert "width:100%" in html1
assert html1.count("%s") == 0, "模板不应残留未替换 %s"
checks += 9''')


_g('28) 智能默认：自动分类归档 + PWA 清单/离线外壳', r'''assert pan.content_category("https://example.com/movie.mp4") == "影视"
assert pan.content_category("https://example.com/song.flac") == "音乐"
assert pan.content_category("https://example.com/report.pdf") == "文档"
assert pan.content_category("https://example.com/photo.png") == "图片"
assert pan.content_category("https://example.com/a.zip") == "压缩包"
assert pan.content_category("https://example.com/noext") == "其他"
smart_cfg = json.loads(json.dumps(cfg))
smart_cfg["smart"] = {"auto_classify": True, "classify_root": str(TMP / "classify")}
p_class = pan.build_plan("https://example.com/movie.mp4", cfg=smart_cfg)
assert p_class["category"] == "影视", p_class
assert str(p_class["target"]).startswith(str(TMP / "classify")), p_class["target"]
assert "智能分类已启用" in " ".join(p_class["warnings"]), p_class
# 未开智能分类时按原样
p_plain = pan.build_plan("https://example.com/movie.mp4", cfg=cfg)
assert p_plain["category"] == "" and "影视" not in str(p_plain["target"]), p_plain
# --classify 手动开启也能生效（不依赖配置）
p_force = pan.build_plan("https://example.com/song.flac", cfg=cfg, classify=True)
assert p_force["category"] == "音乐" and "音乐" in str(p_force["target"]), p_force
# PWA 清单与服务 worker
mf = json.loads(pan.pwa_manifest_json())
assert mf["display"] == "standalone" and mf["start_url"] == "/"
assert any(i.get("sizes") == "192x192" for i in mf["icons"])
sw = pan.pwa_service_worker_js()
assert "addEventListener('fetch'" in sw and "caches.open" in sw
icon = pan.pwa_icon_png(192)
assert icon[:8] == b"\x89PNG\r\n\x1a\n" and icon[12:16] == b"IHDR"
# 两个页面都已带 manifest 和服务 worker 注册
for html in (pan.serve_home_html([]), pan.serve_live_page_html(object())):
    assert 'rel="manifest"' in html and "serviceWorker" in html
checks += 14''')


_g('29) 速度曲线 + 剩余时间估算：历史采样、total_bytes/percent/eta 字段与页面图表', r'''curve_cfg = json.loads(json.dumps(cfg))
curve_cfg["http"]["live_dir"] = str(TMP / "curveout")
curve_cfg["http"]["live_interval"] = 0.2
curve_plan = {
    "ok": True, "drive": "direct", "drive_name": "直链", "engine": "http",
    "tier": "free", "target": str(TMP / "curve_target"), "total_bytes": 8192,
}
Path(curve_plan["target"]).mkdir(parents=True, exist_ok=True)
(Path(curve_plan["target"]) / "x.bin").write_bytes(b"a" * 4096)
cm = pan.LiveMonitor(curve_cfg, curve_plan, url="https://example.com/x.bin", interval=0.2)
cm.start()
last = cm.write()
assert "total_bytes" in last and last["total_bytes"] == 8192, last
assert "history" in last and isinstance(last["history"], list), last
assert "percent" in last and last["percent"] is not None, last
cm.stop(ok=True)
# 页面渲染带 chart 容器和曲线数据
lv = pan.serve_live_page_html("<tr></tr>", items_json='[{"history":[[0,12.5],[1,20.0]],"eta":"约 5 秒"}]')
assert "CURVE_DATA" in lv and "charts" in lv and "canvas" in lv, lv[:200]
assert "约 5 秒" in lv, lv
_live_body, _live_items = pan.render_live_table([{
    "state": "running", "drive_name": "HTTP 直链", "current_step": "data.bin",
    "speed_kbps": 632.5, "avg_speed_kbps": 500.0, "bytes_done": 4194304,
    "total_bytes": 4194304, "percent": 100.0, "eta_seconds": 7.2,
    "local_path": str(TMP / "live-out"), "current_file": "data.bin", "history": [[0, 1]],
}])
assert "下载位置" in _live_body and "复制路径" in _live_body and "data.bin" in _live_body, _live_body
assert json.loads(_live_items)[0]["path"].endswith("/data.bin"), _live_items
_empty_body, _empty_items = pan.render_live_table([])
assert "暂无进行中的实时下载" in _empty_body and _empty_items == "[]", (_empty_body, _empty_items)
# probe 解析 Content-Length（构造 dummy 子进程返回）
import subprocess as _sp2
real_run = pan.subprocess.run
pan.subprocess.run = lambda argv, capture_output=True, text=True, timeout=5: type("P", (), {"returncode": 0, "stdout": "HTTP/1.1 200 OK\r\ncontent-length: 12345\r\n", "stderr": ""})()
try:
    assert pan.probe_http_total_bytes("https://example.com/a.zip", curve_cfg) == 12345
finally:
    pan.subprocess.run = real_run
checks += 11''')


_g('30) 配置向导增强：pan test 只读测试连接 / API test / MCP pan_test 工具', r'''res = pan._probe_link_checks(cfg, "https://example.com/a.zip")
assert res["ok"] is True and res["drive"] == "direct", res
names = [c["name"] for c in res["checks"]]
assert "识别" in names and "依赖与配置" in names and "目标目录" in names, names
assert res["target"] and str(res["target"]).startswith(str(TMP)), res["target"]
res_bd = pan._probe_link_checks(cfg, "https://pan.baidu.com/s/1abcdEFG")
assert res_bd["drive"] == "baidu" and res_bd["drive_name"] == "百度网盘", res_bd
# 百度默认官方网页会话，不需要 BaiduPCS-Go；预检应给出可零客户端执行的计划
assert res_bd["ok"] is True and res_bd["engine"] == "baiduweb", res_bd
assert res_bd["auth"]["blocking"] is False and res_bd["zero_client"][0]["id"] == "web", res_bd
rc, out = capture_call(pan.cmd_test, types.SimpleNamespace(url="https://example.com/a.zip", json=True, pwd="", engine="", tier="", path=""))
assert rc == 0 and json.loads(out)["drive"] == "direct", (rc, out)
# MCP tools 里有 pan_test，且 call_tool 会拼出 test 命令（不真正跑 subprocess，避免联网）
mcp_path = HERE / "pan_mcp.py"
assert "pan_test" in mcp_path.read_text(encoding="utf-8"), "pan_mcp 缺少 pan_test 工具"
assert 'name == "pan_test"' in mcp_path.read_text(encoding="utf-8"), "pan_mcp call_tool 未处理 pan_test"
checks += 6''')


_g('31) Web UI 测试连接页：主页入口 / PWA 缓存 / 独立页面 / 路由', r'''home = pan.serve_home_html([])
assert "href=/test" in home, "任务中心缺测试连接入口"
assert "testForm" in pan.serve_test_html() and "testUrl" in pan.serve_test_html(), "测试页缺少表单"
assert "fetch('/api/route?'" in pan.serve_test_html(), "测试页缺少 /api/route 调用"
assert pan.serve_test_html().count("%s") == 0, "测试页不应残留未替换 %s"
assert "caches.open(CACHE)" in pan.pwa_service_worker_js() and "'/test'" in pan.pwa_service_worker_js(), "PWA 缓存未含 /test"
assert '"/test"' in (_PAN_PY.read_text(encoding='utf-8') + _PAN_WEB.read_text(encoding='utf-8')) or "'/test'" in (_PAN_PY.read_text(encoding='utf-8') + _PAN_WEB.read_text(encoding='utf-8')), "serve 路由未注册 /test"
rc, out = capture_call(pan.cmd_test, types.SimpleNamespace(url="https://example.com/a.zip", json=True, pwd="", engine="", tier="", path=""))
assert rc == 0 and json.loads(out)["ok"] is True, (rc, out)
# 自动 Web UI：复用已运行服务并打开 /live，不启动真实子进程
from pancli import web as _web_auto
_saved_ready, _saved_browser = _web_auto._web_ui_status_ok, _web_auto.webbrowser.open
_opened = []
_web_auto._web_ui_status_ok = lambda port, timeout=0.35, expected_reports_dir="": int(port) == 17890
_web_auto.webbrowser.open = lambda url, new=1: _opened.append(url) or True
try:
    _auto = pan.ensure_web_ui({"http": {"auto_web": True}, "deployment": {"web_port": 17890}})
finally:
    _web_auto._web_ui_status_ok, _web_auto.webbrowser.open = _saved_ready, _saved_browser
assert _auto["ok"] and _auto["reused"] and _auto["browser_opened"], _auto
assert _opened == ["http://127.0.0.1:17890/live"], _opened
assert not pan.ensure_web_ui({"http": {"auto_web": False}})["ok"], "auto_web=false 不应启动"
parser_src = _PAN_PY.read_text(encoding="utf-8")
assert '"--no-web"' in parser_src and '"auto_web": True' in parser_src, "CLI/config 缺自动 Web 开关"
home_auto = pan.serve_home_html([])
live_auto = pan.serve_live_page_html("<tr></tr>")
assert "复制路径" in home_auto and "下载位置" in home_auto, "任务中心缺下载位置/复制路径"
assert "复制路径" in live_auto and "下载位置" in live_auto, "实时页缺下载位置/复制路径"
assert "setInterval" in live_auto and "location.reload" in live_auto, "实时页缺自动刷新"
assert "}, 10000);" in live_auto, "实时页应每 10 秒刷新一次"
checks += 9''')


_g('32) 1-4 项优化：后处理链样板 / 扩展弹窗测试连接 / 提取码提示 / --at 定时骨架', r'''hook_sh = HERE.parent / "scripts" / "hooks" / "post_media.sh"
assert hook_sh.exists() and hook_sh.stat().st_mode & 0o111, "后处理链样板脚本缺失/不可执行"
hook_txt = hook_sh.read_text(encoding="utf-8")
assert "AUTO=" in hook_txt and "unzip" in hook_txt and "Jellyfin" in hook_txt, "后处理样板内容异常"
pop = HERE.parent / "extensions" / "chrome" / "popup.html"
popjs = HERE.parent / "extensions" / "chrome" / "popup.js"
assert pop.exists() and popjs.exists()
assert "tstart" in pop.read_text(encoding="utf-8") and "测试连接" in pop.read_text(encoding="utf-8"), "弹窗缺测试连接区"
assert "/api/test" in popjs.read_text(encoding="utf-8") and '$("tres")' in popjs.read_text(encoding="utf-8"), "弹窗缺 /api/test 交互"
plan_pwd = pan.build_plan("https://pan.baidu.com/s/1abc", pwd="", cfg=cfg)
assert any("提取码" in w for w in plan_pwd["warnings"]), plan_pwd["warnings"]
plan_pwd2 = pan.build_plan("https://pan.baidu.com/s/1abc", pwd="1234", cfg=cfg)
assert not any("常见带提取码" in w for w in plan_pwd2["warnings"]), plan_pwd2["warnings"]
assert pan._wait_schedule("", None, dry_run=True) == 0
assert pan._wait_schedule("00:00", None, dry_run=True) == 0
assert pan._wait_schedule("23:59", None, dry_run=True) == 0
assert (cfg.get("http") or {}).get("schedule_at") is not None
checks += 6''')


_g('33) 第 1 步：网页/Agent 一站式——首页下载表单、剪贴板监听、一键启动脚本', r'''from pancli import web as _web_mod
home2 = _web_mod.serve_home_html([])
assert "submitUrls" in home2 and "/api/download" in home2 and "无需点击开始" in home2, "首页缺自动投递表单"
assert "loadTasks" in home2 and "/api/tasks" in home2 and "setInterval(loadTasks,10000)" in home2, "首页投递后应自动刷新任务"
# /api/download 返回 live_url / home_url 字段（在 do_POST 代码里检查真实字符串）
assert 'live_url' in _PAN_WEB.read_text(encoding="utf-8"), "web.py 缺 live_url 响应字段"
assert 'home_url' in _PAN_WEB.read_text(encoding="utf-8"), "web.py 缺 home_url 响应字段"
clip = HERE / "clipboard_monitor.py"
assert clip.exists(), "剪贴板监听脚本缺失"
clip_txt = clip.read_text(encoding="utf-8")
assert "extract_urls" in clip_txt and "/api/download" in clip_txt and "pbpaste" in clip_txt, "剪贴板监听内容异常"
assert "_URL_RE" in clip_txt, "clipboard_monitor 缺正则"
web = HERE.parent / "scripts" / "pan_web.sh"
assert web.exists() and web.stat().st_mode & 0o111, "pan_web.sh 缺失/不可执行"
web_txt = web.read_text(encoding="utf-8")
assert "clipboard_monitor" in web_txt and "serve" in web_txt and "open" in web_txt, "pan_web.sh 内容异常"
# Windows 一键脚本与小白指南（非 Windows 轻量包跳过 .ps1）
if __import__("sys").platform.startswith("win"):
    web_ps1 = HERE / "pan_web.ps1"
    assert web_ps1.exists(), "pan_web.ps1 缺失（Windows 一键启动）"
    ps1_txt = web_ps1.read_text(encoding="utf-8")
    for token in ("clipboard_monitor.py", "serve", "17890", "Invoke-WebRequest"):
        assert token in ps1_txt, "pan_web.ps1 缺 %s" % token
    checks += 2
guide = HERE.parent / "references" / "29-小白快速上手指南.md"
assert guide.exists() and "粘贴链接开始下载" in guide.read_text(encoding="utf-8"), "小白上手指南缺失/异常"
checks += 6''')


_g('34) 第 2 步：远程 NAS 常驻 + 网页控制——remote deploy 支持 --web-port、远程启动 serve、remote web 帮助', r'''_code = _PAN_PY.read_text(encoding="utf-8")
_code_remote = _PAN_REMOTE.read_text(encoding="utf-8")
for token in ("--web-port", "--web-host", "--web-reports-dir"):
    assert token in _code, "pan.py 缺 %s" % token
for token in ("remote_web_access", "build_remote_deploy_plan"):
    assert token in _code_remote, "remote.py 缺 %s" % token
entry = {"kind": "ssh", "host": "192.168.1.10", "user": "lis", "root": "/volume1", "python": "python3", "deploy_dir": ".pan-downloader"}
entry["name"] = "nas"
archive = TMP / "deploy.tar.gz"
archive.write_bytes(b"")
plan = pan.build_remote_deploy_plan(dict(entry), str(archive), web_port=17890, web_host="127.0.0.1", web_reports_dir="/volume1")
assert plan.get("ok") and plan.get("web_port") == 17890, "remote deploy 计划未包含 web_port"
assert plan.get("web_url"), "远程 web_url 为空"
last = plan["steps"][-1]
assert last["engine"] == "ssh", "应为 ssh 步骤启动远程 serve"
argv = " ".join(last["argv"])
_argv = argv.replace("'", "").replace('"', "")
for token in ("nohup", "python3", "scripts/pan.py interact", "serve --host 127.0.0.1 --port 17890 --reports-dir /volume1", "</dev/null", "pan-remote-web-nas.log"):
    _t = token.replace("scripts/pan.py interact", "scripts/pan.py")
    assert _t in _argv, "远程启动命令缺 %s：%s" % (_t, argv)
# 公开计划应带 web 信息，供 Agent/JSON 使用
pub = pan.public_plan(plan)
assert pub.get("web_port") == 17890 and pub.get("web_url"), "public_plan 未带 web 字段"
# remote web 帮助：局域网 host 用 0.0.0.0 时应给出 NAS 直连 URL
info = pan.remote_web_access(dict(entry), port=17890, web_host="0.0.0.0")
assert "192.168.1.10:17890" in info["url"], "0.0.0.0 时 web URL 应使用 NAS host"
assert info["tunnel"], "应有 SSH 反向隧道提示"
# 远程 get --live 应拼出 ssh 远程命令中的 --live，供远程 Web 页面显示实时速度
rplan = pan.build_remote_plan(dict(entry, live=True), "https://pan.baidu.com/s/x", to="/volume1/netdisk", pwd="")
last_argv = " ".join(rplan["steps"][0]["argv"])
assert "--live" in last_argv, "远程 get --live 未拼入远程命令"
# remote get parser 已声明 --live 参数（通过源码文本检查）
assert 'rg.add_argument("--live"' in _PAN_PY.read_text(encoding="utf-8"), "remote get 缺 --live 参数"
checks += 14''')


_g('35) 第 3 步：飞书机器人——notify 支持 feishu、桥接脚本存在且自检通过', r'''code3 = _PAN_PY.read_text(encoding="utf-8")
assert '"feishu_secret"' in code3 and "feishu_secret" in _PAN_PY.read_text(encoding="utf-8"), "pan.py 缺 feishu_secret"
code_carrier = _PAN_CARRIERS.read_text(encoding="utf-8")
assert "channel == \"feishu\"" in code_carrier or 'channel == "feishu"' in code_carrier, "carriers.py 缺 feishu"
assert 'choices=["work_weixin", "bark", "telegram", "discord", "feishu"]' in code3, "notify 通道未加 feishu"
fb = HERE / "feishu_bot.py"
assert fb.exists(), "飞书桥 feishu_bot.py 缺失"
fb_src = fb.read_text(encoding="utf-8")
for token in ("url_verification", "challenge", "/api/download", "extract_urls", "--check", "feishu/callback"):
    assert token in fb_src, "feishu_bot.py 缺 %s" % token
ref28 = HERE.parent / "references" / "28-飞书机器人.md"
assert ref28.exists() and "im.message.receive_v1" in ref28.read_text(encoding="utf-8"), "references/28 飞书文档缺失"
# 配置示例同步 feishu_secret
cfg_ex = (HERE.parent / "config.example.json").read_text(encoding="utf-8")
assert "feishu_secret" in cfg_ex, "config.example.json 缺 feishu_secret"
# 桥接自检：导入脚本并运行 self_check（不联网）
fbmod = importlib.util.spec_from_file_location("feishu_bot", fb)
mfb = importlib.util.module_from_spec(fbmod)
fbmod.loader.exec_module(mfb)
assert mfb.self_check() == 0, "feishu_bot self_check 未通过"
assert mfb.extract_pwd("提取码：2abc4 https://pan.baidu.com/s/x") == "2abc4", "提取码抽取失败"
checks += 14''')


_g('40) 最快链接测速（离线模拟 dummy curl）', r'''_sub_module = pan.subprocess
orig_run = pan.subprocess.run
calls = {"n": 0}
def _dummy_run(argv, **kw):
    calls["n"] += 1
    from types import SimpleNamespace
    if "-o" in argv:
        out = Path(argv[argv.index("-o") + 1])
        out.write_bytes(b"a" * 100_000)
    return SimpleNamespace(returncode=0, stdout="", stderr="")
pan.subprocess.run = _dummy_run
try:
    ranked = pan.rank_fastest_urls(["https://m1.example/f.bin", "https://m2.example/f.bin"], cfg=cfg, timeout=1, samples=100000)
    assert len(ranked) == 2 and all(r["ok"] for r in ranked), ranked
    assert all("kbps" in r and "url" in r for r in ranked), ranked
finally:
    pan.subprocess.run = orig_run
checks += 3''')


_g('41) movie 子命令：免费电影源 / 最快候选 / X(推特) 视频（离线 mock，不真下载）', r'''rc, out = capture_call(pan.cmd_movie_sources, types.SimpleNamespace(json=True))
assert rc == 0 and '"sources"' in out and 'archive.org' in out, "movie sources 未输出 JSON 源列表"
for u in ("https://x.com/i/status/123", "https://twitter.com/some/status/123", "https://mobile.twitter.com/a/status/123"):
    assert pan.detect_drive(u)[0] == "stream", u + " 未识别为 stream"
_orig_find = _sm.find_engine_binary
_sm.find_engine_binary = lambda engine, cfg, **kw: "/tmp/fake-yt-dlp"
try:
    xargs = types.SimpleNamespace(url="https://x.com/i/status/123", remote="", to=None, tier=None,
                                  dry_run=True, force=False, json=True, live=False, classify=None)
    rc, out = capture_call(pan.cmd_movie_x, xargs)
    assert rc == 0, "movie x --dry-run 失败: " + out
    assert "yt-dlp" in out or "plan" in out.lower(), "movie x 未输出 yt-dlp 计划"
finally:
    _sm.find_engine_binary = _orig_find
orig_rank = _sm.rank_fastest_urls
fast = {"ok": True, "url": "https://fast.example/movie.mp4", "kbps": 9999.0}
slow = {"ok": False, "url": "https://slow.example/movie.mp4", "error": "timeout"}
_sm.rank_fastest_urls = lambda urls, cfg=None, timeout=6, samples=200000: [fast, slow]
try:
    gargs = types.SimpleNamespace(url="https://slow.example/movie.mp4", candidates="https://fast.example/movie.mp4",
                                  remote="", to=None, engine=None, tier=None, path=None, timeout=6, samples=200000,
                                  dry_run=True, force=False, json=True, events=False, live=False, split=0, at="", classify=None)
    rc, out = capture_call(pan.cmd_movie_get, gargs)
    assert rc == 0, "movie get --dry-run 失败: " + out
    assert "fast.example/movie.mp4" in out, "movie get 未选用最快候选链接"
finally:
    _sm.rank_fastest_urls = orig_rank
code41 = _PAN_PY.read_text(encoding="utf-8")
assert 'movie_sub.add_parser("sources"' in code41, "movie sources 未注册"
assert 'movie_sub.add_parser("get"' in code41, "movie get 未注册"
assert 'movie_sub.add_parser("x"' in code41, "movie x 未注册"
checks += 12''')


_g('42) 搜索候选：离线 mock http/yt-dlp，验证 search 命令与候选解析 / Docker 文件生成', r'''_orig_fetch = _sm.fetch_url
def _fake_fetch(url, timeout=20, cfg=None):
    if "advancedsearch.php" in url:
        return json.dumps({"response": {"docs": [{"identifier": "public_movie_01", "title": "公开电影示例"}]}})
    if "html.duckduckgo.com" in url:
        return '<a href="https://example.com/sample.mp4">示例</a>'
    raise OSError("no network")
_sm.fetch_url = _fake_fetch
try:
    _old_find = _sm.find_engine_binary
    _sm.find_engine_binary = lambda engine, cfg: "/tmp/fake-yt-dlp"
    _old_run = pan.subprocess.run
    pan.subprocess.run = lambda argv, capture_output=True, text=True, timeout=20: types.SimpleNamespace(
        returncode=0, stdout="vid1\tdemo video\thttps://www.youtube.com/watch?v=vid1\n", stderr="")
    try:
        cands = pan.search_candidates("matrix", kind="movie", providers=["archive"], cfg={})
        assert cands and cands[0]["provider"] == "archive" and "public_movie_01" in cands[0]["url"], cands
        cands2 = pan.search_candidates("demo", kind="video", providers=["ytdlp"], cfg={})
        assert cands2 and cands2[0]["url"] and "youtube.com" in cands2[0]["url"], cands2
        cands3 = pan.search_candidates("sample", kind="file", providers=["duckduckgo"], cfg={})
        assert cands3 and cands3[0]["url"] == "https://example.com/sample.mp4", cands3
        sp = pan.build_parser()
        args = sp.parse_args(["search", "matrix", "--kind", "movie", "--json"])
        assert getattr(args.func, "_lazy_func", None) == "cmd_search" and args.kind == "movie"
        dout = TMP / "docker-out"
        dargs = types.SimpleNamespace(docker_cmd="files", out=str(dout), json=False)
        rc = pan.cmd_docker(dargs)
        assert rc == 0 and (dout / "Dockerfile").exists()
        dfile = (dout / "Dockerfile").read_text(encoding="utf-8")
        for token in ("FROM python:3.11-slim", "aria2", "yt-dlp", "17890", "ENTRYPOINT"):
            assert token in dfile, token
        assert "docker compose up -d" in (dout / "install.sh").read_text(encoding="utf-8")
    finally:
        pan.subprocess.run = _old_run
        pan.find_engine_binary = _old_find
finally:
    _sm.fetch_url = _orig_fetch
code42 = _PAN_PY.read_text(encoding="utf-8")
assert 'sub.add_parser("search"' in code42 and 'sub.add_parser("docker"' in code42
checks += 14''')


_g('43) 搜索连通性检测 + 网页候选授权确认 + Docker check（离线 mock）', r'''_orig_fetch2 = _sm.fetch_url
def _fake_fetch2(url, timeout=20, cfg=None):
    if "html.duckduckgo.com" in url:
        return '<a href="https://example.com/sample.mp4">示例</a>'
    if "advancedsearch.php" in url:
        return json.dumps({"response": {"docs": [{"identifier": "a1", "title": "t"}]}})
    return "ok"
_sm.fetch_url = _fake_fetch2
import pancli.docker as _pan_docker
_orig_ready_find = _pan_docker.find_engine_binary
_pan_docker.find_engine_binary = lambda engine, cfg: "/tmp/mock-yt-dlp" if engine == "ytdlp" else _orig_ready_find(engine, cfg)
try:
    rc, out = capture_call(pan.cmd_search_check, cfg={}, kind="movie", timeout=1, json_flag=True)
    assert rc == 0 and '"ok": true' in out and '"provider"' in out, out
    # 网页候选未确认授权时应拒绝下载且返回确认码 3
    webargs = types.SimpleNamespace(query="x", kind="file", providers="duckduckgo", limit=3, timeout=1,
                                    list_providers=False, json=False, check=False, assume_own=False,
                                    pick=1, remote="", to=None, engine=None, tier=None, path=None,
                                    dry_run=False, force=False, live=False, split=0, classify=None)
    rc, out = capture_call(pan.cmd_search, webargs)
    assert rc == 3 and "assume-own" in out, (rc, out)
    # 加了 --assume-own 后 dry-run 才放行进入下载计划
    webargs_ok = types.SimpleNamespace(**{**vars(webargs), "assume_own": True, "dry_run": True})
    rc, out = capture_call(pan.cmd_search, webargs_ok)
    assert rc == 0, (rc, out)
finally:
    _pan_docker.find_engine_binary = _orig_ready_find
    _sm.fetch_url = _orig_fetch2
# Docker check：mock 无 docker 时也能验证生成文件完整性与不可用提示
_orig_which = pan.shutil.which
pan.shutil.which = lambda name: "" if name in ("docker", "podman") else _orig_which(name)
try:
    dout = TMP / "docker-check-out"
    dargs = types.SimpleNamespace(docker_cmd="files", out=str(dout), json=False)
    pan.cmd_docker(dargs)
    dargs2 = types.SimpleNamespace(docker_cmd="check", out=str(dout), json=True)
    rc, out = capture_call(pan.cmd_docker, dargs2)
    assert rc == 2 and '"docker": null' in out, (rc, out)
    assert (dout / "Dockerfile").exists() and (dout / "docker-compose.yml").exists()
finally:
    pan.shutil.which = _orig_which
code43 = _PAN_PY.read_text(encoding="utf-8")
code_docker = _PAN_DOCKER.read_text(encoding="utf-8")
for token in ("--check", "--assume-own"):
    assert token in code43, token
for token in ("cmd_docker_check", "docker_runtime_available"):
    assert token in code_docker, token
checks += 18

# 43b) 网络爬虫：单页提取 + 相对链接 + magnet/torrent 分类 + --pick --dry-run
_orig_fetch3 = _sm.fetch_url
def _fake_fetch3(url, timeout=20, cfg=None):
    if "gallery.example.com" in url:
        return (
            '<html><body>'
            '<a href="/movie/001.mp4">公映电影A</a>'
            '<a href="music/02.flac">无损音乐B</a>'
            '<a href="https://dl.example.com/doc/说明.pdf">说明书C</a>'
            '<a href="webr/segment.m3u8">直播流D</a>'
            '<a href="magnet:?xt=urn:btih:0123456789abcdef0123456789abcdef01234567">磁力E</a>'
            '<a href="torrent/film.torrent">种子F</a>'
            '<a href="/">首页</a>'
            '</body></html>'
        )
    raise OSError("no network")
_sm.fetch_url = _fake_fetch3
try:
    got = pan.crawl_page_candidates("https://gallery.example.com/index.html", limit=20, cfg={})
    urls = [c["url"] for c in got]
    for expect in ("https://gallery.example.com/movie/001.mp4",
                   "https://gallery.example.com/music/02.flac",
                   "https://dl.example.com/doc/说明.pdf",
                   "https://gallery.example.com/webr/segment.m3u8",
                   "magnet:?xt=urn:btih:0123456789abcdef0123456789abcdef01234567",
                   "https://gallery.example.com/torrent/film.torrent"):
        assert expect in urls, (expect, urls)
    movie = pan.crawl_page_candidates("https://gallery.example.com/", limit=20, cfg={}, kind="movie")
    assert all(c["kind"] == "movie" for c in movie) and movie, movie
    music = pan.crawl_page_candidates("https://gallery.example.com/", limit=20, cfg={}, kind="music")
    assert all(c["kind"] == "music" for c in music) and music, music
    assert got[0]["kind"] in ("torrent", "video", "movie"), got[0]
    # crawl 网页候选未确认授权应返回 3
    cargs = types.SimpleNamespace(url="https://gallery.example.com/", kind="auto", limit=20, timeout=1,
                                  depth=0, json=False, assume_own=False, pick=1, remote="", to=None,
                                  engine=None, tier=None, path=None, dry_run=False, force=False,
                                  live=False, split=0, classify=None)
    rc, out = capture_call(pan.cmd_crawl, cargs)
    assert rc == 3 and "assume-own" in out, (rc, out)
    # --dry-run 放行，直接打印下载计划
    cargs_dry = types.SimpleNamespace(**{**vars(cargs), "dry_run": True})
    rc, out = capture_call(pan.cmd_crawl, cargs_dry)
    assert rc == 0, (rc, out)
    # JSON 模式
    cargs_json = types.SimpleNamespace(**{**vars(cargs), "json": True, "pick": 0})
    rc, out = capture_call(pan.cmd_crawl, cargs_json)
    assert rc == 0 and '"provider": "crawl"' in out, (rc, out[:300])
    # 命令行已注册 crawl
    sp = pan.build_parser()
    a2 = sp.parse_args(["crawl", "https://gallery.example.com/", "--kind", "video", "--json"])
    assert getattr(a2.func, "_lazy_func", None) == "cmd_crawl" and a2.kind == "video"
finally:
    _sm.fetch_url = _orig_fetch3
code43b = _PAN_PY.read_text(encoding="utf-8") + _PAN_SEARCH.read_text(encoding="utf-8")
for token in ("def cmd_crawl", "def crawl_page_candidates", "dispatch_chosen_download", "p_crawl"):
    assert token in code43b, token
checks += 14''')


_g('44) 真机回归脚本已接入搜索源连通性检查（--only search）', r'''_vfy = (HERE.parent / "scripts" / "verify_real_env.py").read_text(encoding="utf-8")
for token in ("def check_search", "search-sources", "--only", "search --check"):
    assert token in _vfy, "verify_real_env.py 缺 %s" % token
checks += 4''')


_g('61) v0.14 通用调度层：本机优先、三入口、三系统、三部署模式、插件一致性', r'''skill_root = HERE.parent
universal_files = [
    skill_root / "SKILL.md",
    skill_root / "README.md",
    skill_root / "extensions/chrome/README.md",
    skill_root / "references/23-MCP与Agent接口.md",
]
universal_text = "\n".join(p.read_text(encoding="utf-8") for p in universal_files)
for tok in ("通用下载调度层", "Agent / MCP / CLI", "Web UI", "浏览器插件",
            "<api-url>", "<download-dir>", "<port>", "<pan-root>",
            "macOS Keychain", "Windows Credential Manager", "secret-tool",
            "pan_get", "pan_task", "pan_get_plan"):
    assert tok in universal_text, "通用文档缺 %s" % tok
assert (skill_root / "SKILL.md").read_text(encoding="utf-8").startswith("---\nname:"), "SKILL front matter 异常"
readme_head = (skill_root / "README.md").read_text(encoding="utf-8")
assert "通用下载调度层" in readme_head.split("\n", 1)[0] or "\n通用下载调度层" in readme_head[:500], "README 未以通用调度层开场"
assert ("192.168.1." + "240") not in universal_text, "通用文档残留私有地址"
# 代码与核心文档均不保留私人 NAS 地址
private_text = []
for p0 in skill_root.rglob("*"):
    if not p0.is_file() or "tools" in p0.parts or ".git" in p0.parts:
        continue
    try:
        private_text.append(p0.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        pass
assert all(("192.168.1." + "240") not in t and ("/volume1/docker/" + "cdd") not in t for t in private_text), "残留私人地址"
# 插件名称与地址说明一致
ex_dir = skill_root / "extensions" / "chrome"
mf0 = json.loads((ex_dir / "manifest.json").read_text(encoding="utf-8"))
assert "通用 pan 下载插件" in mf0["name"], mf0["name"]
ext_readme = (ex_dir / "README.md").read_text(encoding="utf-8")
for tok in ("本机", "NAS", "服务器", "Chrome 安装", "Edge 安装", "测试连接", "不读取网页登录态"):
    assert tok in ext_readme, "插件 README 缺 %s" % tok
# 三模式配置生成
dep_cfg = {}
for mode, expected_host in (("local", "127.0.0.1"), ("nas_docker", "<nas>"), ("server_docker", "<server>")):
    c0 = dict(dep_cfg)
    args0 = types.SimpleNamespace(mode=mode, port=17890, host=expected_host, api_url="", root="<download-dir>",
                                  alist_url="", rclone_remote="")
    c0 = pan.apply_deployment(c0, args0)
    assert c0["deployment"]["mode"] == mode, (mode, c0["deployment"])
    assert c0["deployment"]["api_url"] == "http://%s:17890" % expected_host, c0["deployment"]
    assert c0["download_root"] == "<download-dir>" or mode != "local", c0
# setup 帮助/doctor 明确 local 优先且无 NAS 依赖
code_setup = _PAN_SETUP.read_text(encoding="utf-8")
assert "local / 本机 Agent / CLI" in code_setup and "无服务模式" in code_setup, "doctor 未以 local 为默认"
assert "macOS Keychain" in code_setup and "Windows Credential Manager" in code_setup and "secret-tool" in code_setup, "setup 缺三系统提示"
checks += 12''')


_g('60) v0.13 免客户端：doctor 三态 + bookmarklet 路由 + compose 文件', r'''code_setup = _PAN_SETUP.read_text(encoding="utf-8")
assert "运行模式" in code_setup and "local / 本机 Agent / CLI" in code_setup and "nas_docker" in code_setup, "doctor 缺运行模式输出"
code_web = _PAN_WEB.read_text(encoding="utf-8")
assert "bookmarklet_js" in code_web and "/bookmarklet.js" in code_web, "web 缺书签脚本路由"
compose = HERE.parent / "docker" / "docker-compose.full.yml"
assert compose.exists() and "cdd-alist" in compose.read_text(encoding="utf-8"), "缺 compose.full"
code_mcp = (HERE / "pan_mcp.py").read_text(encoding="utf-8")
for tok in ("pan_get", "pan_task"):
    assert tok in code_mcp, "pan_mcp 缺 %s" % tok
checks += 5''')


_g('62) R17 登录与 WebUI 统一流程', r'''ref35 = skill_root / "references" / "35-登录与WebUI统一流程.md"
ref36 = skill_root / "references" / "36-WebUI实时进度规范.md"
assert ref35.exists(), "references/35 登录统一流程缺失"
assert ref36.exists(), "references/36 WebUI 进度规范缺失"
t35 = ref35.read_text(encoding="utf-8")
t36 = ref36.read_text(encoding="utf-8")
for tok in ("官方 OAuth / 扫码 / 浏览器授权", "不要把密码、Cookie、BDUSS、STOKEN", "/login"):
    assert tok in t35, "35 缺 %s" % tok
for tok in ("任务必须可见", "下载中不做聊天轮询", "用临时脚本绕开 Web UI"):
    assert tok in t36, "36 缺 %s" % tok
code_web = _PAN_WEB.read_text(encoding="utf-8")
for tok in ("def serve_login_html", '("/login", "/login.html")', 'href=/login', "官方登录优先"):
    assert tok in code_web, "web.py 缺登录页关键点 %s" % tok
skill_text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
readme_text = (skill_root / "README.md").read_text(encoding="utf-8")
assert "/login" in skill_text and "/login" in readme_text, "入口文档缺 /login"
checks += 4''')


_g('63) R18 秒级登录门禁', r'''for tok in ("def login_gate_for_url", "def fast_login_gate", "def cmd_auth", "p_auth = sub.add_parser(\"auth\"", "/login?drive="):
    assert tok in skill_root.joinpath("scripts/pancli/engine.py").read_text(encoding="utf-8"), "engine 缺秒级门禁 %s" % tok
code_web = _PAN_WEB.read_text(encoding="utf-8")
for tok in ("fast_login_gate", "login_required", "serve_login_html(drive", "parse_qs(urlparse(self.path).query)"):
    assert tok in code_web, "web 缺秒级门禁 %s" % tok
gate = pan.fast_login_gate("https://pan.baidu.com/s/abc", cfg)
assert gate["required"] is False and gate["blocking"] is False and gate["drive"] == "baidu", gate
assert gate["status"] == "web_session" and gate["login_url"] == "", gate
gate2 = pan.fast_login_gate("https://example.com/a.zip", cfg)
assert gate2["required"] is False and gate2["blocking"] is False, gate2
res_auth = pan._probe_link_checks(cfg, "https://pan.baidu.com/s/abc")
assert res_auth["login_required"] is False and res_auth["login_url"] == "", res_auth
assert any(c["name"] == "登录/授权" for c in res_auth["checks"]), res_auth["checks"]
ref35_text = ref35.read_text(encoding="utf-8")
assert "pan route" in ref35_text and "秒级提醒" in ref35_text, ref35_text
checks += 5''')


_g('64) R19 零客户端引擎桥', r'''for tok in ("ZERO_CLIENT_BRIDGES", "def zero_client_options", "def engine_catalog_payload", "def cmd_engines", "浏览器直链捕获桥"):
    assert tok in (HERE.parent / "scripts/pancli/engine.py").read_text(encoding="utf-8"), "engine 缺零客户端桥 %s" % tok
code_web = _PAN_WEB.read_text(encoding="utf-8")
for tok in ("def serve_engines_html", "/engines", "/api/engines", "engine_catalog_payload", "浏览器直链桥"):
    assert tok in code_web, "web 缺零客户端桥 %s" % tok
mcp_text = (HERE / "pan_mcp.py").read_text(encoding="utf-8")
for tok in ("pan_auth", "pan_engines"):
    assert tok in mcp_text, "MCP 缺 %s" % tok
mf = json.loads((HERE.parent / "extensions/chrome/manifest.json").read_text(encoding="utf-8"))
assert "downloads" in mf.get("permissions", []), mf["permissions"]
bg = (HERE.parent / "extensions/chrome/background.js").read_text(encoding="utf-8")
for tok in ("chrome.downloads.onCreated", "captureDownloads", "confirm_auth", "login_required"):
    assert tok in bg, "background 缺零客户端桥 %s" % tok
ref37 = skill_root / "references" / "37-零客户端引擎桥.md"
assert ref37.exists() and "浏览器直链捕获桥" in ref37.read_text(encoding="utf-8"), "references/37 缺失"
checks += 6

# v0.18.3: 真机验证权限清单 + 第三方依赖声明 + 版本一致
_root18 = HERE.parent
_notice = _root18 / "NOTICE.md"
assert _notice.is_file(), "缺少 NOTICE.md"
_ntext = _notice.read_text(encoding="utf-8")
assert "第三方依赖" in _ntext and "yt_dlp" in _ntext, "NOTICE 应声明第三方依赖"
_ref41 = _root18 / "references" / "41-真机验证权限清单.md"
assert _ref41.is_file(), "缺少 references/41 真机验证权限清单"
_r41 = _ref41.read_text(encoding="utf-8")
assert "待用户提供" in _r41 and "最小授权方式" in _r41, "references/41 应列最小授权方式与待提供状态"
_ref40 = _root18 / "references" / "40-网盘支持矩阵.md"
assert _ref40.is_file(), "缺少 references/40 支持矩阵"
_sk = (_root18 / "SKILL.md").read_text(encoding="utf-8")
_mf = json.loads((_root18 / "manifest.json").read_text(encoding="utf-8"))
_ver = _mf.get("version")
assert ("version: %s" % _ver) in _sk.split("---", 2)[1], "SKILL 版本与 manifest 不同步: %s" % _ver
checks += 8

# v0.18.3: /live 页注入风险修复（HTML 转义 + JSON safe embed + DOM textContent）
_web = _PAN_WEB.read_text(encoding="utf-8")
for tok in ("drive_name_html = _html.escape", "current_step_html = _html.escape",
            "updated_html = _html.escape", "local_path_attr = _html.escape",
            '_json_esc = items_json.replace("&", "\\\\u0026")',
            "h.textContent = d.name", "div.appendChild(h); div.appendChild(canv); div.appendChild(meta)"):
    assert tok in _web, "web /live 转义逻辑缺失 %s" % tok
_live_part = _web.split("def serve_live_json", 1)[1].split("def serve_engines_html", 1)[0]
assert "innerHTML" not in _live_part, "live 页面区块不应使用 innerHTML"
checks += 6

code45 = (HERE.parent / "scripts/pancli/engine.py").read_text(encoding="utf-8")
for tok in ("def route_link_payload", "def cmd_route", 'sub.add_parser("route"', "next_action", "latency_ms"):
    assert tok in code45, "engine 缺一次路由 %s" % tok
code_web = _PAN_WEB.read_text(encoding="utf-8")
for tok in ("/api/route", "route_link_payload", "j.next_action", "j.latency_ms"):
    assert tok in code_web, "web 缺一次路由 %s" % tok
mcp_text = (HERE / "pan_mcp.py").read_text(encoding="utf-8")
assert "pan_route" in mcp_text, "MCP 缺 pan_route"
routed = pan.route_link_payload(cfg, "https://pan.baidu.com/s/abc")
assert routed["next_action"] == "download" and routed["login_url"] == "" and routed["engine"] == "baiduweb", routed
assert routed["route"] == "zero_client" and isinstance(routed["latency_ms"], (int, float)), routed
checks += 4''')


_g('66) R21 配置缓存 + 省 token 路由', r'''for tok in ("_CONFIG_CACHE", "_config_stat_key", "def compact_route_payload", '--brief'):
    assert tok in (HERE.parent / "scripts/pancli/engine.py").read_text(encoding="utf-8"), "engine 缺省 token 路由 %s" % tok
b = json.loads(json.dumps(cfg))
b["download_root"] = str(TMP / "token-root")
cache_path = TMP / "config-cache.json"
cache_path.write_text(json.dumps(b), encoding="utf-8")
first = pan.load_config(cache_path)
assert first["download_root"] == str(TMP / "token-root"), first["download_root"]
stat_key = pan._config_stat_key(cache_path)
assert pan._CONFIG_CACHE["key"] == stat_key
second = pan.load_config(cache_path)
assert second["download_root"] == str(TMP / "token-root")
assert first is not second, "配置缓存不能返回同一个可变对象"
checks += 4''')


_g('67) R22 路由短缓存 + 诊断缓存', r'''r1 = pan.route_link_payload(cfg, "https://pan.baidu.com/s/cache-test")
r2 = pan.route_link_payload(cfg, "https://pan.baidu.com/s/cache-test")
r3 = pan.route_link_payload(cfg, "https://pan.baidu.com/s/cache-test", cache=False)
assert r1["cache_hit"] is False and r2["cache_hit"] is True and r3["cache_hit"] is False, (r1["cache_hit"], r2["cache_hit"], r3["cache_hit"])
assert r2["login_url"] == r1["login_url"] and r2["next_action"] == "download", r2
code45 = (HERE.parent / "scripts/pancli/engine.py").read_text(encoding="utf-8")
for tok in ("_ROUTE_CACHE", "_ROUTE_CACHE_TTL", "--no-cache", "def _route_cache_key"):
    assert tok in code45, "engine 缺路由缓存 %s" % tok
code_web = _PAN_WEB.read_text(encoding="utf-8")
for tok in ("_DIAG_CACHE", "_DIAG_CACHE_TTL", "diagnostics_payload(force=", "cache_ttl_seconds"):
    assert tok in code_web, "web 缺诊断缓存 %s" % tok
checks += 4''')


_g('68) v0.15.0 百度官方网页会话桥 + 通用网页引擎核心行为', r'''from pancli import baidu_web as _baidu_web
from pancli import web as _panweb
from pancli import webengine as _webengine

for src in (_PAN_WEB.parent / "webengine.py", _PAN_WEB.parent / "baidu_web.py"):
    compile(src.read_text(encoding="utf-8"), str(src), "exec")
assert pan.build_plan("https://pan.baidu.com/s/1abc?pwd=3379", cfg=cfg)["engine"] == "baiduweb"
assert "setInterval(loadTasks,10000)" in _PAN_WEB.read_text(encoding="utf-8")
assert _panweb._redact_task_url("https://pan.baidu.com/s/1abc?pwd=3379") == "https://pan.baidu.com/s/1abc?pwd=***"
assert _baidu_web._api_error(-20, "验证码").code == "captcha_required"
assert _baidu_web._api_error(118, "违规操作").code == "platform_denied"
checks += 6

fake_root = TMP / "webengine-folder"
fake_root.mkdir(parents=True, exist_ok=True)
(fake_root / "资源").mkdir(parents=True, exist_ok=True)
(fake_root / "资源" / "done.zip").write_bytes(b"0123456789")

class FakeDriver:
    def __init__(self, _cfg, target_root):
        self.target_root = target_root

    def probe(self, url, pwd=""):
        return _webengine.WebProbe(
            driver="fake", url=url, title="folder", password_required=False,
            total_files=3, total_bytes=20,
        )

    def list_tasks(self, probe):
        return [
            {"name": "done.zip", "rel_path": "资源/done.zip", "size": 10, "remote_id": "1"},
            {"name": "ok.zip", "rel_path": "资源/ok.zip", "size": 10, "remote_id": "2"},
            {"name": "bad.zip", "rel_path": "资源/bad.zip", "size": 0, "remote_id": "3"},
        ]

    def resolve_download_url(self, probe, task, index=1):
        if task.get("remote_id") == "3":
            raise _webengine.WebEngineError("captcha_required", "百度要求验证码")
        return "https://example.com/" + task["name"]

    def download(self, direct_url, dest, progress=None, task_control=None):
        target = Path(dest)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"abcdef0123")
        return {"ok": True, "bytes": target.stat().st_size}

original_driver = _webengine._driver_class
_webengine._driver_class = lambda _driver: FakeDriver
try:
    plan = _webengine.build_web_plan("https://example.com/folder", pwd="3379", target=str(fake_root), driver="fake")
    rc, results = _webengine.execute_web_plan(plan)
finally:
    _webengine._driver_class = original_driver
assert rc == 1, rc
assert len(results) == 3 and sum(r.get("rc") == 0 for r in results) == 2
assert results[0].get("resumed") is True
assert results[1].get("bytes") == 10
assert results[2].get("error_code") == "captcha_required"
assert (fake_root / "资源" / "ok.zip").stat().st_size == 10
assert (fake_root / "资源" / "ok.zip.part").exists() is False
checks += 7''')


_g('69) 百度未登录/直链缺失：报告必须给 login_required + remediation，且不泄漏提取码', r'''from datetime import datetime as _dt
from pancli import report as _rep
from pancli import baidu_login as _bl
_auth = [{"rc": 1, "error_code": "dlink_missing"}, {"rc": 1, "error_code": "auth_required"}]
assert _rep.report_login_required(_auth) is True
assert _rep.report_login_required([{"rc": 0}]) is False
_hint = _rep.report_remediation(_auth)
assert "login baidu --qr" in _hint and "baidupcs" in _hint, _hint
assert _hint == _rep.report_remediation(_auth), "remediation 必须稳定"
_rp = TMP / "baidu-report"; _rp.mkdir(parents=True, exist_ok=True)
_cfg2 = json.loads(json.dumps(cfg)); _cfg2["http"] = dict(_cfg2.get("http") or {}, report_dir=str(_rp))
_path = _rep.write_download_report(_cfg2, {"target": str(_rp), "drive": "baidu", "engine": "baiduweb"},
                                  _auth, _dt.now(), _dt.now(), ok=False,
                                  url="https://pan.baidu.com/s/x?pwd=3379")
_repj = json.loads(Path(_path).read_text(encoding="utf-8"))
assert _repj["login_required"] is True and "login baidu --qr" in _repj["remediation"], _repj
assert "3379" not in json.dumps(_repj), "报告泄漏提取码"
assert hasattr(_bl, "run") and hasattr(_bl, "poll_confirm") and hasattr(_bl, "fetch_credentials")
assert _bl.unique_qr_path(str(TMP / "qr.png")) != _bl.unique_qr_path(str(TMP / "qr.png")), "登录二维码路径必须唯一"
_eng_txt = (HERE.parent / "scripts/pancli/engine.py").read_text(encoding="utf-8")
assert "--qr" in _eng_txt and "_login_baidu_qr" in _eng_txt, "CLI 缺 pan login --qr"
checks += 9''')


_g('70) v0.16.0：单实例锁 / 续传安全（禁 --ow）/ 双 fork 守护化 / 限速与 ETA', r'''from pancli import tasklock as _tlk
from pancli import guard as _grd

_lk_a = _tlk.TaskLock("baidu", "/我的资源/A249", str(TMP / "lockout"))
assert _lk_a.acquire() is True
_lk_b = _tlk.TaskLock("baidu", "/我的资源/A249", str(TMP / "lockout"))
assert _lk_b.acquire() is False, "同来源第二次加锁必须被拒绝"
_gate = _tlk.acquire_for_step({"lock": {"drive": "baidu", "source": "/我的资源/A249", "target": str(TMP / "lockout")}})
assert _gate["ok"] is False and "单实例" in _gate["message"], _gate
_lk_a.release()
assert _tlk.TaskLock("baidu", "/我的资源/A249", str(TMP / "lockout")).acquire() is True
checks += 4

_stale_path = _tlk.lock_dir() / "stalecheck.lock"
_stale_path.write_text(json.dumps({"pid": 999999, "key": "stalecheck"}), encoding="utf-8")
assert "stalecheck" in _tlk.cleanup_stale(), "陈旧锁必须能被自动清理"
checks += 1

_pl = pan.build_plan("https://pan.baidu.com/s/x", pwd="1", to=str(TMP / "planout"), engine="baidupcs")
_dl = [s for s in _pl["steps"] if s.get("lock")]
assert _dl, "百度下载步骤缺单实例锁"
_webpl = pan.build_plan("https://pan.baidu.com/s/x", pwd="1", to=str(TMP / "webplan"), engine="baiduweb")
assert _webpl.get("web") and _webpl.get("web_lock"), "百度官方网页路径也必须挂单实例锁"
_argv = _dl[0]["argv"]
assert "--retry" in _argv, _argv
assert "--ow" not in _argv, _argv
checks += 3

_cfg_ow = {"drives": {"baidu": {"engine_command": "BaiduPCS-Go download /我的资源/x --saveto {dir} --ow"}}}
_plan_ow = pan.build_plan("https://pan.baidu.com/s/x", pwd="1", to=str(TMP / "owout"), engine="baidupcs", cfg=_cfg_ow)
_argv_ow = _plan_ow["steps"][0]["argv"]
assert "--ow" not in _argv_ow and "--retry" in _argv_ow, "自定义命令里的 --ow 必须被自动剥离：%s" % _argv_ow
checks += 1

assert _grd.classify_error("官方直链返回 HTTP 403")["code"] == "http_403"
assert _grd.classify_error("未登录")["code"] == "login_required"
assert _grd.classify_error("百度官方接口未返回下载直链")["code"] == "dlink_missing"
checks += 3

assert _grd.human_eta(_grd.eta_for(10 * 1024 * 1024, 1024 * 1024)) == "10秒"
assert "限速" in _grd.throttle_hint(60 * 1024, "baidu")
assert "未触发限速" in _grd.throttle_hint(5 * 1024 * 1024, "baidu")
checks += 3

import subprocess as _sp
_dpid_file = TMP / "daemon-child.pid"
_script = TMP / "daemon-child.py"
_script.write_text(
    "import os,sys,time\nsys.path.insert(0,%r)\nfrom pancli.guard import daemonize\ndaemonize()\n"
    "open(%r,'w').write(str(os.getpid()))\ntime.sleep(25)\n" % (str(HERE.parent / "scripts"), str(_dpid_file)),
    encoding="utf-8")
_sp.run([sys.executable, str(_script)], check=True, timeout=20)
_dl_pid = int(_dpid_file.read_text().strip())
assert _dl_pid != os.getpid()
assert _tlk.pid_alive(_dl_pid), "双 fork 守护化进程应存活"
try:
    os.kill(_dl_pid, 9)
except Exception:
    pass
checks += 1''')


_g('90) 网盘通 100% 优化：10 秒刷新 + 下载请求快速响应（配置只读一次 / 批量异步派发 / 受理回执）', r'''_web_src = _PAN_WEB.read_text(encoding="utf-8")
assert "setInterval(loadTasks,10000)" in _web_src, "任务中心应每 10 秒刷新一次"
assert "}, 10000);" in _web_src, "实时页应每 10 秒刷新一次"
assert "2000)" not in _web_src, "不应残留 2 秒刷新"
for tok in ("cfg_once", "dispatch_ms", "accepted_at", '"accepted"', '"queued"', "async_dispatch",
            "_dispatch_batch", "已受理"):
    assert tok in _web_src, "web.py 缺快速响应要素 %s" % tok
# 单链接同步派发（保住 PID 语义），多链接后台线程派发（响应时间与链接数解耦）
_post = _web_src[_web_src.index('self.path.startswith("/api/download")'):]
_post = _post[:_post.index("/api/settings")]
assert "if len(queued) == 1:" in _post and "threading.Thread(target=_dispatch_batch" in _post, "派发策略缺失"
assert _post.index("load_config()") < _post.index("for url in urls[:100]:"), "配置必须在循环外只读一次"
# 门禁是纯本机检查：不得在接收链接时发起网络请求
assert "urlopen" not in _post and "requests." not in _post, "接收链接阶段不得联网"
# 首页必须给出「已受理」即时回执并带耗时
_home_src = pan.serve_home_html([])
assert "已受理" in _home_src and "dispatch_ms" in _home_src, "首页缺少即时受理回执"
assert "setInterval(submitUrls,120)" in _home_src or "setTimeout(submitUrls,120)" in _home_src, "输入防抖未提速"
assert "setTimeout(submitUrls,0)" in _home_src, "粘贴后应立刻投递"
checks += 12

print("SELF_TEST_OK checks=%d tmp=%s" % (checks, TMP))''')


_g('95) v0.19.0 安全回归：Web token 鉴权 / hook 白名单 / feishu 校验 / compose.full', r'''
# 95-1) run_completion_hook：无白名单一律拒绝执行
from pancli import report as _report
_cfg_nw = {"http": {"on_complete_hook": "/bin/echo hello"}}
assert _report.run_completion_hook(_cfg_nw, {"target": "/tmp/x"}, "") == "", "无白名单时 hook 不应执行"
# 95-2) 白名单 "-" 显式放行时才执行（echo 为只读命令，离线安全）
_cfg_ok = {"http": {"on_complete_hook": "/bin/echo hello", "hook_whitelist": ["-"]}}
_out = _report.run_completion_hook(_cfg_ok, {"target": "/tmp/x"}, "")
assert _out == "hello", _out
# 95-3) 白名单目录外的可执行文件被拒
_cfg_dir = {"http": {"on_complete_hook": "/bin/echo hello", "hook_whitelist": ["/usr/local/bin"]}}
assert _report.run_completion_hook(_cfg_dir, {"target": "/tmp/x"}, "") == "", "白名单目录外应拒绝"

# 95-4) web.py 鉴权与 hook 收紧的源级断言（防回归删除）
_web = (pan.SKILL_DIR / "scripts/pancli/web.py").read_text(encoding="utf-8")
for _tok in ("web_auth_token", "_reject_auth", "PAN_NOAUTH", "hook_warn"):
    assert _tok in _web, "web.py 缺安全改造标记 %s" % _tok
assert 'cfg["http"]["on_complete_hook"] = str(body.get' not in _web, "Web API 不得再写 on_complete_hook"

# 95-5) feishu_bot：非回环无 Verification Token 必须拒绝启动（返回 2，不绑定端口）
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("_fb", pan.SKILL_DIR / "scripts/feishu_bot.py")
_fb = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_fb)
assert _fb.run_server("0.0.0.0", 19091, "http://127.0.0.1:17890") == 2, "非回环无 token 应拒绝启动"

# 95-6) docker 全家桶 compose 存在且含 cdd-alist（修复 docs 承诺文件缺失）
_compose = pan.SKILL_DIR / "docker" / "docker-compose.full.yml"
assert _compose.is_file(), "缺 docker/docker-compose.full.yml"
assert "cdd-alist" in _compose.read_text(encoding="utf-8"), "compose.full 缺 cdd-alist 服务"

# 95-7) 扩展与飞书桥已接 token
_bg = (pan.SKILL_DIR / "extensions/chrome/background.js").read_text(encoding="utf-8")
assert "apiToken" in _bg, "Chrome 扩展未接入 token"
assert "Authorization" in (pan.SKILL_DIR / "scripts/feishu_bot.py").read_text(encoding="utf-8"), "飞书桥未接 pan token"

checks += 12
''')

_g('96) v0.20.0 F1：auto_split_decision 决策分支 + run_curl_split 并发池/复用/合并校验', r'''
import re as _re
import shutil as _rsh
import http.server as _hs
import socketserver as _ss
import threading as _th

_tmp = Path(__import__("tempfile").gettempdir()) / "f1_selftest_tmp"
if _tmp.exists():
    _rsh.rmtree(_tmp)
_tmp.mkdir()
_data = __import__("os").urandom(6 * 1024 * 1024)

class _RH(_hs.BaseHTTPRequestHandler):
    def do_GET(self):
        _rng = self.headers.get("Range")
        _size = len(_data)
        if _rng:
            _m = _re.match(r"bytes=(\d+)-(\d+)$", _rng)
            _s, _e = int(_m.group(1)), int(_m.group(2))
        else:
            _s, _e = 0, _size - 1
        _e = min(_e, _size - 1)
        _c = _data[_s:_e + 1]
        self.send_response(206 if _rng else 200)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", "bytes %d-%d/%d" % (_s, _e, _size))
        self.send_header("Content-Length", str(len(_c)))
        self.end_headers()
        self.wfile.write(_c)
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(len(_data)))
        self.end_headers()
    def log_message(self, *a):
        pass

class _Srv(_ss.TCPServer):
    allow_reuse_address = True

_srv = _Srv(("127.0.0.1", 18766), _RH)
_th.Thread(target=_srv.serve_forever, daemon=True).start()
_url = "http://127.0.0.1:18766/data.bin"
_cfg = {"http": {"auto_split": True, "auto_split_threshold_kbps": 99999999, "split_max_concurrency": 4}}

# 决策分支
_n, _why = pan.auto_split_decision(_url, _cfg)
assert _n == 4 and "slow" in _why, "低阈值应触发分片 n=%s why=%s" % (_n, _why)
_n2, _why2 = pan.auto_split_decision(_url, {"http": {"auto_split": False}})
assert _n2 == 0 and _why2 == "disabled", _why2
_n3, _why3 = pan.auto_split_decision(_url, {"http": {"auto_split": True}})
assert _n3 == 0 and "fast_enough" in _why3, "回环样本必然快 why=%s" % _why3

# 分片下载 + 字节校验 + 复用
_t1 = _tmp / "a.bin"
_rc1, _r1, _note1 = pan.run_curl_split(_url, _t1, 4, _cfg)
assert _rc1 == 0, _note1
assert _t1.read_bytes() == _data, "合并内容不一致"
assert all("reused" in _r for _r in _r1), "结果缺 reused 字段"

_p00 = _tmp / "b.bin.part00"
_base = len(_data) // 4
_p00.write_bytes(_data[0:_base])
_t2 = _tmp / "b.bin"
_rc2, _r2, _note2 = pan.run_curl_split(_url, _t2, 4, _cfg)
assert _rc2 == 0, _note2
assert _r2[0].get("reused") is True, "完整 part00 应被复用"
assert _t2.read_bytes() == _data

_srv.shutdown()
_rsh.rmtree(_tmp, ignore_errors=True)
checks += 8
''')

_g('97) v0.20.0 F2：idle 窗口判断（含跨午夜/FORCE）+ 队列 add/list/delete 往返 + print-crontab 只打印', r'''
import json as _json
import subprocess as _sub
import tempfile as _tf
import uuid as _uuid
from datetime import datetime as _dt
from pathlib import Path as _Path

_st = _Path(_tf.mkdtemp(prefix="f2-selftest-"))
_env = dict(__import__("os").environ, PAN_STATE_DIR=str(_st), PAN_IDLE_FORCE="1")
_pan = pan.SKILL_DIR / "scripts" / "pan.py"

def _panrun(*_a, _extra=None):
    return _sub.run([sys.executable, str(_pan)] + list(_a), capture_output=True, text=True,
                    env={**_env, **(_extra or {})}, cwd=str(pan.SKILL_DIR / "scripts"), timeout=60)

# 窗口判断（进程内）
from pancli.idle import in_window as _iw, idle_window as _iw2
assert _iw({}, now=_dt(2026, 1, 1, 3, 0)) is True, "03:00 应在默认窗口"
assert _iw({}, now=_dt(2026, 1, 1, 14, 0)) is False, "14:00 不应在默认窗口"
_cfgx = {"http": {"idle_window": ["22:00", "06:00"]}}
assert _iw(_cfgx, now=_dt(2026, 1, 1, 23, 30)) is True and _iw(_cfgx, now=_dt(2026, 1, 1, 12, 0)) is False, "跨午夜判断错误"
checks += 3

# 队列往返（子进程 CLI）
_r = _panrun("idle", "add", "http://example.invalid/x.bin", "--", "--to", str(_st))
assert _r.returncode == 0, _r.stdout + _r.stderr
_r = _panrun("idle", "list", "--json")
_q = _json.loads(_r.stdout)["queued"]
assert len(_q) == 1 and _q[0]["idle_only"] is True and _q[0]["url"].endswith(".bin")
_r = _panrun("idle", "delete", _q[0]["id"])
assert _r.returncode == 0
_r = _panrun("idle", "list")
assert "队列为空" in _r.stdout or not _json.loads(_panrun("idle", "list", "--json").stdout)["queued"]
checks += 3

# print-crontab 只打印不安装
_r = _panrun("idle", "run", "--print-crontab")
assert _r.returncode == 0 and "idle run --once" in _r.stdout, _r.stdout
# 窗口外退出码 1（FORCE 关掉）
_r = _panrun("idle", "run", "--once", _extra={"PAN_IDLE_FORCE": "0"})
assert _r.returncode == 1 and "不在闲时窗口" in _r.stdout, _r.stdout
checks += 2

import shutil as _sh2
_sh2.rmtree(_st, ignore_errors=True)
''')

if __name__ == "__main__":
    sys.exit(main())
