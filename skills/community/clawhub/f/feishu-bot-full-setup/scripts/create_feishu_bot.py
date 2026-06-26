#!/usr/bin/env python3
"""
飞书开放平台 - 自动创建企业自建机器人

用途:
    1. 扫码登录飞书开放平台
    2. 创建企业自建应用
    3. 开启机器人能力
    4. 导入完整权限
    5. 添加事件订阅并切换为长连接
    6. 添加卡片回调并切换为长连接
    7. 创建版本并提交发布
    8. 给创建者发送成功通知
    9. 返回 app_id 和 app_secret

命令:
    python3 scripts/create_feishu_bot.py init
    python3 scripts/create_feishu_bot.py create
    python3 scripts/create_feishu_bot.py cleanup

输出:
    `create` 成功时，stdout 只输出一行 JSON:
    {"app_id": "...", "app_secret": "..."}

可选环境变量:
    FEISHU_BOT_BROWSER_PATH                 指定已安装浏览器路径，跳过 Playwright 浏览器下载
    PLAYWRIGHT_CHROMIUM_DOWNLOAD_HOST      指定 Chromium 下载源
    PLAYWRIGHT_DOWNLOAD_HOST               指定通用下载源
    PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT 指定下载连接超时（毫秒）
    FEISHU_BOT_QR_PNG_PATH                 登录二维码 PNG 输出路径
    FEISHU_BOT_NAME                        指定机器人名称
    FEISHU_BOT_NAME_PREFIX                 未指定名称时使用此前缀生成默认名称
    FEISHU_BOT_DESC                        指定机器人描述
    FEISHU_BOT_SIGNATURE                   描述别名，优先级高于 FEISHU_BOT_DESC
    FEISHU_BOT_AVATAR_PATH                 指定本地头像文件路径
    FEISHU_BOT_AVATAR_URL                  指定头像下载地址
"""

import importlib
import importlib.util
import json
import mimetypes
import os
import random
import shutil
import signal
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(write_through=True)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(write_through=True)

_REQUIRED_PACKAGES = [
    ("playwright", "playwright"),
    ("qrcode", "qrcode"),
    ("PIL", "pillow"),
]

_SYSTEM_BROWSER_CANDIDATES = [
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "chrome",
]

BASE_URL = "https://open.feishu.cn"
API_BASE = f"{BASE_URL}/developers/v1"
APP_PAGE = f"{BASE_URL}/app"
PASSPORT_BASE = "https://passport.feishu.cn"
LOGIN_URL = (
    "https://accounts.feishu.cn/accounts/page/login"
    "?app_id=7&no_trap=1"
    "&redirect_uri=https%3A%2F%2Fopen.feishu.cn%2Fapp"
)

STATE_DIR = "/tmp"
PROFILE_DIR = os.path.join(STATE_DIR, "feishu-bot-chrome-profile")
AVATAR_PATH = os.path.join(STATE_DIR, "feishu-bot-avatar.png")
CDP_PID_PATH = os.path.join(STATE_DIR, "feishu-bot-chrome.pid")
QR_PNG_PATH = (
    os.environ.get("FEISHU_BOT_QR_PNG_PATH")
    or os.path.join(STATE_DIR, "feishu-login-qr.png")
)
LOGIN_TIMEOUT = 90
QR_MAX_RETRIES = 3
APP_VERSION = "0.0.1"

AVATAR_URL = (
    "https://cloudcache.tencent-cloud.com/qcloud/ui/static/"
    "other_external_resource/4e9ca8c5-0ce4-44a2-8c7c-4f8f43f9e73a.png"
)

