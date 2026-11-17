#!/usr/bin/env python3
"""Doxent 本地 API 客户端，并负责按需唤醒 Doxent CLI。"""

import argparse
import glob
import hashlib
import json
import os
import platform
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request


DEFAULT_LOCAL_PORT = 46588
DEFAULT_TIMEOUT_SECONDS = 10
HEALTH_CHECK_TIMEOUT_SECONDS = 1.5
SERVICE_READY_TIMEOUT_SECONDS = 15
SERVICE_READY_INTERVAL_SECONDS = 0.5
SYNC_WAIT_TIMEOUT_SECONDS = 300
APP_LAUNCH_FILE_NAME = "app_launch.json"
DOXENT_CLI_NAMES = ("doxent-cli", "doxent-cli.exe", "doxent-cli.bat", "doxent-cli.cmd", "doxent-cli.js")
# macOS 只发布一个同时支持 arm64/x64 的 universal 包；配置表必须与真实发布物一一对应，
# 不为同一文件维护重复架构键。Linux 产物包含架构门禁，仍需严格按当前 CPU 分流。
DOXENT_CLI_DOWNLOAD_URLS = {
    "windows-x64": "https://download.iflyink.com/apk/doxent-cli.exe?attname=doxent-cli.exe",
    "darwin-universal": "https://download.iflyink.com/apk/doxent-mac-universal-cli?attname=doxent-cli",
    "linux-arm64": "https://download.iflyink.com/apk/doxent-linux-arm64-cli?attname=doxent-cli",
    "linux-x64": "https://download.iflyink.com/apk/doxent-linux-x64-cli?attname=doxent-cli",
}
MIN_CLI_BYTES = 500000
VERSION_CHECK_TTL_SECONDS = 3600


def normalized_machine():
    """把系统架构名收敛为发布文件使用的 arm64/x64，拒绝猜测未知芯片。"""
    machine = platform.machine().lower()
    if machine in ("arm64", "aarch64"):
        return "arm64"
    if machine in ("x86_64", "amd64"):
        return "x64"
    return ""


def cli_download_url():
    """按当前系统选择上传产物；macOS 默认使用跨 arm64/x64 的 universal 单文件。"""
    generic_override = normalize_path(os.environ.get("DOXENT_CLI_DOWNLOAD_URL"))
    if generic_override:
        return generic_override
    system = platform.system().lower()
    arch = normalized_machine()
    if system == "windows":
        return normalize_path(os.environ.get("DOXENT_WINDOWS_CLI_DOWNLOAD_URL")) or DOXENT_CLI_DOWNLOAD_URLS["windows-x64"]
    if system == "darwin":
        if arch not in ("arm64", "x64"):
            raise RuntimeError("当前 macOS CPU 架构没有可用的 Doxent CLI：{}".format(platform.machine()))
        return normalize_path(os.environ.get("DOXENT_MAC_CLI_DOWNLOAD_URL")) or DOXENT_CLI_DOWNLOAD_URLS["darwin-universal"]
    if system == "linux" and arch:
        environment_name = "DOXENT_LINUX_{}_CLI_DOWNLOAD_URL".format(arch.upper())
        return normalize_path(os.environ.get(environment_name)) or DOXENT_CLI_DOWNLOAD_URLS["linux-" + arch]
    raise RuntimeError("当前系统或 CPU 架构没有可用的 Doxent CLI 下载产物：{} {}".format(system, platform.machine()))


def write_console(text, stream=None):
    """以 UTF-8 写出结果，避免 Windows 控制台默认 GBK 无法承载中文响应。"""
    target = stream or sys.stdout
    payload = str(text).encode("utf-8", errors="replace")
    buffer = getattr(target, "buffer", None)
    if buffer is not None:
        buffer.write(payload)
        buffer.write(b"\n")
        buffer.flush()
        return
    target.write(payload.decode("utf-8", errors="replace") + "\n")
    target.flush()


def unique(items):
    result = []
    seen = set()
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def resolve_timeout(url):
    # 搜索接口可能需要较长时间，保持原有的无超时约定；其余请求避免永久挂起。
    return None if "/search" in str(url or "").lower() else DEFAULT_TIMEOUT_SECONDS


