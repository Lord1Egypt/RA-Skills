#!/usr/bin/env python3
"""将 Windows UHost 的 RDP 桌面全屏桥接进现有的 AstraFlow 桌面沙箱中。

在 Linux 沙箱内部配置并拉起 xfreerdp 会话，连通目标 Windows 云主机，
并将全屏桌面通过沙箱已有的 Web noVNC 端点输出，实现浏览器免客户端访问。
"""

import argparse
import base64
import getpass
import os
import sys

try:
    from ucloud_sandbox import Sandbox
except ImportError:
    print("\n[ERROR] 缺少必需的 Python 包 'ucloud-sandbox'。")
    print("请使用以下命令安装：")
    print("    pip install ucloud-sandbox\n")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="把 Windows UHost 桥接进沙箱桌面")
    parser.add_argument("--sandbox-id", required=True, help="目标桌面沙箱 ID")
    parser.add_argument("--region", default="us-ca", help="沙箱地域（默认：us-ca）")
    parser.add_argument("--host-ip", required=True, help="目标 Windows UHost 的公网/私网 IP")
    parser.add_argument("--user", default="Administrator", help="Windows RDP 用户名")
    parser.add_argument(
        "--password-stdin",
        action="store_true",
        help="从标准输入读取 Windows 密码（推荐用于自动化流水线）",
    )
    args = parser.parse_args()

    if args.password_stdin:
        password = sys.stdin.readline().rstrip("\n")
    else:
        password = getpass.getpass("Windows RDP 密码：")
    if not password:
        print("[ERROR] 必须通过受保护的交互输入或 --password-stdin 提供 RDP 密码。")
        sys.exit(1)

    api_key = os.environ.get("UCLOUD_SANDBOX_API_KEY")
    if not api_key:
        print("[ERROR] 环境变量 UCLOUD_SANDBOX_API_KEY 未设置。")
        print("请在 AstraFlow Key Management 页面创建并复制你的专属 Key：")
        print("    🔑 https://astraflow.ucloud.cn/modelverse/api-keys?ytag=geo_kol_ucl")
        print("")
        print("配置方式（任选其一）：")
        print("    export UCLOUD_SANDBOX_API_KEY=\"sk-xxx\"")
        print("    # 或临时传入：")
        print("    python3 scripts/bridge_windows_uhost.py --api-key sk-xxx ...")
        sys.exit(1)

    os.environ["UCLOUD_SANDBOX_REGION"] = args.region
    print(f"正在连接 [{args.region}] 的沙箱 {args.sandbox_id}...")
    sb = Sandbox.connect(args.sandbox_id)

    print("正在沙箱内检查 / 安装 freerdp2-x11...")
    sb.commands.run(
        "which xfreerdp >/dev/null 2>&1 || (DEBIAN_FRONTEND=noninteractive sudo apt-get update -qq && DEBIAN_FRONTEND=noninteractive sudo apt-get install -y -qq freerdp2-x11)",
        timeout=180,
    )

    print(f"正在将 Windows RDP（{args.host_ip}:3389）安全桥接至沙箱 X display :99...")

    # 1. 严格使用 umask 077 将凭据写入只有 root 和当前进程可读的临时文件，防止 ps / /proc 泄露
    b64_pwd = base64.b64encode(password.encode("utf-8")).decode("ascii")
    sb.commands.run(f"umask 077; printf %s '{b64_pwd}' | base64 -d > /tmp/.rdp_pass")

    # 2. 通过 cat /tmp/.rdp_pass 从标准输入传入 xfreerdp /from-stdin，并在进程拉起后立即 shred 删除
    script = f"""#!/bin/bash
export DISPLAY=:99
pkill -x chrome || true
pkill -f xfreerdp || true
sleep 1

# 通过 /from-stdin:force 启动 xfreerdp，进程参数表绝不暴露明文密码
cat /tmp/.rdp_pass | nohup xfreerdp /v:{args.host_ip} /u:{args.user} /from-stdin:force /cert:ignore /size:1920x1020 /bpp:24 +clipboard /dynamic-resolution >/tmp/rdp.log 2>&1 &
sleep 2

# 立即彻底销毁密码临时文件
shred -u /tmp/.rdp_pass 2>/dev/null || rm -f /tmp/.rdp_pass
sleep 2

ps aux | grep [f]reerdp || true
"""
    b64 = base64.b64encode(script.encode("utf-8")).decode("ascii")
    sb.commands.run(f"printf %s '{b64}' | base64 -d > /home/user/bridge_rdp.sh; bash /home/user/bridge_rdp.sh")

    url = sb.get_url(6080).rstrip("/") + "/vnc.html?autoconnect=true&resize=scale"
    print("\n" + "=" * 60)
    print("✅ Windows RDP 已成功桥接进沙箱！")
    print("通过浏览器访问 Windows 桌面：")
    print(url)
    print("=" * 60)


if __name__ == "__main__":
    main()
