# -*- coding: utf-8 -*-
import os
import json
import time
import ctypes
import subprocess
from typing import Dict, Any, Optional, List
from ctypes import wintypes


CONFIG_FILE = "config.json"

SUPPORTED_APPS = {
    "abaqus",
    "ansys",
    "ansa",
    "hyperworks"
}

SUPPORTED_FILE_EXTS = {
    "abaqus": {
        ".cae", ".odb", ".jnl", ".py"
    },
    "ansys": {
        ".wbpj", ".mechdb", ".agdb", ".cdb", ".rst"
    },
    "ansa": {
        ".ansa", ".nas", ".bdf", ".dat", ".key", ".k", ".inp"
    },
    "hyperworks": {
        ".hm", ".mvw", ".fem", ".op2", ".res", ".h3d"
    }
}

APP_WINDOW_KEYWORDS = {
    "abaqus": ["abaqus", "simulia"],
    "ansys": ["ansys", "workbench", "mechanical"],
    "ansa": ["ansa"],
    "hyperworks": ["hyperworks", "hypermesh", "hyperview", "altair"]
}


def ok(**kwargs) -> Dict[str, Any]:
    data = {"success": True}
    data.update(kwargs)
    return data


def fail(message: str, **kwargs) -> Dict[str, Any]:
    data = {"success": False, "message": message}
    data.update(kwargs)
    return data


def load_config(config_file: str = CONFIG_FILE) -> Dict[str, Any]:
    if not os.path.isfile(config_file):
        return fail(f"配置文件不存在: {config_file}")

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        return ok(config=cfg)
    except Exception as e:
        return fail(f"读取配置文件失败: {e}")


def save_config(config: Dict[str, Any], config_file: str = CONFIG_FILE) -> Dict[str, Any]:
    try:
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return ok(config_file=config_file)
    except Exception as e:
        return fail(f"写入配置文件失败: {e}", config_file=config_file)