def config_paths(file_name):
    home = (os.environ.get("HOME") or os.path.expanduser("~") or "").strip()
    appdata = (os.environ.get("APPDATA") or "").strip()
    xdg = (os.environ.get("XDG_CONFIG_HOME") or "").strip()
    paths = []
    if appdata:
        paths.extend([
            os.path.join(appdata, "doxent", file_name),
            os.path.join(appdata, "Doxent", "config", file_name),
        ])
    if home:
        paths.extend([
            os.path.join(home, "Library", "Application Support", "doxent", file_name),
            os.path.join(xdg or os.path.join(home, ".config"), "doxent", file_name),
            os.path.join(home, "doxent", file_name),
        ])
    return unique(paths)


def configured_port():
    for path in config_paths("open_model_config.json"):
        try:
            with open(path, "r", encoding="utf-8-sig") as handle:
                port = int((json.load(handle) or {}).get("port") or 0)
            if 0 < port <= 65535:
                return port
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            # 配置文件可能尚未生成或正在更新，此时继续使用其他候选入口。
            continue
    return DEFAULT_LOCAL_PORT


def running_cli_ports():
    """从当前用户的 Doxent daemon 命令行发现实际端口，修复旧配置未随 --port 更新的问题。"""
    if platform.system().lower() != "windows":
        return []
    command = [
        "powershell.exe",
        "-NoProfile",
        "-NonInteractive",
        "-Command",
        "$ErrorActionPreference='SilentlyContinue'; "
        "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'doxent-cli\\.js' -and $_.CommandLine -match '--doxent-cli-daemon' } | "
        "ForEach-Object { $_.CommandLine }",
    ]
    try:
        result = subprocess.run(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            creationflags=hidden_creation_flags(),
            text=False,
            timeout=5,
            shell=False,
        )
        output = result.stdout.decode("utf-8", errors="replace")
        ports = []
        for value in re.findall(r"--port\s+(\d+)", output, re.IGNORECASE):
            port = int(value)
            if 0 < port <= 65535:
                ports.append(port)
        return unique(ports)
    except (OSError, subprocess.SubprocessError, UnicodeError):
        return []


def local_url_candidates(url):
    parsed = urllib.parse.urlsplit(str(url or "").strip())
    if parsed.scheme not in ("http", "https") or (parsed.hostname or "").lower() not in ("127.0.0.1", "localhost"):
        return [url]
    host = parsed.hostname or "127.0.0.1"
    ports = unique([parsed.port or DEFAULT_LOCAL_PORT, configured_port()] + running_cli_ports())
    return [urllib.parse.urlunsplit((parsed.scheme, "{}:{}".format(host, port), parsed.path, parsed.query, parsed.fragment)) for port in ports]


def is_local_api_url(url):
    """Doxent 开放接口只允许回环地址，防止 token 或真实数据被转发到第三方主机。"""
    parsed = urllib.parse.urlsplit(str(url or "").strip())
    return parsed.scheme == "http" and (parsed.hostname or "").lower() in ("127.0.0.1", "localhost")


def health_url(url):
    parsed = urllib.parse.urlsplit(url)
    path = parsed.path or ""
    if path.startswith("/open-model-schedule"):
        path = "/open-model-schedule/health"
    elif path.startswith("/open-model-book"):
        path = "/open-model-book/health"
    elif path.startswith("/open-model-common"):
        path = "/open-model-common/health"
    else:
        path = "/open-model-note/health"
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, path, "", ""))


def service_ready(url):
    try:
        request = urllib.request.Request(health_url(url), method="GET")
        with urllib.request.urlopen(request, timeout=HEALTH_CHECK_TIMEOUT_SECONDS):
            return True
    except urllib.error.HTTPError as error:
        # 只有鉴权拒绝能证明这是目标 Core；404 可能只是同端口上的其他本地服务。
        return error.code in (401, 403)
    except (OSError, urllib.error.URLError):
        return False


def sync_status_url(url):
    """把任意本地 Core 地址转换为仅返回同步状态的协调接口。"""
    parsed = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, "/sync/status", "", ""))


