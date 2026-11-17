#!/usr/bin/env python3
"""
腾讯云智能顾问 - 配置清理脚本

清理本机上 tencent-cloudq 产生的所有配置和缓存文件，
可选删除云端通过本工具创建的 CAM 角色。

用法:
    python3 cleanup.py               # 交互式清理（逐项确认）
    python3 cleanup.py --all         # 一键清理所有本地配置（不含云端角色）
    python3 cleanup.py --all --cloud # 一键清理所有本地配置 + 云端角色

清理范围:
    1. 配置目录  ~/.tencent-cloudq/（含 config.json）
    2. 凭证文件（其他版本残留）  ~/.tencent-cloudq/credential.json
    3. 临时缓存  {系统临时目录}/.tcloud_advisor_uin_cache
    4. 环境变量  TENCENTCLOUD_* 系列环境变量
    5. 云端角色  CAM 角色 advisor（可选，需 AK/SK）

返回码:
    0 - 清理完成
    1 - 用户取消

跨平台支持: Windows / Linux / macOS
"""

import json
import os
import platform
import shutil
import sys
import tempfile
from pathlib import Path

# 导入 tcloud_api 模块（用于可选的云端角色删除）
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from i18n import T  # noqa: E402

# ============== 配置 ==============
CONFIG_DIR = Path.home() / ".tencent-cloudq"
CONFIG_FILE = CONFIG_DIR / "config.json"
CREDENTIAL_FILE = CONFIG_DIR / "credential.json"
CACHE_FILE = Path(tempfile.gettempdir()) / ".tcloud_advisor_uin_cache"
ROLE_NAME = "advisor"

# 智能顾问使用的所有环境变量
ENV_VARS = [
    "TENCENTCLOUD_SECRET_ID",
    "TENCENTCLOUD_SECRET_KEY",
    "TENCENTCLOUD_TOKEN",
    "TENCENTCLOUD_ROLE_ARN",
    "TENCENTCLOUD_ROLE_NAME",
    "TENCENTCLOUD_ROLE_SESSION",
    "TENCENTCLOUD_STS_DURATION",
]


# ============== 终端颜色 ==============
def _supports_color() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if platform.system() == "Windows":
        return os.environ.get("TERM") == "xterm" or hasattr(sys.stderr, "reconfigure")
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


_COLOR = _supports_color()


def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if _COLOR else text


def green(t: str) -> str:
    return _c("32", t)


def red(t: str) -> str:
    return _c("31", t)


def yellow(t: str) -> str:
    return _c("33", t)


def bold(t: str) -> str:
    return _c("1", t)


def dim(t: str) -> str:
    return _c("2", t)


# ============== 工具函数 ==============
def confirm(prompt: str) -> bool:
    """交互式确认，默认为 No"""
    try:
        answer = input(f"{prompt} [y/N]: ").strip().lower()
        return answer in ("y", "yes")
    except (EOFError, KeyboardInterrupt):
        print()
        return False


def read_config() -> dict:
    """读取现有配置文件"""
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def remove_file(path: Path, label: str) -> bool:
    """删除单个文件"""
    if not path.exists():
        print(f"  {dim('[-]')} {label}: {dim(T('不存在，跳过'))}")
        return False
    try:
        path.unlink()
        print(f"  {green('[OK]')} {label}: {T('已删除')}")
        return True
    except OSError as e:
        print(f"  {red('[FAIL]')} {label}: {T('删除失败 - {error}', error=e)}")
        return False


def remove_dir(path: Path, label: str) -> bool:
    """删除目录及其所有内容"""
    if not path.exists():
        print(f"  {dim('[-]')} {label}: {dim(T('不存在，跳过'))}")
        return False
    try:
        shutil.rmtree(str(path))
        print(f"  {green('[OK]')} {label}: {T('已删除')}")
        return True
    except OSError as e:
        print(f"  {red('[FAIL]')} {label}: {T('删除失败 - {error}', error=e)}")
        return False


