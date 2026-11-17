#!/usr/bin/env python3
"""对 astraflow-remote-lab 环境运行综合自检。"""
import os
import shutil
import sys


def check_sdk():
    try:
        import ucloud_sandbox
        print(f"[OK] Python SDK 'ucloud-sandbox' 已安装（版本 {getattr(ucloud_sandbox, '__version__', '未知')}）。")
        return True
    except ImportError:
        print("[FAIL] 缺少 Python SDK 'ucloud-sandbox'，请执行：pip install ucloud-sandbox")
        return False


def check_env():
    key = os.environ.get("UCLOUD_SANDBOX_API_KEY")
    reg = os.environ.get("UCLOUD_SANDBOX_REGION", "us-ca（默认）")
    ok = True
    if not key:
        print("[WARN] UCLOUD_SANDBOX_API_KEY 未设置。")
        print("       请在 AstraFlow Key Management 页面获取后执行：")
        print("       export UCLOUD_SANDBOX_API_KEY=\"你的_key\"")
        ok = False
    else:
        print(f"[OK] UCLOUD_SANDBOX_API_KEY 已设置（长度 {len(key)}）。目标地域：{reg}")
    return ok


def check_ucloud_cli():
    cli_path = shutil.which("ucloud")
    if not cli_path:
        print("[WARN] PATH 中未找到 'ucloud' CLI（仅在管理 Windows UHost 实例时需要）。")
        return False

    print(f"[OK] 已找到 'ucloud' CLI：{cli_path}")

    # 检查凭据
    cred_file = os.path.expanduser("~/.ucloud/credential.json")
    if os.path.isfile(cred_file):
        print(f"[OK] 已找到 UCloud CLI 凭据：{cred_file}")
    else:
        print(f"[WARN] UCloud CLI 凭据缺失（{cred_file}），请执行：ucloud config init")
    return True


def main():
    print("=== 星图 AstraFlow 远程实验室环境检查 ===\n")
    s1 = check_sdk()
    s2 = check_env()
    s3 = check_ucloud_cli()
    print("\n===============================================")
    if s1 and s2:
        print("🎉 核心环境已就绪，可以开始使用 AstraFlow 沙箱！")
    else:
        print("⚠️  部分前置条件缺失，请检查上述项目。")


if __name__ == "__main__":
    main()