def wait_for_sync(url):
    """在读取业务数据前等待 CLI 首轮/定时同步结束，避免把旧缓存当成最新数据。"""
    deadline = time.time() + SYNC_WAIT_TIMEOUT_SECONDS
    announced = False
    status_url = sync_status_url(url)
    while time.time() < deadline:
        try:
            request = urllib.request.Request(status_url, method="GET")
            with urllib.request.urlopen(request, timeout=HEALTH_CHECK_TIMEOUT_SECONDS) as response:
                payload = json.loads(response.read().decode("utf-8"))
            status = payload.get("data") if isinstance(payload, dict) else {}
            if not isinstance(status, dict) or not isinstance(status.get("running"), bool) or not isinstance(status.get("startupSyncPending"), bool):
                write_console("Doxent 同步状态响应无效，本次请求已停止；请检查或更新 CLI 后重试。", sys.stderr)
                return False
            active = status["running"] or status["startupSyncPending"]
            if not active:
                if isinstance(status, dict) and status.get("lastSyncSucceeded") is False:
                    reason = str(status.get("lastSyncError") or "最近一轮同步失败")
                    write_console("Doxent 数据同步失败：{}。本次请求已停止，请稍后重试。".format(reason), sys.stderr)
                    return False
                return True
            if not announced:
                write_console("Doxent 正在同步数据，请稍候；同步完成后再返回最新数据。")
                announced = True
            time.sleep(SERVICE_READY_INTERVAL_SECONDS)
        except urllib.error.HTTPError as error:
            # 没有状态接口就无法证明启动同步已经完成。继续返回缓存会把旧数据误报为最新数据，
            # 因此要求更新 CLI，而不是沿用旧版的静默降级行为。
            if error.code == 404:
                write_console("当前 Doxent CLI 不支持同步状态检查，本次请求已停止；请等待自动更新后重试。", sys.stderr)
                return False
            write_console("Doxent 同步状态接口返回 HTTP {}，本次请求已停止。".format(error.code), sys.stderr)
            return False
        except (ValueError, TypeError, json.JSONDecodeError):
            write_console("Doxent 同步状态无法解析，本次请求已停止；请检查 CLI 日志后重试。", sys.stderr)
            return False
        except (OSError, urllib.error.URLError) as error:
            write_console("Doxent 同步状态接口不可用：{}。本次请求已停止。".format(error), sys.stderr)
            return False
    write_console("Doxent 同步等待已超时，本次请求已停止；请稍后重试。", sys.stderr)
    return False


def normalize_path(value):
    text = str(value or "").strip().strip('"')
    if not text:
        return ""
    if "," in text and not os.path.exists(text):
        text = text.split(",", 1)[0].strip().strip('"')
    return text


def cli_install_path():
    """返回用户级安装路径，避免管理员权限和对桌面应用安装目录的写入。"""
    override = normalize_path(os.environ.get("DOXENT_CLI_INSTALL_DIR"))
    if override:
        filename = "doxent-cli.exe" if platform.system().lower() == "windows" else "doxent-cli"
        return os.path.join(override, filename)
    if platform.system().lower() == "windows":
        base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
        return os.path.join(base, "Doxent", "CoreCLI", "doxent-cli.exe")
    # POSIX 入口放入约定的用户级 bin；自解压后的 JS/版本资源由入口自行放到 XDG data 目录。
    return os.path.join(os.path.expanduser("~"), ".local", "bin", "doxent-cli")


def persist_posix_cli_environment(executable):
    """幂等写入登录 shell 配置，使新终端可直接执行统一的 doxent-cli 命令。"""
    home = os.path.expanduser("~")
    system = platform.system().lower()
    profile = os.path.join(home, ".zprofile" if system == "darwin" else ".profile")
    marker_start = "# >>> Doxent CLI >>>"
    marker_end = "# <<< Doxent CLI <<<"
    install_directory = os.path.dirname(executable)
    block = "\n".join([
        marker_start,
        "export DOXENT_CLI_PATH={}".format(shlex.quote(executable)),
        "case \":$PATH:\" in *:{0}:*) ;; *) export PATH={0}:\"$PATH\" ;; esac".format(shlex.quote(install_directory)),
        marker_end,
    ])
    try:
        existing = ""
        if os.path.isfile(profile):
            with open(profile, "r", encoding="utf-8") as handle:
                existing = handle.read()
        pattern = re.compile(re.escape(marker_start) + r"[\s\S]*?" + re.escape(marker_end))
        updated = pattern.sub(block, existing) if pattern.search(existing) else existing.rstrip() + "\n\n" + block + "\n"
        with open(profile, "w", encoding="utf-8") as handle:
            handle.write(updated.lstrip("\n"))
    except OSError:
        # 当前进程已能启动 CLI；配置文件不可写时不破坏已完成的用户级安装。
        pass


