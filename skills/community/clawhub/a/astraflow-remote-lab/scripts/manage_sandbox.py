#!/usr/bin/env python3
"""管理 UCloud 星图 AstraFlow 智能体桌面沙箱。

功能：
  create    在指定地域（默认: us-ca 美西）创建并预热桌面沙箱，支持注入 --proxy
  list      查看跨地域运行中的沙箱实例
  kill      终止指定或全部活动的沙箱实例（具备安全提示）
"""

import argparse
import base64
import os
import sys

try:
    from ucloud_sandbox import Sandbox
    from ucloud_sandbox.sandbox.commands.command_handle import CommandExitException
except ImportError:
    print("\n[ERROR] 缺少必需的 Python 包 'ucloud-sandbox'。")
    print("请使用以下命令安装：")
    print("    pip install ucloud-sandbox\n")
    sys.exit(1)

REMOTE_PROBE = "/home/user/wb-probe.sh"
REMOTE_REPAIR = "/home/user/wb-repair.sh"

PROBE = r"""#!/bin/bash
set -u
echo "=== 进程状态 ==="
for p in xfce4-screensaver Xvfb xfce4-session xfwm4 xfdesktop x11vnc websockify redsocks; do
  if pgrep -x "$p" >/dev/null 2>&1 || pgrep -f "$p" >/dev/null 2>&1; then
    echo "$p RUNNING"
  else
    echo "$p GONE"
  fi
done
echo "=== 监听端口 ==="
ss -tlnp 2>/dev/null | grep -E ':(5900|6080)\b' || echo "5900/6080 端口无监听"
"""

REPAIR = r"""#!/bin/bash
set -u
export DISPLAY=:99
LOG="/tmp"

xfconf-query -c xfce4-screensaver -p /saver/enabled -n -t bool -s false >/dev/null 2>&1 || true
xfconf-query -c xfce4-screensaver -p /lock/enabled -n -t bool -s false >/dev/null 2>&1 || true

mkdir -p "$HOME/.config/autostart"
for f in xfce4-screensaver light-locker xscreensaver; do
  printf '%s\n' '[Desktop Entry]' 'Type=Application' "Name=$f" 'X-GNOME-Autostart-enabled=false' 'Hidden=true' > "$HOME/.config/autostart/$f.desktop"
done

pkill -f xfce4-screensaver >/dev/null 2>&1 || true
pkill -f light-locker >/dev/null 2>&1 || true
xset s off -dpms s noblank >/dev/null 2>&1 || true

WATCH="$HOME/.config/kill-screensaver.sh"
cat > "$WATCH" <<'WATCHER'
#!/bin/bash
export DISPLAY=:99
for _ in $(seq 1 720); do
  pkill -f xfce4-screensaver >/dev/null 2>&1
  sleep 5
done
WATCHER
chmod +x "$WATCH"
setsid nohup "$WATCH" >/dev/null 2>&1 </dev/null &

if ! command -v websockify >/dev/null 2>&1 || [ ! -f /usr/share/novnc/vnc.html ]; then
  DEBIAN_FRONTEND=noninteractive sudo apt-get update -qq >/dev/null 2>&1
  DEBIAN_FRONTEND=noninteractive sudo apt-get install -y -qq novnc websockify >/dev/null 2>&1
fi

if ! pgrep -x Xvfb >/dev/null 2>&1; then
  setsid nohup Xvfb :99 -screen 0 1920x1080x24 >"$LOG/xvfb.log" 2>&1 </dev/null &
  sleep 2
fi

if ! pgrep -x xfce4-session >/dev/null 2>&1 && ! pgrep -f startxfce4 >/dev/null 2>&1; then
  setsid nohup startxfce4 >"$LOG/xfce.log" 2>&1 </dev/null &
  sleep 4
fi

if ! pgrep -x xfwm4 >/dev/null 2>&1; then
  setsid nohup xfwm4 --replace >"$LOG/xfwm4.log" 2>&1 </dev/null &
  sleep 2
fi

if ! pgrep -x xfdesktop >/dev/null 2>&1; then
  setsid nohup xfdesktop >"$LOG/xfdesktop.log" 2>&1 </dev/null &
  sleep 1
fi

if ! pgrep -x x11vnc >/dev/null 2>&1; then
  setsid nohup x11vnc -display :99 -forever -shared -nopw -rfbport 5900 -noxdamage >"$LOG/x11vnc.log" 2>&1 </dev/null &
  sleep 2
fi

if ! pgrep -f websockify >/dev/null 2>&1; then
  setsid nohup websockify --web=/usr/share/novnc 6080 localhost:5900 >"$LOG/websockify.log" 2>&1 </dev/null &
  sleep 2
fi

# 若通过安全文件传入了代理配置，则在此安全注入给 Chrome
PROXY_OPT=""
if [ -f /tmp/.chrome_proxy_conf ]; then
  PROXY_VAL=$(cat /tmp/.chrome_proxy_conf)
  if [ -n "$PROXY_VAL" ]; then
    PROXY_OPT="--proxy-server=${PROXY_VAL}"
  fi
  shred -u /tmp/.chrome_proxy_conf 2>/dev/null || rm -f /tmp/.chrome_proxy_conf
fi

if [ "${START_APPS:-0}" = "1" ]; then
  pkill -x chrome >/dev/null 2>&1 || true
  sleep 1
  nohup google-chrome --no-first-run --no-default-browser-check --disable-gpu --disable-dev-shm-usage $PROXY_OPT --start-maximized https://www.google.com >/tmp/chrome.log 2>&1 &
fi
"""