BOT_SCOPES = {
    "tenant": [
        "application:application:self_manage",
        "cardkit:card:read",
        "cardkit:card:write",
        "contact:contact.base:readonly",
        "contact:user.basic_profile:readonly",
        "docx:document:readonly",
        "im:chat:read",
        "im:chat:update",
        "im:message.group_at_msg:readonly",
        "im:message.p2p_msg:readonly",
        "im:message.pins:read",
        "im:message.pins:write_only",
        "im:message.reactions:read",
        "im:message.reactions:write_only",
        "im:message:readonly",
        "im:message:recall",
        "im:message:send_as_bot",
        "im:message:send_multi_users",
        "im:message:send_sys_msg",
        "im:message:update",
        "im:resource",
    ],
    "user": [
        "base:app:copy",
        "base:app:create",
        "base:app:read",
        "base:app:update",
        "base:field:create",
        "base:field:delete",
        "base:field:read",
        "base:field:update",
        "base:record:create",
        "base:record:delete",
        "base:record:retrieve",
        "base:record:update",
        "base:table:create",
        "base:table:read",
        "base:table:update",
        "base:view:read",
        "base:view:write_only",
        "board:whiteboard:node:create",
        "board:whiteboard:node:read",
        "calendar:calendar.event:create",
        "calendar:calendar.event:read",
        "calendar:calendar.event:reply",
        "calendar:calendar.event:update",
        "calendar:calendar.free_busy:read",
        "calendar:calendar:read",
        "contact:contact.base:readonly",
        "contact:user.base:readonly",
        "contact:user.basic_profile:readonly",
        "contact:user.employee_id:readonly",
        "contact:user:search",
        "docs:document.comment:create",
        "docs:document.comment:read",
        "docs:document.comment:update",
        "docs:document.media:download",
        "docs:document.media:upload",
        "docs:document:copy",
        "docs:document:export",
        "docx:document:create",
        "docx:document:readonly",
        "docx:document:write_only",
        "drive:drive.metadata:readonly",
        "drive:file:download",
        "drive:file:upload",
        "im:chat.members:read",
        "im:chat:read",
        "im:message",
        "im:message.group_msg:get_as_user",
        "im:message.p2p_msg:get_as_user",
        "im:message:readonly",
        "offline_access",
        "search:docs:read",
        "search:message",
        "sheets:spreadsheet.meta:read",
        "sheets:spreadsheet:create",
        "sheets:spreadsheet:read",
        "sheets:spreadsheet:write_only",
        "space:document:move",
        "space:document:retrieve",
        "task:comment:read",
        "task:comment:write",
        "task:task:read",
        "task:task:write",
        "task:task:writeonly",
        "task:tasklist:write",
        "wiki:node:copy",
        "wiki:node:create",
        "wiki:node:move",
        "wiki:node:read",
        "wiki:node:retrieve",
        "wiki:space:read",
        "wiki:space:retrieve",
        "wiki:space:write_only",
    ],
}

BOT_EVENTS = [
    "im.message.receive_v1",
    "im.message.reaction.created_v1",
    "im.message.reaction.deleted_v1",
]

BOT_CALLBACKS = [
    "card.action.trigger",
]

LONG_CONNECTION_MODE = 4

SCOPE_NAME_ALIASES = {
    "contact:user.basic_profile:readonly": [
        "contact:user.basic_profile:readonly",
        "contact:user.base:readonly",
    ],
}


def _status(step: str, message: str) -> None:
    print(f"[{step}] {message}", file=sys.stderr, flush=True)


def _warn(step: str, message: str) -> None:
    print(f"[{step}] WARNING: {message}", file=sys.stderr, flush=True)


def _fail(step: str, message: str, exit_code: int = 1) -> None:
    print(f"[{step}] ERROR: {message}", file=sys.stderr, flush=True)
    sys.exit(exit_code)