def persist_cli_path(executable):
    """保存用户级环境变量，并同步当前进程，后续 Codex/终端可直接发现 CLI。"""
    os.environ["DOXENT_CLI_PATH"] = executable
    install_directory = os.path.dirname(executable)
    current_path = os.environ.get("PATH", "")
    if install_directory not in current_path.split(os.pathsep):
        os.environ["PATH"] = install_directory + os.pathsep + current_path
    if os.environ.get("DOXENT_DISABLE_ENV_PERSISTENCE") == "1":
        return
    if platform.system().lower() != "windows":
        persist_posix_cli_environment(executable)
        return
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "DOXENT_CLI_PATH", 0, winreg.REG_EXPAND_SZ, executable)
    except (OSError, ImportError):
        # 环境变量持久化失败不应阻断当前会话，当前进程仍已具备正确路径。
        pass


def parse_cli_version(text):
    match = re.search(r"DOXENT CLI\s+v(\d+(?:\.\d+)+)", str(text or ""), re.IGNORECASE)
    if not match:
        return None
    return tuple(int(part) for part in match.group(1).split("."))


def cli_command(executable, arguments):
    """按入口类型构造命令；POSIX 下载产物与 Windows EXE 都可直接执行。"""
    suffix = os.path.splitext(executable)[1].lower()
    if suffix in (".bat", ".cmd"):
        return [os.environ.get("COMSPEC", "cmd.exe"), "/d", "/s", "/c", executable] + list(arguments)
    if suffix == ".js":
        return [os.environ.get("DOXENT_NODE", "node"), executable] + list(arguments)
    return [executable] + list(arguments)


def hidden_creation_flags(new_process_group=False):
    """返回隐藏控制台所需标记；非 Windows 平台保持为 0。"""
    if platform.system().lower() != "windows":
        return 0
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    if new_process_group:
        flags |= getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    return flags


def resolve_node_runtime():
    """优先复用显式/系统 Node，并自动发现 Codex 自带运行时，避免要求用户手工安装配置。"""
    configured = normalize_path(os.environ.get("DOXENT_NODE"))
    if configured and os.path.isfile(configured):
        return configured
    system_node = shutil.which("node")
    if system_node:
        return system_node
    user_profile = os.environ.get("USERPROFILE") or os.path.expanduser("~")
    node_name = "node.exe" if platform.system().lower() == "windows" else "node"
    patterns = [
        os.path.join(user_profile, ".cache", "codex-runtimes", "*", "dependencies", "node", "bin", node_name),
        os.path.join(user_profile, ".codex", "runtimes", "*", "dependencies", "node", "bin", node_name),
    ]
    candidates = sorted((candidate for pattern in patterns for candidate in glob.glob(pattern)), reverse=True)
    return candidates[0] if candidates else ""


def cli_environment():
    """把自动发现的 Node 注入子进程环境，使 SFX 和旧 BAT 都能零配置启动。"""
    environment = os.environ.copy()
    node_runtime = resolve_node_runtime()
    if node_runtime:
        environment["DOXENT_NODE"] = node_runtime
        node_directory = os.path.dirname(node_runtime)
        environment["PATH"] = node_directory + os.pathsep + environment.get("PATH", "")
    return environment


def cli_version(executable):
    """读取 CLI 帮助首屏中的版本号；旧版没有 --version，因此不能依赖该参数。"""
    try:
        result = subprocess.run(
            cli_command(executable, ["--help"]),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=cli_environment(),
            creationflags=hidden_creation_flags(),
            text=False,
            timeout=15,
            shell=False,
        )
        return parse_cli_version((result.stdout + result.stderr).decode("utf-8", errors="replace"))
    except (OSError, subprocess.SubprocessError, UnicodeError):
        return None


def file_sha256(path):
    """流式计算文件摘要，避免把完整 CLI 载入内存。"""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def version_cache_path():
    return os.path.join(os.path.dirname(cli_install_path()), "cli-version.json")


def load_version_cache():
    try:
        with open(version_cache_path(), "r", encoding="utf-8-sig") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return {}


