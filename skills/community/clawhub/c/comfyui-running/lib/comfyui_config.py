#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ComfyUI 配置读取模块
==================

【配置优先级】
    环境变量 > config.json > 自动检测默认值

【跨平台支持】
    - Windows: 自动检测 D:/ E:/ H:/ 等盘符
    - Linux: /opt/ComfyUI, ~/ComfyUI 等
    - macOS: /Applications/ComfyUI, ~/ComfyUI
    - WSL: /mnt/c/, /mnt/h/ 访问 Windows 盘符

【环境变量】
    COMFYUI_ROOT           - ComfyUI 安装根目录
    COMFYUI_PORT           - ComfyUI 端口（默认 8188）
    CDP_PORT               - Chrome 调试端口（默认 9222）
    COMFYUI_WORKFLOWS_DIR  - 工作流目录
    COMFYUI_MODELS_DIR     - 模型目录
    COMFYUI_OUTPUT_DIR     - 输出目录

【用法示例】
    from comfyui_config import get_comfyui_root, get_workflows_dir

【Windows/Linux 路径差异】
    Windows: H:/ComfyUI-aki-v3/ComfyUI 或 H:\\ComfyUI-aki-v3\\ComfyUI
    Linux:   /opt/ComfyUI/ComfyUI
    WSL:     /mnt/h/ComfyUI-aki-v3/ComfyUI (访问 Windows 盘符)

    ⚠️ 推荐始终使用正斜杠 /，Python 的 os.path 会自动处理跨平台兼容性