# ============== 清理动作 ==============
def clean_config_dir(interactive: bool) -> bool:
    """清理配置目录 ~/.tencent-cloudq/"""
    print("\n" + bold(T("1. 配置目录")))

    if not CONFIG_DIR.exists():
        print(f"  {dim('[-]')} {CONFIG_DIR}: {dim(T('不存在，跳过'))}")
        return False

    # 列出目录内容
    files = list(CONFIG_DIR.iterdir())
    print("  " + T("路径: {path}", path=CONFIG_DIR))
    if files:
        for f in files:
            size = f.stat().st_size if f.is_file() else 0
            print(f"    - {f.name} ({size} bytes)")
        # 双装共存保护：目录含凭证/配置文件时警告（国际站自身不使用这些文件）
        if any(f.name in ("credential.json", "config.json") for f in files):
            print(f"  {yellow('[!]')} " + T(
                "注意：目录中的 credential.json / config.json 可能正被其他 CloudQ 版本"
                "（如中文版）使用，删除后该版本需重新登录并重新配置。"))
    else:
        print(f"    {dim(T('(空目录)'))}")

    if interactive and not confirm("\n  " + T("确认删除 {path} ?", path=CONFIG_DIR)):
        print(f"  {yellow('[SKIP]')} {T('用户跳过')}")
        return False

    return remove_dir(CONFIG_DIR, str(CONFIG_DIR))


def clean_oauth_credential(interactive: bool) -> bool:
    """清理凭证文件（其他版本残留）"""
    print("\n" + bold(T("2. 凭证文件")))

    if not CREDENTIAL_FILE.exists():
        print(f"  {dim('[-]')} {CREDENTIAL_FILE}: {dim(T('不存在，跳过'))}")
        return False

    print("  " + T("路径: {path}", path=CREDENTIAL_FILE))
    try:
        cred_data = json.loads(CREDENTIAL_FILE.read_text(encoding="utf-8"))
        secret_id = cred_data.get("secretId", "")
        masked = secret_id[:4] + "****" + secret_id[-4:] if len(secret_id) > 8 else "****"
        print("    - " + T("凭证类型: {type}", type=cred_data.get("type", T("未知"))))
        print(f"    - SecretId: {masked}")
        # 双装共存保护：该文件可能是中文版的活跃登录态（国际站自身不使用文件凭证）
        if cred_data.get("type") in ("oauth", "connector"):
            print(f"  {yellow('[!]')} " + T(
                "注意：该凭证文件可能正被其他 CloudQ 版本（如中文版）使用，"
                "删除后该版本需重新授权登录。"))
    except (json.JSONDecodeError, OSError):
        pass

    if interactive and not confirm("\n  " + T("确认删除凭证文件?")):
        print(f"  {yellow('[SKIP]')} {T('用户跳过')}")
        return False

    return remove_file(CREDENTIAL_FILE, T("凭证文件"))


def clean_cache_file(interactive: bool) -> bool:
    """清理临时缓存文件"""
    print("\n" + bold(T("3. 临时缓存")))

    if not CACHE_FILE.exists():
        print(f"  {dim('[-]')} {CACHE_FILE}: {dim(T('不存在，跳过'))}")
        return False

    print("  " + T("路径: {path}", path=CACHE_FILE))
    try:
        size = CACHE_FILE.stat().st_size
        print(f"    - .tcloud_advisor_uin_cache ({size} bytes)")
    except OSError:
        pass

    if interactive and not confirm("\n  " + T("确认删除 {path} ?", path=CACHE_FILE)):
        print(f"  {yellow('[SKIP]')} {T('用户跳过')}")
        return False

    return remove_file(CACHE_FILE, str(CACHE_FILE))