def save_version_cache(version, fingerprint, remote_sha256="", installed_path="", installed_sha256="", installed_version=None):
    """保存远端与已安装产物身份；版本号相同但构建变化时仍能识别更新。"""
    try:
        os.makedirs(os.path.dirname(version_cache_path()), exist_ok=True)
        cached = load_version_cache()
        payload = {
            "version": ".".join(str(part) for part in version),
            "fingerprint": fingerprint,
            "remoteSha256": remote_sha256 or cached.get("remoteSha256", ""),
            "installedPath": installed_path or cached.get("installedPath", ""),
            "installedSha256": installed_sha256 or cached.get("installedSha256", ""),
            "installedVersion": ".".join(str(part) for part in installed_version) if installed_version else cached.get("installedVersion", ""),
            "checkedAt": time.time(),
        }
        with open(version_cache_path(), "w", encoding="utf-8") as handle:
            json.dump(payload, handle)
    except OSError:
        pass


def remote_cli_metadata():
    """读取远端版本与摘要；云端同版本重新构建时以摘要变化作为更新依据。"""
    cache = load_version_cache()
    fingerprint = ""
    try:
        head = urllib.request.Request(cli_download_url(), method="HEAD", headers={"User-Agent": "Doxent-Skill/1.0"})
        with urllib.request.urlopen(head, timeout=15) as response:
            fingerprint = "|".join([
                response.headers.get("ETag") or "",
                response.headers.get("Last-Modified") or "",
                response.headers.get("Content-Length") or "",
            ]).strip("|")
    except (OSError, urllib.error.URLError):
        pass
    cached_version = parse_cli_version("DOXENT CLI v{}".format(cache.get("version", "")))
    cache_age = time.time() - float(cache.get("checkedAt") or 0)
    cached_sha256 = str(cache.get("remoteSha256") or "")
    if cached_version and cached_sha256 and ((fingerprint and fingerprint == cache.get("fingerprint")) or (not fingerprint and cache_age < VERSION_CHECK_TTL_SECONDS)):
        return {"version": cached_version, "fingerprint": fingerprint or cache.get("fingerprint", ""), "sha256": cached_sha256}
    directory = os.path.dirname(cli_install_path())
    os.makedirs(directory, exist_ok=True)
    suffix = ".exe" if platform.system().lower() == "windows" else ""
    temporary = tempfile.NamedTemporaryFile(prefix="doxent-cli-version-", suffix=suffix, dir=directory, delete=False)
    temporary.close()
    try:
        downloaded = download_cli(temporary.name, persist=False)
        # 云端文件是自解压安装器，直接执行它来读取 --help 会改写正式安装目录。
        # 更新判定以完整文件摘要为准；版本仅复用上次已安装产物确认过的值。
        version = cached_version or (0, 0, 0)
        remote_sha256 = file_sha256(downloaded)
        save_version_cache(version, fingerprint, remote_sha256=remote_sha256)
        return {"version": version, "fingerprint": fingerprint, "sha256": remote_sha256}
    except (OSError, urllib.error.URLError, RuntimeError):
        return None
    finally:
        if os.path.exists(temporary.name):
            os.remove(temporary.name)


def stop_cli_for_update(executable):
    """请求当前 daemon 退出，让 Windows 可以原子替换正在使用的 CLI 文件。"""
    try:
        subprocess.run(
            cli_command(executable, ["--stop"]),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=cli_environment(),
            creationflags=hidden_creation_flags(),
            timeout=15,
            shell=False,
        )
    except (OSError, subprocess.SubprocessError):
        # 后续原子替换仍会给出确定结果；停止命令失败不在这里吞掉安装错误。
        return


def install_staged_cli(staged, target):
    """重试替换，覆盖 daemon 刚退出时 Windows 短暂持有映像文件的窗口。"""
    deadline = time.time() + 15
    while True:
        try:
            os.replace(staged, target)
            return
        except PermissionError:
            if time.time() >= deadline:
                raise
            time.sleep(0.25)