"""
import os
import json
import platform
import shutil
import requests
import re

# ============ 常量定义 ============
DEFAULT_COMFYUI_PORT = 8188  # ComfyUI 默认端口
DEFAULT_CDP_PORT = 9222      # Chrome DevTools Protocol 默认端口

# Windows 盘符列表（用于自动检测）
# WINDOWS_DRIVES = ["C", "D", "E", "F", "G", "H", ...]


def _get_config_path():
    """
    获取 config.json 路径
    
    【路径规则】
        - 优先: 与本文件同目录的 config.json
        - 回退: 上一级目录的 config.json（兼容 skill 目录结构）
    """
    # 获取本文件所在目录（lib/）
    base = os.path.dirname(os.path.abspath(__file__))
    # 上一级目录（skill 根目录）
    parent = os.path.dirname(base)
    
    # 优先查找 lib/ 目录下的 config.json
    config_in_lib = os.path.join(base, "config.json")
    if os.path.exists(config_in_lib):
        return config_in_lib
    
    # 回退到 parent 目录
    return os.path.join(parent, "config.json")


def _load_config():
    """加载 config.json"""
    config_path = _get_config_path()
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            # 尝试 UTF-8-BOM 编码（部分 Windows 文件）
            try:
                with open(config_path, "r", encoding="utf-8-sig") as f:
                    return json.load(f)
            except Exception:
                return {}
    return {}


def _save_config(config):
    """保存 config.json"""
    config_path = _get_config_path()
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return True
    except Exception:
        return False


def _is_wsl():
    """
    检测是否在 WSL (Windows Subsystem for Linux) 环境下
    
    【判断方法】
        读取 /proc/version，检查是否包含 "microsoft"（大小写不敏感）
    
    【返回值】
        True  - WSL 环境
        False - 非 WSL 环境
    """
    if platform.system() != "Linux":
        return False
    try:
        with open("/proc/version", "r") as f:
            content = f.read().lower()
            return "microsoft" in content
    except Exception:
        return False


def _get_system():
    """
    获取当前系统类型
    
    【返回值】
        'windows' - Windows 系统
        'linux'   - Linux 系统（非 WSL）
        'darwin'  - macOS 系统
        'wsl'     - WSL 环境（Linux 内核但能访问 Windows 文件）
    
    【注意】
        WSL 返回 'wsl' 而非 'linux'，因为路径处理方式不同
    """
    if _is_wsl():
        return "wsl"
    return platform.system().lower()


def _normalize_path(path):
    """
    标准化路径分隔符
    
    【作用】
        将路径中的反斜杠 \\ 转换为正斜杠 /
        确保跨平台兼容性
    
    【示例】
        Windows: "H:\\ComfyUI\\ComfyUI" → "H:/ComfyUI/ComfyUI"
        Linux:   "/opt/ComfyUI/ComfyUI" → "/opt/ComfyUI/ComfyUI"（不变）
    """
    if not path:
        return path
    return os.path.normpath(path)


def _get_windows_drives():
    """
    获取 Windows 上所有可用盘符
    
    【返回值】
        ['C', 'D', 'E', 'F', ...]  盘符列表
    
    【注意】
        - 始终包含系统盘 C:
        - 自动检测 D: E: F: ... 是否存在
        - 仅 Windows 有效，其他系统返回 ['C']
    """
    drives = []
    system = _get_system()
    
    if system == "windows":
        # 系统盘
        system_drive = os.environ.get('SystemDrive', 'C:')
        drives.append(system_drive[0])
        
        # 扫描其他盘符 A-Z
        for letter in "DEFGHIJKLMNOPQRSTUVWXYZ":
            if letter != system_drive[0]:
                # Windows 下检测盘符是否存在
                path = f"{letter}:\\"
                try:
                    if os.path.exists(path):
                        drives.append(letter)
                except (OSError, PermissionError):
                    pass
    else:
        # 非 Windows 系统只有 C 盘概念（WSL 访问 Windows 时用）
        drives = ['c']
    
    return drives


def _find_executable(name):
    """
    跨平台查找可执行文件
    
    【参数】
        name - 可执行文件名（如 "python", "python3", "chrome"）
    
    【返回值】
        完整路径 或 None（未找到）
    
    【搜索顺序】
        1. shutil.which() 系统查找
        2. 常见路径遍历
    """
    # 优先用 shutil.which（跨平台）
    exe = shutil.which(name)
    if exe:
        return exe
    
    system = _get_system()
    
    if system in ("linux", "wsl"):
        # Linux/WLS 常见路径
        candidates = [
            f"/usr/bin/{name}",
            f"/usr/local/bin/{name}",
            f"/snap/bin/{name}",
            os.path.expanduser(f"~/.local/bin/{name}"),
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
    
    elif system == "darwin":
        # macOS 特殊路径
        if "chrome" in name.lower():
            candidates = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium",
            ]
            for c in candidates:
                if os.path.exists(c):
                    return c
    
    return None


def _find_python():
    """
    跨平台查找 Python 解释器
    
    【搜索顺序】
        1. conda 环境 (CONDA_DEFAULT_ENV / CONDA_PREFIX)
        2. 虚拟环境 (VIRTUAL_ENV)
        3. 系统 Python (python3 / python.exe)
        4. 常见安装路径
    
    【返回值】
        Python 解释器完整路径
    
    【Windows vs Linux 差异】
        Windows: 返回 python.exe，优先找 conda/venv 的 Scripts/python.exe
        Linux:   返回 python3，优先找 conda/venv 的 bin/python
    """
    system = _get_system()
    
    # 1. conda 环境
    if "CONDA_DEFAULT_ENV" in os.environ:
        if system == "windows":
            # Windows conda: {CONDA_PREFIX}/python.exe
            conda_python = os.path.join(os.environ.get("CONDA_PREFIX", ""), "python.exe")
        else:
            # Linux/macOS conda: {CONDA_PREFIX}/bin/python
            conda_python = os.path.join(os.environ.get("CONDA_PREFIX", ""), "bin", "python")
        
        if os.path.exists(conda_python):
            return conda_python
    
    # 2. 虚拟环境
    if "VIRTUAL_ENV" in os.environ:
        if system == "windows":
            # Windows venv: {VIRTUAL_ENV}/Scripts/python.exe
            venv_python = os.path.join(os.environ.get("VIRTUAL_ENV", ""), "Scripts", "python.exe")
        else:
            # Linux/macOS venv: {VIRTUAL_ENV}/bin/python
            venv_python = os.path.join(os.environ.get("VIRTUAL_ENV", ""), "bin", "python")
        
        if os.path.exists(venv_python):
            return venv_python
    
    # 3. 系统 Python
    for name in ["python3", "python"]:
        exe = _find_executable(name)
        if exe:
            return exe
    
    # 4. Windows 常见安装路径
    if system == "windows":
        for ver in ["3.11", "3.10", "3.12", "3.9", "3.8"]:
            paths = [
                f"C:\\Python{ver}\\python.exe",
                f"C:\\Program Files\\Python{ver}\\python.exe",
                os.path.expanduser(f"~\\AppData\\Local\\Programs\\Python\\Python{ver}\\python.exe"),
            ]
            for path in paths:
                if os.path.exists(path):
                    return path
        return "python.exe"  # 最后 fallback
    else:
        return "python3"  # Linux/macOS fallback


# ============ ComfyUI 检测增强 ============

# ComfyUI 关键文件标记（满足任一即认为是有效安装）
# 这些文件是 ComfyUI 特有的，可用于识别安装目录
COMFYUI_MARKERS = [
    "main.py",                  # 主入口文件（必须有）
    "extra_model_paths.yaml",   # 秋叶版配置文件
    "python.bat",               # Windows 启动脚本（秋叶版）
    "python.sh",                # Linux 启动脚本
    "run.bat",                  # Windows 快捷启动
    "ComfyUI_Manager",         # 管理器目录
]

# 版本文件
VERSION_FILES = [
    "version.txt",
    "__init__.py",
]


def _check_comfyui_markers(path):
    """
    检查路径中包含多少个 ComfyUI 标记文件
    
    【参数】
        path - 疑似 ComfyUI 目录路径
    
    【返回值】
        (marker_count, version_hint)
        - marker_count: 找到的标记文件数量
        - version_hint: 版本号字符串 或 None
    """
    if not path or not os.path.exists(path):
        return 0, None
    
    marker_count = 0
    version_hint = None
    
    # 检查关键文件
    for marker in COMFYUI_MARKERS:
        if os.path.exists(os.path.join(path, marker)):
            marker_count += 1
    
    # 检查版本文件
    for vf in VERSION_FILES:
        vp = os.path.join(path, vf)
        if os.path.exists(vp):
            try:
                with open(vp, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read(200)
                    # 尝试提取版本号（如 0.15.1）
                    vmatch = re.search(r'(\d+\.\d+(?:\.\d+)?)', content)
                    if vmatch:
                        version_hint = vmatch.group(1)
                        break
            except Exception:
                pass
    
    # 检查 nodes 目录（表示有自定义节点）
    if os.path.isdir(os.path.join(path, "models", "nodes")):
        marker_count += 1
    
    return marker_count, version_hint


def _is_comfyui_installation(path):
    """
    检测路径是否是有效的 ComfyUI 安装
    
    【检测规则】
        1. main.py 必须存在（最基础验证）
        2. 至少再满足一个条件：
           - python.bat / python.sh（启动脚本）
           - extra_model_paths.yaml（秋叶版配置）
           - models/ 目录
           - custom_nodes/ 目录
    
    【返回值】
        True  - 有效 ComfyUI 安装
        False - 不是有效安装
    
    【示例】
        _is_comfyui_installation("H:/ComfyUI-aki-v3/ComfyUI")  # True
        _is_comfyui_installation("H:/SomeOtherApp")              # False
    """
    if not path or not os.path.exists(path):
        return False
    
    main_py = os.path.join(path, "main.py")
    if not os.path.exists(main_py):
        return False
    
    # main.py 必须存在，再检查至少一个辅助标记
    extras = [
        os.path.exists(os.path.join(path, "python.bat")),       # Windows 启动
        os.path.exists(os.path.join(path, "python.sh")),        # Linux 启动
        os.path.exists(os.path.join(path, "run.bat")),         # Windows run脚本
        os.path.exists(os.path.join(path, "extra_model_paths.yaml")),  # 秋叶版
        os.path.isdir(os.path.join(path, "models")),            # 有models目录
        os.path.isdir(os.path.join(path, "custom_nodes")),      # 有custom_nodes
    ]
    
    return any(extras)


def _get_comfyui_version(path):
    """
    获取 ComfyUI 版本号
    
    【检测顺序】
        1. version.txt 文件
        2. __init__.py 中的 __version__
    
    【返回值】
        版本字符串 或 None
    """
    if not path:
        return None
    
    # 尝试从 version.txt
    version_file = os.path.join(path, "version.txt")
    if os.path.exists(version_file):
        try:
            with open(version_file, "r", encoding="utf-8", errors="ignore") as f:
                return f.read().strip()
        except Exception:
            pass
    
    # 尝试从 __init__.py
    init_file = os.path.join(path, "__init__.py")
    if os.path.exists(init_file):
        try:
            with open(init_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(500)
                vmatch = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
                if vmatch:
                    return vmatch.group(1)
        except Exception:
            pass
    
    return None


def _check_api_and_get_info(port, timeout=2):
    """
    检查 ComfyUI API 是否响应，并获取版本信息
    
    【参数】
        port    - ComfyUI 端口
        timeout - 超时时间（秒）
    
    【返回值】
        (is_running, version)
        - is_running: True/False
        - version: 版本字符串 或 None
    """
    try:
        url = f"http://127.0.0.1:{port}/system_stats"
        r = requests.get(url, timeout=timeout)
        if r.status_code == 200:
            data = r.json()
            version = data.get("system", {}).get("comfyui_version", "")
            return True, version
    except Exception:
        pass
    return False, None


def _detect_running_comfyui_port():
    """
    检测当前是否有 ComfyUI 在运行
    
    【返回值】
        (port, version)
        - port: 端口号 或 None
        - version: 版本字符串 或 None
    """
    # 检查常见端口
    for port in [8188, 8189, 8190, 8200]:
        is_running, version = _check_api_and_get_info(port)
        if is_running:
            return port, version
    return None, None


def _rank_comfyui_installation(path, running_port=None):
    """
    评估 ComfyUI 安装的质量分数
    
    【评分规则】
        - 有 main.py: +1 分
        - 每有一个标记文件: +0.5 分
        - 有版本号: 额外加分
        - 正在运行: +10 分
        - 有完整目录结构(models, custom_nodes, output): 每项+0.3分
    
    【参数】
        path         - ComfyUI 路径
        running_port - 如果知道正在运行的端口，传入用于加分
    
    【返回值】
        (score, details_dict)
    """
    if not _is_comfyui_installation(path):
        return 0, {}
    
    details = {
        "path": path,
        "has_main_py": True,
        "markers_found": 0,
        "version": None,
        "is_running": False,
        "score": 0
    }
    
    score = 1  # 基础分数
    
    # 标记文件分数
    markers, version = _check_comfyui_markers(path)
    details["markers_found"] = markers
    details["version"] = version
    score += markers * 0.5
    
    # 版本分数
    ver = version or _get_comfyui_version(path)
    if ver:
        details["version"] = ver
        try:
            parts = ver.split(".")
            if len(parts) >= 2:
                score += float(parts[0]) * 0.1 + float(parts[1]) * 0.01
        except Exception:
            pass
    
    # 是否正在运行
    if running_port:
        is_running, running_ver = _check_api_and_get_info(running_port)
        if is_running:
            details["is_running"] = True
            score += 10
            if running_ver:
                details["version"] = running_ver
    
    # 目录结构完整性
    important_dirs = ["models", "custom_nodes", "output"]
    for d in important_dirs:
        if os.path.isdir(os.path.join(path, d)):
            score += 0.3
    
    details["score"] = score
    return score, details


# ============ 公共 API ============

def get_comfyui_root():
    """
    获取 ComfyUI 根目录（增强版多安装检测）
    
    【优先级】
        1. 环境变量 COMFYUI_ROOT
        2. config.json 的 comfyui_root
        3. 自动检测（综合评分最高）
    
    【自动检测策略】
        - 验证 main.py 必须存在
        - 验证至少有一个辅助标记
        - 优先选择正在运行的实例
        - 版本号作为参考
    
    【返回值】
        标准化后的路径字符串（正斜杠分隔）
    
    【示例】
        Windows: "H:/ComfyUI-aki-v3/ComfyUI"
        Linux:   "/opt/ComfyUI/ComfyUI"
    """
    # 1. 环境变量
    root = os.environ.get("COMFYUI_ROOT")
    if root and _is_comfyui_installation(root):
        return _normalize_path(root)
    
    # 2. config.json
    config = _load_config()
    if config.get("comfyui_root"):
        root = config["comfyui_root"]
        if _is_comfyui_installation(root):
            return _normalize_path(root)
    
    # 3. 自动检测
    candidates = _get_detection_candidates()
    running_port, _ = _detect_running_comfyui_port()
    
    best_path = None
    best_score = 0
    
    for path in candidates:
        if not path:
            continue
        if not _is_comfyui_installation(path):
            continue
        
        score, _ = _rank_comfyui_installation(path, running_port)
        
        if score > best_score:
            best_score = score
            best_path = path
    
    if best_path:
        return _normalize_path(best_path)
    
    return ""


def get_models_dir():
    """
    获取 ComfyUI 模型目录
    
    【优先级】
        1. 环境变量 COMFYUI_MODELS_DIR
        2. config.json 的 models_dir
        3. {comfyui_root}/models
    """
    models = os.environ.get("COMFYUI_MODELS_DIR")
    if models:
        return _normalize_path(models)
    
    config = _load_config()
    if config.get("models_dir"):
        return _normalize_path(config["models_dir"])
    
    root = get_comfyui_root()
    if root:
        models_path = os.path.join(root, "models")
        if os.path.exists(models_path):
            return _normalize_path(models_path)
    
    return ""


def get_workflows_dir():
    """
    获取工作流目录
    
    【优先级】
        1. 环境变量 COMFYUI_WORKFLOWS_DIR
        2. config.json 的 workflows_dir
        3. skill 自带的 example_workflows
        4. {comfyui_root}/user/default/workflows
    
    【注意】
        优先使用 skill 自带的 example_workflows，确保开箱即用
    """
    workflows = os.environ.get("COMFYUI_WORKFLOWS_DIR")
    if workflows:
        return _normalize_path(workflows)
    
    config = _load_config()
    if config.get("workflows_dir"):
        return _normalize_path(config["workflows_dir"])
    
    # 优先使用 skill 自带的 example_workflows
    skill_wf_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        "..", 
        "example_workflows"
    )
    skill_wf_dir = os.path.normpath(skill_wf_dir)
    if os.path.isdir(skill_wf_dir):
        return skill_wf_dir
    
    # 回退到 ComfyUI 默认工作流目录
    root = get_comfyui_root()
    if root:
        return f"{root}/user/default/workflows"
    
    return ""


def get_output_dir():
    """
    获取输出目录
    
    【优先级】
        1. 环境变量 COMFYUI_OUTPUT_DIR
        2. config.json 的 output_dir
        3. {comfyui_root}/output
    """
    output = os.environ.get("COMFYUI_OUTPUT_DIR")
    if output:
        return _normalize_path(output)
    
    config = _load_config()
    if config.get("output_dir"):
        return _normalize_path(config["output_dir"])
    
    root = get_comfyui_root()
    if root:
        output_path = os.path.join(root, "output")
        if os.path.exists(output_path):
            return _normalize_path(output_path)
    
    return ""


def get_comfyui_port():
    """
    获取 ComfyUI 端口
    
    【优先级】
        1. 环境变量 COMFYUI_PORT
        2. config.json 的 comfyui_port
        3. 自动检测正在运行的端口
        4. 默认值 8188
    """
    port = os.environ.get("COMFYUI_PORT")
    if port:
        try:
            return int(port)
        except ValueError:
            pass
    
    config = _load_config()
    if config.get("comfyui_port"):
        try:
            return int(config["comfyui_port"])
        except ValueError:
            pass
    
    # 检测正在运行的端口
    running_port, _ = _detect_running_comfyui_port()
    if running_port:
        return running_port
    
    return DEFAULT_COMFYUI_PORT


def get_cdp_port():
    """
    获取 Chrome/Edge 调试端口
    """
    port = os.environ.get("CDP_PORT")
    if port:
        try:
            return int(port)
        except ValueError:
            pass
    
    config = _load_config()
    if config.get("cdp_port"):
        try:
            return int(config["cdp_port"])
        except ValueError:
            pass
    
    return DEFAULT_CDP_PORT


def get_browser_path():
    """
    获取浏览器可执行文件路径（跨平台自动检测）
    
    【Windows 检测顺序】
        1. config.json 的 browser_path
        2. Edge: "C:/Program Files (x86)/Microsoft/Edge/..."
        3. Chrome: 用户目录下的 AppData/Local/Google/Chrome/...
        4. 系统 PATH 中的 chrome/edge
    
    【Linux 检测顺序】
        1. config.json 的 browser_path
        2. /usr/bin/google-chrome
        3. /usr/bin/chromium-browser
        4. /snap/bin/chromium
    
    【macOS 检测顺序】
        1. config.json 的 browser_path
        2. /Applications/Google Chrome.app/...
    
    【返回值】
        浏览器完整路径 或 空字符串
    """
    config = _load_config()
    if config.get("browser_path"):
        return config["browser_path"]
    
    system = _get_system()
    
    if system == "windows":
        # Edge 路径
        edge_paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        ]
        for path in edge_paths:
            if os.path.exists(path):
                return path
        
        # Chrome 路径
        chrome_paths = [
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        ]
        for path in chrome_paths:
            if os.path.exists(path):
                return path
    
    elif system in ("linux", "wsl"):
        chrome_paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium-browser",
            "/usr/bin/chromium",
            "/snap/bin/chromium",
            os.path.expanduser("~/.local/bin/google-chrome"),
        ]
        for path in chrome_paths:
            if os.path.exists(path):
                return path
    
    elif system == "darwin":
        chrome_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        ]
        for path in chrome_paths:
            if os.path.exists(path):
                return path
    
    # 最后的 fallback：系统 PATH 中查找
    for name in ["google-chrome", "chromium-browser", "chromium", "msedge"]:
        exe = _find_executable(name)
        if exe:
            return exe
    
    return ""


def get_browser_type():
    """
    获取浏览器类型（edge / chrome）
    
    【判断依据】
        根据 browser_path 路径中是否包含 "edge" 判断
    """
    config = _load_config()
    if config.get("browser_type"):
        return config["browser_type"].lower()
    
    browser_path = get_browser_path()
    if not browser_path:
        return "chrome"
    
    browser_path_lower = browser_path.lower()
    if "edge" in browser_path_lower or "msedge" in browser_path_lower:
        return "edge"
    
    return "chrome"


def get_ui_type():
    """
    获取 UI 类型
    
    【返回值】
        "aki"      - 秋叶版 ComfyUI-aki-v3
        "official" - 官方原版 ComfyUI
        "auto"     - 自动检测
    """
    config = _load_config()
    return config.get("ui_type", "auto")


def get_python_path():
    """
    获取 Python 解释器路径
    
    【优先级】
        1. config.json 的 python_path
        2. _find_python() 自动检测
    
    【注意】
        Windows: 返回 python.exe 完整路径
        Linux:   返回 python3 或完整路径
    """
    config = _load_config()
    if config.get("python_path"):
        path = config["python_path"]
        if os.path.exists(path):
            return path
    
    return _find_python()


def get_comfyui_url():
    """获取 ComfyUI 访问 URL"""
    return f"http://127.0.0.1:{get_comfyui_port()}/"


# ============ 自动检测候选路径 ============

def _get_detection_candidates():
    """
    获取自动检测候选路径列表（跨平台自动适配）
    
    【返回值】
        按优先级排序的路径列表
    
    【Windows 路径示例】
        - H:/ComfyUI-aki-v3/ComfyUI
        - D:/ComfyUI/ComfyUI
        - C:/Users/{user}/ComfyUI/ComfyUI
    
    【Linux 路径示例】
        - /home/{user}/ComfyUI/ComfyUI
        - /opt/ComfyUI/ComfyUI
    
    【WSL 路径示例】
        - /mnt/h/ComfyUI-aki-v3/ComfyUI (访问 Windows 盘符)
        - /mnt/c/Users/{user}/ComfyUI/ComfyUI
    """
    candidates = []
    system = _get_system()
    
    if system == "windows":
        user = os.environ.get("USERNAME", "User")
        drives = _get_windows_drives()
        
        # 优先级1：用户目录
        home = os.path.expanduser("~")
        candidates.extend([
            os.path.join(home, "ComfyUI", "ComfyUI"),
            os.path.join(home, "ComfyUI-aki-v3", "ComfyUI"),
        ])
        
        # 优先级2：常用安装位置
        candidates.extend([
            "H:/ComfyUI-aki-v3/ComfyUI",
            "H:/ComfyUI/ComfyUI",
            "D:/ComfyUI-aki-v3/ComfyUI",
            "D:/ComfyUI/ComfyUI",
        ])
        
        # 扫描所有盘符
        for drive in drives:
            base = f"{drive}:/"
            candidates.extend([
                f"{base}ComfyUI-aki-v3/ComfyUI",
                f"{base}ComfyUI-aki-v1.4/ComfyUI-aki-v1.4",
                f"{base}ComfyUI/ComfyUI",
                f"{base}ComfyUI-aki/ComfyUI",
                f"{base}Program Files/ComfyUI/ComfyUI",
                f"{base}Users/{user}/ComfyUI/ComfyUI",
            ])
    
    elif system in ("linux", "wsl"):
        user = os.environ.get("USER", "user")
        
        candidates.extend([
            os.path.expanduser("~/ComfyUI/ComfyUI"),
            f"/home/{user}/ComfyUI/ComfyUI",
            "/opt/ComfyUI/ComfyUI",
            "/usr/local/ComfyUI/ComfyUI",
            "/snap/ComfyUI/current/ComfyUI",
        ])
        
        # WSL 额外访问 Windows 盘符
        if system == "wsl":
            for drive in ["h", "g", "f", "e", "d", "c"]:
                candidates.extend([
                    f"/mnt/{drive}/ComfyUI-aki-v3/ComfyUI",
                    f"/mnt/{drive}/ComfyUI-aki-v1.4/ComfyUI-aki-v1.4",
                    f"/mnt/{drive}/ComfyUI/ComfyUI",
                ])
    
    elif system == "darwin":
        user = os.environ.get("USER", "user")
        candidates.extend([
            "/Applications/ComfyUI.app/Contents/MacOS/ComfyUI",
            f"/Users/{user}/ComfyUI/ComfyUI",
            os.path.expanduser("~/ComfyUI/ComfyUI"),
        ])
    
    # 去重（保持顺序）
    seen = set()
    result = []
    for c in candidates:
        if c and c not in seen:
            seen.add(c)
            result.append(c)
    
    return result


def detect_and_save_config():
    """
    自动检测 ComfyUI 并生成/更新 config.json
    
    【返回值】
        检测到的配置字典
    """
    config_path = _get_config_path()
    
    # 如果已有有效配置，不覆盖
    if os.path.exists(config_path):
        config = _load_config()
        if config.get("comfyui_root") and _is_comfyui_installation(config.get("comfyui_root", "")):
            return config
    
    # 检测正在运行的
    running_port, running_ver = _detect_running_comfyui_port()
    
    best_path = None
    best_score = 0
    
    for path in _get_detection_candidates():
        if not path or not _is_comfyui_installation(path):
            continue
        
        score, _ = _rank_comfyui_installation(path, running_port)
        if score > best_score:
            best_score = score
            best_path = path
    
    if best_path:
        # 判断 UI 类型
        ui_type = "aki" if "aki" in best_path.lower() else "official"
        
        # 判断浏览器类型
        browser_path = get_browser_path()
        browser_type = "edge" if browser_path and "edge" in browser_path.lower() else "chrome"
        
        config = {
            "comfyui_root": best_path,
            "comfyui_port": running_port or DEFAULT_COMFYUI_PORT,
            "cdp_port": DEFAULT_CDP_PORT,
            "ui_type": ui_type,
            "browser_type": browser_type,
            "browser_path": browser_path if browser_path else None,
            "_note": "auto-detected, please verify",
            "_detected_system": _get_system(),
            "_version": running_ver or _get_comfyui_version(best_path),
            "_is_running": running_port is not None
        }
        
        # 移除 None 值
        config = {k: v for k, v in config.items() if v is not None}
        _save_config(config)
        return config
    
    return {}


# ============ 诊断函数 ============

def diagnose_comfyui_installations():
    """
    诊断所有检测到的 ComfyUI 安装（用于调试）
    
    【返回值】
        按评分排序的安装列表
    """
    running_port, running_ver = _detect_running_comfyui_port()
    
    results = []
    for path in _get_detection_candidates():
        if not path or not os.path.exists(path):
            continue
        
        if not _is_comfyui_installation(path):
            continue
        
        score, details = _rank_comfyui_installation(path, running_port)
        details["detected_path"] = path
        results.append(details)
    
    results.sort(key=lambda x: x.get("score", 0), reverse=True)
    return results


if __name__ == "__main__":
    """调试信息输出"""
    print("=== ComfyUI Config ===")
    print(f"Platform: {platform.system()}")
    print(f"System: {_get_system()}")
    print(f"WSL: {_is_wsl()}")
    print(f"COMFYUI_ROOT: {get_comfyui_root() or '(not set)'}")
    print(f"MODELS_DIR: {get_models_dir() or '(not set)'}")
    print(f"WORKFLOWS_DIR: {get_workflows_dir() or '(not set)'}")
    print(f"OUTPUT_DIR: {get_output_dir() or '(not set)'}")
    print(f"COMFYUI_PORT: {get_comfyui_port()}")
    print(f"CDP_PORT: {get_cdp_port()}")
    print(f"BROWSER_PATH: {get_browser_path() or '(not set)'}")
    print(f"BROWSER_TYPE: {get_browser_type()}")
    print(f"UI_TYPE: {get_ui_type()}")
    print(f"PYTHON_PATH: {get_python_path()}")
    
    print("\n=== Installation Diagnostics ===")
    diag = diagnose_comfyui_installations()
    for i, d in enumerate(diag, 1):
        print(f"\n{i}. Path: {d.get('detected_path', 'N/A')}")
        print(f"   Score: {d.get('score', 0):.2f}")
        print(f"   Version: {d.get('version', 'unknown')}")
        print(f"   Running: {d.get('is_running', False)}")
        print(f"   Markers: {d.get('markers_found', 0)}")
