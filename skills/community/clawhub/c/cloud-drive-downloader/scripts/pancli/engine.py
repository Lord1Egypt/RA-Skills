#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pan-downloader v0.6 — 多网盘统一下载入口（本机 + Windows + 远程设备）。

Ponytail full 设计原则：
- 不自己实现各家网盘协议；协议差异交给各网盘已有 CLI / AList / aria2。
- 核心只做四件事：识别链接、管理配置与目录、拼装引擎命令、执行并记录日志。
- 直链 HTTP 下载用系统 curl，开箱即用；分享链接走引擎适配器，未安装引擎时给出安装指引。

免费账号默认：并发 1、重试 3、断点续传、单任务日志。
会员账号可选：在配置里把 tier 设为 vip，引擎按自身能力提高并发，但本工具不做任何限速绕过。

远程设备不绑定品牌：只要目标开放 SSH/SFTP、WebDAV、SMB、S3 或 rclone，即可登记为 remote。
远程执行模式让 NAS 自己跑下载；远程落地模式在本机下载后通过 rclone 写入目标存储。
"""
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


import argparse

import i18n
import copy
import hashlib
import getpass
import json
import os
import platform
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse
import urllib.request

try:
    from http_downloader import HTTPDownloader
    from http_downloader.compliance import COMPLIANCE_NOTICE
    GENERIC_DIRECT_OK = True
except Exception:  # pragma: no cover - 缺少该模块时 pan direct 不可用，其余功能不受影响
    GENERIC_DIRECT_OK = False
    COMPLIANCE_NOTICE = None

APP = "pan-downloader"
VALID_TIERS = ("free", "vip", "auto")
KEYCHAIN_SERVICE = "com.lis.pan-downloader"
SECURITY_BIN = os.environ.get("PAN_SECURITY_BIN", "/usr/bin/security")
SKILL_DIR = Path(__file__).resolve().parent.parent.parent


def platform_paths(system=None, env=None, home=None):
    """返回跨平台配置、状态、日志和默认下载目录。"""
    env = dict(os.environ if env is None else env)
    home = Path(home or env.get("HOME") or Path.home())
    system = (system or env.get("PAN_PLATFORM") or platform.system()).lower()
    if system.startswith("win"):
        appdata = Path(env.get("APPDATA") or (home / "AppData" / "Roaming"))
        local = Path(env.get("LOCALAPPDATA") or (home / "AppData" / "Local"))
        return {
            "config": appdata / APP / "config.json",
            "state": local / APP / "state",
            "log": local / APP / "logs" / (APP + ".log"),
            "download": home / "Downloads" / "网盘下载",
        }
    if system == "darwin":
        return {
            "config": home / ".config" / APP / "config.json",
            "state": home / ".local" / "share" / APP,
            "log": home / "Library" / "Logs" / (APP + ".log"),
            "download": home / "Downloads" / "网盘下载",
        }
    xdg_config = Path(env.get("XDG_CONFIG_HOME") or (home / ".config"))
    xdg_state = Path(env.get("XDG_STATE_HOME") or (home / ".local" / "state"))
    return {
        "config": xdg_config / APP / "config.json",
        "state": xdg_state / APP,
        "log": xdg_state / APP / "logs" / (APP + ".log"),
        "download": home / "Downloads" / "网盘下载",
    }


PATHS = platform_paths()
CONFIG_PATH = Path(os.environ.get("PAN_CONFIG", str(PATHS["config"])))
STATE_DIR = Path(os.environ.get("PAN_STATE_DIR", str(PATHS["state"])))
LOG_PATH = Path(os.environ.get("PAN_LOG", str(PATHS["log"])))
CREDENTIAL_REF_PREFIX = "credential:"

# ---------------------------------------------------------------- 网盘定义
DRIVES = {
    "baidu": {
        "name": "百度网盘",
        "domains": [
            "pan.baidu.com",
            "yun.baidu.com"
        ],
        "engine": "baiduweb",
        "reference": "references/01-百度网盘.md"
    },
    "aliyun": {
        "name": "阿里云盘",
        "domains": [
            "aliyundrive.com",
            "alipan.com",
            "www.aliyundrive.com"
        ],
        "engine": "alist",
        "reference": "references/02-阿里云盘.md"
    },
    "quark": {
        "name": "夸克网盘",
        "domains": [
            "pan.quark.cn"
        ],
        "engine": "quarkcli",
        "reference": "references/03-夸克网盘.md"
    },
    "tianyi": {
        "name": "天翼云盘",
        "domains": [
            "cloud.189.cn"
        ],
        "engine": "alist",
        "reference": "references/04-天翼云盘.md"
    },
    "thunder": {
        "name": "迅雷云盘",
        "domains": [
            "pan.xunlei.com"
        ],
        "engine": "alist",
        "reference": "references/05-迅雷云盘.md"
    },
    "115": {
        "name": "115 网盘",
        "domains": [
            "115.com",
            "anxia.com",
            "115cdn.com",
            "115.com.cn"
        ],
        "engine": "alist",
        "reference": "references/07-115网盘.md"
    },
    "123pan": {
        "name": "123 云盘",
        "domains": [
            "123pan.com",
            "123684.com",
            "123912.com",
            "123865.com"
        ],
        "engine": "alist",
        "reference": "references/08-123云盘.md"
    },
    "139yun": {
        "name": "移动云盘 / 和彩云",
        "domains": [
            "yun.139.com",
            "cloud.139.com",
            "caiyun.139.com"
        ],
        "engine": "alist",
        "reference": "references/09-移动云盘.md"
    },
    "wopan": {
        "name": "联通沃盘",
        "domains": [
            "wopan.wo.cn",
            "pan.wo.cn"
        ],
        "engine": "alist",
        "reference": "references/10-联通沃盘.md"
    },
    "uc": {
        "name": "UC 网盘",
        "domains": [
            "drive.uc.cn",
            "pan.uc.cn",
            "fast.uc.cn"
        ],
        "engine": "alist",
        "reference": "references/11-UC网盘.md"
    },
    "pikpak": {
        "name": "PikPak",
        "domains": [
            "mypikpak.com",
            "pikpak.com"
        ],
        "engine": "alist",
        "reference": "references/12-PikPak.md"
    },
    "jianguoyun": {
        "name": "坚果云",
        "domains": [
            "jianguoyun.com",
            "dav.jianguoyun.com"
        ],
        "engine": "webdav",
        "reference": "references/13-坚果云.md"
    },
    "onedrive": {
        "name": "OneDrive / SharePoint",
        "domains": [
            "onedrive.live.com",
            "1drv.ms",
            "sharepoint.com",
            "sharepoint.cn",
            "onedrive.com"
        ],
        "engine": "alist",
        "reference": "references/14-OneDrive与SharePoint.md"
    },
    "googledrive": {
        "name": "Google Drive",
        "domains": [
            "drive.google.com",
            "docs.google.com",
            "photos.google.com"
        ],
        "engine": "alist",
        "reference": "references/15-GoogleDrive.md"
    },
    "dropbox": {
        "name": "Dropbox",
        "domains": [
            "dropbox.com",
            "db.tt"
        ],
        "engine": "alist",
        "reference": "references/16-Dropbox.md"
    },
    "weiyun": {
        "name": "腾讯微云",
        "domains": [
            "weiyun.com"
        ],
        "engine": "alist",
        "reference": "references/17-腾讯微云.md"
    },
    "lanzou": {
        "name": "蓝奏云 / 新蓝奏",
        "domains": [
            "lanzou.com",
            "lanzoui.com",
            "lanzoux.com",
            "lanzouw.com",
            "lanzoup.com",
            "lanzoub.com",
            "lanzoue.com",
            "lanzous.com",
            "lanzoa.com",
            "lanzn.com",
            "ilanzou.com"
        ],
        "engine": "alist",
        "reference": "references/18-蓝奏云.md"
    },
    "wukong": {
        "name": "悟空网盘",
        "domains": [
            "wukong.com",
            "pan.wukong.com"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "doubao": {
        "name": "豆包新盘",
        "domains": [
            "doubao.com",
            "pan.doubao.com",
            "www.doubao.com"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "mega": {
        "name": "Mega",
        "domains": [
            "mega.nz",
            "mega.io"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "terabox": {
        "name": "TeraBox",
        "domains": [
            "terabox.com",
            "1024terabox.com",
            "teraboxapp.com"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "pcloud": {
        "name": "pCloud",
        "domains": [
            "pcloud.com",
            "pcloud.link"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "protondrive": {
        "name": "Proton Drive",
        "domains": [
            "drive.proton.me",
            "proton.me"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "yandexdisk": {
        "name": "Yandex Disk",
        "domains": [
            "disk.yandex.com",
            "disk.yandex.ru",
            "yadi.sk"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "mediafire": {
        "name": "MediaFire",
        "domains": [
            "mediafire.com"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "trainbit": {
        "name": "Trainbit",
        "domains": [
            "trainbit.com"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "guangyapan": {
        "name": "光雅盘",
        "domains": [
            "guangyapan.com"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "feijipan": {
        "name": "飞鸡云",
        "domains": [
            "feijipan.com"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "shandian": {
        "name": "闪电盘",
        "domains": [
            "shandianpan.com"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "chengtong": {
        "name": "城通网盘",
        "domains": [
            "ctfile.com",
            "400gb.com"
        ],
        "engine": "custom",
        "reference": "references/19-其他网盘.md"
    },
    "stream": {
        "name": "网页视频 / HLS 流媒体",
        "domains": [
            "youtube.com",
            "youtu.be",
            "bilibili.com",
            "b23.tv",
            "ixigua.com",
            "douyin.com",
            "vimeo.com",
            "twitter.com",
            "x.com",
            "twitch.tv"
        ],
        "engine": "ytdlp",
        "reference": "references/00-使用说明.md"
    },
    "bittorrent": {
        "name": "磁力链接 / BitTorrent",
        "domains": [],
        "engine": "aria2",
        "reference": "references/00-使用说明.md"
    },
    "direct": {
        "name": "HTTP 直链",
        "domains": [],
        "engine": "http",
        "reference": "references/00-使用说明.md"
    }
}
ENGINE_BINARIES = {
    "alist": ["alist", "AList"],
    "baidupcs": ["BaiduPCS-Go", "baidupcs-go", "BaiduPCS"],
    "quarkcli": ["quark", "quark-cli", "kuake"],
    "aria2": ["aria2c"],
    "rclone": ["rclone"],
    "ssh": ["ssh"],
    "scp": ["scp"],
    "tar": ["tar"],
    "ytdlp": ["yt-dlp"],
    "stream": ["yt-dlp"],
}
DEFAULT_CONFIG = {
    "version": 5,
    "download_root": "",
    "tier": "auto",
    "smart": {
        "auto_classify": False,
        "classify_root": ""
    },
    "http": {
        "retries": 3,
        "retry_delay": 5,
        "connect_timeout": 30,
        "timeout": 0,
        "max_connections_free": 1,
        "max_connections_vip": 4,
        "report_dir": "",
        "on_complete_hook": "",
        "range_split": False,
        "range_split_connections": 0,
        "live_status": False,
        "live_interval": 1.0,
        "live_dir": "",
        "auto_web": True,
        "schedule_at": ""
    },
    "ytdlp": {
        "format": "bv*+ba/b",
        "concurrent_fragments": 4,
        "cookies_from_browser": "",
        "max_filesize": 0
    },
    "bt": {
        "trackers": "",
        "seed_time": 0,
        "enable_dht": True,
        "dht_listen_port": "6881-6999",
        "bt_max_peers": "64",
        "connections_free": 4,
        "connections_vip": 16
    },
    "remote": {
        "staging_root": "",
        "keep_staging": False
    },
    "transfer": {
        "allow_company_dest": False,
        "default_transfers": 4,
        "default_checkers": 8
    },
    "notify": {
        "work_weixin_secret": "",
        "bark_secret": "",
        "telegram_secret": "",
        "discord_secret": "",
        "feishu_secret": ""
    },
    "remotes": {},
    "engines": {
        "alist": "",
        "baidupcs": "",
        "quarkcli": "",
        "aria2c": "",
        "yt-dlp": "",
        "rclone": "",
        "alist_url": "",
        "alist_user": "",
        "alist_password_ref": "",
        "rclone_remote": "",
        "webdav_url": "",
        "webdav_user": "",
        "webdav_password_ref": ""
    },
    "drives": {
        "baidu": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": "",
            "save_path": "/网盘下载"
        },
        "aliyun": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "quark": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "tianyi": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "thunder": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "115": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "123pan": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "139yun": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "wopan": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "uc": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "pikpak": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "jianguoyun": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "onedrive": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "googledrive": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "dropbox": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "weiyun": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "lanzou": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "wukong": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "doubao": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "mega": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "terabox": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "pcloud": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "protondrive": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "yandexdisk": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "mediafire": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "trainbit": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "guangyapan": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "feijipan": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "shandian": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "chengtong": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "stream": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "bittorrent": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "direct": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        }
    },
    "extensions": {}
}
SECRET_RE = re.compile(r"(cookie|token|password|passwd|secret|bduss|credential|authorization|auth|pass)", re.I)
KEYCHAIN_REF_PREFIX = "keychain:"


# ---------------------------------------------------------------- 基础工具
def deep_merge(base, over):
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


_CONFIG_CACHE = {"key": None, "cfg": {}}
_ROUTE_CACHE = {}
_ROUTE_CACHE_TTL = 2.0


def _config_stat_key(path):
    try:
        st = path.stat()
        return (str(path), st.st_mtime_ns, st.st_size, st.st_ino)
    except OSError:
        return (str(path), -1, -1, -1)


def load_config(path=None):
    """读取配置；按 mtime/size/inode 缓存，避免高频路由重复读盘。"""
    path = Path(path or CONFIG_PATH)
    key = _config_stat_key(path)
    if not path.exists():
        return copy.deepcopy(DEFAULT_CONFIG)
    if _CONFIG_CACHE["key"] == key:
        return copy.deepcopy(_CONFIG_CACHE["cfg"])
    try:
        user = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return copy.deepcopy(DEFAULT_CONFIG)
    cfg = deep_merge(DEFAULT_CONFIG, user)
    _CONFIG_CACHE.update(key=key, cfg=cfg)
    return copy.deepcopy(cfg)


def save_config(cfg, path=None):
    path = Path(path or CONFIG_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        os.chmod(path, 0o600)  # 凭据文件只允许本人读写
    except OSError:
        pass
    _CONFIG_CACHE.update(key=_config_stat_key(path), cfg=deep_merge(DEFAULT_CONFIG, cfg))
    return path


def mask_value(key, value):
    if isinstance(value, dict):
        return {k: mask_value(k, v) for k, v in value.items()}
    if isinstance(value, list):
        return [mask_value(key, v) for v in value]
    if SECRET_RE.search(str(key)) and value:
        return "***"
    return value


def _valid_secret_name(name):
    name = str(name or "").strip()
    if not re.fullmatch(r"[A-Za-z0-9._@-]{1,80}", name):
        raise ValueError("凭据名只允许字母、数字、点、下划线、@ 和连字符")
    return name


def credential_ref(name):
    return CREDENTIAL_REF_PREFIX + _valid_secret_name(name)


def normalize_secret_ref(value):
    text = str(value or "").strip()
    if is_secret_ref(text):
        return text
    return credential_ref(text)


def keychain_ref(name):
    """兼容旧调用；新配置统一推荐 credential: 引用。"""
    return credential_ref(name)


def is_secret_ref(value):
    return isinstance(value, str) and value.startswith((CREDENTIAL_REF_PREFIX, KEYCHAIN_REF_PREFIX))


def secret_ref_name(ref):
    if not is_secret_ref(ref):
        return ""
    for prefix in (CREDENTIAL_REF_PREFIX, KEYCHAIN_REF_PREFIX):
        if ref.startswith(prefix):
            return ref[len(prefix):].strip()
    return ""


def is_keychain_ref(value):
    return is_secret_ref(value)


def keychain_name(ref):
    return secret_ref_name(ref)


def credential_backend(system=None):
    system = (system or platform.system()).lower()
    if system.startswith("win"):
        return "windows"
    if system == "darwin":
        return "macos"
    if shutil.which("secret-tool"):
        return "secret-tool"
    return "unsupported"


def credential_available(system=None):
    backend = credential_backend(system)
    if backend == "macos":
        return bool(SECURITY_BIN and Path(SECURITY_BIN).exists())
    return backend in ("windows", "secret-tool")


def keychain_available():
    """兼容旧函数名；返回当前平台的系统凭据库是否可用。"""
    return credential_available()


def _secret_name(name):
    return re.sub(r"[^A-Za-z0-9._@-]+", "_", str(name or "").strip())


def _macos_keychain_store(name, value):
    if not (SECURITY_BIN and Path(SECURITY_BIN).exists()):
        raise RuntimeError("macOS security 命令不可用，拒绝保存明文；请在正常终端执行")
    proc = subprocess.run(
        [SECURITY_BIN, "add-generic-password", "-U", "-a", name, "-s", KEYCHAIN_SERVICE, "-w"],
        input=value + "\n" + value + "\n", text=True, capture_output=True,
    )
    if proc.returncode != 0:
        msg = (proc.stderr or proc.stdout or "钥匙串写入失败").strip().splitlines()
        raise RuntimeError(msg[-1] if msg else "钥匙串写入失败")


def _macos_keychain_get(name):
    if not (SECURITY_BIN and Path(SECURITY_BIN).exists()):
        return ""
    proc = subprocess.run(
        [SECURITY_BIN, "find-generic-password", "-a", name, "-s", KEYCHAIN_SERVICE, "-w"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        return ""
    return proc.stdout.rstrip("\r\n")


def _macos_keychain_delete(name):
    if not (SECURITY_BIN and Path(SECURITY_BIN).exists()):
        return False
    proc = subprocess.run(
        [SECURITY_BIN, "delete-generic-password", "-a", name, "-s", KEYCHAIN_SERVICE],
        capture_output=True, text=True,
    )
    return proc.returncode == 0


def _windows_target(name):
    return "%s:%s" % (APP, name)


def _windows_credential_store(name, value):
    """Windows Credential Manager 写入；密码不经过 argv / stdin。"""
    import ctypes
    from ctypes import wintypes

    class FILETIME(ctypes.Structure):
        _fields_ = [("dwLowDateTime", wintypes.DWORD), ("dwHighDateTime", wintypes.DWORD)]

    class CREDENTIAL_ATTRIBUTE(ctypes.Structure):
        _fields_ = [
            ("Keyword", wintypes.LPWSTR),
            ("Flags", wintypes.DWORD),
            ("ValueSize", wintypes.DWORD),
            ("Value", ctypes.POINTER(ctypes.c_ubyte)),
        ]

    class CREDENTIAL(ctypes.Structure):
        _fields_ = [
            ("Flags", wintypes.DWORD),
            ("Type", wintypes.DWORD),
            ("TargetName", wintypes.LPWSTR),
            ("Comment", wintypes.LPWSTR),
            ("LastWritten", FILETIME),
            ("CredentialBlobSize", wintypes.DWORD),
            ("CredentialBlob", ctypes.POINTER(ctypes.c_ubyte)),
            ("Persist", wintypes.DWORD),
            ("AttributeCount", wintypes.DWORD),
            ("Attributes", ctypes.POINTER(CREDENTIAL_ATTRIBUTE)),
            ("TargetAlias", wintypes.LPWSTR),
            ("UserName", wintypes.LPWSTR),
        ]

    blob = value.encode("utf-16-le")
    buffer = ctypes.create_string_buffer(blob, len(blob))
    cred = CREDENTIAL()
    cred.Type = 1  # CRED_TYPE_GENERIC
    cred.TargetName = _windows_target(name)
    cred.UserName = name
    cred.CredentialBlobSize = len(blob)
    cred.CredentialBlob = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_ubyte))
    cred.Persist = 2  # CRED_PERSIST_LOCAL_MACHINE
    if not ctypes.windll.advapi32.CredWriteW(ctypes.byref(cred), 0):
        raise RuntimeError("Windows 凭据管理器写入失败（错误码 %s）" % ctypes.get_last_error())


def _windows_credential_get(name):
    import ctypes
    from ctypes import wintypes

    class FILETIME(ctypes.Structure):
        _fields_ = [("dwLowDateTime", wintypes.DWORD), ("dwHighDateTime", wintypes.DWORD)]

    class CREDENTIAL_ATTRIBUTE(ctypes.Structure):
        _fields_ = [
            ("Keyword", wintypes.LPWSTR),
            ("Flags", wintypes.DWORD),
            ("ValueSize", wintypes.DWORD),
            ("Value", ctypes.POINTER(ctypes.c_ubyte)),
        ]

    class CREDENTIAL(ctypes.Structure):
        _fields_ = [
            ("Flags", wintypes.DWORD),
            ("Type", wintypes.DWORD),
            ("TargetName", wintypes.LPWSTR),
            ("Comment", wintypes.LPWSTR),
            ("LastWritten", FILETIME),
            ("CredentialBlobSize", wintypes.DWORD),
            ("CredentialBlob", ctypes.POINTER(ctypes.c_ubyte)),
            ("Persist", wintypes.DWORD),
            ("AttributeCount", wintypes.DWORD),
            ("Attributes", ctypes.POINTER(CREDENTIAL_ATTRIBUTE)),
            ("TargetAlias", wintypes.LPWSTR),
            ("UserName", wintypes.LPWSTR),
        ]

    ptr = ctypes.POINTER(CREDENTIAL)()
    if not ctypes.windll.advapi32.CredReadW(_windows_target(name), 1, 0, ctypes.byref(ptr)):
        return ""
    try:
        cred = ptr.contents
        raw = ctypes.string_at(cred.CredentialBlob, cred.CredentialBlobSize)
        return raw.decode("utf-16-le").rstrip("\x00")
    finally:
        ctypes.windll.advapi32.CredFree(ptr)


def _windows_credential_delete(name):
    import ctypes

    return bool(ctypes.windll.advapi32.CredDeleteW(_windows_target(name), 1, 0))


def _secret_tool_store(name, value):
    proc = subprocess.run(
        ["secret-tool", "store", "--label", APP + " " + name, "service", APP, "account", name],
        input=value, text=True, capture_output=True,
    )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or "secret-tool 写入失败").strip())


def _secret_tool_get(name):
    proc = subprocess.run(
        ["secret-tool", "lookup", "service", APP, "account", name],
        capture_output=True, text=True,
    )
    return proc.stdout.rstrip("\r\n") if proc.returncode == 0 else ""


def _secret_tool_delete(name):
    proc = subprocess.run(
        ["secret-tool", "clear", "service", APP, "account", name],
        capture_output=True, text=True,
    )
    return proc.returncode == 0


def credential_store(name, value):
    """把密码写入当前平台的系统凭据库；不把明文写入 config。"""
    name = _secret_name(name)
    if not name:
        raise ValueError("凭据名为空")
    if not value:
        raise ValueError("凭据为空")
    backend = credential_backend()
    if backend == "macos":
        _macos_keychain_store(name, value)
    elif backend == "windows":
        _windows_credential_store(name, value)
    elif backend == "secret-tool":
        _secret_tool_store(name, value)
    else:
        raise RuntimeError("当前系统没有可用的系统凭据库；拒绝把密码保存为明文")
    return credential_ref(name)


def keychain_store(name, value):
    """兼容旧函数名；实际写入当前平台的系统凭据库。"""
    return credential_store(name, value)


def credential_get(name):
    name = secret_ref_name(name) or _secret_name(name)
    if not name:
        return ""
    backend = credential_backend()
    if backend == "macos":
        return _macos_keychain_get(name)
    if backend == "windows":
        return _windows_credential_get(name)
    if backend == "secret-tool":
        return _secret_tool_get(name)
    return ""


def keychain_get(name):
    """兼容旧函数名。"""
    return credential_get(name)


def credential_delete(name):
    name = secret_ref_name(name) or _secret_name(name)
    if not name:
        return False
    backend = credential_backend()
    if backend == "macos":
        return _macos_keychain_delete(name)
    if backend == "windows":
        return _windows_credential_delete(name)
    if backend == "secret-tool":
        return _secret_tool_delete(name)
    return False


def keychain_delete(name):
    """兼容旧函数名。"""
    return credential_delete(name)


def resolve_secret(value):
    """解析 credential:/keychain: 引用；兼容旧配置里的明文值但不主动展示。"""
    if not value:
        return ""
    if is_secret_ref(value):
        # 通过兼容入口读取，便于旧测试/旧调用方替换 keychain_get。
        return keychain_get(secret_ref_name(value))
    return str(value)


def resolve_engine_secret(cfg, ref_key, legacy_key=""):
    eng = cfg.get("engines") or {}
    return resolve_secret(eng.get(ref_key) or eng.get(legacy_key) or "")


def configured_secret_refs(cfg):
    refs = {}
    eng = cfg.get("engines") or {}
    for key, label in (("alist_password_ref", "engine.alist"), ("webdav_password_ref", "engine.webdav")):
        ref = str(eng.get(key) or "")
        if ref:
            refs[label] = ref
    for drive, entry in (cfg.get("drives") or {}).items():
        ref = str((entry or {}).get("credential_ref") or "")
        if ref:
            refs["drive." + drive] = ref
    for remote, entry in (cfg.get("remotes") or {}).items():
        ref = str((entry or {}).get("credential_ref") or "")
        if ref:
            refs["remote." + remote] = ref
    return refs


def migrate_plaintext_secrets(cfg):
    """迁移已知明文凭据到系统凭据库，返回 (migrated, errors)。"""
    migrated, errors = [], []
    eng = cfg.setdefault("engines", {})
    for plain_key, ref_key, secret_name in (
        ("alist_password", "alist_password_ref", "engine.alist"),
        ("webdav_password", "webdav_password_ref", "engine.webdav"),
    ):
        value = str(eng.get(plain_key) or "")
        if not value:
            continue
        try:
            eng[ref_key] = keychain_store(secret_name, value)
            eng.pop(plain_key, None)
            migrated.append(secret_name)
        except (OSError, ValueError, RuntimeError) as exc:
            errors.append("%s: %s" % (secret_name, exc))
    for drive, entry in (cfg.get("drives") or {}).items():
        if not isinstance(entry, dict) or entry.get("credential_ref"):
            continue
        for plain_key in ("password", "passwd", "token", "cookie", "credential", "bduss"):
            value = str(entry.get(plain_key) or "")
            if not value:
                continue
            secret_name = "drive." + drive
            try:
                entry["credential_ref"] = keychain_store(secret_name, value)
                entry.pop(plain_key, None)
                migrated.append(secret_name)
            except (OSError, ValueError, RuntimeError) as exc:
                errors.append("%s: %s" % (secret_name, exc))
            break
    for remote, entry in (cfg.get("remotes") or {}).items():
        if not isinstance(entry, dict) or entry.get("credential_ref"):
            continue
        for plain_key in ("password", "passwd", "token", "secret", "credential"):
            value = str(entry.get(plain_key) or "")
            if not value:
                continue
            secret_name = "remote." + remote
            try:
                entry["credential_ref"] = keychain_store(secret_name, value)
                entry.pop(plain_key, None)
                migrated.append(secret_name)
            except (OSError, ValueError, RuntimeError) as exc:
                errors.append("%s: %s" % (secret_name, exc))
            break
    return migrated, errors


def all_drives(cfg):
    drives = dict(DRIVES)
    for name, spec in (cfg.get("extensions") or {}).items():
        drives[name] = {
            "name": spec.get("name", name),
            "domains": spec.get("domains", []),
            "engine": spec.get("engine", "custom"),
            "reference": spec.get("reference", "references/06-扩展新网盘.md"),
        }
    return drives


def is_stream_url(url):
    """网页视频 / HLS / DASH：m3u8 或 mpd 或已知视频站点可直接走 yt-dlp。"""
    low = str(url or "").lower()
    if low.startswith("http://") or low.startswith("https://"):
        path = urlparse(low).path.lower()
        if path.endswith((".m3u8", ".mpd", ".m3u")):
            return True
    return low.startswith(("http://", "https://"))




def is_magnet_url(url):
    return str(url or "").lower().startswith("magnet:")


def is_torrent_path(url):
    """url 或本机路径以 .torrent 结尾（去查询串后判断）。"""
    try:
        tail = (urlparse(str(url or "")).path or str(url or "")).lower()
    except (TypeError, ValueError):
        tail = str(url or "").lower()
    return tail.endswith(".torrent")


def is_ftp_url(url):
    return str(url or "").lower().startswith(("ftp://", "ftps://"))


def detect_drive(url, cfg=None):
    """返回 (drive_key, spec)；http(s)/ftp(s) 回退 direct，磁力/BT 回退 bittorrent，视频站点走 stream(yt-dlp)。"""
    cfg = cfg or load_config()
    if is_magnet_url(url) or is_torrent_path(url):
        return "bittorrent", all_drives(cfg)["bittorrent"]
    host = (urlparse(url).hostname or "").lower()
    if host:
        for key, spec in all_drives(cfg).items():
            for domain in spec.get("domains", []):
                d = domain.lower()
                if host == d or host.endswith("." + d):
                    return key, spec
    if is_stream_url(url):
        # 视频主机优先走 stream；纯直链（非视频主机且非流媒体后缀）仍回退 direct
        if host and host not in ("", "example.com"):
            for domain in all_drives(cfg)["stream"].get("domains", []):
                if host == domain.lower() or host.endswith("." + domain.lower()):
                    return "stream", all_drives(cfg)["stream"]
        if url.lower().endswith((".m3u8", ".mpd", ".m3u")):
            return "stream", all_drives(cfg)["stream"]
    if url.lower().startswith(("http://", "https://", "ftp://", "ftps://")):
        return "direct", all_drives(cfg)["direct"]
    return "", {}


AUTH_HINTS = {
    "baidu": ("官方网页会话", "百度分享默认走官方网页零客户端会话；不读取浏览器 Cookie，也不需要粘贴 BDUSS/STOKEN。"),
    "aliyun": ("官方 OAuth / AList 授权", "先在 AList 添加阿里云盘并完成官方授权；refresh_token 不进聊天。"),
    "quark": ("quark-cli / AList 登录", "先完成夸克官方登录/授权；Cookie 只写工具配置或系统凭据库。"),
    "weiyun": ("OAuth / AList 授权", "先完成微云官方登录/授权，再转存到可访问路径。"),
    "lanzou": ("AList 授权 / 公开链接", "必要时先在 AList 授权；公开直链可不登录。"),
}
AUTH_HINT_DEFAULT = ("官方 OAuth / AList / 官方 CLI", "先完成官方登录或 AList 授权；凭据不进聊天。")


def _baidupcs_login_state(cfg=None):
    """只读检查 BaiduPCS-Go 本机登录态；不读取/输出凭据。"""
    cfg = cfg or load_config()
    if (cfg.get("drives") or {}).get("baidu", {}).get("credential_ref"):
        return True
    home = Path.home()
    candidates = [
        home / ".config" / "BaiduPCS-Go" / "pcs_config.json",
        home / "Library" / "Application Support" / "BaiduPCS-Go" / "pcs_config.json",
        home / "BaiduPCS-Go" / "pcs_config.json",
    ]
    # 本机 BaiduPCS-Go 默认把配置放在可执行文件同目录；登录态检查必须覆盖它。
    binary = find_engine_binary("baidupcs", cfg)
    if binary:
        candidates.insert(0, Path(binary).resolve().parent / "pcs_config.json")
    for path in candidates:
        try:
            if not path.is_file():
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("active_user"):
                return True
        except (OSError, ValueError):
            continue
    return False


def login_gate_for_url(url, cfg=None):
    """识别到网盘链接后立即返回登录/授权提示；不做网络请求、不读取凭据明文。"""
    cfg = cfg or load_config()
    key, spec = detect_drive(url, cfg)
    if not key or key in ("direct", "stream", "bittorrent"):
        return {"required": False, "blocking": False, "status": "not_required"}
    drive_cfg = (cfg.get("drives") or {}).get(key, {})
    engine = spec.get("engine", "")
    mode, message = AUTH_HINTS.get(key, AUTH_HINT_DEFAULT)
    if key == "baidu":
        # 默认走官方网页匿名会话；只有显式选择 baidupcs 时才检查本机登录态。
        if engine in ("baiduweb", "baidu_web", "web", "browser"):
            return {
                "required": False,
                "blocking": False,
                "status": "web_session",
                "drive": key,
                "drive_name": spec.get("name", key),
                "engine": engine,
                "mode": mode,
                "message": message,
                "login_url": "",
                "reference": spec.get("reference", ""),
            }
        ready = _baidupcs_login_state(cfg) or bool(drive_cfg.get("credential_ref") or drive_cfg.get("cookie_file"))
        status = "ready" if ready else "not_ready"
    elif engine == "alist":
        alist_url = (cfg.get("engines") or {}).get("alist_url", "").strip()
        status = "ready" if (alist_url and (drive_cfg.get("credential_ref") or drive_cfg.get("cookie_file"))) else ("unknown" if alist_url else "not_ready")
    else:
        ready = bool(drive_cfg.get("credential_ref") or drive_cfg.get("cookie_file"))
        status = "ready" if ready else "unknown" if engine == "custom" else "not_ready"
    return {
        "required": True,
        "blocking": status != "ready",
        "status": status,
        "drive": key,
        "drive_name": spec.get("name", key),
        "engine": engine,
        "mode": mode,
        "message": message,
        "login_url": "/login?drive=" + quote(key),
        "reference": spec.get("reference", ""),
    }


def fast_login_gate(url, cfg=None):
    """兼容更直观的 API 名称；纯本地检查，用于 Agent/Web 接收链接后立即提醒。"""
    return login_gate_for_url(url, cfg)


ZERO_CLIENT_BRIDGES = {
    "web": {
        "id": "web",
        "label": "官方网页会话桥",
        "requirement": "Python；仅使用官方分享页和官方接口，不读取浏览器 Cookie，不要求桌面客户端。",
        "steps": ["识别登录态、提取码、单文件/多文件", "递归列出目录并拆成文件任务", "逐文件获取官方直链、断点续传和失败重试"],
        "client_required": "无网盘客户端；遇验证码/风控/会员/付费限制安全失败",
    },
    "browser": {
        "id": "browser",
        "label": "浏览器直链捕获桥",
        "requirement": "Chrome/Edge 插件 + 官方网页登录；插件只捕获你主动触发的下载 URL，不读取登录态。",
        "steps": ["在官方网页登录并点击下载", "插件捕获官方生成的直链", "网盘通用内置 HTTP/aria2 续传下载"],
        "client_required": "无网盘客户端；不破解登录/签名/风控",
    },
    "alist": {
        "id": "alist",
        "label": "AList 驱动桥",
        "requirement": "已有 AList 服务并挂载对应网盘；网盘授权留在 AList。",
        "steps": ["AList 添加网盘存储", "分享文件转存到自己网盘", "WebDAV/rclone/HTTP 从 AList 下载"],
        "client_required": "无各家网盘客户端；AList 是统一服务桥",
    },
    "oauth": {
        "id": "oauth",
        "label": "官方 OAuth / WebDAV 桥",
        "requirement": "官方开放平台或 WebDAV 凭据；凭据只进系统凭据库。",
        "steps": ["完成官方授权", "用 rclone/AList/官方 API 拉取", "无需安装网盘桌面客户端"],
        "client_required": "无网盘客户端",
    },
    "builtin": {
        "id": "builtin",
        "label": "内置 HTTP / 流媒体桥",
        "requirement": "Python；可选 aria2 / yt-dlp。",
        "steps": ["识别直链或公开流", "用内置 HTTPDownloader/aria2/yt-dlp 下载"],
        "client_required": "无网盘客户端",
    },
}
OAUTH_DRIVE_KEYS = {"aliyun", "onedrive", "googledrive", "dropbox", "mega", "pcloud", "protondrive", "yandexdisk"}


def zero_client_options(key, cfg=None):
    """返回某类链接的零网盘客户端桥；不承诺绕过官方限制。"""
    cfg = cfg or load_config()
    spec = all_drives(cfg).get(key or "", {})
    engine = spec.get("engine", "")
    if not spec:
        return [dict(ZERO_CLIENT_BRIDGES["builtin"], recommended=True)]
    options = []
    if key in ("direct", "stream", "bittorrent"):
        return [dict(ZERO_CLIENT_BRIDGES["builtin"], recommended=True)]
    if key == "baidu" or engine in ("baiduweb", "baidu_web", "web"):
        options.append(dict(ZERO_CLIENT_BRIDGES["web"], recommended=True))
    options.append(dict(ZERO_CLIENT_BRIDGES["browser"], recommended=not options))
    if engine in ("alist", "webdav") or key == "baidu":
        options.append(dict(ZERO_CLIENT_BRIDGES["alist"], recommended=len(options) == 1 and engine == "alist"))
    if key in OAUTH_DRIVE_KEYS or engine == "webdav":
        options.append(dict(ZERO_CLIENT_BRIDGES["oauth"], recommended=False))
    # 不再推荐安装各家桌面客户端；baidupcs/quark-cli 只作为显式指定的兼容回退。
    return options


def engine_catalog_payload(url="", cfg=None):
    """输出零客户端桥、本地兼容回退和静态适用范围。"""
    cfg = cfg or load_config()
    if url:
        key, spec = detect_drive(url, cfg)
    else:
        key, spec = "", {}
    drives = []
    for drive_key, drive_spec in sorted(all_drives(cfg).items()):
        if drive_key in ("direct", "stream", "bittorrent"):
            continue
        drives.append({
            "drive": drive_key,
            "name": drive_spec.get("name", drive_key),
            "default_engine": drive_spec.get("engine", ""),
            "zero_client": zero_client_options(drive_key, cfg),
        })
    return {
        "ok": True,
        "url": url,
        "detected": {"drive": key, "name": spec.get("name", ""), "engine": spec.get("engine", "")} if key else {},
        "zero_client": zero_client_options(key, cfg) if key else [],
        "drives": drives,
        "boundary": "零客户端指不安装百度/夸克等桌面客户端；不绕过登录、签名、风控、限速或 DRM。官方未给直链时仍无法下载。",
    }


def cmd_engines(args):
    payload = engine_catalog_payload(args.url or "")
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def login_gate_for_drive_key(key, cfg=None):
    """按网盘 key 返回登录/授权提示；供 /login?drive= 使用。"""
    cfg = cfg or load_config()
    spec = all_drives(cfg).get(key)
    if not spec:
        return {"required": False, "blocking": False, "status": "not_required"}
    domain = (spec.get("domains") or [""])[0]
    return login_gate_for_url("https://" + domain if domain else "", cfg)


def cmd_auth(args):
    gate = login_gate_for_url(args.url)
    payload = dict(gate)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if not gate.get("required"):
            print("✅ 该链接不需要提前登录/授权。")
            return 0
        print("%s：%s" % (gate.get("drive_name"), gate.get("mode")))
        print("  %s" % gate.get("message"))
        print("  登录页：%s" % gate.get("login_url"))
    return 0 if not gate.get("blocking") else 2


def sanitize(name, fallback="download"):
    name = unquote(name or "").strip()
    name = re.sub(r"[\\/:*?\"<>|\x00-\x1f]", "_", name)
    name = re.sub(r"\s+", " ", name).strip(" .")
    return name[:80] or fallback


def filename_from_url(url):
    path = urlparse(url).path
    base = sanitize(Path(path).name)
    if not base or base in (".", ".."):
        return "download.bin"
    return base


def url_slug(url):
    path = urlparse(url).path.rstrip("/")
    tail = sanitize(Path(path).name, fallback="share")
    return tail or "share"


def default_root(cfg):
    configured = (cfg.get("download_root") or "").strip()
    if configured:
        return Path(os.path.expanduser(configured))
    if platform.system().lower() == "darwin":
        for vol in ("/Volumes/拓展", "/Volumes/办公"):
            p = Path(vol)
            if p.is_dir() and os.access(str(p), os.W_OK):
                return p / "网盘下载"
    return Path(PATHS["download"])


def task_dir(cfg, drive_name, url, to=None):
    if to:
        return Path(os.path.expanduser(to))
    stamp = datetime.now().strftime("%Y%m%d")
    return default_root(cfg) / sanitize(drive_name) / (stamp + "-" + url_slug(url))


CONTENT_CATEGORIES = {
    "影视": (".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".ts"),
    "音乐": (".mp3", ".flac", ".wav", ".aac", ".ogg", ".m4a", ".ape", ".wma"),
    "文档": (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md", ".csv", ".epub"),
    "图片": (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".heic", ".tiff"),
    "压缩包": (".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso"),
}
DEFAULT_CATEGORY = "其他"


def content_category(url):
    """按文件名后缀猜测内容分类（影视/音乐/文档/图片/压缩包/其他）。"""
    name = filename_from_url(url).lower()
    for cat, exts in CONTENT_CATEGORIES.items():
        if name.endswith(exts):
            return cat
    return DEFAULT_CATEGORY


def smart_classify_dir(cfg, drive_name, url):
    """智能默认：把目标目录自动落到 根目录/分类/网盘/日期-文件名。"""
    smart = cfg.get("smart") or {}
    root = str((smart.get("classify_root") or "").strip())
    base = Path(os.path.expanduser(root)) if root else default_root(cfg)
    stamp = datetime.now().strftime("%Y%m%d")
    return base / content_category(url) / sanitize(drive_name or "网盘") / (stamp + "-" + url_slug(url))


def smart_auto_classify_enabled(cfg, classify=None):
    if classify is None:
        return bool((cfg.get("smart") or {}).get("auto_classify"))
    return bool(classify)


def find_engine_binary(engine, cfg):
    configured = ((cfg.get("engines") or {}).get(engine) or "").strip()
    if configured:
        p = Path(os.path.expanduser(configured))
        if p.exists():
            return str(p)
    # 兼容：路径写在 drives.<网盘>.engine_command（如 drives.baidu.engine_command）
    # 网盘的默认 engine 可能已被换成别的（如百度默认 baiduweb），这里按引擎↔网盘映射兜底。
    engine_drive_hints = {
        "baidupcs": ("baidu",), "quarkcli": ("quark",), "alist": ("alist",),
        "aria2": ("direct", "bittorrent"), "ytdlp": ("stream",),
    }
    try:
        hints = engine_drive_hints.get(engine, ())
        for dkey, dspec in all_drives(cfg).items():
            if dspec.get("engine") != engine and dkey not in hints:
                continue
            cand = str((cfg.get("drives") or {}).get(dkey, {}).get("engine_command") or "").strip()
            if not cand:
                continue
            p = Path(os.path.expanduser(cand))
            if p.is_file() and os.access(str(p), os.X_OK):
                return str(p)
    except Exception:
        pass
    for name in ENGINE_BINARIES.get(engine, []):
        found = shutil.which(name)
        if found:
            return found
    # 技能自带便携目录：tools/bin/*、tools/aria2/bin/*、tools/pylib/bin/*
    engines_map = {
        "ytdlp": ["yt-dlp", "yt_dlp"],
        "stream": ["yt-dlp", "yt_dlp"],
        "aria2": ["aria2c"],
    }
    for sub in ("bin", "pylib/bin", "aria2/bin", "aria2"):
        try:
            base = SKILL_DIR / "tools" / sub
            if not base.is_dir():
                continue
            for cand in engines_map.get(engine, []):
                p = base / cand
                if p.is_file() and os.access(str(p), os.X_OK):
                    return str(p)
        except OSError:
            continue
    return ""


# ---------------------------------------------------------------- 远程设备
def log_line(text, path=None):
    path = Path(path or LOG_PATH)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as fh:
            fh.write("[%s] %s\n" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), text))
    except OSError:
        pass


def _redact_argument(item):
    text = str(item)
    text = re.sub(
        r"(?i)(--(?:password|passwd|pwd|cookie|token|secret|credential|bduss|authorization|webdav-pass|alist-password)(?:\s+|=))(\S+)",
        r"\1***", text,
    )
    if re.match(r"(?i)^(--?(?:password|passwd|cookie|token|secret|credential|bduss|authorization)=)", text):
        return "***"
    if re.match(r"(?i)^(--?(?:password|passwd|pwd|cookie|token|secret|credential|bduss|authorization))$", text):
        return text
    if re.match(r"(?i)^(authorization|cookie):", text):
        return "***"
    if re.match(r"(?i)^-bduss=", text):
        return "***"
    return text


def mask_argv(argv):
    """隐藏命令行凭据；真正推荐路径是把密码放系统凭据库并从 stdin 传给引擎。"""
    out = []
    skip_next = False
    secret_flags = {
        "--password", "--passwd", "--pwd", "-p", "--cookie", "--token", "--secret",
        "--credential", "--bduss", "--user", "-u", "--webdav-pass", "--alist-password",
        "--webdav-password", "--alist-pass",
    }
    for i, item in enumerate(argv):
        if skip_next:
            out.append("***")
            skip_next = False
            continue
        current = _redact_argument(item)
        out.append(current)
        if item in secret_flags and i + 1 < len(argv):
            skip_next = True
    return out


def public_plan(plan):
    """给 agent/JSON 输出用的无凭据计划。"""
    steps = []
    for step in plan.get("steps", []):
        steps.append({
            "engine": step.get("engine", ""),
            "note": step.get("note", ""),
            "argv": mask_argv(step.get("argv") or []),
            "uses_stdin_credential": bool(step.get("stdin")),
        })
    return {
        "ok": plan.get("ok", False),
        "drive": plan.get("drive", ""),
        "drive_name": plan.get("drive_name", ""),
        "engine": plan.get("engine", ""),
        "tier": plan.get("tier", ""),
        "tier_source": plan.get("tier_source", ""),
        "auth": plan.get("auth", {}),
        "login_url": (plan.get("auth") or {}).get("login_url", ""),
        "zero_client": plan.get("zero_client", []),
        "target": plan.get("target", ""),
        "remote_kind": plan.get("remote_kind", ""),
        "remote_name": plan.get("remote_name", ""),
        "staging": plan.get("staging", ""),
        "steps": steps,
        "missing": plan.get("missing", []),
        "warnings": plan.get("warnings", []),
        "reference": plan.get("reference", ""),
        "web_port": plan.get("web_port", 0),
        "web_host": plan.get("web_host", ""),
        "web_url": plan.get("web_url", ""),
        "web_guide": plan.get("web_guide", ""),
        "web_bridge": ({"driver": (plan.get("web") or {}).get("driver", "")}
                       if plan.get("web") else {}),
    }


def _looks_like_baidupcs_download(argv):
    """判断某步骤是不是"用 BaiduPCS-Go 下载"（含自定义 engine_command 的情况）。"""
    if not argv:
        return False
    head = str(argv[0])
    small = head.lower()
    if "baidupcs" not in small and "baidupcs-go" not in small:
        return False
    return any(str(a) == "download" for a in argv[:4])


def _is_bare_baidupcs_binary(argv):
    """engine_command 只写了 BaiduPCS-Go 可执行文件、没有子命令的情况。"""
    if len(argv) != 1:
        return False
    return "baidupcs" in str(argv[0]).lower()


def _baidu_save_path(cfg):
    try:
        return (((cfg or {}).get("drives") or {}).get("baidu", {}) or {}).get("save_path") or "/网盘下载"
    except Exception:
        return "/网盘下载"


def _attach_step_locks(plan, key, target, cfg=None):
    """给网盘下载步骤挂单实例锁，并做续传安全修正。

    2026-10-15 教训：同一来源被多个 BaiduPCS-Go 进程同时下载，
    互相抢带宽/覆盖断点，表现为"跑了很久没进展"；且 --ow 会让已下分片从头重下。
    规则：同 (drive, source, target) 只允许一个进程；一律禁止 --ow；补 --retry。
    """
    if key != "baidu":
        return plan
    for step in plan.get("steps", []) or []:
        if step.get("lock"):
            continue
        argv = list(step.get("argv") or [])
        engine = step.get("engine", "")
        if engine == "custom" and _is_bare_baidupcs_binary(argv):
            argv = [argv[0], "download", _baidu_save_path(cfg), "--saveto", str(target), "--retry", "5"]
            step["argv"] = argv
            step["note"] = "BaiduPCS-Go 从自己网盘下载（断点续传；禁止 --ow；分享需先转存到自己网盘）"
        is_dl = engine == "baidupcs" or (engine == "custom" and _looks_like_baidupcs_download(argv))
        if not is_dl:
            continue
        src = ""
        try:
            i = argv.index("download")
            src = argv[i + 1] if len(argv) > i + 1 else ""
        except ValueError:
            src = ""
        if "--ow" in argv:
            argv = [a for a in argv if a != "--ow"]
            step["note"] = (step.get("note") or "") + "（已自动移除 --ow：否则已下分片会从头重下）"
        if "--retry" not in argv:
            argv = argv + ["--retry", "5"]
        step["argv"] = argv
        step["lock"] = {"drive": key, "source": src, "target": str(target)}
    return plan


def build_plan(url, pwd="", to=None, cfg=None, engine=None, tier=None, path=None, classify=None):
    cfg = cfg or load_config()
    key, spec = detect_drive(url, cfg)
    if not key:
        return {"ok": False, "error": "无法识别的链接（既不是已知网盘域名，也不是 http(s)/ftp(s) 直链或磁力/BT 链接）"}
    drive_cfg = (cfg.get("drives") or {}).get(key, {})
    requested_tier = str(tier or drive_cfg.get("tier") or cfg.get("tier") or "auto").strip().lower()
    if to:
        target = task_dir(cfg, spec["name"], url, to)
    elif smart_auto_classify_enabled(cfg, classify):
        target = smart_classify_dir(cfg, spec["name"], url)
    else:
        target = task_dir(cfg, spec["name"], url, to)
    category = content_category(url) if (not to and smart_auto_classify_enabled(cfg, classify)) else ""
    engine = engine or (cfg.get("extensions", {}).get(key, {}) or {}).get("engine") or spec.get("engine", "http")
    plan = {
        "ok": True,
        "drive": key,
        "drive_name": spec["name"],
        "engine": engine,
        "tier": "",
        "requested_tier": requested_tier,
        "tier_source": "",
        "category": category,
        "target": str(target),
        "reference": str(SKILL_DIR / spec.get("reference", "")),
        "steps": [],
        "missing": [],
        "warnings": [],
    }
    auth = login_gate_for_url(url, cfg)
    plan["auth"] = auth
    plan["zero_client"] = zero_client_options(key, cfg)
    if not pwd:
        try:
            from pancli.webengine import extract_pwd_from_url as _epfu
            pwd = _epfu(url)
        except Exception:
            pwd = ""
    if auth.get("required"):
        plan["warnings"].insert(0, "%s：%s" % (auth.get("mode"), auth.get("message")))
    # 常见分享盘常带提取码：未提供 --pwd 时提前用人话提示，避免下载失败后无头绪
    if not pwd and key in ("baidu", "quark", "lanzou", "123pan", "weiyun"):
        plan["warnings"].append(
            "%s 分享链接常见带提取码，未提供 --pwd；若下载失败，请先从分享来源拿到提取码重试。" % spec["name"]
        )

    if requested_tier not in VALID_TIERS:
        plan["warnings"].append("tier=%s 不合法，已按 free 处理" % requested_tier)
        requested_tier = "free"

    if requested_tier == "auto":
        from pancli.engines import detect_account_tier as _dat
        detected, source = _dat(key, drive_cfg, cfg)
        if detected:
            tier = detected
            plan["tier_source"] = source
            plan["warnings"].append("账号等级自动识别为 %s（%s）" % (detected, source))
        else:
            tier = "free"
            plan["tier_source"] = source
            plan["warnings"].append(
                "账号等级未自动识别（%s），先按免费账号处理；登录后可用"
                " set-drive %s --account-tier free|vip 记录，或本次加 --tier vip 强制" % (source, key)
            )
    else:
        tier = requested_tier

    plan["tier"] = tier

    if engine in ("baiduweb", "baidu_web", "web") and key == "baidu":
        from pancli.webengine import build_web_plan as _bwp
        plan["web"] = _bwp(url, pwd=pwd or "", target=str(target), driver="baidu", cfg=cfg)
        plan["zero_client_selected"] = True
        plan["web_lock"] = {"drive": key, "source": url, "target": str(target)}
        plan["steps"].append({
            "engine": "baiduweb",
            "argv": [],
            "note": "百度官方网页会话：探测分享页 → 递归列出文件 → 按文件获取官方直链并断点续传",
        })
        return plan

    if category:
        plan["warnings"].append("智能分类已启用：自动保存到「%s」目录" % category)

    if engine == "browser":
        # 浏览器桥只接受用户/插件已经捕获到的直链；原始分享链接不能伪装成直链。
        plan["zero_client_selected"] = True
        if key not in ("direct", "stream", "bittorrent"):
            plan["missing"].append("浏览器桥捕获到的官方直链（先在官方网页触发下载）")
            plan["steps"] = []
            return plan
        engine = "aria2" if find_engine_binary("aria2", cfg) else "http"

    custom_cmd = (drive_cfg.get("engine_command") or "").strip()

    if custom_cmd:
        argv = shlex.split(
            custom_cmd.format(url=url, pwd=pwd or "", dir=str(target), name=sanitize(spec["name"]), tier=tier)
        )
        plan["steps"].append({"engine": "custom", "argv": argv, "note": "自定义引擎命令"})
        _attach_step_locks(plan, key, target, cfg)
        return plan

    if engine == "http":
        from pancli.engines import http_step as _hs
        plan["steps"].append(_hs(url, target, cfg, tier))

    elif engine == "aria2":
        binary = find_engine_binary("aria2", cfg)
        if not binary:
            plan["missing"].append("aria2c")
        bt = cfg.get("bt", {})
        base = [binary or "aria2c", "-c", "--retry-wait=5",
                "-m", str(cfg.get("http", {}).get("retries", 3))]
        if is_magnet_url(url) or is_torrent_path(url):
            seed = str(int(bt.get("seed_time", 0) or 0))
            trackers = str(bt.get("trackers") or "").strip()
            peers = str(bt.get("bt_max_peers", "64") or "64")
            argv = list(base)
            if bt.get("enable_dht", True):
                argv += ["--enable-dht=true", "--bt-save-metadata=true",
                         "--dht-listen-port", str(bt.get("dht_listen_port", "6881-6999"))]
            else:
                argv += ["--enable-dht=false"]
            argv += ["--bt-max-peers", peers, "--seed-time", seed]
            if trackers:
                argv += ["--bt-tracker", trackers]
            argv += ["-d", str(target), url]
            plan["steps"].append({"engine": "aria2", "argv": argv,
                                  "note": "aria2 磁力/BT 下载（DHT=%s，最大peer=%s，做种 %s 秒）" % (
                                      "开" if bt.get("enable_dht", True) else "关", peers, seed)})
        else:
            bt_conn = bt.get("connections_vip" if tier == "vip" else "connections_free", 0)
            try:
                bt_conn = int(bt_conn)
            except (TypeError, ValueError):
                bt_conn = 0
            if bt_conn and bt_conn > 0:
                conn = bt_conn
            else:
                conn = cfg.get("http", {}).get("max_connections_vip" if tier == "vip" else "max_connections_free", 1)
            filename = filename_from_url(url)
            argv = base + ["-x", str(conn), "-s", str(conn),
                           "-d", str(target), "-o", filename, url]
            plan["steps"].append({"engine": "aria2", "argv": argv,
                                  "note": "aria2 多线程下载（tier=%s，并发 %s）" % (tier, conn)})

    elif engine in ("ytdlp", "stream"):
        binary = find_engine_binary(engine, cfg) or find_engine_binary("ytdlp", cfg)
        if not binary:
            plan["missing"].append("yt-dlp")
        fmt = (cfg.get("ytdlp") or {}).get("format", "bv*+ba/b")
        conn = (cfg.get("ytdlp") or {}).get("concurrent_fragments", 4)
        try:
            conn = int(conn) or 4
        except (TypeError, ValueError):
            conn = 4
        argv = [binary or "yt-dlp", "-f", fmt, "--concurrent-fragments", str(conn),
                "--no-progress", "--newline", "-o", str(Path(target) / "%(title).80s.%(ext)s"), url]
        if (cfg.get("ytdlp") or {}).get("cookies_from_browser"):
            argv += ["--cookies-from-browser", str((cfg.get("ytdlp") or {}).get("cookies_from_browser"))]
        plan["steps"].append({"engine": "ytdlp", "argv": argv,
                              "note": "yt-dlp 视频流多分段下载（并发 %s）" % conn})

    elif engine == "alist":
        server = ((cfg.get("engines") or {}).get("alist_url") or "").strip()
        dav_user = ((cfg.get("engines") or {}).get("alist_user") or "").strip()
        dav_ref = ((cfg.get("engines") or {}).get("alist_password_ref") or "").strip()
        dav_pass = resolve_engine_secret(cfg, "alist_password_ref", "alist_password")
        if dav_ref and not dav_pass:
            plan["warnings"].append("AList 凭据引用无法从系统凭据库读取；请在本机终端运行 secret set engine.alist")
        if not path:
            plan["missing"].append("AList 路径：分享链接需先在 AList 中挂载/转存，再用 --path /挂载名/子目录 指定")
            plan["steps"].append({"engine": "alist", "argv": [], "note": "建议流程：1) AList 添加对应网盘存储 2) 浏览器打开分享链接转存到自己账号 3) 用 --path 指向 AList 中的目录"})
        elif not server:
            plan["missing"].append("alist_url（在 config.json 的 engines.alist_url 填写 AList 地址）")
        else:
            remote = path if path.startswith("/") else "/" + path
            filename = sanitize(Path(remote).name, fallback="download")
            rclone_bin = find_engine_binary("rclone", cfg)
            rclone_remote = ((cfg.get("engines") or {}).get("rclone_remote") or "").strip()
            if rclone_bin and rclone_remote:
                # rclone 远端名必须带冒号；允许用户只填 alist，脚本自动补成 alist:。
                if ":" not in rclone_remote:
                    rclone_remote += ":"
                remote_path = rclone_remote.rstrip("/") + remote
                try:
                    conn = int(cfg.get("http", {}).get("max_connections_vip" if tier == "vip" else "max_connections_free", 1))
                except (TypeError, ValueError):
                    conn = 1
                conn = max(1, conn)
                checkers = max(1, min(conn * 2, 8))
                argv = [
                    rclone_bin, "copy", "--progress",
                    "--transfers", str(conn), "--checkers", str(checkers),
                    remote_path, str(target),
                ]
                plan["steps"].append({"engine": "rclone", "argv": argv,
                                      "note": "通过 rclone/AList WebDAV 递归下载（tier=%s，并发 %s，远端 %s）" % (tier, conn, remote_path)})
            else:
                if rclone_bin and not rclone_remote:
                    plan["warnings"].append("已安装 rclone 但未配置 engines.rclone_remote，回退为 curl 单文件下载")
                elif not rclone_bin:
                    plan["warnings"].append("未安装 rclone；curl 回退只适合单文件，目录请在 Finder 挂载 AList WebDAV 或安装 rclone")
                argv = ["curl", "-L", "--fail", "-C", "-", "-o", str(target / filename), server.rstrip("/") + "/dav" + remote]
                from pancli.engines import curl_basic_auth_step as _cbas
                step = _cbas(argv, dav_user, dav_pass)
                step["engine"] = "alist"
                step["note"] = "通过 AList WebDAV 下载单文件（挂载路径 %s；凭据走 stdin）" % remote
                plan["steps"].append(step)

    elif engine == "webdav":
        eng = cfg.get("engines") or {}
        server = (eng.get("webdav_url") or "").strip().rstrip("/")
        dav_user = (eng.get("webdav_user") or "").strip()
        dav_ref = (eng.get("webdav_password_ref") or "").strip()
        dav_pass = resolve_engine_secret(cfg, "webdav_password_ref", "webdav_password")
        if dav_ref and not dav_pass:
            plan["warnings"].append("WebDAV 凭据引用无法从系统凭据库读取；请在本机终端运行 secret set engine.webdav")
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
        download_url = ""
        if host == "dav.jianguoyun.com" and parsed.path.startswith("/dav"):
            download_url = url
        elif path and server:
            download_url = server + "/" + path.lstrip("/")
        if not download_url:
            plan["missing"].append("webdav_url + --path，或直接使用 dav.jianguoyun.com 的 WebDAV 文件地址")
        else:
            filename = sanitize(Path(urlparse(download_url).path).name or filename_from_url(url), fallback="download")
            argv = ["curl", "-L", "--fail", "-C", "-", "-o", str(target / filename), download_url]
            from pancli.engines import curl_basic_auth_step as _cbas
            step = _cbas(argv, dav_user, dav_pass)
            step["engine"] = "webdav"
            step["note"] = "通过 WebDAV 断点续传下载（坚果云/通用 WebDAV；凭据走 stdin）"
            plan["steps"].append(step)

    elif engine == "baidupcs":
        binary = find_engine_binary("baidupcs", cfg)
        if not binary:
            plan["missing"].append("BaiduPCS-Go")
        save_path = ((cfg.get("drives") or {}).get("baidu", {}).get("save_path") or "/网盘下载").strip()
        binary = binary or "BaiduPCS-Go"
        plan["steps"].append({"engine": "baidupcs", "argv": [binary, "transfer", url, pwd or "", save_path],
                              "note": "转存到自己网盘（需已用 BaiduPCS-Go login 登录）"})
        plan["steps"].append({"engine": "baidupcs",
                              "argv": [binary, "download", save_path, "--saveto", str(target), "--retry", "5"],
                              "note": "从自己网盘批量下载到本地（断点续传；禁止加 --ow，否则已下分片会从头重下）",
                              "lock": {"drive": "baidu", "source": save_path, "target": str(target)}})

    elif engine == "quarkcli":
        binary = find_engine_binary("quarkcli", cfg)
        if not binary:
            plan["missing"].append("quark-cli（夸克命令行工具）")
        argv = [binary or "quark", "download", url]
        if pwd:
            argv += ["--pwd", pwd]
        argv += ["--dir", str(target)]
        plan["steps"].append({"engine": "quarkcli", "argv": argv, "note": "夸克分享链接转存并下载（Cookie 登录）"})

    else:
        plan["missing"].append("引擎 %s 未配置 engine_command" % engine)
        plan["steps"].append({"engine": engine, "argv": [], "note": "在 config.json 的 drives.%s.engine_command 配置命令模板" % key})

    _attach_step_locks(plan, key, target, cfg)
    return plan


def run_plan(plan, timeout=0, dry_run=True):
    if not plan.get("ok"):
        return 1
    for step in plan["steps"]:
        argv = step.get("argv") or []
        if not argv:
            continue
        if dry_run:
            print("DRY-RUN:", " ".join(shlex.quote(x) for x in mask_argv(argv)))
            continue
        if step.get("lock"):
            import atexit as _atexit
            from pancli import tasklock as _tlk
            _gate = _tlk.acquire_for_step(step)
            if not _gate["ok"]:
                print("⛔ %s" % _gate["message"])
                log_line("LOCK-BUSY: " + _gate["message"])
                return 9
            _atexit.register(_gate["lock"].release)
        print("RUN:", " ".join(shlex.quote(x) for x in mask_argv(argv)))
        log_line("RUN: " + " ".join(mask_argv(argv)))
        started = time.time()
        try:
            cwd = str(step.get("cwd") or plan.get("run_cwd") or plan.get("target") or "")
            kwargs = {"timeout": timeout or None}
            if cwd and Path(cwd).exists():
                kwargs["cwd"] = cwd
            if step.get("stdin"):
                kwargs["input"] = step["stdin"]
                kwargs["text"] = True
            proc = subprocess.run(argv, **kwargs)
            rc = proc.returncode
        except subprocess.TimeoutExpired:
            print("❌ 超时：%s" % step.get("note", argv[0]))
            log_line("TIMEOUT: " + " ".join(mask_argv(argv)))
            return 124
        except OSError as exc:
            print("❌ 执行失败：%s（%s）" % (argv[0], exc))
            log_line("ERROR: %s %s" % (argv[0], exc))
            return 127
        log_line("EXIT %s (%.1fs): %s" % (rc, time.time() - started, " ".join(mask_argv(argv))))
        if rc != 0:
            print("❌ 步骤失败（exit=%s）：%s" % (rc, step.get("note", "")))
            return rc
    return 0

def humanize_step_error(step, rc):
    """把常见退出码/引擎错误翻译成中文动作提示；无法可靠判断时返回空串。"""
    engine = (step or {}).get("engine", "")
    if rc == 124:
        return "超时：网络慢或文件大。重跑任务会从断点续传（curl -C - / 引擎自带续传）。"
    if rc in (126, 127):
        name = ((step or {}).get("argv") or ["命令"])[0]
        return "找不到或无法执行 %s：请先运行 `pan doctor` 检查并安装依赖。" % (name or "命令",)
    if rc == 7:
        return "连接失败：检查网络是否可用、分享链接是否还在有效期内，必要时重新登录该网盘。"
    if rc == 22:
        return "服务器返回非 2xx（可能是 401/403）：授权过期、提取码错误或无权限，请重新登录该网盘。"
    if engine == "webdav":
        return "WebDAV 授权可能已过期：请用 `pan secret set engine.webdav --stdin` 更新密码后重试。"
    if engine == "baidupcs":
        return "百度网盘未登录或分享链接失效：请先 `pan login baidu`，分享链接需先转存到自己网盘。"
    if engine == "quarkcli":
        return "夸克登录 Cookie 可能已失效：请先 `pan login quark` 后重试。"
    return ""


def run_plan_detailed(plan, timeout=0, dry_run=True, emit_events=False, live=None, task_control=None):
    """执行计划并返回 (rc, 逐步骤结果列表)；用于本机 get 的统计、报告与 JSON 事件流。"""
    if task_control is not None:
        task_control.set_step("")
    results = []
    if not plan.get("ok"):
        return 1, results
    if plan.get("web"):
        from pancli.webengine import execute_web_plan as _ewp
        _gate = None
        lock_spec = plan.get("web_lock")
        if lock_spec:
            from pancli import tasklock as _tlk
            _gate = _tlk.acquire_for_step({"lock": lock_spec, "note": "百度官方网页会话下载"})
            if not _gate["ok"]:
                message = _gate["message"]
                print("⛔ %s" % message)
                log_line("LOCK-BUSY: " + message)
                return 9, [{
                    "index": 1,
                    "engine": "baiduweb",
                    "note": "百度官方网页会话下载",
                    "argv": [],
                    "rc": 9,
                    "elapsed": 0.0,
                    "error": message,
                    "hint": message,
                }]
        try:
            return _ewp(plan, emit_events=emit_events, live=live, task_control=task_control)
        finally:
            if _gate is not None:
                _gate["lock"].release()
    for idx, step in enumerate(plan.get("steps", []), start=1):
        argv = step.get("argv") or []
        entry = {
            "index": idx,
            "engine": step.get("engine", ""),
            "note": step.get("note", ""),
            "argv": mask_argv(argv),
            "uses_stdin_credential": bool(step.get("stdin")),
            "started": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
            "rc": -1,
            "elapsed": 0.0,
            "error": "",
        }
        results.append(entry)
        if live is not None:
            live.set_step(entry["note"])
        if emit_events:
            print(json.dumps({"event": "step_start", "index": idx, "engine": entry["engine"], "note": entry["note"]}, ensure_ascii=False))
        if not argv:
            entry["error"] = "空步骤（仅配置说明）"
            results[-1] = entry
            if emit_events:
                print(json.dumps({"event": "step_skip", "index": idx}, ensure_ascii=False))
            continue
        if dry_run:
            print("DRY-RUN:", " ".join(shlex.quote(x) for x in mask_argv(argv)))
            entry["rc"] = 0
            entry["dry_run"] = True
            results[-1] = entry
            continue
        if step.get("lock"):
            import atexit as _atexit
            from pancli import tasklock as _tlk
            _gate = _tlk.acquire_for_step(step)
            if not _gate["ok"]:
                print("⛔ %s" % _gate["message"])
                log_line("LOCK-BUSY: " + _gate["message"])
                entry["rc"] = 9
                entry["error"] = _gate["message"]
                entry["hint"] = _gate["message"]
                results[-1] = entry
                if emit_events:
                    print(json.dumps({"event": "step_done", "index": idx, "engine": entry["engine"], "rc": 9, "error": entry["error"]}, ensure_ascii=False))
                return 9, results
            _atexit.register(_gate["lock"].release)
        print("RUN:", " ".join(shlex.quote(x) for x in mask_argv(argv)))
        log_line("RUN: " + " ".join(mask_argv(argv)))
        started = time.time()
        try:
            cwd = str(step.get("cwd") or plan.get("run_cwd") or plan.get("target") or "")
            kwargs = {"timeout": timeout or None}
            if cwd and Path(cwd).exists():
                kwargs["cwd"] = cwd
            if step.get("stdin"):
                kwargs["input"] = step["stdin"]
                kwargs["text"] = True
            if task_control is not None:
                task_control.set_step(entry["note"])
                from pancli.report import _run_step_controlled as _rsc
                rc, _status, _exc = _rsc(argv, kwargs, task_control, timeout=timeout or 0)
                if _exc:
                    raise _exc
                if _status == "cancelled":
                    print("🛑 任务已取消：%s" % step.get("note", ""))
                    entry["rc"] = 130
                    entry["error"] = "任务已取消"
                    results[-1] = entry
                    if emit_events:
                        print(json.dumps({"event": "step_done", "index": idx, "rc": 130, "error": "任务已取消"}, ensure_ascii=False))
                    return 130, results
                if _status == "timeout":
                    raise subprocess.TimeoutExpired(argv[0], timeout)
            else:
                proc = subprocess.run(argv, **kwargs)
                rc = proc.returncode
        except subprocess.TimeoutExpired:
            print("❌ 超时：%s" % step.get("note", argv[0]))
            log_line("TIMEOUT: " + " ".join(mask_argv(argv)))
            entry["rc"] = 124
            entry["error"] = "超时"
            hint_tmp = humanize_step_error(step, 124)
            if hint_tmp:
                entry["hint"] = hint_tmp
                print("  💡 " + hint_tmp)
            results[-1] = entry
            if emit_events:
                print(json.dumps({"event": "step_done", "index": idx, "rc": 124, "error": "超时", "hint": entry.get("hint", "")}, ensure_ascii=False))
            return 124, results
        except OSError as exc:
            print("❌ 执行失败：%s（%s）" % (argv[0], exc))
            log_line("ERROR: %s %s" % (argv[0], exc))
            entry["rc"] = 127
            entry["error"] = str(exc)
            hint_tmp = humanize_step_error(step, 127)
            if hint_tmp:
                entry["hint"] = hint_tmp
                print("  💡 " + hint_tmp)
            results[-1] = entry
            if emit_events:
                print(json.dumps({"event": "step_done", "index": idx, "rc": 127, "error": str(exc), "hint": entry.get("hint", "")}, ensure_ascii=False))
            return 127, results
        entry["rc"] = rc
        entry["elapsed"] = round(time.time() - started, 2)
        results[-1] = entry
        log_line("EXIT %s (%.1fs): %s" % (rc, entry["elapsed"], " ".join(mask_argv(argv))))
        if emit_events:
            print(json.dumps({
                "event": "step_done",
                "index": idx,
                "engine": entry["engine"],
                "rc": rc,
                "elapsed": entry["elapsed"],
            }, ensure_ascii=False))
        if rc != 0:
            print("❌ 步骤失败（exit=%s）：%s" % (rc, step.get("note", "")))
            hint_tmp = humanize_step_error(step, rc)
            if hint_tmp:
                entry["hint"] = hint_tmp
                print("  💡 " + hint_tmp)
            entry["error"] = "步骤失败 exit=%s" % rc
            results[-1] = entry
            if emit_events:
                print(json.dumps({"event": "step_done", "index": idx, "engine": entry["engine"], "rc": rc, "error": entry["error"], "hint": entry.get("hint", "")}, ensure_ascii=False))
            return rc, results
    return 0, results


def is_http_url(url):
    return str(url or "").lower().startswith(("http://", "https://"))


def probe_http_total_bytes(url, cfg=None, timeout=8):
    """尽力读取直链 Content-Length，用于剩余时间估算；失败返回 0（不阻塞下载）。"""
    cfg = cfg or {}
    connect_timeout = int((cfg.get("http") or {}).get("connect_timeout", 15))
    argv = ["curl", "-sI", "-L", "--connect-timeout", str(connect_timeout), "--max-time", str(timeout), url]
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout + 2)
    except (OSError, subprocess.TimeoutExpired):
        return 0
    text = (proc.stdout or "") + "\n" + (proc.stderr or "")
    # 取最后一次 Content-Length，兼容重定向后真实资源
    value = None
    for line in text.splitlines():
        head = line.split(":", 1)
        if len(head) == 2 and head[0].strip().lower() == "content-length":
            value = head[1].strip()
    try:
        return max(0, int(value or 0))
    except (TypeError, ValueError):
        return 0


def resolve_split_count(cfg, args):
    v = getattr(args, "split", 0) or 0
    try:
        n = int(v)
    except (TypeError, ValueError):
        n = 0
    if n and n > 0:
        return n
    http = cfg.get("http", {})
    if http.get("range_split"):
        try:
            return int(http.get("range_split_connections") or 0)
        except (TypeError, ValueError):
            return 0
    return 0


def auto_split_decision(url, cfg=None, sample_bytes=1048576):
    """F1（v0.20.0）：单连接慢且支持 Range 时自动返回分片数，否则返回 (0, 原因)。

    决策口径（§四F1）：
      1. http.auto_split 关闭 → (0, "disabled")
      2. Range 不支持 / 文件 < 4MB → (0, 原因)（小文件分片得不偿失）
      3. 样本测速 ≥ auto_split_threshold_kbps（默认 1024）→ (0, "fast_enough")
      4. 否则返回 split_max_concurrency（默认 4）作为分片数。
    只做样本测速 + 阈值判断，不是"智能限速"；账号级限速此路也绕不开，
    只对"单连接被限、多连接放开"的服务器有效。
    """
    cfg = cfg or load_config()
    http = cfg.get("http") or {}

    def _int(key, default):
        try:
            v = int(http.get(key, default))
            return v if v > 0 else default
        except (TypeError, ValueError):
            return default

    if not http.get("auto_split", True):
        return 0, "disabled"
    length, accept_ranges = probe_http_range(url)
    if not length or not accept_ranges:
        return 0, "range_unsupported"
    if length < 4 * 1024 * 1024:
        return 0, "file_too_small"

    threshold = _int("auto_split_threshold_kbps", 1024)
    import time as _time
    tmp = tempfile.NamedTemporaryFile(prefix="pan-autosplit-", delete=False, suffix=".bin")
    tmp.close()
    probe = Path(tmp.name)
    issued = _time.time()
    argv = ["curl", "-sS", "-L", "--max-time", "20",
            "-r", "0-%d" % (sample_bytes - 1), "-o", str(probe), url]
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=23)
        elapsed = max(_time.time() - issued, 0.001)
        size = probe.stat().st_size if probe.exists() else 0
    except (OSError, subprocess.TimeoutExpired):
        size, elapsed = 0, 1.0
    finally:
        try:
            probe.unlink()
        except OSError:
            pass
    if size < sample_bytes:
        # 样本都没拉全：要么链接已失效要么慢到没救，交给上层走整文件重试逻辑。
        return 0, "probe_incomplete"
    kbps = (size * 8.0 / 1024.0) / elapsed
    if kbps >= threshold:
        return 0, "fast_enough(%.0fkbps>=%d)" % (kbps, threshold)
    return _int("split_max_concurrency", 4), "slow_single_conn(%.0fkbps<%d)" % (kbps, threshold)


def probe_http_range(url, timeout=15):
    try:
        proc = subprocess.run(["curl", "-sI", "-L", "--max-time", str(timeout), url],
                              capture_output=True, text=True, timeout=timeout + 5)
    except (OSError, subprocess.TimeoutExpired):
        return None, False
    if proc.returncode != 0:
        return None, False
    length = None
    accept_ranges = False
    for line in (proc.stdout or "").splitlines():
        low = line.lower()
        if low.startswith("content-length:"):
            try:
                length = int(line.split(":", 1)[1].strip())
            except ValueError:
                pass
        elif low.startswith("accept-ranges:"):
            accept_ranges = "bytes" in line.split(":", 1)[1].strip().lower()
    return (length if length and length > 0 else None), accept_ranges


def rank_fastest_urls(urls, cfg=None, timeout=6, samples=200000):
    """对多个候选直链做小范围真实测速（各下约 samples 字节），返回按平均速度降序的 [(url, kbps)]。
    只适用于可 HEAD/Range 的 HTTP(S) 直链；失败或不可测的排到队尾标注 error。"""
    import time as _time
    cfg = cfg or load_config()
    results = []
    for u in (urls or []):
        url = str(u or "").strip()
        if not url:
            continue
        tmp = tempfile.NamedTemporaryFile(prefix="pan-probe-", delete=False, suffix=".bin")
        tmp.close()
        probe_url = Path(tmp.name)
        issued = _time.time()
        argv = ["curl", "-sS", "-L", "--max-time", str(int(timeout)),
                "-r", "0-%d" % (samples - 1), "-o", str(probe_url), url]
        try:
            proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout + 3)
            elapsed = max(_time.time() - issued, 0.001)
            size = probe_url.stat().st_size if probe_url.exists() else 0
            kbps = (size * 8.0 / 1024.0) / elapsed if elapsed else 0.0
            if proc.returncode != 0 and size < 1:
                results.append({"url": url, "ok": False, "error": (proc.stderr or "").strip()[:120] or "exit=%s" % proc.returncode})
            else:
                results.append({"url": url, "ok": True, "bytes": size, "elapsed": round(elapsed, 3), "kbps": round(kbps, 1)})
        except (OSError, subprocess.TimeoutExpired) as exc:
            results.append({"url": url, "ok": False, "error": str(exc)[:120]})
        finally:
            try:
                probe_url.unlink(missing_ok=True)
            except OSError:
                pass
    ok = sorted([r for r in results if r.get("ok")], key=lambda r: r.get("kbps", 0), reverse=True)
    bad = [r for r in results if not r.get("ok")]
    return ok + bad


MOVIE_SOURCES = [
    {"name": "公开/公版电影（Internet Archive / Public Domain）", "how": "https://archive.org/details/movies_and_films（公开可下）", "direct": "archive.org 内选文件直链，再 get/probe"},
    {"name": "公有领域电影（Public Domain Torrents）", "how": "https://www.publicdomaintorrents.info/（种子直下）", "direct": "复制磁力/.torrent 给 get 走 aria2"},
    {"name": "互联网档案馆 bt 直链", "how": "archive.org 选中条目复制 .torrent 或磁力", "direct": "get 自动识别 bittorrent"},
    {"name": "官方公开资源（只下你有权下的内容）", "how": "各站公开课/开源影片、Vimeo CC、b站自制=你本人有授权内容", "direct": "get 自动识别 stream(yt-dlp)"},
]


SEARCH_KINDS = ("auto", "movie", "video", "music", "file")



def cmd_init(args):
    if getattr(args, "wizard", False):
        from pancli.setup import cmd_init_wizard as _cmd_init_wizard
        return _cmd_init_wizard(args)
    cfg = load_config()
    if CONFIG_PATH.exists() and not args.force:
        print("已存在，未变更：%s" % CONFIG_PATH)
        return 0
    path = save_config(cfg)
    print("已创建：%s（权限 600；账号密码另存系统凭据库，不写入此文件）" % path)
    return 0


def cmd_show(args):
    cfg = load_config()
    print(json.dumps(mask_value("config", cfg), ensure_ascii=False, indent=2))
    return 0


def cmd_detect(args):
    key, spec = detect_drive(args.url)
    if not key:
        print("❌ 无法识别")
        return 1
    auth = login_gate_for_url(args.url)
    print(json.dumps({"drive": key, "name": spec["name"], "engine": spec["engine"],
                      "reference": spec.get("reference", ""), "auth": auth}, ensure_ascii=False, indent=2))
    return 0



def _route_cache_key(cfg, url, pwd="", engine="", tier="", path=""):
    """路由短缓存键：链接/参数 + 配置内容签名 + 百度本机登录态。"""
    config_blob = json.dumps(cfg, ensure_ascii=False, sort_keys=True, default=str)
    config_sig = hashlib.sha256(config_blob.encode("utf-8")).hexdigest()
    return (str(url or ""), str(pwd or ""), str(engine or ""), str(tier or ""), str(path or ""),
            config_sig, bool(_baidupcs_login_state(cfg)))


def route_link_payload(cfg, url, pwd="", engine="", tier="", path="", cache=True):
    """一次返回识别、登录门禁、依赖、目标目录、零客户端桥和下一步动作；纯本地不联网。

    服务内同参数短缓存 2 秒；百度登录态或配置变化会自动失效。
    """
    started = time.perf_counter()
    now = time.time()
    key = _route_cache_key(cfg, url, pwd, engine, tier, path) if cache else None
    if cache:
        item = _ROUTE_CACHE.get(key)
        if item and now - item["expires"] < _ROUTE_CACHE_TTL:
            res = copy.deepcopy(item["payload"])
            res["cache_hit"] = True
            res["cache_ttl_seconds"] = _ROUTE_CACHE_TTL
            res["latency_ms"] = round((time.perf_counter() - started) * 1000, 1)
            return res
    res = _probe_link_checks(cfg, url, pwd=pwd, engine=engine, tier=tier, path=path)
    auth = res.get("auth") or {}
    if auth.get("blocking"):
        action = "login"
    elif res.get("missing"):
        action = "install_or_configure"
    elif not res.get("ok"):
        action = "fix_preflight"
    else:
        action = "download"
    res["route"] = "zero_client" if any((x or {}).get("id") == "browser" for x in res.get("zero_client", [])) else "default"
    res["next_action"] = action
    res["latency_ms"] = round((time.perf_counter() - started) * 1000, 1)
    res["cache_hit"] = False
    res["cache_ttl_seconds"] = _ROUTE_CACHE_TTL
    if cache:
        _ROUTE_CACHE[key] = {"payload": copy.deepcopy(res), "expires": now}
        # 只保留最近 128 条，避免常驻服务增长。
        if len(_ROUTE_CACHE) > 128:
            oldest = sorted(_ROUTE_CACHE.items(), key=lambda kv: kv[1]["expires"])[:len(_ROUTE_CACHE) - 128]
            for k, _ in oldest:
                _ROUTE_CACHE.pop(k, None)
    return res


def compact_route_payload(res):
    """给 Agent/LLM 输出的最小路由结果；足够决定下一步，避免整份预检刷屏。"""
    return {
        "ok": bool(res.get("ok")),
        "drive": res.get("drive", ""),
        "drive_name": res.get("drive_name", ""),
        "engine": res.get("engine", ""),
        "route": res.get("route", ""),
        "next_action": res.get("next_action", ""),
        "blocking": bool((res.get("auth") or {}).get("blocking")),
        "login_required": bool(res.get("login_required")),
        "login_url": res.get("login_url", ""),
        "missing": res.get("missing", []) if res.get("next_action") == "install_or_configure" else [],
        "warnings": (res.get("warnings") or [])[:2] if res.get("next_action") == "download" else [],
        "target": res.get("target", ""),
        "latency_ms": res.get("latency_ms", 0),
    }


def cmd_route(args):
    res = route_link_payload(load_config(), args.url, pwd=args.pwd or "", engine=args.engine or "",
                             tier=args.tier or "", path=args.path or "",
                             cache=not getattr(args, "no_cache", False))
    if args.json:
        if getattr(args, "brief", False):
            print(json.dumps(compact_route_payload(res), ensure_ascii=False, separators=(",", ":")))
        else:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    print("路由：%s" % args.url)
    print("  网盘：%s（%s）" % (res.get("drive_name"), res.get("drive")))
    print("  下一步：%s" % res.get("next_action"))
    print("  路径：%s · 耗时：%sms" % (res.get("route"), res.get("latency_ms")))
    for c in res.get("checks", []):
        mark = "✅" if c.get("ok") else "❌"
        print("  %s %s：%s" % (mark, c.get("name"), c.get("detail")))
    return 0 if res.get("next_action") == "download" else 2


def _probe_link_checks(cfg, url, pwd="", engine="", tier="", path=""):
    """只读测试一条下载链接：识别、依赖/配置、目标目录、提取码；不下载不写盘。"""
    key, spec = detect_drive(url, cfg)
    if not key:
        return {"ok": False, "drive": "", "drive_name": "未知", "engine": "",
                "checks": [{"name": "识别", "ok": False, "detail": "无法识别该链接"}],
                "missing": [], "warnings": ["这不是默认支持的网盘域名，也不是 http(s) 直链"]}
    plan = build_plan(url, pwd=pwd, cfg=cfg, engine=engine or None, tier=tier or None, path=path or None)
    auth = plan.get("auth") or login_gate_for_url(url, cfg)
    checks = []
    checks.append({"name": "识别", "ok": True, "detail": "%s（%s）" % (spec["name"], key)})
    checks.append({"name": "登录/授权", "ok": not auth.get("blocking"),
                   "detail": auth.get("message", "") if auth.get("blocking") else "%s（状态：%s）" % (auth.get("mode"), auth.get("status"))})
    missing = list(plan.get("missing") or [])
    checks.append({"name": "依赖与配置", "ok": not missing,
                   "detail": "；".join(missing) if missing else "依赖与配置齐备"})
    warnings = list(plan.get("warnings") or [])
    if warnings:
        checks.append({"name": "注意", "ok": True, "detail": "；".join(warnings[:5])})
    target = Path(plan.get("target") or ".")
    if target.exists():
        target_ok = os.access(str(target), os.W_OK)
        detail = "目录存在，可写" if target_ok else "目录存在但当前用户无写权限"
    else:
        parent = target
        while parent and not parent.exists():
            parent = parent.parent
        target_ok = bool(parent) and os.access(str(parent), os.W_OK)
        detail = "目录不存在，父目录可写（将自动创建）" if target_ok else "父目录不可写，请更换下载目录"
    checks.append({"name": "目标目录", "ok": target_ok, "detail": detail})
    if pwd:
        checks.append({"name": "提取码", "ok": True, "detail": "已提供"})
    return {"ok": (not missing) and target_ok and not auth.get("blocking"), "drive": key, "drive_name": spec["name"],
            "engine": plan.get("engine", ""), "target": str(target), "auth": auth,
            "zero_client": plan.get("zero_client", []),
            "login_required": auth.get("required", False), "login_url": auth.get("login_url", ""),
            "checks": checks, "missing": missing, "warnings": warnings}


def cmd_test(args):
    cfg = load_config()
    res = _probe_link_checks(cfg, args.url, pwd=args.pwd or "", engine=args.engine or "",
                             tier=args.tier or "", path=args.path or "")
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    print("链接测试：%s" % args.url)
    print("  识别：%s（%s）" % (res["drive_name"], res["drive"]))
    for c in res["checks"]:
        mark = "✅" if c["ok"] else "❌"
        print("  %s %s：%s" % (mark, c["name"], c["detail"]))
    if res["ok"]:
        print("✅ 可以开始下载（目录：%s）" % res["target"])
        return 0
    print("❌ 当前配置还不能直接下载，请先处理标记 ❌ 的项。")
    return 1


def _read_stdin_secret():
    value = sys.stdin.read().rstrip("\r\n")
    if not value:
        raise ValueError("stdin 没有收到密码")
    return value


def _save_engine_secret(eng, ref_key, legacy_key, value, secret_name):
    if not value:
        return True
    try:
        eng[ref_key] = keychain_store(secret_name, value)
        eng.pop(legacy_key, None)
    except (OSError, ValueError, RuntimeError) as exc:
        print("❌ 凭据未保存：%s" % exc)
        return False
    return True


def cmd_secret_set(args):
    try:
        value = _read_stdin_secret() if args.stdin else getpass.getpass("凭据（不回显）：")
        ref = keychain_store(args.name, value)
    except (OSError, EOFError, KeyboardInterrupt, ValueError, RuntimeError) as exc:
        print("❌ 凭据保存失败：%s" % exc)
        return 1
    print("✅ 已存入系统凭据库：%s（明文不写入 config.json）" % ref)
    return 0


def cmd_secret_check(args):
    names = [args.name] if args.name else sorted(configured_secret_refs(load_config()))
    rows = []
    for name in names:
        rows.append({"name": name, "present": bool(keychain_get(name))})
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        for row in rows:
            print("%s  %s" % ("✅" if row["present"] else "❌", row["name"]))
    return 0 if all(row["present"] for row in rows) else 1


def cmd_secret_delete(args):
    if keychain_delete(args.name):
        print("✅ 已从系统凭据库删除：%s" % args.name)
        return 0
    print("❌ 未找到或删除失败：%s" % args.name)
    return 1


def cmd_secret_list(args):
    cfg = load_config()
    refs = configured_secret_refs(cfg)
    rows = [{"name": name, "ref": ref, "present": bool(keychain_get(keychain_name(ref)))}
            for name, ref in sorted(refs.items())]
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        if not rows:
            print("未配置凭据引用。保存方式：pan secret set engine.webdav --stdin")
        for row in rows:
            print("%s  %-18s %s" % ("✅" if row["present"] else "❌", row["name"], row["ref"]))
    return 0


def cmd_secret_migrate(args):
    cfg = load_config()
    migrated, errors = migrate_plaintext_secrets(cfg)
    if errors:
        for item in errors:
            print("❌ %s" % item)
        return 1
    if migrated:
        path = save_config(cfg)
        print("✅ 已迁移 %d 项到系统凭据库：%s" % (len(migrated), path))
    else:
        print("未发现需要迁移的明文凭据")
    return 0


def cmd_set(args):
    cfg = load_config()
    if args.root is not None:
        cfg["download_root"] = args.root
    if args.tier is not None:
        cfg["tier"] = args.tier
    if args.engine is not None and args.engine_name:
        cfg.setdefault("engines", {})[args.engine_name] = args.engine
    if getattr(args, "auto_classify", "") in ("on", "off"):
        cfg.setdefault("smart", {})["auto_classify"] = (args.auto_classify == "on")
    eng = cfg.setdefault("engines", {})
    if args.alist_url:
        eng["alist_url"] = args.alist_url
    if args.alist_user:
        eng["alist_user"] = args.alist_user
    if args.rclone_remote:
        eng["rclone_remote"] = args.rclone_remote
    if args.webdav_url:
        eng["webdav_url"] = args.webdav_url
    if args.webdav_user:
        eng["webdav_user"] = args.webdav_user

    secret_values = (
        ("alist_password_ref", "alist_password", "engine.alist", args.alist_password, args.alist_password_stdin),
        ("webdav_password_ref", "webdav_password", "engine.webdav", args.webdav_password, args.webdav_password_stdin),
    )
    for ref_key, legacy_key, secret_name, legacy_value, from_stdin in secret_values:
        if legacy_value and from_stdin:
            print("❌ 同一凭据不能同时使用命令行和 --stdin")
            return 1
        try:
            value = _read_stdin_secret() if from_stdin else (legacy_value or "")
        except ValueError as exc:
            print("❌ %s" % exc)
            return 1
        if not _save_engine_secret(eng, ref_key, legacy_key, value, secret_name):
            return 1
        if legacy_value:
            print("⚠️ 为兼容旧命令已改存系统凭据库；以后请用 --stdin 或 secret set，避免命令行暴露")
    path = save_config(cfg)
    print("已保存：%s" % path)
    return 0


def cmd_set_drive(args):
    cfg = load_config()
    drives = cfg.setdefault("drives", {})
    entry = drives.setdefault(args.drive, {})
    if args.tier:
        entry["tier"] = args.tier
    if args.account_tier:
        entry["account_tier"] = args.account_tier
    if args.tier_detector:
        entry["tier_detector"] = args.tier_detector
    if args.cookie_file:
        entry["cookie_file"] = args.cookie_file
    if args.engine_command:
        entry["engine_command"] = args.engine_command
    if args.save_path:
        entry["save_path"] = args.save_path
    if args.credential_ref:
        try:
            entry["credential_ref"] = normalize_secret_ref(args.credential_ref)
        except ValueError as exc:
            print("❌ %s" % exc)
            return 1
    if args.credential_stdin:
        try:
            entry["credential_ref"] = keychain_store("drive." + args.drive, _read_stdin_secret())
        except (OSError, EOFError, ValueError, RuntimeError) as exc:
            print("❌ 凭据未保存：%s" % exc)
            return 1
    path = save_config(cfg)
    print("已保存 %s 配置：%s" % (args.drive, path))
    return 0


def _login_baidu_qr(args):
    """百度官方扫码登录：委托 pancli.baidu_login，登录态写入 BaiduPCS-Go。"""
    cfg = load_config()
    drive_key = getattr(args, "drive", "baidu")
    if "baidu" not in drive_key and "pan.baidu.com" not in drive_key:
        print("❌ --qr 目前只支持百度网盘")
        return 1
    binary = find_engine_binary("baidupcs", cfg) or "BaiduPCS-Go"
    if find_engine_binary("baidupcs", cfg) is None:
        print("⚠️ 未找到 BaiduPCS-Go，请先安装并 set-drive baidu --engine-command <路径>")
    from pancli.baidu_login import run as _qr_run
    res = _qr_run(binary, emit_json=bool(getattr(args, "json", False)))
    if getattr(args, "json", False):
        print(json.dumps(res, ensure_ascii=False))
    elif res.get("ok"):
        print("✅ 已登录 BaiduPCS-Go；接下来：pan get <链接> --engine baidupcs")
    else:
        print("❌ 扫码登录未完成：%s" % res.get("error", ""))
    return 0 if res.get("ok") else 1


def cmd_login(args):
    if getattr(args, "qr", False):
        return _login_baidu_qr(args)
    drive_key, spec = detect_drive(args.drive) if "://" in args.drive else (args.drive, all_drives(load_config()).get(args.drive, {}))
    if not spec:
        print("❌ 未找到网盘：%s（可用 detect 或 references/06-扩展新网盘.md 自定义）" % drive_key)
        return 1
    ref = SKILL_DIR / (spec.get("reference") or "references/00-使用说明.md")
    print("按以下文件完成一次登录（凭据只存本机系统凭据库/客户端配置）：%s" % ref)
    print("安全提示：账号、密码、Cookie、Token 不要发到聊天里；在本机终端用 pan secret set 保存。")
    if getattr(args, "open", False):
        import webbrowser as _wb
        try:
            opened = _wb.open(ref.resolve().as_uri())
        except Exception as _wexc:
            opened = False
            print("⚠️ 自动打开失败：%s（请手动打开上面路径）" % _wexc)
        if opened:
            print("已尝试用默认程序打开教程，请按文档完成授权后回到终端继续。")
    if ref.exists():
        text = ref.read_text(encoding="utf-8").splitlines()
        for line in text[:80]:
            print(line)
    return 0


REMOTE_KINDS = ("ssh", "rclone", "webdav", "smb", "s3", "mount")


def build_parser(lang="zh"):
    desc = ("Unified cloud-drive download entry (free-account default)." if lang == "en"
            else "多网盘统一下载入口（免费账号默认）")
    p = argparse.ArgumentParser(prog="pan", description=desc)
    i18n.add_lang_arg(p, default=lang)
    sub = p.add_subparsers(dest="cmd")

    d = sub.add_parser("doctor", help=("check environment and dependencies" if lang == "en" else "检查环境与依赖"))
    d.add_argument("--json", action="store_true")
    d.set_defaults(func=_lazy_cmd("pancli.setup", "cmd_doctor"))

    p_init = sub.add_parser("init", help=("create config file" if lang == "en" else "创建配置文件"))
    p_init.add_argument("--force", action="store_true")
    p_init.add_argument("--wizard", action="store_true", help="环境检测向导")
    p_init.add_argument("--json", action="store_true", help="输出 JSON")
    p_init.set_defaults(func=cmd_init)

    p_setup = sub.add_parser("setup", help=("one-click install + config wizard; local default, nas_docker/server_docker optional" if lang == "en" else "一键安装 + 配置向导；local 默认，nas_docker/server_docker 可选"))
    p_setup.add_argument("--root", help="设置默认下载目录")
    p_setup.add_argument("--mode", choices=["local", "nas_docker", "server_docker"], help="部署模式")
    p_setup.add_argument("--host", help="服务对外主机/IP")
    p_setup.add_argument("--port", type=int, default=17890, help="Web/API 端口")
    p_setup.add_argument("--api-url", help="Agent/插件使用的 API 地址")
    p_setup.add_argument("--alist-url", help="AList 服务地址")
    p_setup.add_argument("--rclone-remote", help="rclone 远端名，例如 alist:")
    p_setup.add_argument("--force", action="store_true", help="配置已存在也重新写入")
    p_setup.add_argument("--apply", action="store_true", help="兼容标志：仅列出安装命令，不自动执行")
    p_setup.add_argument("--json", action="store_true", help="输出 JSON")
    p_setup.set_defaults(func=_lazy_cmd("pancli.setup", "cmd_setup"))

    sub.add_parser("show", help=("show config (credentials masked)" if lang == "en" else "显示配置（凭据打码）")).set_defaults(func=cmd_show)

    p_auth = sub.add_parser("auth", help=("check login/auth hint after link recognition (local only, no network)" if lang == "en" else "链接识别后立即检查登录/授权提示（纯本地，不联网）"))
    p_auth.add_argument("url")
    p_auth.add_argument("--json", action="store_true", help="输出 JSON")
    p_auth.set_defaults(func=cmd_auth)

    p_route = sub.add_parser("route", help=("route a link: recognize + auth gate + preflight + next action (local)" if lang == "en" else "链接一次路由：识别 + 登录门禁 + 预检 + 下一步动作（纯本地）"))
    p_route.add_argument("url")
    p_route.add_argument("--pwd", help="分享提取码")
    p_route.add_argument("--engine")
    p_route.add_argument("--tier", choices=["free", "vip", "auto"])
    p_route.add_argument("--path", help="AList/WebDAV 已挂载路径")
    p_route.add_argument("--json", action="store_true", help="输出 JSON")
    p_route.add_argument("--brief", action="store_true", help="输出给 Agent 的最小 JSON，省 token")
    p_route.add_argument("--no-cache", action="store_true", help="跳过 2 秒本地路由短缓存")
    p_route.set_defaults(func=cmd_route)

    p_engines = sub.add_parser("engines", help=("show zero-client bridge, recommended path and local fallbacks" if lang == "en" else "查看零客户端桥、推荐路径与本地兼容回退"))
    p_engines.add_argument("url", nargs="?", default="", help="可选：只分析这一条链接")
    p_engines.add_argument("--json", action="store_true", help="输出 JSON")
    p_engines.set_defaults(func=cmd_engines)

    p_detect = sub.add_parser("detect", help=("identify which drive a link belongs to" if lang == "en" else "识别链接属于哪个网盘"))
    p_detect.add_argument("url")
    p_detect.add_argument("--json", action="store_true", help="输出 JSON（默认即 JSON）")
    p_detect.set_defaults(func=cmd_detect)

    p_direct = sub.add_parser("direct", help=("generic HTTP/HTTPS direct download (only public links you are authorized to download)" if lang == "en" else "通用 HTTP/HTTPS 直链下载（只下载你有授权的公开直链）"))
    p_direct.add_argument("url")
    p_direct.add_argument("--to", help="保存目录（默认当前目录）")
    p_direct.add_argument("--split", type=int, default=4, help="Range 分片并发数")
    p_direct.add_argument("--retries", type=int, default=3)
    p_direct.add_argument("--timeout", type=float, default=30)
    p_direct.add_argument("--sha256", help="下载后校验 SHA-256（hex）")
    p_direct.add_argument("--md5", help="下载后校验 MD5（hex）")
    p_direct.add_argument("--json", action="store_true", help="给 agent 输出 JSON")
    p_direct.add_argument("--confirm-own-use", action="store_true",
                          help="明确确认你已获授权/该内容为公开许可，非交互必需")
    p_direct.set_defaults(func=_lazy_cmd("pancli.carriers", "cmd_direct"))

    p_test = sub.add_parser("test", help=("test connection: recognize link and check deps/dirs (no download)" if lang == "en" else "测试连接：识别链接并检查依赖/目录是否就绪（不下载）"))
    p_test.add_argument("url")
    p_test.add_argument("--pwd", help="分享提取码")
    p_test.add_argument("--engine")
    p_test.add_argument("--tier", choices=["free", "vip", "auto"])
    p_test.add_argument("--path", help="AList/WebDAV 已挂载路径")
    p_test.add_argument("--json", action="store_true", help="给 agent 输出 JSON")
    p_test.set_defaults(func=cmd_test)

    p_set = sub.add_parser("set", help=("modify global config" if lang == "en" else "修改全局配置"))
    p_set.add_argument("--root")
    p_set.add_argument("--tier", choices=["free", "vip", "auto"])
    p_set.add_argument("--engine-name")
    p_set.add_argument("--engine")
    p_set.add_argument("--alist-url")
    p_set.add_argument("--alist-user")
    p_set.add_argument("--alist-password", help=argparse.SUPPRESS)
    p_set.add_argument("--alist-password-stdin", action="store_true", help="从 stdin 读取 AList 密码并存入系统凭据库")
    p_set.add_argument("--rclone-remote")
    p_set.add_argument("--webdav-url")
    p_set.add_argument("--webdav-user")
    p_set.add_argument("--webdav-password", help=argparse.SUPPRESS)
    p_set.add_argument("--webdav-password-stdin", action="store_true", help="从 stdin 读取 WebDAV 密码并存入系统凭据库")
    p_set.add_argument("--auto-classify", choices=["on", "off", ""], default="", help="智能默认：按扩展名自动归档（on/off）")
    p_set.set_defaults(func=cmd_set)

    p_sd = sub.add_parser("set-drive", help=("modify one drive config" if lang == "en" else "修改单个网盘配置"))
    p_sd.add_argument("drive")
    p_sd.add_argument("--tier", choices=["free", "vip", "auto"])
    p_sd.add_argument("--account-tier", choices=["free", "vip"])
    p_sd.add_argument("--tier-detector")
    p_sd.add_argument("--cookie-file")
    p_sd.add_argument("--credential-ref", help="绑定现有 credential:/keychain: 名称，不会打印密码")
    p_sd.add_argument("--credential-stdin", action="store_true", help="从 stdin 读取本网盘密码并存入系统凭据库")
    p_sd.add_argument("--engine-command")
    p_sd.add_argument("--save-path")
    p_sd.set_defaults(func=cmd_set_drive)

    p_secret = sub.add_parser("secret", help=("safely save/check/delete/migrate credentials" if lang == "en" else "安全保存、检查、删除或迁移凭据"))
    secret_sub = p_secret.add_subparsers(dest="secret_cmd")
    ps = secret_sub.add_parser("set", help="把密码写入系统凭据库")
    ps.add_argument("name")
    ps.add_argument("--stdin", action="store_true", help="从 stdin 读取，适合脚本/agent")
    ps.set_defaults(func=cmd_secret_set)
    pc = secret_sub.add_parser("check", help="检查指定凭据是否存在")
    pc.add_argument("name", nargs="?")
    pc.add_argument("--json", action="store_true")
    pc.set_defaults(func=cmd_secret_check)
    pl = secret_sub.add_parser("list", help="列出配置引用的凭据状态")
    pl.add_argument("--json", action="store_true")
    pl.set_defaults(func=cmd_secret_list)
    pd = secret_sub.add_parser("delete", help="从系统凭据库删除指定凭据")
    pd.add_argument("name")
    pd.set_defaults(func=cmd_secret_delete)
    pm = secret_sub.add_parser("migrate", help="把旧配置里的已知明文凭据迁入系统凭据库")
    pm.set_defaults(func=cmd_secret_migrate)

    p_login = sub.add_parser("login", help=("show login/authorization steps for a drive; Baidu supports --qr official QR" if lang == "en" else "查看某网盘的登录/授权步骤；百度支持 --qr 官方扫码"))
    p_login.add_argument("drive")
    p_login.add_argument("--open", action="store_true", help="用默认程序打开授权教程")
    p_login.add_argument("--qr", action="store_true", help="百度：走官方扫码登录，写入 BaiduPCS-Go 本机登录态")
    p_login.add_argument("--json", action="store_true", help="百度 --qr：以 JSON 输出结果")
    p_login.set_defaults(func=cmd_login)

    p_movie = sub.add_parser("movie", help=("free movie / X video / NAS download" if lang == "en" else "免费电影/X视频/NAS 下载"))
    movie_sub = p_movie.add_subparsers(dest="movie_cmd")
    ms = movie_sub.add_parser("sources", help="列出公开/公版/官方免费电影资源入口")
    ms.add_argument("--json", action="store_true", help="给 agent 输出 JSON")
    ms.set_defaults(func=_lazy_cmd("pancli.search_movie", "cmd_movie"))
    mg = movie_sub.add_parser("get", help="多候选直链测速后选最快下载（可 --remote 交给 NAS）")
    mg.add_argument("url")
    mg.add_argument("--candidates", help="逗号分隔的其余候选链接")
    mg.add_argument("--remote", help="下载到已登记的远程设备（remote add 创建）")
    mg.add_argument("--to", help="指定下载目录")
    mg.add_argument("--engine")
    mg.add_argument("--tier", choices=["free", "vip", "auto"])
    mg.add_argument("--path", help="AList 中已挂载的路径")
    mg.add_argument("--timeout", type=int, default=6, help="每个候选测速超时秒（默认 6）")
    mg.add_argument("--samples", type=int, default=200000, help="每个候选吸取字节数（默认 200000）")
    mg.add_argument("--dry-run", action="store_true", help="只打印计划，不实际下载")
    mg.add_argument("--force", action="store_true", help="依赖缺失时也尝试执行")
    mg.add_argument("--json", action="store_true", help="给 agent 输出 JSON")
    mg.add_argument("--events", action="store_true", help="实际下载时输出逐步 JSON 事件")
    mg.add_argument("--live", action="store_true", help="写入实时速度状态文件")
    mg.add_argument("--split", type=int, default=0, help="http 直链单文件 Range 分片并发数（默认0=关闭）")
    mg.add_argument("--at", default="", help="定时/低峰：HH:MM")
    mg.add_argument("--generic-direct", action="store_true", help="http/https 直链改走通用 http_downloader 模块")
    mg.add_argument("--confirm-own-use", action="store_true", help="与 --generic-direct 搭配：确认授权")
    mg.add_argument("--classify", action="store_true", default=None, help="按扩展名自动归档")
    mg.set_defaults(func=_lazy_cmd("pancli.search_movie", "cmd_movie"))
    mx = movie_sub.add_parser("x", help="下载 X(原推特) 视频（走 yt-dlp）")
    mx.add_argument("url")
    mx.add_argument("--remote", help="下载到已登记的远程设备")
    mx.add_argument("--to", help="指定下载目录")
    mx.add_argument("--tier", choices=["free", "vip", "auto"])
    mx.add_argument("--dry-run", action="store_true", help="只打印计划，不实际下载")
    mx.add_argument("--force", action="store_true", help="依赖缺失时也尝试执行")
    mx.add_argument("--json", action="store_true", help="给 agent 输出 JSON")
    mx.add_argument("--live", action="store_true", help="写入实时速度状态文件")
    mx.add_argument("--classify", action="store_true", default=None, help="按扩展名自动归档")
    mx.set_defaults(func=_lazy_cmd("pancli.search_movie", "cmd_movie"))

    p_search = sub.add_parser("search", help=("search web for documents/movies/videos/music candidates, one-command download" if lang == "en" else "联网搜索资料/电影/视频/音乐候选，可一键下载"))
    p_search.add_argument("query", nargs="?", default="", help="要搜索的关键词")
    p_search.add_argument("--kind", choices=SEARCH_KINDS, default="auto", help="候选类型：auto/movie/video/music/file")
    p_search.add_argument("--providers", default="auto", help="搜索源：auto/archive,duckduckgo,ytdlp")
    p_search.add_argument("--limit", type=int, default=8, help="每个源最多候选数（默认 8）")
    p_search.add_argument("--timeout", type=int, default=20, help="单个源搜索超时秒（默认 20）")
    p_search.add_argument("--list-providers", action="store_true", help="列出可用搜索源")
    p_search.add_argument("--check", action="store_true", help="检查各搜索源连通性（不搜索）")
    p_search.add_argument("--assume-own", action="store_true", help="明确确认你对该网页候选内容有权访问（下载网页搜索候选需要此确认）")
    p_search.add_argument("--pick", type=int, default=0, help="选中第 N 个候选直接下载")
    p_search.add_argument("--remote", help="下载到已登记的远程设备（remote add 创建）")
    p_search.add_argument("--to", help="指定下载目录")
    p_search.add_argument("--engine")
    p_search.add_argument("--tier", choices=["free", "vip", "auto"])
    p_search.add_argument("--path", help="AList 中已挂载的路径")
    p_search.add_argument("--dry-run", action="store_true", help="只打印计划，不实际下载")
    p_search.add_argument("--force", action="store_true", help="依赖缺失时也尝试执行")
    p_search.add_argument("--json", action="store_true", help="给 agent 输出 JSON")
    p_search.add_argument("--live", action="store_true", help="写入实时速度状态文件")
    p_search.add_argument("--split", type=int, default=0, help="http 直链单文件 Range 分片并发数（默认0=关闭）")
    p_search.add_argument("--classify", action="store_true", default=None, help="按扩展名自动归档")
    p_search.set_defaults(func=_lazy_cmd("pancli.search_movie", "cmd_search"))

    p_crawl = sub.add_parser("crawl", help=("crawler: harvest media/file/magnet candidates from directory pages" if lang == "en" else "网络爬虫：抓取网页目录页里的媒体/文件/磁力候选并一键下载"))
    p_crawl.add_argument("url", nargs="?", help="要抓取的网页 URL（可含 HTTP/FTP/HTTPS 页面）")
    p_crawl.add_argument("--kind", choices=SEARCH_KINDS, default="auto", help="候选类型：auto/movie/video/music/file")
    p_crawl.add_argument("--limit", type=int, default=20, help="最多候选数（默认 20）")
    p_crawl.add_argument("--timeout", type=int, default=20, help="单页抓取超时秒（默认 20）")
    p_crawl.add_argument("--depth", type=int, default=0, help="是否跟进同域分页/目录页（0=单页，1=最多跟进 5 个子页）")
    p_crawl.add_argument("--assume-own", action="store_true", help="明确确认你对该网页候选内容有权访问")
    p_crawl.add_argument("--pick", type=int, default=0, help="选中第 N 个候选直接下载")
    p_crawl.add_argument("--remote", help="下载到已登记的远程设备（remote add 创建）")
    p_crawl.add_argument("--to", help="指定下载目录")
    p_crawl.add_argument("--engine")
    p_crawl.add_argument("--tier", choices=["free", "vip", "auto"])
    p_crawl.add_argument("--path", help="AList 中已挂载的路径")
    p_crawl.add_argument("--dry-run", action="store_true", help="只打印计划，不实际下载")
    p_crawl.add_argument("--force", action="store_true", help="依赖缺失时也尝试执行")
    p_crawl.add_argument("--json", action="store_true", help="给 agent 输出 JSON")
    p_crawl.add_argument("--live", action="store_true", help="写入实时速度状态文件")
    p_crawl.add_argument("--split", type=int, default=0, help="http 直链单文件 Range 分片并发数")
    p_crawl.add_argument("--classify", action="store_true", default=None, help="按扩展名自动归档")
    p_crawl.set_defaults(func=_lazy_cmd("pancli.search_movie", "cmd_crawl"))

    p_docker = sub.add_parser("docker", help=("generate/check Docker/NAS run files (no system install)" if lang == "en" else "生成/检查 Docker/NAS 运行文件（不执行系统安装）"))
    p_docker.add_argument("docker_cmd", nargs="?", default="files", help="files（默认）：生成 Docker 文件；check：检测 docker 可用性并校验文件")
    p_docker.add_argument("--out", help="输出目录（默认 技能根目录/docker）")
    p_docker.add_argument("--json", action="store_true", help="给 agent 输出 JSON")
    p_docker.set_defaults(func=_lazy_cmd("pancli.docker", "cmd_docker"))

    p_probe = sub.add_parser("probe", help=("probe multiple candidate direct links and recommend fastest" if lang == "en" else "对多个候选直链真实测速，推荐最快（默认各取前约 200KB）"))
    p_probe.add_argument("url", nargs="?", help="第一个候选链接")
    p_probe.add_argument("--candidates", help="逗号分隔的其余候选链接")
    p_probe.add_argument("--timeout", type=int, default=6)
    p_probe.add_argument("--samples", type=int, default=200000, help="每个候选吸取字节数（默认 200000）")
    p_probe.add_argument("--json", action="store_true", help="给 agent 输出 JSON")
    p_probe.set_defaults(func=_lazy_cmd("pancli.docker", "cmd_probe"))

    p_get = sub.add_parser("get", help=("download a share link or direct link" if lang == "en" else "下载分享链接或直链"))
    p_get.add_argument("url")
    p_get.add_argument("--pwd", help="分享提取码")
    p_get.add_argument("--at", dest="at", default="", help="定时/低峰：HH:MM（如 --at 02:30），到点再开始下载；over 当前时间则立即用配置默认")
    p_get.add_argument("--to", help="指定下载目录")
    p_get.add_argument("--engine")
    p_get.add_argument("--tier", choices=["free", "vip", "auto"])
    p_get.add_argument("--path", help="AList 中已挂载的路径")
    p_get.add_argument("--remote", help="下载到已登记的远程设备（remote add 创建）")
    p_get.add_argument("--dry-run", action="store_true", help="只打印计划，不实际下载")
    p_get.add_argument("--force", action="store_true", help="依赖缺失时也尝试执行")
    p_get.add_argument("--json", action="store_true", help="给 agent 输出无凭据 JSON")
    p_get.add_argument("--events", action="store_true", help="实际下载时输出逐步 JSON 事件")
    p_get.add_argument("--live", action="store_true", help="写入实时速度状态文件（下载速度.live.json），可在 serve 页面查看")
    p_get.add_argument("--no-web", dest="no_web", action="store_true", help="本次下载不自动启动/打开 Web UI")
    p_get.add_argument("--split", type=int, default=0, help="http 直链单文件 Range 分片并发数（默认0=关闭，仅对支持 Range 的直链生效）")
    p_get.add_argument("--classify", action="store_true", default=None, help="按扩展名自动归档到 影视/音乐/文档/图片/压缩包/其他（覆盖 smart.auto_classify，未开启时可手动启用）")
    p_get.add_argument("--generic-direct", action="store_true",
                       help="http/https 直链改走通用 http_downloader 模块（需 --confirm-own-use）")
    p_get.add_argument("--confirm-own-use", action="store_true",
                       help="与 --generic-direct 搭配：确认你对该直链拥有下载/使用授权")
    p_get.set_defaults(func=_lazy_cmd("pancli.carriers", "cmd_get"))

    p_remote = sub.add_parser("remote", help="管理 NAS、飞牛、群晖、私有云盘等远程设备")
    remote_sub = p_remote.add_subparsers(dest="remote_cmd")
    ra = remote_sub.add_parser("add", help="登记或修改远程设备（不保存明文密码）")
    ra.add_argument("name")
    ra.add_argument("--kind", choices=REMOTE_KINDS)
    ra.add_argument("--host")
    ra.add_argument("--port")
    ra.add_argument("--user")
    ra.add_argument("--root", help="远程下载根目录；mount 类型填本机挂载路径")
    ra.add_argument("--remote-name", help="rclone 配置里的 remote 名，例如 nas")
    ra.add_argument("--python", default=None, help="SSH 远程 Python 命令，默认 python3")
    ra.add_argument("--deploy-dir", help="SSH 远程技能目录，默认 .pan-downloader")
    ra.add_argument("--web-port", type=int, default=None, help="默认远程 Web 端口（remote deploy 未显式指定时使用）")
    ra.add_argument("--web-host", default=None, help="默认远程 Web 监听地址（127.0.0.1 或 0.0.0.0）")
    ra.add_argument("--description")
    ra.add_argument("--credential-ref", help="已有系统凭据引用；只保存引用，不保存明文")
    ra.add_argument("--credential-stdin", action="store_true", help="从 stdin 读取远程凭据并存系统凭据库")
    ra.set_defaults(func=_lazy_cmd("pancli.remote", "cmd_remote_add"))

    rl = remote_sub.add_parser("list", help="列出远程设备（不含密码）")
    rl.add_argument("--json", action="store_true")
    rl.set_defaults(func=_lazy_cmd("pancli.remote", "cmd_remote_list"))

    rr = remote_sub.add_parser("remove", help="删除远程设备配置（不删除下载文件）")
    rr.add_argument("name")
    rr.set_defaults(func=_lazy_cmd("pancli.remote", "cmd_remote_remove"))

    rc = remote_sub.add_parser("check", help="检查远程配置；可选 --probe 联网探测")
    rc.add_argument("name")
    rc.add_argument("--probe", action="store_true")
    rc.add_argument("--json", action="store_true")
    rc.set_defaults(func=_lazy_cmd("pancli.remote", "cmd_remote_check"))

    rd = remote_sub.add_parser("deploy", help="把无凭据技能包部署到 SSH 设备；可选 --web-port 后台启动远程 Web 控制页")
    rd.add_argument("name")
    rd.add_argument("--web-port", type=int, default=0, help="部署后远程后台启动 serve（默认 0=不启动；示例 17890）")
    rd.add_argument("--web-host", default=None, help="远程 Web 监听地址（默认 127.0.0.1；局域网访问填 0.0.0.0）")
    rd.add_argument("--web-reports-dir", default=None, help="远程 Web 报告目录（默认远程 root，可扫描实时速度与历史报告）")
    rd.add_argument("--dry-run", action="store_true")
    rd.add_argument("--json", action="store_true", help="输出打码后的部署计划，不执行上传")
    rd.set_defaults(func=_lazy_cmd("pancli.remote", "cmd_remote_deploy"))

    rw = remote_sub.add_parser("web", help="打印远程 Web 控制页访问地址与 SSH 反向隧道命令（不实际连接）")
    rw.add_argument("name")
    rw.add_argument("--port", type=int, default=0, help="远程 Web 端口（默认取配置/17890）")
    rw.add_argument("--host", default=None, help="远程监听地址（默认取配置/127.0.0.1）")
    rw.add_argument("--local-port", type=int, default=0, help="本机反向隧道端口（默认同远程端口）")
    rw.add_argument("--json", action="store_true", help="输出 JSON 访问信息")
    rw.set_defaults(func=_lazy_cmd("pancli.remote", "cmd_remote_web"))

    rg = remote_sub.add_parser("get", help="从分享链接下载到指定远程设备")
    rg.add_argument("name")
    rg.add_argument("url")
    rg.add_argument("--pwd", help="分享提取码")
    rg.add_argument("--to", help="覆盖远程目标目录")
    rg.add_argument("--engine")
    rg.add_argument("--tier", choices=["free", "vip", "auto"])
    rg.add_argument("--path", help="AList 中已挂载的路径")
    rg.add_argument("--live", action="store_true", help="远程下载时写入实时速度文件，供远程 Web 页面查看")
    rg.add_argument("--dry-run", action="store_true", help="只打印计划，不实际下载")
    rg.add_argument("--force", action="store_true", help="依赖缺失时也尝试执行")
    rg.add_argument("--json", action="store_true", help="给 agent 输出无凭据 JSON")
    rg.set_defaults(func=_lazy_cmd("pancli.remote", "cmd_remote_get"))

    p_dirs = sub.add_parser("dirs", help="查看默认下载目录")
    p_dirs.add_argument("--json", action="store_true", help="输出 JSON")
    p_dirs.set_defaults(func=_lazy_cmd("pancli.carriers", "cmd_dirs"))

    p_idle = sub.add_parser("idle", help="闲时下载队列（add/list/delete/run；窗口默认 00:00-08:00）")
    idle_sub = p_idle.add_subparsers(dest="idle_cmd")
    ia = idle_sub.add_parser("add", help="把一个下载链接排入闲时队列")
    ia.add_argument("url")
    ia.add_argument("pass_through", nargs=argparse.REMAINDER,
                    help="透传给 pan get 的参数（如 -- --to /path --split 4）")
    ia.set_defaults(func=_lazy_cmd("pancli.idle", "cmd_idle"))
    idl = idle_sub.add_parser("list", help="查看闲时队列")
    idl.add_argument("--json", action="store_true")
    idl.set_defaults(func=_lazy_cmd("pancli.idle", "cmd_idle"))
    idd = idle_sub.add_parser("delete", help="删除队列任务")
    idd.add_argument("id")
    idd.set_defaults(func=_lazy_cmd("pancli.idle", "cmd_idle"))
    idr = idle_sub.add_parser("run", help="启动 idle-daemon（前台常驻；--once 单轮；--print-crontab 只打印不安装）")
    idr.add_argument("--once", action="store_true", help="只投递一轮（自测/手动触发）")
    idr.add_argument("--print-crontab", dest="print_crontab", action="store_true",
                     help="打印现成 cron 条目，不自动安装（红线）")
    idr.set_defaults(func=_lazy_cmd("pancli.idle", "cmd_idle"))

    p_task = sub.add_parser("task", help="任务控制（list/show/pause/resume/delete/retry）")
    p_task.add_argument("--json", action="store_true", help="输出 JSON")
    p_task.add_argument("--reports-dir", default="", help="报告目录（默认读配置 http.report_dir/live_dir）")
    task_sub = p_task.add_subparsers(dest="task_cmd")
    tl = task_sub.add_parser("list", help="任务列表")
    tl.add_argument("--state", default="", help="按状态过滤：running/done/failed/paused/cancelled")
    tl.set_defaults(func=_lazy_cmd("pancli.carriers", "cmd_task"))
    ts = task_sub.add_parser("show", help="查看单任务详情")
    ts.add_argument("id")
    ts.set_defaults(func=_lazy_cmd("pancli.carriers", "cmd_task"))
    for name in ("pause", "resume", "delete", "retry"):
        tp = task_sub.add_parser(name, help="%s 指定任务" % name)
        tp.add_argument("id")
        tp.set_defaults(func=_lazy_cmd("pancli.carriers", "cmd_task"))

    p_tr = sub.add_parser("transfer", help="AList/rclone 跨盘转存（rclone copy，默认 dry-run）")
    p_tr.add_argument("src")
    p_tr.add_argument("dst")
    p_tr.add_argument("--transfers", type=int, default=0)
    p_tr.add_argument("--checkers", type=int, default=0)
    p_tr.add_argument("--apply", action="store_true", help="实际执行 rclone copy（默认只打印 dry-run）")
    p_tr.add_argument("--json", action="store_true", help="输出 JSON 计划")
    p_tr.add_argument("--allow-company-dest", action="store_true", help="明确允许写入公司目录（默认禁止）")
    p_tr.set_defaults(func=_lazy_cmd("pancli.carriers", "cmd_transfer"))

    p_sync = sub.add_parser("sync", help="增量同步（rclone sync，会删除目标多余文件，需 --delete + --apply）")
    p_sync.add_argument("src")
    p_sync.add_argument("dst")
    p_sync.add_argument("--delete", action="store_true", help="允许删除目标多余文件（必须显式）")
    p_sync.add_argument("--transfers", type=int, default=0)
    p_sync.add_argument("--checkers", type=int, default=0)
    p_sync.add_argument("--apply", action="store_true", help="实际执行 rclone sync")
    p_sync.add_argument("--json", action="store_true", help="输出 JSON 计划")
    p_sync.add_argument("--allow-company-dest", action="store_true", help="明确允许写入公司目录（默认禁止）")
    p_sync.set_defaults(func=_lazy_cmd("pancli.carriers", "cmd_sync"))

    p_notify = sub.add_parser("notify", help="发送完成/失败通知（webhook 地址存系统凭据库，默认 dry-run）")
    p_ns = p_notify.add_subparsers(dest="notify_cmd")
    ns = p_ns.add_parser("send", help="发送通知")
    ns.add_argument("--channel", choices=["work_weixin", "bark", "telegram", "discord", "feishu"], default="work_weixin")
    ns.add_argument("--chat-id", default="", help="telegram 必填：接收消息的 chat_id")
    ns.add_argument("--title", default="pan-downloader")
    ns.add_argument("--body", default="")
    ns.add_argument("--send", action="store_true", help="真正发送（默认只渲染 dry-run）")
    ns.add_argument("--json", action="store_true", help="输出 JSON")
    ns.set_defaults(func=_lazy_cmd("pancli.carriers", "cmd_notify_send"))

    p_mcp = sub.add_parser("mcp", help="MCP 注册指引")
    pm = p_mcp.add_subparsers(dest="mcp_cmd")
    mg = pm.add_parser("guide", help="输出 Codex MCP 注册片段")
    mg.add_argument("--json", action="store_true")
    mg.set_defaults(func=_lazy_cmd("pancli.setup", "cmd_mcp_guide"))

    p_guard = sub.add_parser("guard", help="单实例锁 / 后台守护 / 限速与 ETA 预估")
    p_guard.add_argument("action", nargs="?", default="status",
                         choices=["status", "locks", "clean", "speed", "eta", "daemon", "error"])
    p_guard.add_argument("--drive", default="", help="网盘 key，如 baidu")
    p_guard.add_argument("--source", default="", help="远端来源路径（当前仅用于展示）")
    p_guard.add_argument("--target", default="", help="下载目录（speed 采样用）")
    p_guard.add_argument("--seconds", type=int, default=20, help="吞吐采样秒数")
    p_guard.add_argument("--total", type=float, default=0, help="eta：总字节数")
    p_guard.add_argument("--bps", type=float, default=0, help="eta：每秒字节数")
    p_guard.add_argument("--cmd", default="", help="daemon：要后台执行的命令")
    p_guard.add_argument("--log", default="", help="daemon：日志文件")
    p_guard.add_argument("--text", default="", help="error：要归类的错误文本")
    p_guard.add_argument("--json", action="store_true")
    p_guard.set_defaults(func=_lazy_cmd("pancli.guard", "cmd_guard"))

    p_live = sub.add_parser("live", help="实时进度：把外部 BaiduPCS-Go 日志接入 Web UI")
    p_live_sub = p_live.add_subparsers(dest="live_cmd")
    p_live_attach = p_live_sub.add_parser("attach", help="接入 BaiduPCS-Go 下载日志并持续写入实时状态")
    p_live_attach.add_argument("--log", required=True, help="BaiduPCS-Go 下载日志路径")
    p_live_attach.add_argument("--target", required=True, help="实际下载目录（Web UI 下载位置）")
    p_live_attach.add_argument("--total-bytes", type=int, default=0, help="分享总字节数；不填则只显示当前分片批次")
    p_live_attach.add_argument("--files-total", type=int, default=0, help="分享文件总数")
    p_live_attach.add_argument("--url", default="", help="分享链接（会自动脱敏提取码）")
    p_live_attach.add_argument("--pid", type=int, default=0, help="BaiduPCS-Go 进程 PID；进程退出后自动结束监控")
    p_live_attach.add_argument("--interval", type=float, default=1.0, help="采样间隔秒（默认 1.0）")
    p_live_attach.add_argument("--state-dir", default="", help="Web UI 状态目录；需与 pan serve --reports-dir 一致")
    p_live_attach.add_argument("--once", action="store_true", help="只写一次状态后退出，适合测试")
    p_live_attach.add_argument("--open", action="store_true", help="自动启动/复用 Web UI 并打开 /live")
    p_live_attach.add_argument("--json", action="store_true", help="输出实时状态 JSON")
    p_live_attach.set_defaults(func=_lazy_cmd("pancli.report", "cmd_live_attach"))

    p_serve = sub.add_parser("serve", help="Web 控制台（任务投递/设置等写接口，token 鉴权；默认 127.0.0.1:17890）")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=17890)
    p_serve.add_argument("--reports-dir", default="", help="报告目录（默认读配置 http.report_dir）")
    p_serve.set_defaults(func=_web_cmd("cmd_serve"))
    return p


def main(argv=None):
    raw = list(sys.argv[1:] if argv is None else argv)
    lang = i18n.argv_lang(raw)
    parser = build_parser(lang=lang)
    args = parser.parse_args(raw)
    if not getattr(args, "func", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())


def _web_cmd(name):
    """懒加载 Web 子模块的可调用命令（避免与 engine 相互 import 造成循环）。"""

    def _run(args, **kw):
        from pancli import web as _web
        return getattr(_web, name)(args, **kw)

    return _run


def _lazy_cmd(module_name, func_name):
    """通用懒加载命令代理。"""

    def _run(args, **kw):
        import importlib
        mod = importlib.import_module(module_name)
        return getattr(mod, func_name)(args, **kw)

    _run._lazy_module = module_name
    _run._lazy_func = func_name
    return _run