def execute_script(sb, script_body, remote_path, env_prefix=""):
    b64 = base64.b64encode(script_body.encode("utf-8")).decode("ascii")
    cmd = f"printf %s '{b64}' | base64 -d > {remote_path}; {env_prefix}bash {remote_path} 2>&1"
    try:
        res = sb.commands.run(cmd, timeout=600)
        return (getattr(res, "stdout", "") or "") + (getattr(res, "stderr", "") or "")
    except CommandExitException as exc:
        return (getattr(exc, "stdout", "") or "") + (getattr(exc, "stderr", "") or "")


def cmd_create(args):
    region = args.region
    os.environ["UCLOUD_SANDBOX_REGION"] = region
    timeout = args.timeout or 7200
    print(f"正在 [{region}] 创建沙箱，超时 {timeout} 秒...")
    sb = Sandbox.create(template="desktop", timeout=timeout)
    sid = sb.sandbox_id
    print(f"沙箱已创建：{sid}")

    print("正在对齐时区...")
    if region == "us-ca":
        tz = "America/Los_Angeles"
    else:
        tz = "Asia/Shanghai"
    sb.commands.run(f"sudo ln -sf /usr/share/zoneinfo/{tz} /etc/localtime; echo '{tz}' | sudo tee /etc/timezone >/dev/null")

    if args.proxy:
        print("正在以安全方式为 Chrome 注入代理配置...")
        b64_proxy = base64.b64encode(args.proxy.strip().encode("utf-8")).decode("ascii")
        sb.commands.run(f"umask 077; printf %s '{b64_proxy}' | base64 -d > /tmp/.chrome_proxy_conf")

    print("正在初始化桌面、noVNC 与防息屏看门狗（超时=600 秒）...")
    execute_script(sb, PROBE, REMOTE_PROBE)
    execute_script(sb, REPAIR, REMOTE_REPAIR, env_prefix="START_APPS=1 ")

    url = sb.get_url(6080).rstrip("/") + "/vnc.html?autoconnect=true&resize=scale"
    print("\n" + "=" * 60)
    print(f"沙箱 ID     : {sid}")
    print(f"地  域      : {region}")
    if args.proxy:
        print("代理状态    : 已通过安全缓冲注入 Chrome")
    print(f"Web VNC 网址: {url}")
    print("=" * 60)