def ensure_cli_current(executable, service_is_running=False):
    """确保用户级 CLI 与云端产物一致，返回“路径、是否更新”。"""
    local_version = cli_version(executable)
    remote = remote_cli_metadata()
    if not remote:
        return executable, False
    try:
        local_sha256 = file_sha256(executable)
    except OSError:
        local_sha256 = ""
    remote_has_version = remote["version"] != (0, 0, 0)
    if local_version and remote_has_version and local_version > remote["version"]:
        # CDN 尚未上传新构建时绝不能用旧版本覆盖本地新版本；等待远端版本追平后再比较摘要。
        needs_update = False
    else:
        needs_update = local_version is None or (remote_has_version and local_version < remote["version"]) or local_sha256 != remote["sha256"]
    if not needs_update:
        save_version_cache(
            remote["version"],
            remote["fingerprint"],
            remote_sha256=remote["sha256"],
            installed_path=executable,
            installed_sha256=local_sha256,
            installed_version=local_version,
        )
        persist_cli_path(executable)
        return executable, False

    target = cli_install_path()
    os.makedirs(os.path.dirname(target), exist_ok=True)
    staged = target + ".update"
    try:
        download_cli(staged, persist=False, expected_sha256=remote["sha256"])
        if service_is_running:
            stop_cli_for_update(executable)
        install_staged_cli(staged, target)
        persist_cli_path(target)
        installed_sha256 = file_sha256(target)
        installed_version = cli_version(target) or remote["version"]
        save_version_cache(
            remote["version"],
            remote["fingerprint"],
            remote_sha256=remote["sha256"],
            installed_path=target,
            installed_sha256=installed_sha256,
            installed_version=installed_version,
        )
        write_console("Doxent CLI 已自动更新到 v{}。".format(".".join(str(part) for part in installed_version)))
        return target, True
    finally:
        if os.path.exists(staged):
            os.remove(staged)


def download_cli(target=None, persist=True, expected_sha256=""):
    """下载并原子安装当前平台 CLI，校验平台格式后统一落盘为 doxent-cli。"""
    target = target or cli_install_path()
    directory = os.path.dirname(target)
    os.makedirs(directory, exist_ok=True)
    temporary = target + ".download"
    digest = hashlib.sha256()
    try:
        request = urllib.request.Request(cli_download_url(), headers={"User-Agent": "Doxent-Skill/1.0"})
        with urllib.request.urlopen(request, timeout=60) as response, open(temporary, "wb") as output:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                output.write(chunk)
                digest.update(chunk)
        size = os.path.getsize(temporary)
        with open(temporary, "rb") as handle:
            prefix = handle.read(16384)
        if platform.system().lower() == "windows":
            valid_format = prefix.startswith(b"MZ")
            format_error = "不是完整的 Windows EXE"
        else:
            valid_format = prefix.startswith(b"#!/bin/sh\n") and b"__DOXENT_CLI_PAYLOAD_BELOW__" in prefix
            format_error = "不是完整的 POSIX Doxent CLI 单文件包"
        if size < MIN_CLI_BYTES or not valid_format:
            raise RuntimeError("下载的 CLI 文件校验失败（{}）".format(format_error))
        downloaded_sha256 = digest.hexdigest()
        if expected_sha256 and downloaded_sha256.lower() != expected_sha256.lower():
            raise RuntimeError("下载的 CLI 文件摘要与版本探测结果不一致")
        os.replace(temporary, target)
        if platform.system().lower() != "windows":
            os.chmod(target, 0o755)
        if persist:
            persist_cli_path(target)
        return target
    finally:
        if os.path.exists(temporary):
            os.remove(temporary)


def launch_info():
    entries = []
    # 显式配置和 Skill 用户级安装目录必须优先于桌面应用残留配置，避免启动旧构建。
    env_path = normalize_path(os.environ.get("DOXENT_CLI_PATH"))
    if env_path:
        entries.append((env_path, ""))
    entries.append((cli_install_path(), ""))

    for path in config_paths(APP_LAUNCH_FILE_NAME):
        try:
            with open(path, "r", encoding="utf-8-sig") as handle:
                data = json.load(handle) or {}
            executable = normalize_path(data.get("exePath") or data.get("appPath") or data.get("path"))
            # app_launch.json 也可能记录桌面端入口；只有明确的 CLI 文件才允许被 skill 唤醒。
            if executable and "doxent-cli" in os.path.basename(executable).lower():
                entries.append((executable, ""))
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            continue

    if platform.system().lower() == "windows":
        for base in (os.environ.get("LOCALAPPDATA"), os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)")):
            if not base:
                continue
            for folder in (os.path.join("Doxent", "CoreCLI"), "Doxent"):
                for name in DOXENT_CLI_NAMES:
                    entries.append((os.path.join(base, folder, name), ""))
    elif platform.system().lower() == "darwin":
        entries.append(("/Applications/Doxent.app/Contents/Resources/app.asar.unpacked/cli/doxent-cli.js", ""))
    result = []
    seen = set()
    for executable, argument in entries:
        key = (executable, argument)
        if key not in seen:
            seen.add(key)
            result.append(key)
    return result