def get_app_info(app: str, config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return config.get("apps", {}).get(app.lower())


def validate_app(app: str) -> Dict[str, Any]:
    if not app:
        return fail("未提供 app 参数")

    app = app.strip().lower()
    if app not in SUPPORTED_APPS:
        return fail(f"不支持的 app: {app}，当前支持: {sorted(SUPPORTED_APPS)}")

    return ok(app=app)


def validate_file_path(file_path: str) -> Dict[str, Any]:
    if not file_path:
        return fail("未提供 file_path")

    if not os.path.isfile(file_path):
        return fail("文件不存在", file_path=file_path)

    return ok(file_path=file_path)


def validate_file_type_for_app(app: str, file_path: str) -> Dict[str, Any]:
    ext = os.path.splitext(file_path)[1].lower()
    allowed = SUPPORTED_FILE_EXTS.get(app, set())

    if ext not in allowed:
        return fail(
            f"{app} 暂不支持该文件类型: {ext}",
            app=app,
            file_path=file_path,
            ext=ext
        )

    return ok(app=app, file_path=file_path, ext=ext)


def _tasklist_output() -> str:
    try:
        return subprocess.check_output(
            ["tasklist"],
            text=True,
            encoding="gbk",
            errors="ignore"
        ).lower()
    except Exception:
        return subprocess.check_output(
            ["tasklist"],
            text=True,
            encoding="utf-8",
            errors="ignore"
        ).lower()


def _get_active_window_title() -> str:
    user32 = ctypes.WinDLL("user32", use_last_error=True)

    GetForegroundWindow = user32.GetForegroundWindow
    GetForegroundWindow.restype = wintypes.HWND

    GetWindowTextLengthW = user32.GetWindowTextLengthW
    GetWindowTextLengthW.argtypes = [wintypes.HWND]
    GetWindowTextLengthW.restype = ctypes.c_int

    GetWindowTextW = user32.GetWindowTextW
    GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    GetWindowTextW.restype = ctypes.c_int

    hwnd = GetForegroundWindow()
    if not hwnd:
        return ""

    length = GetWindowTextLengthW(hwnd)
    if length == 0:
        return ""

    buf = ctypes.create_unicode_buffer(length + 1)
    GetWindowTextW(hwnd, buf, length + 1)
    return buf.value.strip()


def _detect_app_from_window_title(title: str) -> Optional[str]:
    if not title:
        return None

    title_lower = f" {title.lower()} "
    for app, keywords in APP_WINDOW_KEYWORDS.items():
        for kw in keywords:
            if kw in title_lower:
                return app
    return None


def detect_app_path(app: str, config_file: str = CONFIG_FILE) -> Dict[str, Any]:
    """
    注意：
    abaqus 启动/打开文件优先使用命令 `abaqus ...`，不依赖这里的路径。
    这个函数仍然保留，用于配置管理一致性。
    """
    app_check = validate_app(app)
    if not app_check["success"]:
        return app_check
    app = app_check["app"]

    cfg = load_config(config_file)
    if not cfg["success"]:
        return cfg
    config = cfg["config"]

    app_info = get_app_info(app, config)
    if not app_info:
        return fail(f"配置中未找到软件: {app}", app=app)

    saved_paths = app_info.get("saved_paths", [])
    candidate_paths = app_info.get("candidate_paths", [])

    for p in saved_paths:
        if os.path.isfile(p):
            return ok(
                app=app,
                path=p,
                source="saved_paths",
                message=f"已从保存路径中找到 {app}"
            )

    for p in candidate_paths:
        if os.path.isfile(p):
            return ok(
                app=app,
                path=p,
                source="candidate_paths",
                message=f"已从常规路径中找到 {app}"
            )

    return fail(
        f"未找到 {app} 安装路径，请用户提供可执行文件完整路径",
        app=app,
        need_user_path=True
    )


def set_app_path(app: str, path: str, config_file: str = CONFIG_FILE) -> Dict[str, Any]:
    app_check = validate_app(app)
    if not app_check["success"]:
        return app_check
    app = app_check["app"]

    if not path:
        return fail("未提供 path 参数", app=app)

    path = path.strip()

    if not os.path.isfile(path):
        return fail("提供的路径不存在或不是文件", app=app, path=path)

    cfg = load_config(config_file)
    if not cfg["success"]:
        return cfg
    config = cfg["config"]

    app_info = get_app_info(app, config)
    if not app_info:
        return fail(f"配置中未找到软件: {app}", app=app)

    saved_paths = app_info.setdefault("saved_paths", [])

    if path not in saved_paths:
        saved_paths.insert(0, path)

    save_result = save_config(config, config_file=config_file)
    if not save_result["success"]:
        return save_result

    return ok(
        app=app,
        path=path,
        message=f"已保存 {app} 路径"
    )


def find_executable(app: str, config: Dict[str, Any]) -> Optional[str]:
    app_info = get_app_info(app, config)
    if not app_info:
        return None

    for p in app_info.get("saved_paths", []):
        if os.path.isfile(p):
            return p

    for p in app_info.get("candidate_paths", []):
        if os.path.isfile(p):
            return p

    return None


def is_app_running(app: str, config_file: str = CONFIG_FILE) -> Dict[str, Any]:
    app_check = validate_app(app)
    if not app_check["success"]:
        return app_check
    app = app_check["app"]

    cfg = load_config(config_file)
    if not cfg["success"]:
        return cfg

    config = cfg["config"]
    app_info = get_app_info(app, config)
    if not app_info:
        return fail(f"配置中未找到软件: {app}", app=app)

    process_names = [x.lower() for x in app_info.get("process_names", [])]
    if not process_names:
        return fail(f"{app} 未配置 process_names", app=app)

    try:
        output = _tasklist_output()
    except Exception as e:
        return fail(f"检查进程失败: {e}", app=app)

    running = any(name in output for name in process_names)
    return ok(app=app, running=running, process_names=process_names)


def get_running_apps(config_file: str = CONFIG_FILE) -> Dict[str, Any]:
    cfg = load_config(config_file)
    if not cfg["success"]:
        return cfg

    config = cfg["config"]

    try:
        output = _tasklist_output()
    except Exception as e:
        return fail(f"检查进程失败: {e}")

    running_apps: List[str] = []

    for app in sorted(SUPPORTED_APPS):
        app_info = get_app_info(app, config)
        if not app_info:
            continue

        process_names = [x.lower() for x in app_info.get("process_names", [])]
        if any(name in output for name in process_names):
            running_apps.append(app)

    return ok(running_apps=running_apps)


def build_launch_command(app: str, exe_path: str = "") -> List[str]:
    app = app.lower()

    if app == "abaqus":
        return ["cmd", "/k", "abaqus", "cae"]

    if app == "ansys":
        return [exe_path]

    if app == "ansa":
        return [exe_path]

    if app == "hyperworks":
        return [exe_path]

    return [exe_path]


def build_open_file_command(app: str, exe_path: str, file_path: str) -> List[str]:
    app = app.lower()
    ext = os.path.splitext(file_path)[1].lower()

    if app == "abaqus":
        if ext == ".cae":
            return ["cmd", "/k", "abaqus", "cae", f"database={file_path}"]

        if ext == ".odb":
            return ["cmd", "/k", "abaqus", "viewer", f"database={file_path}"]

        if ext in {".jnl", ".py"}:
            return ["cmd", "/k", "abaqus", "cae", f"script={file_path}"]

        return ["cmd", "/k", "abaqus", "cae"]

    if app == "ansys":
        return [exe_path, file_path]

    if app == "ansa":
        return [exe_path, file_path]

    if app == "hyperworks":
        return [exe_path, file_path]

    return [exe_path, file_path]


def launch_app(app: str, config_file: str = CONFIG_FILE) -> Dict[str, Any]:
    app_check = validate_app(app)
    if not app_check["success"]:
        return app_check
    app = app_check["app"]

    exe_path = ""

    if app != "abaqus":
        cfg = load_config(config_file)
        if not cfg["success"]:
            return cfg

        config = cfg["config"]
        exe_path = find_executable(app, config)

        if not exe_path:
            detect_result = detect_app_path(app, config_file=config_file)
            if detect_result["success"]:
                exe_path = detect_result["path"]
            else:
                return detect_result

    command = build_launch_command(app, exe_path)

    try:
        if app == "abaqus":
            p = subprocess.Popen(
                command,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            p = subprocess.Popen(command, shell=False)

        return ok(
            message=f"{app} 已启动",
            app=app,
            exe_path=exe_path if exe_path else None,
            command=command,
            pid=p.pid
        )
    except Exception as e:
        return fail(
            f"{app} 启动失败: {e}",
            app=app,
            exe_path=exe_path if exe_path else None,
            command=command
        )


def open_file_in_app(
    app: str,
    file_path: str,
    config_file: str = CONFIG_FILE,
    auto_launch: bool = True,
    wait_seconds: float = 5.0
) -> Dict[str, Any]:
    app_check = validate_app(app)
    if not app_check["success"]:
        return app_check
    app = app_check["app"]

    file_check = validate_file_path(file_path)
    if not file_check["success"]:
        return file_check

    type_check = validate_file_type_for_app(app, file_path)
    if not type_check["success"]:
        return type_check

    exe_path = ""

    if app != "abaqus":
        cfg = load_config(config_file)
        if not cfg["success"]:
            return cfg

        config = cfg["config"]
        exe_path = find_executable(app, config)

        if not exe_path:
            detect_result = detect_app_path(app, config_file=config_file)
            if detect_result["success"]:
                exe_path = detect_result["path"]
            else:
                return detect_result

    status = is_app_running(app, config_file=config_file)
    if not status["success"]:
        return status

    try:
        if not status["running"]:
            if not auto_launch:
                return fail(
                    f"{app} 当前未启动，且 auto_launch=False",
                    app=app,
                    file_path=file_path
                )

            launch_result = launch_app(app, config_file=config_file)
            if not launch_result["success"]:
                return launch_result

            time.sleep(wait_seconds)

        command = build_open_file_command(app, exe_path, file_path)

        if app == "abaqus":
            p = subprocess.Popen(
                command,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            p = subprocess.Popen(command, shell=False)

        return ok(
            message=f"已使用 {app} 打开文件",
            app=app,
            file_path=file_path,
            exe_path=exe_path if exe_path else None,
            command=command,
            pid=p.pid
        )

    except Exception as e:
        return fail(
            f"打开文件失败: {e}",
            app=app,
            file_path=file_path,
            exe_path=exe_path if exe_path else None
        )


def close_app(app: str, config_file: str = CONFIG_FILE, force: bool = True) -> Dict[str, Any]:
    app_check = validate_app(app)
    if not app_check["success"]:
        return app_check
    app = app_check["app"]

    cfg = load_config(config_file)
    if not cfg["success"]:
        return cfg

    config = cfg["config"]
    app_info = get_app_info(app, config)
    if not app_info:
        return fail(f"配置中未找到软件: {app}", app=app)

    process_names = app_info.get("process_names", [])
    if not process_names:
        return fail(f"{app} 未配置 process_names", app=app)

    status = is_app_running(app, config_file=config_file)
    if not status["success"]:
        return status

    if not status["running"]:
        return ok(
            message=f"{app} 当前未运行，无需关闭",
            app=app,
            closed=False
        )

    errors = []
    closed_any = False

    for proc in process_names:
        cmd = ["taskkill", "/IM", proc]
        if force:
            cmd.append("/F")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="gbk",
                errors="ignore"
            )
            if result.returncode == 0:
                closed_any = True
            else:
                msg = result.stderr.strip() or result.stdout.strip()
                if msg:
                    errors.append(msg)
        except Exception as e:
            errors.append(str(e))

    if closed_any:
        return ok(
            message=f"{app} 已关闭",
            app=app,
            closed=True,
            errors=errors
        )

    return fail(
        f"{app} 关闭失败",
        app=app,
        errors=errors
    )


def get_active_app(config_file: str = CONFIG_FILE) -> Dict[str, Any]:
    cfg = load_config(config_file)
    if not cfg["success"]:
        return cfg

    try:
        title = _get_active_window_title()
    except Exception as e:
        return fail(f"获取当前活动窗口失败: {e}")

    active_app = _detect_app_from_window_title(title)

    running_result = get_running_apps(config_file=config_file)
    if not running_result["success"]:
        return running_result

    return ok(
        active_app=active_app,
        active_window_title=title,
        detected=active_app is not None,
        running_apps=running_result["running_apps"],
        message="检测完成"
    )


if __name__ == "__main__":
    print("Use skill_runner.py to execute cae_skill actions.")