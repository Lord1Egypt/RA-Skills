"""
start_chrome.py - 以 CDP 模式启动 Chrome（browser-use-init skill 核心脚本）

Chrome 130+ 要求 remote debugging 必须使用非默认 user-data-dir。
本脚本将 Default profile 复制到自定义目录，绕开此限制。

环境变量配置（可选）:
    CHROME_EXE              Chrome 可执行文件路径（默认自动检测）
    CHROME_SRC_DIR          Chrome 源 profile 目录（默认 %LOCALAPPDATA%）
    CHROME_PROFILE_DIR      目标 profile 复制目录（默认 %TEMP%/browser-use-chrome-profile）
    CDP_PORT                CDP 调试端口（默认 9222）

用法:
    python start_chrome.py
    
    或设置环境变量后:
    $env:CHROME_PROFILE_DIR = "E:\my-profile"; python start_chrome.py
"""

import subprocess, time, shutil, urllib.request, json, sys, os, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# 配置项 - 可通过环境变量覆盖
CHROME_EXE = os.getenv(
    "CHROME_EXE",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe"
)
SRC_DIR = os.path.expandvars(
    os.getenv("CHROME_SRC_DIR", r"%LOCALAPPDATA%\Google\Chrome\User Data")
)
DST_DIR = os.getenv(
    "CHROME_PROFILE_DIR",
    os.path.join(os.path.expandvars("%TEMP%"), "browser-use-chrome-profile")
)
PORT = int(os.getenv("CDP_PORT", "9222"))


def copy_profile_if_needed():
    if os.path.exists(DST_DIR):
        print(f"[profile] 已存在，跳过复制")
        return
    print(f"[profile] 首次复制 profile...")
    os.makedirs(DST_DIR, exist_ok=True)
    # 复制 Local State
    src_ls = os.path.join(SRC_DIR, "Local State")
    if os.path.exists(src_ls):
        shutil.copy2(src_ls, os.path.join(DST_DIR, "Local State"))
    # 复制 Default profile
    src_def = os.path.join(SRC_DIR, "Default")
    dst_def = os.path.join(DST_DIR, "Default")
    if os.path.exists(src_def):
        print(f"  复制 Default (~可能需要几分钟)...")
        shutil.copytree(src_def, dst_def, ignore=shutil.ignore_patterns(
            "Cache", "Code Cache", "GPUCache", "DawnCache",
            "ShaderCache", "logs", "*.log"
        ))
    print(f"[profile] 复制完成: {DST_DIR}")


def kill_chrome():
    subprocess.run(["taskkill", "/F", "/IM", "chrome.exe", "/T"], capture_output=True)
    time.sleep(2)


def start_chrome():
    cmd = (
        f'"{CHROME_EXE}"'
        f' --remote-debugging-port={PORT}'
        f' --remote-allow-origins=*'
        f' --user-data-dir="{DST_DIR}"'
        f' --profile-directory=Default'
        f' --no-first-run'
        f' --no-default-browser-check'
    )
    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def wait_for_cdp(timeout=20):
    for i in range(timeout):
        time.sleep(1)
        try:
            resp = urllib.request.urlopen(f"http://localhost:{PORT}/json/version", timeout=1)
            data = json.loads(resp.read())
            return data
        except:
            print(f"  等待 CDP... {i+1}s")
    return None


def get_ws_url():
    resp = urllib.request.urlopen(f"http://localhost:{PORT}/json/version", timeout=3)
    return json.loads(resp.read())["webSocketDebuggerUrl"]


if __name__ == "__main__":
    print("[INFO] Chrome Profile Dir:", DST_DIR)
    print("[INFO] CDP Port:", PORT)
    print()
    
    print("[1] 关闭现有 Chrome...")
    kill_chrome()

    print("[2] 准备 profile...")
    copy_profile_if_needed()

    print("[3] 启动 Chrome (CDP 模式)...")
    start_chrome()

    print("[4] 等待 CDP 就绪...")
    info = wait_for_cdp()
    if info:
        print(f"[OK] Chrome 已启动: {info.get('Browser')}")
        print(f"[OK] CDP 端口 {PORT} 就绪")
        print(f"[OK] WS URL: {info.get('webSocketDebuggerUrl')}")
        print(f"\n提示: 如果登录态丢失，请在浏览器中手动登录一次，Cookie 将保存到自定义 profile。")
    else:
        print("[ERROR] CDP 超时，请检查 Chrome 是否正常安装")
        sys.exit(1)