def start_cli(preferred_executable="", check_update=True):
    candidates = [(preferred_executable, "")] if preferred_executable else launch_info()
    existing = next((executable for executable, _ in candidates if executable and os.path.isfile(executable)), "")
    if existing:
        if check_update:
            try:
                existing, _ = ensure_cli_current(existing, service_is_running=False)
            except (OSError, urllib.error.URLError, RuntimeError) as error:
                write_console("Doxent CLI 更新失败，将继续使用当前版本：{}".format(error), sys.stderr)
        # ensure_service 已经完成更新判断时会传 check_update=False；该分支必须直接启动
        # 既有文件，绝不能误入“未安装”分支再次下载并覆盖刚确认的新版本。
        candidates = [(existing, "")]
    else:
        try:
            installed = download_cli()
            candidates = [(installed, "")]
        except (OSError, urllib.error.URLError, RuntimeError) as error:
            write_console("Doxent CLI 自动下载/安装失败：{}。下载地址：{}".format(error, cli_download_url()), sys.stderr)
            return False
    for executable, extra_argument in candidates:
        if not executable or not os.path.exists(executable):
            continue
        try:
            command = cli_command(executable, [])
            # Doxent CLI 无参数即可启动后台 Core，并在无会话时自行打开登录页；
            # 不传不存在的 background 参数，避免把旧版 Ainote 约定误传给 Doxent。
            # CLI 由 Skill 作为后台服务唤醒，不能继承 Codex/Agent 的控制台；登录页由 CLI
            # 自己打开浏览器，控制台窗口对用户没有价值，反而会造成误以为需要手工操作。
            subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True, creationflags=hidden_creation_flags(new_process_group=True), env=cli_environment(), shell=False)
            return True
        except (OSError, subprocess.SubprocessError):
            # 一个候选入口失败时继续尝试安装目录中的其他入口。
            continue
    return False


def ensure_service(url):
    """确保 CLI daemon 已启动并返回可用地址；本函数永远不会停止已启动的 daemon。"""
    candidates = local_url_candidates(url)
    ready_candidate = next((candidate for candidate in candidates if service_ready(candidate)), "")
    launch_candidates = launch_info()
    executable = next((item for item, _ in launch_candidates if item and os.path.isfile(item)), "")
    updated = False
    if executable:
        try:
            executable, updated = ensure_cli_current(executable, service_is_running=bool(ready_candidate))
        except (OSError, urllib.error.URLError, RuntimeError) as error:
            # 网络失败时复用仍可工作的本地版本；替换失败则保留原文件，不让一次更新检查打断已有服务。
            write_console("Doxent CLI 更新检查失败，将继续使用当前版本：{}".format(error), sys.stderr)
    else:
        try:
            executable = download_cli()
        except (OSError, urllib.error.URLError, RuntimeError) as error:
            write_console("Doxent CLI 自动下载/安装失败：{}。下载地址：{}".format(error, cli_download_url()), sys.stderr)
            if ready_candidate:
                return ready_candidate
            raise RuntimeError("Doxent CLI 自动下载/安装失败") from error

    # 更新过程可能为了替换 EXE 停止了旧 daemon，因此必须重新探测，不能沿用更新前的健康结论。
    if ready_candidate and not updated:
        return ready_candidate
    ready_candidate = next((candidate for candidate in candidates if service_ready(candidate)), "")
    if ready_candidate:
        return ready_candidate
    if not start_cli(executable, check_update=False):
        raise RuntimeError("Doxent CLI 进程无法启动")
    deadline = time.time() + SERVICE_READY_TIMEOUT_SECONDS
    while time.time() < deadline:
        for candidate in candidates:
            if service_ready(candidate):
                return candidate
        time.sleep(SERVICE_READY_INTERVAL_SECONDS)
    raise RuntimeError("Doxent CLI 启动后未在 {} 秒内提供本地服务".format(SERVICE_READY_TIMEOUT_SECONDS))