def clean_env_vars(interactive: bool) -> bool:
    """清理智能顾问相关环境变量"""
    print("\n" + bold(T("5. 环境变量")))

    # 检测哪些环境变量当前已设置
    found = {}
    for var in ENV_VARS:
        val = os.environ.get(var, "")
        if val:
            found[var] = val

    if not found:
        print(f"  {dim('[-]')} {T('未检测到已设置的 TENCENTCLOUD_* 环境变量，跳过')}")
        return False

    # 显示已设置的变量（敏感值掩码）
    print("  " + T("检测到 {count} 个已设置的环境变量:", count=len(found)))
    for var, val in found.items():
        if "SECRET" in var or "TOKEN" in var or "KEY" in var:
            display = val[:4] + "****" + val[-4:] if len(val) > 8 else "****"
        else:
            display = val
        print(f"    - {var} = {display}")

    if interactive and not confirm("\n  " + T("确认清理以上 {count} 个环境变量?", count=len(found))):
        print(f"  {yellow('[SKIP]')} {T('用户跳过')}")
        return False

    # 生成清理命令
    is_windows = platform.system() == "Windows"
    print()

    if is_windows:
        # Windows: 生成 PowerShell 脚本
        script_file = Path(tempfile.gettempdir()) / "cleanup_tencent_env.ps1"
        lines = [T("# 腾讯云智能顾问 - 环境变量清理脚本 (PowerShell)"),
                 T("# 自动生成，执行后可删除此文件"), ""]
        for var in found:
            lines.append(f'Remove-Item Env:\\{var} -ErrorAction SilentlyContinue')
            lines.append('Write-Host "  [OK] ' + T("已清除 {var}", var=var) + '"')
        lines.append("")
        lines.append('Write-Host ""')
        lines.append('Write-Host "  ' + T("已清理 {count} 个环境变量（仅影响当前会话）", count=len(found)) + '"')

        script_file.write_text("\n".join(lines), encoding="utf-8")
        print("  " + T("已生成 PowerShell 清理脚本: {path}", path=script_file))
        print("  " + T("请在 PowerShell 中执行:"))
        print(f"    . {script_file}")

    else:
        # Linux / macOS: 生成 source 脚本
        script_file = Path(tempfile.gettempdir()) / "cleanup_tencent_env.sh"
        lines = ["#!/bin/sh",
                 T("# 腾讯云智能顾问 - 环境变量清理脚本"),
                 T("# 自动生成，执行后可删除此文件"), ""]
        for var in found:
            lines.append(f'unset {var}')
            lines.append('echo "  [OK] ' + T("已清除 {var}", var=var) + '"')
        lines.append("")
        lines.append('echo ""')
        lines.append('echo "  ' + T("已清理 {count} 个环境变量（仅影响当前会话）", count=len(found)) + '"')

        script_file.write_text("\n".join(lines), encoding="utf-8")
        try:
            os.chmod(str(script_file), 0o755)
        except OSError:
            pass
        print("  " + T("已生成清理脚本: {path}", path=script_file))
        print("  " + T("请在当前终端执行:"))
        print(f"    source {script_file}")

    print()
    print(f"  {yellow(T('注意'))}: {T('环境变量存在于 shell 进程中，Python 脚本无法直接修改父 shell。')}")
    print("         " + T("请执行上方命令完成清理（仅影响当前终端会话）。"))
    print("         " + T("如果变量写在 ~/.bashrc、~/.zshrc 或系统环境中，请手动移除对应行。"))

    return True