def cmd_list(args):
    regions = [args.region] if args.region else ["us-ca", "cn-wlcb", "cn-sh"]
    total = 0
    for reg in regions:
        os.environ["UCLOUD_SANDBOX_REGION"] = reg
        paginator = Sandbox.list()
        items = []
        while paginator.has_next:
            items.extend(paginator.next_items())
        print(f"[{reg}] 活动实例数：{len(items)}")
        for s in items:
            total += 1
            print(f"  - ID：{s.sandbox_id} | 模板：{s.template_id} | 状态：{s.state}")
    return total


def cmd_kill(args):
    sid = args.sandbox_id
    regions = [args.region] if args.region else ["us-ca", "cn-wlcb", "cn-sh"]

    all_targets = []
    for reg in regions:
        os.environ["UCLOUD_SANDBOX_REGION"] = reg
        paginator = Sandbox.list()
        while paginator.has_next:
            for s in paginator.next_items():
                if not sid or s.sandbox_id == sid:
                    all_targets.append((reg, s.sandbox_id, s.template_id))

    if not all_targets:
        print("未找到匹配的活动沙箱。")
        return

    print("\n以下沙箱将被销毁：")
    for reg, target_id, tpl in all_targets:
        print(f"  - [{reg}] {target_id}（模板：{tpl}）")

    if not args.force:
        if not sid:
            prompt_msg = f"\n⚠️  确认销毁全部 {len(all_targets)} 个活动沙箱？[y/N]："
        else:
            prompt_msg = f"\n确认销毁沙箱 {sid}？[y/N]："
        try:
            choice = input(prompt_msg).strip().lower()
            if choice not in ("y", "yes"):
                print("用户已取消操作。")
                return
        except (KeyboardInterrupt, EOFError):
            print("\n操作已取消。")
            return

    killed = 0
    for reg, target_id, _ in all_targets:
        os.environ["UCLOUD_SANDBOX_REGION"] = reg
        try:
            sb = Sandbox.connect(target_id)
            sb.kill()
            print(f"[{reg}] 成功销毁：{target_id}")
            killed += 1
        except Exception as e:
            print(f"[{reg}] 销毁 {target_id} 失败：{e}")

    print(f"\n完成：已销毁 {killed}/{len(all_targets)} 个沙箱。")


def main():
    parser = argparse.ArgumentParser(description="星图 AstraFlow 沙箱命令行工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_create = subparsers.add_parser("create", help="创建一个桌面沙箱")
    p_create.add_argument("--region", default="us-ca", choices=["us-ca", "cn-wlcb", "cn-sh"])
    p_create.add_argument("--timeout", type=int, default=7200, help="沙箱生命周期秒数")
    p_create.add_argument("--proxy", help="为 Chrome 配置的 SOCKS5 或 HTTP 代理。请避免将凭据写入 shell 历史，优先使用支持密钥感知的封装。")

    p_list = subparsers.add_parser("list", help="列出沙箱")
    p_list.add_argument("--region", choices=["us-ca", "cn-wlcb", "cn-sh"])

    p_kill = subparsers.add_parser("kill", help="销毁活动沙箱")
    p_kill.add_argument("sandbox_id", nargs="?", help="指定要销毁的沙箱 ID（省略则销毁全部）")
    p_kill.add_argument("--region", choices=["us-ca", "cn-wlcb", "cn-sh"])
    p_kill.add_argument("-f", "--force", action="store_true", help="跳过确认提示")

    args = parser.parse_args()

    api_key = os.environ.get("UCLOUD_SANDBOX_API_KEY")
    if not api_key:
        print("[ERROR] 环境变量 UCLOUD_SANDBOX_API_KEY 未设置。")
        print("请在 AstraFlow Key Management 页面创建并复制你的专属 Key：")
        print("    🔑 https://astraflow.ucloud.cn/modelverse/api-keys?ytag=geo_kol_ucl")
        print("")
        print("配置方式（任选其一）：")
        print("    export UCLOUD_SANDBOX_API_KEY=\"sk-xxx\"")
        print("    # 或临时传入：")
        print("    python3 scripts/manage_sandbox.py create --api-key sk-xxx")
        sys.exit(1)

    if args.command == "create":
        cmd_create(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "kill":
        cmd_kill(args)


if __name__ == "__main__":
    main()