def run_cli_command(argument):
    candidates = launch_info()
    if not any(executable and os.path.isfile(executable) for executable, _ in candidates):
        if argument in ("--stop", "--logout"):
            write_console("Doxent CLI 当前未安装或未运行，无需执行 {}。".format(argument))
            return 0
        try:
            candidates = [(download_cli(), "")]
        except (OSError, urllib.error.URLError, RuntimeError) as error:
            write_console("Doxent CLI 自动下载/安装失败：{}。下载地址：{}".format(error, cli_download_url()), sys.stderr)
            return 1
    for executable, _ in candidates:
        if not executable or not os.path.exists(executable):
            continue
        try:
            if argument not in ("--stop", "--logout"):
                default_url = "http://127.0.0.1:{}/open-model-note/health".format(configured_port())
                executable, _ = ensure_cli_current(executable, service_is_running=service_ready(default_url))
            command = cli_command(executable, [argument])
            result = subprocess.run(
                command,
                shell=False,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=cli_environment(),
                # help 的文本由当前 Python 客户端转发，login/stop 则完全静默执行；所有动作都
                # 禁止 Windows 为 console subsystem EXE 创建新的黑色窗口。
                creationflags=hidden_creation_flags(),
                text=False,
            )
            if argument == "--help" and result.stdout:
                write_console(result.stdout.decode("utf-8", errors="replace"))
            if result.returncode != 0 and result.stderr:
                write_console(result.stderr.decode("utf-8", errors="replace"), sys.stderr)
            return result.returncode
        except (OSError, subprocess.SubprocessError):
            continue
    return 127


def main():
    parser = argparse.ArgumentParser(description="Doxent 本地 API 客户端")
    parser.add_argument("--url", help="完整请求 URL")
    parser.add_argument("--method", default="GET", help="HTTP 方法")
    parser.add_argument("--body-encoded", dest="body_encoded", help="UTF-8 JSON 的 URL 百分号编码字符串")
    parser.add_argument("--body-file", dest="body_file", help="UTF-8 JSON 文件路径")
    parser.add_argument("--body", help="JSON 字符串；Windows PowerShell 5.1 不建议使用")
    parser.add_argument("--token", help="Bearer token")
    parser.add_argument("--no-auto-start", action="store_true", help="服务不可用时不自动启动 Doxent CLI")
    parser.add_argument("--cli-action", choices=("login", "logout", "stop", "help"), help="直接控制 Doxent CLI 生命周期")
    args = parser.parse_args()

    if args.cli_action:
        return run_cli_command("--" + args.cli_action)
    if not args.url:
        parser.error("API 请求必须提供 --url")
    if not is_local_api_url(args.url):
        write_console("Doxent API 只允许访问 http://127.0.0.1 或 http://localhost，本次请求已拒绝。", sys.stderr)
        return 2

    data = None
    if args.body_encoded:
        data = urllib.parse.unquote(args.body_encoded, encoding="utf-8").encode("utf-8")
    elif args.body_file:
        with open(args.body_file, "r", encoding="utf-8-sig") as handle:
            data = handle.read().encode("utf-8")
    elif args.body:
        data = args.body.encode("utf-8")

    request_url = local_url_candidates(args.url)[0]
    # 每次真实数据脚本都先确保后台 CLI 存活；请求完成后不发送 stop，供后续脚本复用同一 daemon。
    if not args.no_auto_start:
        try:
            request_url = ensure_service(args.url)
        except RuntimeError as error:
            write_console(str(error), sys.stderr)
            return 1
    if not wait_for_sync(request_url):
        # 同步未完成时禁止继续读取业务接口，避免把旧缓存误报成刚同步的数据。
        return 2
    request = urllib.request.Request(request_url, data=data, headers={"Content-Type": "application/json; charset=utf-8"}, method=args.method.upper())
    if args.token:
        request.add_header("Authorization", "Bearer " + args.token)
    try:
        timeout = resolve_timeout(request_url)
        response = urllib.request.urlopen(request, **({} if timeout is None else {"timeout": timeout}))
        with response:
            write_console(response.read().decode("utf-8"))
        return 0
    except urllib.error.HTTPError as error:
        write_console("HTTP {}: {}".format(error.code, error.read().decode("utf-8", errors="replace")), sys.stderr)
        return 1
    except urllib.error.URLError as error:
        # 自动安装、路径发现和启动均已在 ensure_service 中完成；这里不再把安装责任推给用户。
        # 唯一可能需要用户参与的是浏览器登录，因此错误提示只保留可执行的登录/重试建议。
        write_console("Doxent CLI 已自动安装并尝试启动，但本地服务仍不可用：{}。如已打开登录页，请先完成登录，然后重试。".format(error.reason), sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
