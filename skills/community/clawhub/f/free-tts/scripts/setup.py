#!/usr/bin/env python3
"""
setup.py — free-tts 初始化向导。

子命令:
    check        检查 FISH_API_KEY / MIMO_API_KEY 配置状态（只显示脱敏信息）
    set-fish     写入 FISH_API_KEY 到 Windows 用户级环境变量（隐藏输入或 --from-file）
    set-mimo     写入 MIMO_API_KEY 到 Windows 用户级环境变量
    test-fish    用一次轻量 GET /model 请求验证 Fish key 有效性
    test-mimo    用一次最小 TTS 请求验证 MiMo key 有效性

安全原则:
    - key 只写环境变量，不写入任何 skill 文件
    - 输出永远脱敏: abcd***1234
    - --from-file 读取后立即删除该临时文件
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

FISH_KEY_URL = "https://fish.audio/app/api-keys/"
MIMO_KEY_URL = "https://platform.xiaomimimo.com/#/console/api-keys"
MIMO_REGISTER_URL = "https://id.mi.com/"
FISH_TTS_ENDPOINT = "https://api.fish.audio/v1/tts"
FISH_MODEL_ENDPOINT = "https://api.fish.audio/model"
MIMO_BASE_URL = "https://api.xiaomimimo.com/v1"


def mask(key: str) -> str:
    if not key:
        return "(空)"
    if len(key) <= 8:
        return key[:2] + "***"
    return f"{key[:4]}***{key[-4:]} (len={len(key)})"


def check_env():
    fish = os.environ.get("FISH_API_KEY", "").strip()
    mimo = os.environ.get("MIMO_API_KEY", "").strip()
    print("=== free-tts 环境检查 ===\n")
    print(f"🐟 FISH_API_KEY : {'✅ ' + mask(fish) if fish else '❌ 未设置'}")
    print(f"📱 MIMO_API_KEY : {'✅ ' + mask(mimo) if mimo else '❌ 未设置'}")
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or os.environ.get("HTTP_PROXY")
    print(f"🌐 代理         : {proxy or '(未设置，Windows 系统代理会自动生效)'}")
    print()
    if not fish:
        print("── 获取 Fish Audio key（克隆声音首选）──")
        print(f"  1. 注册/登录 https://fish.audio/ （免费，无需信用卡）")
        print(f"  2. 打开 {FISH_KEY_URL} → Create API Key → 复制 32 字符 key")
        print(f"  3. 运行: python setup.py set-fish   （或把 key 贴给助手帮你写入环境变量）")
        print()
    if not mimo:
        print("── 获取小米 MiMo key（中文音色首选）──")
        print(f"  1. 用小米账号登录 https://platform.xiaomimimo.com/ （没有就去 {MIMO_REGISTER_URL} 注册）")
        print(f"  2. 控制台 → API Keys → 创建（格式 sk-xxxxx）")
        print(f"  3. 运行: python setup.py set-mimo")
        print()
    if fish and mimo:
        print("✅ 双引擎就绪。跑 test-fish / test-mimo 验证连通性。")
    return 0


def set_env_var(name: str, value: str) -> bool:
    """写入 Windows 用户级环境变量（注册表 HKCU\\Environment）。"""
    if sys.platform == "win32":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0,
                                winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE) as k:
                winreg.SetValueEx(k, name, 0, winreg.REG_SZ, value)
            # 广播环境变量变更（新开的终端自动生效）
            try:
                import ctypes
                HWND_BROADCAST = 0xFFFF
                WM_SETTINGCHANGE = 0x001A
                ctypes.windll.user32.SendMessageW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment")
            except Exception:
                pass
            os.environ[name] = value  # 当前进程立即可用
            return True
        except Exception as e:
            print(f"✗ 写入注册表失败: {e}", file=sys.stderr)
            return False
    else:
        print("✗ 非 Windows 平台，请手动 export", file=sys.stderr)
        return False


def do_set(name: str, args):
    value = None
    if args.from_file:
        from pathlib import Path
        p = Path(args.from_file)
        if not p.exists():
            print(f"✗ 文件不存在: {args.from_file}", file=sys.stderr)
            return 1
        value = p.read_text(encoding="utf-8").strip()
        try:
            p.unlink()  # 读完即删，避免 key 残留
            print(f"  (已读取并删除临时文件 {p})")
        except Exception as e:
            print(f"  ⚠️ 读取成功但删除临时文件失败，请手动删除: {p} ({e})")
    elif sys.stdin.isatty():
        import getpass
        value = getpass.getpass(f"粘贴 {name}（输入不回显）: ").strip()
    else:
        print(f"✗ 非交互终端请用 --from-file <path>（文件内容为 key，读完自动删除）", file=sys.stderr)
        return 1

    if not value:
        print("✗ key 为空", file=sys.stderr)
        return 1
    if name == "FISH_API_KEY" and len(value) != 32:
        print(f"⚠️ Fish key 通常 32 字符，当前 {len(value)} 字符——仍然写入，如失败请核对")
    if name == "MIMO_API_KEY" and not value.startswith(("sk-", "tp-")):
        print(f"⚠️ MiMo key 通常以 sk- / tp- 开头，当前格式异常——仍然写入，如失败请核对")

    if set_env_var(name, value):
        print(f"✅ {name} 已写入用户级环境变量: {mask(value)}")
        print("   （新开的终端自动生效；本进程已立即可用）")
        return 0
    return 1


def http_post_json(url: str, payload: dict, headers: dict, timeout: int = 120):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read(), dict(resp.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), {}
    except urllib.error.URLError as e:
        return None, str(e.reason).encode(), {}


def test_fish(args):
    key = os.environ.get("FISH_API_KEY", "").strip()
    if not key:
        print("✗ FISH_API_KEY 未设置，先跑 check / set-fish", file=sys.stderr)
        return 1
    print(f"🐟 验证 Fish Audio key {mask(key)} ...")
    req = urllib.request.Request(
        FISH_MODEL_ENDPOINT + "?pageSize=1",
        headers={"Authorization": f"Bearer {key}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            print(f"✅ Fish API 连通 (HTTP {resp.status})，key 有效。")
            try:
                data = json.loads(body)
                items = data.get("items", []) if isinstance(data, dict) else data
                print(f"   账号下已有 {len(items) if isinstance(items, list) else '?'} 个 voice 模型（首页）。")
            except json.JSONDecodeError:
                pass
            return 0
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("❌ 401 — key 无效，请重新到 fish.audio/app/api-keys 生成", file=sys.stderr)
        else:
            print(f"❌ HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:300]}", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"❌ 网络错误: {e.reason}", file=sys.stderr)
        print("   💡 Fish 是海外 API。若直连失败，设置代理后重试:", file=sys.stderr)
        print("      set HTTPS_PROXY=http://127.0.0.1:7897  (Clash 默认端口)", file=sys.stderr)
        return 1


def test_mimo(args):
    key = os.environ.get("MIMO_API_KEY", "").strip()
    if not key:
        print("✗ MIMO_API_KEY 未设置，先跑 check / set-mimo", file=sys.stderr)
        return 1
    print(f"📱 验证小米 MiMo key {mask(key)} ...（会发起一次最小合成请求）")
    payload = {
        "model": "mimo-v2.5-tts",
        "messages": [{"role": "assistant", "content": "测试。"}],
        "audio": {"format": "wav", "voice": "冰糖"},
    }
    headers = {
        "Authorization": f"Bearer {key}",
        "api-key": key,
        "Content-Type": "application/json",
    }
    status, body, _ = http_post_json(MIMO_BASE_URL + "/chat/completions", payload, headers, timeout=60)
    if status == 200:
        print("✅ MiMo API 连通，key 有效，TTS 合成成功。")
        return 0
    text = body.decode("utf-8", errors="replace")[:400] if body else ""
    if status in (401, 403):
        print(f"❌ {status} — key 无效，请到 {MIMO_KEY_URL} 重新创建", file=sys.stderr)
    elif status is None:
        print(f"❌ 网络错误: {text}", file=sys.stderr)
    else:
        print(f"❌ HTTP {status}: {text}", file=sys.stderr)
    return 1


def main():
    ap = argparse.ArgumentParser(description="free-tts 初始化向导（Fish Audio + 小米 MiMo）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", help="检查 key 配置状态")
    for name in ("fish", "mimo"):
        p = sub.add_parser(f"set-{name}", help=f"写入 {name.upper()}_API_KEY")
        p.add_argument("--from-file", help="从文件读取 key（读完自动删除，适合非交互场景）")
    sub.add_parser("test-fish", help="验证 Fish key")
    sub.add_parser("test-mimo", help="验证 MiMo key")
    args = ap.parse_args()

    if args.cmd == "check":
        return check_env()
    if args.cmd == "set-fish":
        return do_set("FISH_API_KEY", args)
    if args.cmd == "set-mimo":
        return do_set("MIMO_API_KEY", args)
    if args.cmd == "test-fish":
        return test_fish(args)
    if args.cmd == "test-mimo":
        return test_mimo(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