def clean_cloud_role(interactive: bool) -> bool:
    """删除云端 CAM 角色（可选）"""
    print("\n" + bold(T("4. 云端 CAM 角色")))

    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")

    if not secret_id or not secret_key:
        print(f"  {dim('[-]')} {T('未配置 AK/SK 环境变量，跳过云端角色清理')}")
        print("      " + T("如需删除云端角色，请设置 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY 后重试"))
        return False

    # 加载 tcloud_api
    try:
        from tcloud_api import call_api
    except ImportError:
        print(f"  {red('[FAIL]')} {T('无法加载 tcloud_api 模块')}")
        return False

    # 检查角色是否存在
    print("  " + T("正在检查角色 {role} ...", role=ROLE_NAME))
    check_result = call_api(
        "cam", "cam.tencentcloudapi.com",
        "GetRole", "2019-01-16",
        {"RoleName": ROLE_NAME},
    )

    if not check_result.get("success"):
        err_code = check_result.get("error", {}).get("code", "")
        if "NotFound" in err_code or "not exist" in check_result.get("error", {}).get("message", "").lower():
            print(f"  {dim('[-]')} {T('角色 {role} 不存在，无需删除', role=ROLE_NAME)}")
            return False
        else:
            err_msg = check_result.get('error', {}).get('message', T('未知错误'))
            print(f"  {red('[FAIL]')} {T('查询角色失败: {message}', message=err_msg)}")
            return False

    role_data = check_result.get("data", {})
    role_id = role_data.get("RoleId", "unknown")
    description = role_data.get("Description", T("无描述"))
    print("  " + T("检测到角色:"))
    print("    " + T("名称: {role}", role=ROLE_NAME))
    print(f"    ID:   {role_id}")
    print("    " + T("描述: {description}", description=description))

    if interactive and not confirm("\n  " + T("确认删除云端角色 {role} ? (此操作不可恢复)", role=ROLE_NAME)):
        print(f"  {yellow('[SKIP]')} {T('用户跳过')}")
        return False

    # 执行删除
    print("  " + T("正在删除角色 {role} ...", role=ROLE_NAME))
    delete_result = call_api(
        "cam", "cam.tencentcloudapi.com",
        "DeleteRole", "2019-01-16",
        {"RoleName": ROLE_NAME},
    )

    if delete_result.get("success"):
        print(f"  {green('[OK]')} {T('云端角色 {role} 已删除', role=ROLE_NAME)}")
        return True
    else:
        err_msg = delete_result.get("error", {}).get("message", T("未知错误"))
        print(f"  {red('[FAIL]')} {T('删除角色失败: {message}', message=err_msg)}")
        return False


# ============== 主流程 ==============
def main():
    args = set(sys.argv[1:])

    # 帮助信息
    if args & {"-h", "--help"}:
        print(__doc__)
        sys.exit(0)

    auto_mode = "--all" in args
    include_cloud = "--cloud" in args

    # 标题
    print(f"\n{'=' * 58}")
    print("  " + T("腾讯云智能顾问 - 配置清理"))
    print(f"{'=' * 58}")

    # 显示当前配置摘要
    config = read_config()
    if config:
        print("\n" + T("当前配置:"))
        print("  " + T("账号 UIN:  {uin}", uin=config.get('accountUin', T('未知'))))
        print("  " + T("角色名称:  {role}", role=config.get('roleName', T('未知'))))
        print("  " + T("角色 ARN:  {arn}", arn=config.get('roleArn', T('未知'))))
        print("  " + T("配置时间:  {time}", time=config.get('configuredAt', T('未知'))))

    interactive = not auto_mode

    if interactive:
        print("\n" + dim(T("提示: 使用 --all 跳过确认，--cloud 同时删除云端角色")))

    # 执行清理（注意：云端角色删除必须在环境变量清理之前，因为需要 AK/SK）
    results = []
    results.append((T("配置目录"), clean_config_dir(interactive)))
    results.append((T("凭证文件"), clean_oauth_credential(interactive)))
    results.append((T("临时缓存"), clean_cache_file(interactive)))

    if include_cloud:
        results.append((T("云端角色"), clean_cloud_role(interactive)))
    else:
        print("\n" + bold(T("4. 云端 CAM 角色")))
        print(f"  {dim('[-]')} {T('未指定 --cloud 参数，跳过云端角色清理')}")
        print("      " + T("如需同时删除云端角色，请添加 --cloud 参数"))

    # 环境变量清理放在最后（云端角色删除可能需要用到 AK/SK）
    results.append((T("环境变量"), clean_env_vars(interactive)))

    # 汇总
    cleaned = sum(1 for _, ok in results if ok)
    total = len(results)

    print(f"\n{'=' * 58}")
    print("  " + T("清理完成: {cleaned}/{total} 项已清理", cleaned=cleaned, total=total))
    print(f"{'=' * 58}\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