def _ensure_pip() -> None:
    try:
        importlib.import_module("pip")
        return
    except ImportError:
        pass

    try:
        subprocess.check_call(
            [sys.executable, "-m", "ensurepip", "--upgrade"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
        urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", f.name)
        subprocess.check_call(
            [sys.executable, f.name, "--quiet", "--break-system-packages"]
        )


def _build_playwright_install_env() -> dict:
    env = os.environ.copy()
    env["PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD"] = "0"
    env["DEBIAN_FRONTEND"] = "noninteractive"
    env.setdefault("PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT", "120000")
    return env


def _candidate_browser_paths():
    explicit = os.environ.get("FEISHU_BOT_BROWSER_PATH", "").strip()
    if explicit:
        yield explicit

    for name in _SYSTEM_BROWSER_CANDIDATES:
        path = shutil.which(name)
        if path:
            yield path


def _is_usable_browser(path: str) -> bool:
    if not path or not os.path.isfile(path) or not os.access(path, os.X_OK):
        return False
    try:
        subprocess.check_call(
            [path, "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except (OSError, subprocess.CalledProcessError):
        return False


def _find_system_browser() -> Optional[str]:
    for path in _candidate_browser_paths():
        if _is_usable_browser(path):
            return path
    return None


def _install_system_deps() -> None:
    libs_yum = [
        "nss",
        "nspr",
        "atk",
        "at-spi2-atk",
        "at-spi2-core",
        "libdrm",
        "libXcomposite",
        "libXdamage",
        "libXrandr",
        "mesa-libgbm",
        "pango",
        "cups-libs",
        "libxkbcommon",
        "alsa-lib",
        "libXfixes",
        "libxshmfence",
    ]
    libs_apt = [
        "libnss3",
        "libnspr4",
        "libatk1.0-0",
        "libatk-bridge2.0-0",
        "libdrm2",
        "libxcomposite1",
        "libxdamage1",
        "libxrandr2",
        "libgbm1",
        "libpango-1.0-0",
        "libcups2",
        "libxkbcommon0",
        "libasound2",
        "libxfixes3",
        "libxshmfence1",
    ]

    for pkg_mgr, libs in [
        (["yum", "install", "-y"], libs_yum),
        (["dnf", "install", "-y"], libs_yum),
        (["apt-get", "install", "-y"], libs_apt),
    ]:
        try:
            subprocess.check_call(
                [pkg_mgr[0], "--version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
        try:
            subprocess.call(
                pkg_mgr + libs,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            pass
        return


def _ensure_dependencies() -> None:
    missing = [pip for mod, pip in _REQUIRED_PACKAGES if not importlib.util.find_spec(mod)]
    if missing:
        _status("init", f"安装 Python 依赖: {', '.join(missing)}")
        _ensure_pip()
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet", "--break-system-packages"] + missing
        )
        importlib.invalidate_caches()

    system_browser = _find_system_browser()
    if system_browser:
        _status("init", f"使用系统浏览器: {system_browser}")
        return

    from playwright.sync_api import sync_playwright

    try:
        pw = sync_playwright().start()
        pw.chromium.launch(headless=True).close()
        pw.stop()
        return
    except Exception:
        pass

    _status("init", "未检测到可用浏览器，准备安装 Playwright Chromium")
    _install_system_deps()
    env = _build_playwright_install_env()
    host = env.get("PLAYWRIGHT_CHROMIUM_DOWNLOAD_HOST") or env.get("PLAYWRIGHT_DOWNLOAD_HOST")
    if host:
        _status("init", f"使用下载源: {host}")
    subprocess.check_call(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        env=env,
    )


def _env(name: str) -> str:
    return os.environ.get(name, "").strip()


def _resolve_bot_name() -> str:
    explicit_name = _env("FEISHU_BOT_NAME")
    if explicit_name:
        return explicit_name

    prefix = _env("FEISHU_BOT_NAME_PREFIX") or "OpenClaw机器人"
    return f"{prefix}-{random.randint(1000, 9999)}"


def _resolve_bot_desc(name: str) -> str:
    return _env("FEISHU_BOT_SIGNATURE") or _env("FEISHU_BOT_DESC") or name


def _resolve_avatar_path() -> str:
    avatar_path = _env("FEISHU_BOT_AVATAR_PATH")
    if avatar_path:
        if os.path.isfile(avatar_path) and os.path.getsize(avatar_path) > 0:
            return avatar_path
        _fail("create", f"指定头像文件不存在或为空: {avatar_path}")

    avatar_url = _env("FEISHU_BOT_AVATAR_URL") or AVATAR_URL
    return _download_avatar(avatar_url)


def _write_qr_artifacts(content: str) -> None:
    try:
        import qrcode
    except Exception as e:
        _warn("login", f"二维码图片生成失败，已跳过 PNG 输出: {e}")
        return

    try:
        os.makedirs(os.path.dirname(QR_PNG_PATH) or ".", exist_ok=True)
        qr = qrcode.QRCode(border=4, box_size=10)
        qr.add_data(content)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.convert("RGB")
        with open(QR_PNG_PATH, "wb") as f:
            img.save(f)
        _status("login", f"已写入登录二维码 PNG: {QR_PNG_PATH}")
    except Exception as e:
        _warn("login", f"二维码图片生成失败，已跳过 PNG 输出: {e}")


def _download_avatar(avatar_url: str) -> str:
    avatar_ext = os.path.splitext(urllib.parse.urlparse(avatar_url).path)[1].lower()
    if avatar_ext not in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
        avatar_ext = ".png"
    target_path = AVATAR_PATH if avatar_ext == ".png" else os.path.join(STATE_DIR, f"feishu-bot-avatar{avatar_ext}")

    if avatar_url == AVATAR_URL and os.path.isfile(target_path) and os.path.getsize(target_path) > 0:
        return target_path

    _status("create", f"下载机器人头像: {avatar_url}")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(avatar_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            data = resp.read()
        with open(target_path, "wb") as f:
            f.write(data)
        _status("create", f"已下载机器人头像: {target_path}")
        return target_path
    except Exception as e:
        _warn("create", f"头像下载失败，继续使用空头像: {e}")
        return ""


def _pick_free_port() -> int:
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        sock.listen(1)
        return int(sock.getsockname()[1])


def _save_browser_pid(pid: int) -> None:
    try:
        with open(CDP_PID_PATH, "w", encoding="utf-8") as f:
            f.write(str(pid))
    except OSError:
        pass


def _clear_browser_pid() -> None:
    try:
        os.remove(CDP_PID_PATH)
    except OSError:
        pass


def _kill_cdp_browser() -> None:
    try:
        with open(CDP_PID_PATH, "r", encoding="utf-8") as f:
            pid = int(f.read().strip())
        try:
            os.kill(pid, signal.SIGKILL)
        except (OSError, ProcessLookupError):
            pass
    except (OSError, ValueError):
        pass
    finally:
        _clear_browser_pid()

    for lock_name in ("SingletonLock", "SingletonSocket", "SingletonCookie"):
        path = os.path.join(PROFILE_DIR, lock_name)
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass


def _get_chromium_path() -> str:
    system_browser = _find_system_browser()
    if system_browser:
        return system_browser

    from playwright.sync_api import sync_playwright

    pw = sync_playwright().start()
    path = pw.chromium.executable_path
    pw.stop()
    return path


def _launch_detached_chromium(port: int) -> int:
    chrome_path = _get_chromium_path()
    if not os.path.isfile(chrome_path):
        raise FileNotFoundError(f"Chromium 不存在: {chrome_path}")

    os.makedirs(PROFILE_DIR, exist_ok=True)
    proc = subprocess.Popen(
        [
            chrome_path,
            "--headless=new",
            f"--remote-debugging-port={port}",
            f"--user-data-dir={PROFILE_DIR}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-background-networking",
            "--no-sandbox",
            "about:blank",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    _save_browser_pid(proc.pid)
    return proc.pid


def _wait_for_cdp_ready(port: int, timeout: int = 20) -> bool:
    import socket

    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            s = socket.create_connection(("127.0.0.1", port), timeout=1)
            s.close()
            return True
        except (ConnectionRefusedError, OSError):
            time.sleep(0.5)
    return False


class FeishuBotCreator:
    def __init__(self, page: "Page"):
        self.page = page
        self.csrf_token: Optional[str] = None
        self.app_id: Optional[str] = None
        self.app_secret: Optional[str] = None
        self.version_id: Optional[str] = None
        self.creator_internal_id: Optional[str] = None

    def install_network_capture(self) -> None:
        def _on_request(req):
            if "open.feishu.cn" not in req.url:
                return
            token = req.headers.get("x-csrf-token") or req.headers.get("X-CSRF-Token")
            if token:
                self.csrf_token = token

        self.page.on("request", _on_request)

    def _csrf(self) -> Optional[str]:
        if self.csrf_token:
            return self.csrf_token
        try:
            token = self.page.evaluate("window.csrfToken || ''")
            if token:
                self.csrf_token = token
                return token
        except Exception:
            pass
        try:
            cookies = {c["name"]: c["value"] for c in self.page.context.cookies([BASE_URL])}
            token = (
                cookies.get("lark_oapi_csrf_token")
                or cookies.get("lgw_csrf_token")
                or cookies.get("swp_csrf_token")
            )
            if token:
                self.csrf_token = token
            return token
        except Exception:
            return None

    def _headers(self, *, with_body: bool = False, referer: Optional[str] = None) -> dict:
        headers = {"accept": "*/*", "x-timezone-offset": "-480"}
        if with_body:
            headers.update(
                {
                    "content-type": "application/json",
                    "origin": BASE_URL,
                    "referer": referer or APP_PAGE,
                }
            )
        csrf = self._csrf()
        if csrf:
            headers["x-csrf-token"] = csrf
        return headers

    def _cookie_string(self, *urls: str) -> str:
        targets = [url for url in urls if url]
        if not targets:
            targets = [BASE_URL]

        cookies = {}
        try:
            for cookie in self.page.context.cookies(targets):
                cookies[cookie["name"]] = cookie["value"]
        except Exception:
            return ""
        return "; ".join(f"{name}={value}" for name, value in cookies.items())

    def _post(self, url: str, payload: dict, *, referer: Optional[str] = None) -> Optional[dict]:
        try:
            return self.page.request.post(
                url,
                data=payload,
                headers=self._headers(with_body=True, referer=referer),
            ).json()
        except Exception:
            return None

    def _get(self, url: str, *, referer: Optional[str] = None) -> Optional[dict]:
        try:
            return self.page.request.get(url, headers=self._headers(referer=referer)).json()
        except Exception:
            return None

    def _ok(self, body: Optional[dict], step: str) -> Optional[dict]:
        if body is None:
            _warn(step, "请求失败或响应不可解析")
            return None
        if body.get("code") != 0:
            _warn(step, f"code={body.get('code')}, msg={body.get('msg')}")
            return None
        return body

    @staticmethod
    def _build_multipart(fields: dict, files: dict):
        boundary = f"----WebKitFormBoundary{uuid.uuid4().hex[:16]}"
        parts = []
        for key, value in fields.items():
            parts.append(f"--{boundary}\r\n".encode())
            parts.append(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode())
            parts.append(f"{value}\r\n".encode())
        for key, (filename, data, content_type) in files.items():
            parts.append(f"--{boundary}\r\n".encode())
            parts.append(
                f'Content-Disposition: form-data; name="{key}"; filename="{filename}"\r\n'.encode()
            )
            parts.append(f"Content-Type: {content_type}\r\n\r\n".encode())
            parts.append(data)
            parts.append(b"\r\n")
        parts.append(f"--{boundary}--\r\n".encode())
        return b"".join(parts), f"multipart/form-data; boundary={boundary}"

    def _upload_avatar(self, avatar_path: str) -> str:
        if not avatar_path or not os.path.isfile(avatar_path):
            return ""

        with open(avatar_path, "rb") as f:
            img_data = f.read()
        content_type = mimetypes.guess_type(avatar_path)[0] or "image/png"
        if not content_type.startswith("image/"):
            content_type = "image/png"

        csrf = self._csrf()
        if not csrf:
            return ""

        cookies = self.page.context.cookies([BASE_URL])
        cookie_str = "; ".join(f"{c['name']}={c['value']}" for c in cookies)
        body, content_type = self._build_multipart(
            fields={
                "uploadType": "4",
                "isIsv": "false",
                "scale": '{"width":240,"height":240}',
            },
            files={
                "file": (os.path.basename(avatar_path), img_data, content_type),
            },
        )

        req = urllib.request.Request(
            f"{API_BASE}/app/upload/image",
            data=body,
            headers={
                "Accept": "*/*",
                "Content-Type": content_type,
                "Cookie": cookie_str,
                "Origin": BASE_URL,
                "Referer": APP_PAGE,
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/145.0.0.0 Safari/537.36"
                ),
                "x-csrf-token": csrf,
                "x-timezone-offset": "-480",
            },
            method="POST",
        )

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            with urllib.request.urlopen(req, context=ctx) as resp:
                result = json.loads(resp.read())
            if result.get("code") != 0:
                return ""
            return result.get("data", {}).get("url", "")
        except Exception:
            return ""

    def create_app(self, name: str, desc: str, avatar_path: str) -> bool:
        _status("create", f"创建应用: {name}")
        avatar_url = self._upload_avatar(avatar_path)
        body = self._post(
            f"{API_BASE}/app/create",
            {
                "appSceneType": 0,
                "name": name,
                "desc": desc,
                "avatar": avatar_url,
                "i18n": {"zh_cn": {"name": name, "description": desc}},
                "primaryLang": "zh_cn",
            },
        )
        result = self._ok(body, "create")
        if result is None:
            return False
        self.app_id = result["data"]["ClientID"]
        _status("create", f"已创建应用: {self.app_id}")
        return True

    def get_credentials(self) -> bool:
        _status("credential", "获取应用凭证")
        body = self._get(f"{API_BASE}/secret/{self.app_id}")
        result = self._ok(body, "credential")
        if result is None:
            return False
        data = result.get("data", {})
        self.app_secret = (
            data.get("appSecret")
            or data.get("app_secret")
            or data.get("secret")
            or data.get("AppSecret")
        )
        if not self.app_secret:
            _warn("credential", f"未在响应中找到 app_secret，keys={list(data.keys())}")
            return False
        _status("credential", "已获取应用凭证")
        return True

    def enable_bot(self) -> bool:
        _status("bot", "配置机器人能力")
        switch_body = self._post(f"{API_BASE}/robot/switch/{self.app_id}", {"enable": True})
        if self._ok(switch_body, "bot") is None:
            return False
        create_body = self._post(f"{API_BASE}/robot/{self.app_id}", {})
        if self._ok(create_body, "bot") is None:
            return False
        _status("bot", "已开启机器人能力")
        return True

    def configure_events(self) -> bool:
        _status("event", "配置事件订阅")
        referer = f"{BASE_URL}/app/{self.app_id}/event?tab=event"
        body = self._post(
            f"{API_BASE}/event/update/{self.app_id}",
            {
                "operation": "add",
                "events": [],
                "appEvents": BOT_EVENTS,
                "userEvents": [],
                "eventMode": 1,
            },
            referer=referer,
        )
        if self._ok(body, "event") is None:
            return False
        switch_body = self._post(
            f"{API_BASE}/event/switch/{self.app_id}",
            {
                "eventMode": LONG_CONNECTION_MODE,
            },
            referer=referer,
        )
        if self._ok(switch_body, "event") is None:
            return False
        _status("event", "已配置事件订阅为长连接")
        return True

    def configure_callbacks(self) -> bool:
        _status("callback", "配置卡片回调订阅方式")
        referer = f"{BASE_URL}/app/{self.app_id}/event?tab=callback"
        mode_body = self._post(
            f"{API_BASE}/callback/switch/{self.app_id}",
            {"callbackMode": LONG_CONNECTION_MODE},
            referer=referer,
        )
        if self._ok(mode_body, "callback") is None:
            return False
        _status("callback", "已配置卡片回调订阅方式为长连接")

        time.sleep(0.5)
        _status("callback", "添加卡片回调")
        update_body = self._post(
            f"{API_BASE}/callback/update/{self.app_id}",
            {
                "operation": "add",
                "callbacks": BOT_CALLBACKS,
                "callbackMode": LONG_CONNECTION_MODE,
            },
            referer=referer,
        )
        if self._ok(update_body, "callback") is None:
            return False
        _status("callback", "已添加卡片回调，订阅方式为长连接")
        return True

    @staticmethod
    def _scope_candidates(name: str) -> list[str]:
        return SCOPE_NAME_ALIASES.get(name, [name])

    def grant_permissions(self) -> bool:
        _status("permission", "配置应用权限")
        body = self._get(f"{API_BASE}/scope/all/{self.app_id}")
        result = self._ok(body, "permission")
        if result is None:
            return False

        tenant_name_to_id = {}
        user_name_to_id = {}
        fallback_name_to_id = {}
        for scope in result.get("data", {}).get("scopes", []):
            name = scope.get("name") or scope.get("scopeName", "")
            sid = scope.get("id", "")
            identity_type = scope.get("scopeIdentityType") or scope.get("identityType") or scope.get("scope_identity_type")
            if not name or not sid:
                continue

            sid = str(sid)
            fallback_name_to_id.setdefault(name, sid)
            if str(identity_type) == "2":
                tenant_name_to_id[name] = sid
            elif str(identity_type) == "1":
                user_name_to_id[name] = sid

        def _collect_scope_ids(scope_names: list[str], primary_map: dict, fallback_map: dict) -> tuple[list[str], list[str]]:
            matched = []
            missing = []
            seen = set()
            for scope_name in scope_names:
                sid = None
                for candidate in self._scope_candidates(scope_name):
                    sid = primary_map.get(candidate) or fallback_map.get(candidate)
                    if sid:
                        break
                if not sid:
                    missing.append(scope_name)
                    continue
                if sid not in seen:
                    seen.add(sid)
                    matched.append(sid)
            return matched, missing

        tenant_scope_ids, missing_tenant = _collect_scope_ids(
            BOT_SCOPES["tenant"],
            tenant_name_to_id,
            fallback_name_to_id,
        )
        user_scope_ids, missing_user = _collect_scope_ids(
            BOT_SCOPES["user"],
            user_name_to_id,
            fallback_name_to_id,
        )

        if missing_tenant:
            _warn("permission", f"以下 tenant 权限未匹配: {', '.join(missing_tenant)}")
            return False
        if missing_user:
            _warn("permission", f"以下 user 权限未匹配: {', '.join(missing_user)}")
            return False
        if not tenant_scope_ids and not user_scope_ids:
            _warn("permission", "未匹配到任何权限 ID")
            return False

        body = self._post(
            f"{API_BASE}/scope/update/{self.app_id}",
            {
                "clientId": self.app_id,
                "appScopeIDs": tenant_scope_ids,
                "userScopeIDs": user_scope_ids,
                "scopeIds": [],
                "operation": "add",
                "isDeveloperPanel": True,
            },
        )
        if self._ok(body, "permission") is None:
            return False
        _status("permission", "已导入完整权限")
        return True

    def _get_creator_internal_id(self) -> Optional[str]:
        if self.creator_internal_id:
            return self.creator_internal_id
        body = None
        url = f"{PASSPORT_BASE}/accounts/web/user?app_id=7&support_anonymous=0&_t={int(time.time() * 1000)}"
        headers = {
            "accept": "application/json",
            "origin": BASE_URL,
            "referer": f"{BASE_URL}/",
            "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/145.0.0.0 Safari/537.36"
            ),
            "x-api-version": "1.0.28",
            "x-app-id": "7",
            "x-device-info": "platform=websdk",
        }
        cookie_string = self._cookie_string(BASE_URL, PASSPORT_BASE)
        if cookie_string:
            headers["cookie"] = cookie_string
        try:
            body = self.page.request.get(url, headers=headers).json()
        except Exception:
            return None

        if body.get("code") != 0:
            _warn("version", f"获取创建者信息失败，code={body.get('code')}, msg={body.get('msg')}")
            return None
        self.creator_internal_id = body.get("data", {}).get("user", {}).get("id")
        return self.creator_internal_id

    def _transform_to_open_id(self, internal_id: str) -> Optional[str]:
        body = self._post(
            f"{BASE_URL}/api_explorer/v1/resource_id/transform",
            {
                "resource": "user",
                "id": internal_id,
                "clientId": self.app_id,
            },
        )
        result = self._ok(body, "notify")
        if result is None:
            return None
        return result.get("data", {}).get("ids", {}).get("open_id")

    def _tenant_access_token(self) -> Optional[str]:
        req = urllib.request.Request(
            f"{BASE_URL}/open-apis/auth/v3/tenant_access_token/internal",
            data=json.dumps(
                {
                    "app_id": self.app_id,
                    "app_secret": self.app_secret,
                }
            ).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/145.0.0.0 Safari/537.36"
                ),
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req) as resp:
                body = json.loads(resp.read())
        except Exception as e:
            _warn("notify", f"获取 tenant_access_token 失败: {e}")
            return None

        if body.get("code") not in (0, None):
            _warn("notify", f"获取 tenant_access_token 失败，code={body.get('code')}, msg={body.get('msg')}")
            return None
        return body.get("tenant_access_token")

    def notify_creator(self, name: str, desc: str) -> bool:
        _status("notify", "发送创建成功通知")
        creator_id = self._get_creator_internal_id()
        if not creator_id:
            _warn("notify", "未获取到创建者 user_id")
            return False

        open_id = self._transform_to_open_id(creator_id)
        if not open_id:
            _warn("notify", "未获取到创建者 open_id")
            return False

        tenant_access_token = self._tenant_access_token()
        if not tenant_access_token:
            return False

        message = {
            "receive_id": open_id,
            "msg_type": "text",
            "content": json.dumps(
                {
                    "text": "\n".join(
                        [
                            "飞书机器人创建成功",
                            f"名称: {name}",
                            f"描述: {desc}",
                            f"App ID: {self.app_id}",
                            f"App Secret: {self.app_secret}",
                            f"应用链接: {BASE_URL}/app/{self.app_id}",
                            f"版本链接: {BASE_URL}/app/{self.app_id}/version/{self.version_id}",
                        ]
                    )
                },
                ensure_ascii=False,
            ),
        }
        req = urllib.request.Request(
            f"{BASE_URL}/open-apis/im/v1/messages?receive_id_type=open_id",
            data=json.dumps(message, ensure_ascii=False).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {tenant_access_token}",
                "Content-Type": "application/json",
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/145.0.0.0 Safari/537.36"
                ),
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req) as resp:
                body = json.loads(resp.read())
        except Exception as e:
            _warn("notify", f"发送通知失败: {e}")
            return False

        if body.get("code") not in (0, None):
            _warn("notify", f"发送通知失败，code={body.get('code')}, msg={body.get('msg')}")
            return False

        _status("notify", "已发送创建成功通知")
        return True

    def create_version_and_publish(self) -> bool:
        _status("version", "创建应用版本并提交发布")
        creator_id = self._get_creator_internal_id()
        if not creator_id:
            _warn("version", "未获取到创建者 user_id")
            return False

        body = self._post(
            f"{API_BASE}/app_version/create/{self.app_id}",
            {
                "appVersion": APP_VERSION,
                "mobileDefaultAbility": "bot",
                "pcDefaultAbility": "bot",
                "changeLog": APP_VERSION,
                "visibleSuggest": {
                    "departments": [],
                    "members": [creator_id],
                    "groups": [],
                    "isAll": 0,
                },
                "applyReasonConfig": {
                    "apiPrivilegeNeedReason": False,
                    "contactPrivilegeNeedReason": False,
                    "dataPrivilegeReasonMap": {},
                    "visibleScopeNeedReason": False,
                    "apiPrivilegeReasonMap": {},
                    "contactPrivilegeReason": "",
                    "isDataPrivilegeExpandMap": {},
                    "visibleScopeReason": "",
                    "dataPrivilegeNeedReason": False,
                    "isAutoAudit": False,
                    "isContactExpand": False,
                },
                "b2cShareSuggest": False,
                "autoPublish": False,
                "blackVisibleSuggest": {
                    "departments": [],
                    "members": [],
                    "groups": [],
                    "isAll": 0,
                },
            },
        )
        result = self._ok(body, "version")
        if result is None:
            return False

        version_id = result.get("data", {}).get("versionId")
        if not version_id:
            _warn("version", "创建版本成功，但未返回 versionId")
            return False

        self.version_id = str(version_id)
        commit_body = self._post(f"{API_BASE}/publish/commit/{self.app_id}/{self.version_id}", {})
        if self._ok(commit_body, "version") is None:
            return False

        _status("version", f"已创建应用版本并提交发布: {self.version_id}")
        return True

def _create_bot(creator: FeishuBotCreator) -> dict:
    creator.app_id = None
    creator.app_secret = None
    creator.version_id = None
    creator.creator_internal_id = None

    bot_name = _resolve_bot_name()
    bot_desc = _resolve_bot_desc(bot_name)
    avatar_path = _resolve_avatar_path()
    _status("create", f"创建机器人: {bot_name}")

    if not creator.create_app(bot_name, bot_desc, avatar_path):
        _fail("create", "创建应用失败")
    if not creator.get_credentials():
        _fail("credential", "获取应用凭证失败")
    if not creator.enable_bot():
        _fail("bot", "开启机器人能力失败")
    if not creator.grant_permissions():
        _fail("permission", "导入完整权限失败")
    if not creator.configure_events():
        _fail("event", "添加事件订阅失败")
    if not creator.configure_callbacks():
        _fail("callback", "添加卡片回调并配置长连接失败")
    if not creator.create_version_and_publish():
        _fail("version", "创建版本并发布失败")
    if not creator.notify_creator(bot_name, bot_desc):
        _warn("notify", "发送成功通知失败，但机器人已创建并发布")

    return {
        "name": bot_name,
        "desc": bot_desc,
        "app_id": creator.app_id,
        "app_secret": creator.app_secret,
        "version_id": creator.version_id,
    }


def _login_open_platform():
    _status("login", "启动浏览器并获取登录二维码")
    _kill_cdp_browser()
    time.sleep(1)

    if os.path.isdir(PROFILE_DIR):
        for _ in range(3):
            try:
                shutil.rmtree(PROFILE_DIR)
                break
            except OSError:
                time.sleep(0.5)

    cdp_port = _pick_free_port()
    chrome_pid = _launch_detached_chromium(cdp_port)
    if not _wait_for_cdp_ready(cdp_port):
        try:
            os.kill(chrome_pid, signal.SIGKILL)
        except OSError:
            pass
        _clear_browser_pid()
        _fail("login", "Chromium 启动超时")

    from playwright.sync_api import sync_playwright

    pw = sync_playwright().start()
    try:
        browser = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{cdp_port}")
    except Exception as e:
        pw.stop()
        try:
            os.kill(chrome_pid, signal.SIGKILL)
        except OSError:
            pass
        _clear_browser_pid()
        _fail("login", f"连接 Chromium 失败: {e}")

    contexts = browser.contexts
    page = contexts[0].pages[0] if contexts and contexts[0].pages else browser.new_context().new_page()
    state = {"qr_token": None}

    def _on_response(resp):
        try:
            if "qrlogin/init" in resp.url:
                body = resp.json()
                if body.get("code") == 0:
                    state["qr_token"] = body["data"]["step_info"]["token"]
        except Exception:
            pass

    page.on("response", _on_response)

    def _fetch_qr_token() -> bool:
        state["qr_token"] = None
        try:
            page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=30000)
        except Exception:
            try:
                page.goto(LOGIN_URL, wait_until="commit", timeout=30000)
            except Exception:
                return False

        for _ in range(40):
            if state["qr_token"]:
                return True
            page.wait_for_timeout(100)

        try:
            page.reload(wait_until="domcontentloaded", timeout=30000)
        except Exception:
            return False

        for _ in range(20):
            if state["qr_token"]:
                return True
            page.wait_for_timeout(200)
        return False

    def _poll_qr_login() -> bool:
        login_state = {"ok": False, "scanned": False}

        def _on_poll_response(resp):
            try:
                if "qrlogin/polling" not in resp.url:
                    return
                body = resp.json()
                if body.get("code") != 0:
                    return
                data = body.get("data", {})
                info = data.get("step_info", {})
                if info.get("status") == 2 and not login_state["scanned"]:
                    login_state["scanned"] = True
                    _status("login", "已扫码，请在手机上确认登录")
                if data.get("redirect_url"):
                    login_state["ok"] = True
            except Exception:
                pass

        page.on("response", _on_poll_response)
        deadline = time.time() + LOGIN_TIMEOUT
        while time.time() < deadline:
            if login_state["ok"]:
                break
            if login_state["scanned"]:
                try:
                    current_url = page.url
                    if "open.feishu.cn" in current_url and "accounts.feishu.cn" not in current_url:
                        login_state["ok"] = True
                        break
                except Exception:
                    pass
            try:
                page.wait_for_timeout(500)
            except Exception:
                pass

        page.remove_listener("response", _on_poll_response)
        return login_state["ok"]

    for attempt in range(1, QR_MAX_RETRIES + 1):
        if not _fetch_qr_token():
            if attempt < QR_MAX_RETRIES:
                _warn("login", f"获取二维码失败，正在重试 ({attempt}/{QR_MAX_RETRIES})")
                time.sleep(2)
                continue
            pw.stop()
            _kill_cdp_browser()
            _fail("login", "未能获取二维码")

        qr_json = json.dumps({"qrlogin": {"token": state["qr_token"]}}, ensure_ascii=False)
        _write_qr_artifacts(qr_json)

        if _poll_qr_login():
            break

        if attempt < QR_MAX_RETRIES:
            _warn("login", f"二维码已过期，准备刷新 ({attempt}/{QR_MAX_RETRIES})")
            time.sleep(1)
        else:
            pw.stop()
            _kill_cdp_browser()
            _fail("login", f"{QR_MAX_RETRIES} 次尝试后仍未登录成功")

    page.goto(APP_PAGE, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(1500)
    _status("login", "已登录飞书开放平台")
    return pw, page


def _prepare_runtime() -> None:
    _status("init", "检查运行依赖")
    _ensure_dependencies()
    _status("init", "运行依赖已就绪")


def cmd_init() -> None:
    _prepare_runtime()


def cmd_create() -> None:
    _prepare_runtime()

    pw = None
    try:
        pw, page = _login_open_platform()
        creator = FeishuBotCreator(page)
        creator.install_network_capture()

        result = _create_bot(creator)
        output = {
            "app_id": result["app_id"],
            "app_secret": result["app_secret"],
        }
        print(json.dumps(output, ensure_ascii=False))
    finally:
        _kill_cdp_browser()
        if pw is not None:
            try:
                pw.stop()
            except Exception:
                pass


def cmd_cleanup() -> None:
    _kill_cdp_browser()
    if os.path.isdir(PROFILE_DIR):
        try:
            shutil.rmtree(PROFILE_DIR)
        except OSError:
            pass
    _status("cleanup", "已清理浏览器残留")


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print(__doc__.strip())
        return

    cmd = sys.argv[1]
    if cmd == "init":
        cmd_init()
    elif cmd == "create":
        if len(sys.argv) > 2:
            _fail("main", "create 不接受额外参数；请使用环境变量配置名称、描述、头像")
        cmd_create()
    elif cmd == "cleanup":
        cmd_cleanup()
    else:
        _fail("main", f"未知命令: {cmd}")


if __name__ == "__main__":
    main()
