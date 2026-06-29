#!/usr/bin/env python3
"""
keepalive.py — douyin skill 的 cookie / state 管理

与 zhihu 不同,本 skill 不需要 ab daemon 长驻;
只在 video 命令需要抓评论时才用 ab 拿 video 页面 DOM。

子命令:
  setup    从浏览器导 cookie 到 /tmp/douyin/cookies.txt
  check    验证 cookie 是否还有效
  inject   把 /tmp/douyin/cookies-raw.txt(你贴的 k=v; k=v; 格式)转成 Netscape
  state    ab state save / load (管理 video 命令的 ab session)
"""
import argparse
import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from paths import COOKIE_RAW, COOKIE_FILE, STATE_FILE, DATA_DIR, report as report_paths

# 验证 ab 登录态用的稳定视频页(比主页反爬轻;作者删了就改这里)
PROBE_VIDEO = "https://www.douyin.com/video/7649948072239271211"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
COMMON = "device_platform=webapp&aid=6383&channel=channel_pc_web&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Linux+x86_64&browser_name=Chrome&browser_version=120.0.0.0&browser_online=true&engine_name=Blink&engine_version=120.0.0.0&os_name=Linux&os_version=x86_64&device_memory=16&platform=PC&downlink=10&effective_type=4g&round_trip_time=50"


def err(msg):
    print(f"❌ {msg}", file=sys.stderr)


def ok(msg):
    print(f"✅ {msg}")


def cmd_setup(args):
    """从 Chrome 导 cookie:用户用 ab cookies set 一次性灌入,然后我 export"""
    print("=" * 60)
    print("Setup 流程 (一次性):")
    print("=" * 60)
    print("""
1. 在 Chrome 打开 https://www.douyin.com/ 并登录
2. F12 → Application → Cookies → 选 www.douyin.com
3. 把所有 cookie 粘到 /tmp/douyin/cookies-raw.txt (k=v; k=v; 格式)
4. 跑: keepalive.py inject  ← 把 raw 转成 Netscape 标准格式
5. 跑: keepalive.py check   ← 验证 cookie 还有效

如果需要用 video 命令看评论,额外:
6. 跑: keepalive.py state save  ← 把 ab session 持久化
""")


def cmd_inject(args):
    raw_path = Path(COOKIE_RAW)
    if not raw_path.exists():
        err(f"找不到 {COOKIE_RAW}")
        print(f"  → 先把浏览器导出的 cookie 粘到该文件(k=v; k=v; 格式)", file=sys.stderr)
        sys.exit(1)
    raw = raw_path.read_text().strip()
    out_lines = [
        "# Netscape HTTP Cookie File",
        "# https://curl.haxx.se/rfc/cookie_spec.html",
        "# This is a generated file! Do not edit.",
        "",
    ]
    count = 0
    for part in raw.split(";"):
        part = part.strip()
        if not part or "=" not in part or part.startswith("douyin.com"):
            continue
        name, _, value = part.partition("=")
        name = name.strip()
        value = value.strip()
        if not name or not value:
            continue
        # domain TAB flag TAB path TAB secure TAB expiry TAB name TAB value
        out_lines.append(f".douyin.com\tTRUE\t/\tFALSE\t0\t{name}\t{value}")
        count += 1
    Path(COOKIE_FILE).write_text("\n".join(out_lines) + "\n")
    os.chmod(COOKIE_FILE, 0o600)
    ok(f"已写入 {COOKIE_FILE} ({count} 个 cookie)")


def cmd_check(args):
    """调一次轻量 API 验证 cookie 是否还活着"""
    p = Path(COOKIE_FILE)
    if not p.exists():
        err(f"找不到 {COOKIE_FILE},先跑 inject")
        sys.exit(1)
    raw = p.read_text()
    cookie_parts = []
    for line in raw.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        cols = line.split("\t")
        if len(cols) >= 7:
            cookie_parts.append(f"{cols[5]}={cols[6]}")
    if not cookie_parts:
        err("cookie 文件解析失败")
        sys.exit(1)
    cookie = "; ".join(cookie_parts)
    import urllib.request
    from urllib.parse import quote
    url = f"https://www.douyin.com/aweme/v1/web/general/search/single/?{COMMON}&search_type=user&keyword={quote('小Lin说')}&count=1"
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Referer": "https://www.douyin.com/",
        "Cookie": cookie,
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = r.read().decode("utf-8")
    except Exception as e:
        err(f"网络错误: {e}")
        sys.exit(1)
    if not data:
        err("返回空 (cookie 过期或 verify_check 拦截)")
        sys.exit(1)
    import json
    try:
        d = json.loads(data)
    except json.JSONDecodeError:
        err(f"返回非 JSON: {data[:200]}")
        sys.exit(1)
    users = (d.get("data") or [{}])[0].get("user_list") or []
    if users:
        ui = users[0].get("user_info", users[0])
        ok(f"cookie 有效 — 命中: @{ui.get('nickname')} ({ui.get('follower_count', 0) // 10000}万粉)")
    else:
        err(f"API 没返回用户 — cookie 可能过期")
        sys.exit(1)


def cmd_state(args):
    """ab state save / load / check — 给 video 命令的 ab session 持久化"""
    sub = args.state_cmd
    state_path = Path(STATE_FILE)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    if sub == "save":
        # ⚠ 关键:必须先杀 daemon,否则新开的 ab 不会带 cookie (daemon 抢占)
        # ⚠ 不再调 pkill 兜底 — 在某些 shell hook 下 pkill 完全卡死(Python 看不到子进程),
        # 仅依赖 agent-browser close。daemon 残留时手动跑: agent-browser close && sleep 2
        print("→ 清理 daemon (防抢占)...")
        subprocess.run(["agent-browser", "close"], capture_output=True, timeout=10)
        import time
        time.sleep(2)
        # 1) fresh ab + 注入 cookie
        print("→ 启动 fresh ab session 注入 cookie...")
        subprocess.run(["agent-browser", "open", "https://www.douyin.com/"], capture_output=True, timeout=30)
        time.sleep(3)
        # 读 cookie 灌入
        raw = Path(COOKIE_FILE).read_text()
        cookie_parts = []
        for line in raw.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            cols = line.split("\t")
            if len(cols) >= 7:
                cookie_parts.append((cols[5], cols[6]))
        if not cookie_parts:
            err("cookie 解析失败")
            sys.exit(1)
        for name, value in cookie_parts:
            subprocess.run(["agent-browser", "cookies", "set", name, value,
                          "--domain", ".douyin.com", "--path", "/"],
                         capture_output=True)
        # 2) save state
        r = subprocess.run(["agent-browser", "state", "save", str(state_path)],
                          capture_output=True, text=True)
        if r.returncode != 0:
            err(f"state save 失败: {r.stderr}")
            sys.exit(1)
        ok(f"state 已保存到 {state_path}")
        # 3) 验证 — 用一个已知的视频页 URL(比主页反爬轻)
        if _verify_state_login(state_path, probe_url=PROBE_VIDEO):
            print("→ 之后 video 命令会用 --state 启动,登录态保持")
        else:
            err("state 保存了但 cookie 注入失败(可能是 daemon 抢占未完全清理或 cookie 过期)")
            print("  → 手动跑: agent-browser close && pkill -9 -f agent-browser && sleep 2 && state save")
            sys.exit(1)
    elif sub == "load":
        if not state_path.exists():
            err(f"state 文件不存在: {state_path},先跑 save")
            sys.exit(1)
        # ⚠ 先杀 daemon,否则 --state 被忽略(这才是 load 失败的最高频原因)
        # 不再调 pkill 兜底 — 在某些 shell hook 下完全卡死
        subprocess.run(["agent-browser", "close"], capture_output=True, timeout=10)
        import time
        time.sleep(2)
        # 用视频页 URL 验证(主页反爬太严,容易误报)
        r = subprocess.run(["agent-browser", "--state", str(state_path), "open", PROBE_VIDEO],
                          capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            err(f"state load 失败: {r.stderr}")
            sys.exit(1)
        time.sleep(5)
        # 验证登录态真的注入了 (不只是 file 存在)
        if _verify_state_login(state_path, skip_open=True):
            ok(f"state 已加载到 ab,可直接用 video 命令")
        else:
            err(f"state load 成功但 cookie 未注入 — state 可能已过期,跑 state save 重新生成")
            sys.exit(1)
    elif sub == "check":
        if not state_path.exists():
            err(f"state 文件不存在: {state_path}")
            sys.exit(1)
        ok(f"state 文件存在: {state_path} ({state_path.stat().st_size} bytes)")
        # 额外: 实际启动验证(用视频页,主页反爬严)
        if _verify_state_login(state_path, probe_url=PROBE_VIDEO):
            print("→ state 实际可用 (已验证登录态)")
        else:
            err("state 文件存在但实际不可用 (cookie 已过期或 daemon 抢占)")
            print("  → 跑 state save 重新生成")
            sys.exit(1)


def _verify_state_login(state_path: Path, skip_open: bool = False,
                        probe_url: str = PROBE_VIDEO) -> bool:
    """实际启动 ab 带 state,检查页面是否登录态
    skip_open=True → 跳过 ab open 步骤(调用方已经 open 过了)
    probe_url      → 打开的 URL,默认用稳定视频页(反爬轻)
    返回 True = 登录成功,False = 失败
    """
    import time
    if not skip_open:
        # 检查并清理 daemon(不再调 pkill 兜底,某些 shell hook 下完全卡死)
        subprocess.run(["agent-browser", "close"], capture_output=True, timeout=10)
        time.sleep(2)
        r = subprocess.run(
            ["agent-browser", "--state", str(state_path), "open", probe_url],
            capture_output=True, text=True, timeout=30,
        )
        if r.returncode != 0:
            err(f"ab open 失败: {r.stderr[:200]}")
            return False
        time.sleep(5)
    # eval 检查登录态
    # 已登录 → title 含昵称 / 有 user-info 元素
    # 未登录 → title 是 "抖音-记录美好生活" 或 "验证码中间页"
    check_js = """(() => {
        const title = document.title;
        // ⚠ 不要只看 #nocaptcha-container — 那个 iframe 在 douyin 页面里总是存在但是空的
        // 只看实际渲染的 captcha 元素(可见 + 尺寸 > 0)
        const captchaIframes = Array.from(document.querySelectorAll('iframe[id*="captcha"]'))
            .filter(f => f.offsetWidth > 100 && f.offsetHeight > 100);
        // 此外: 看是不是有 verify 验证码大背景遮罩
        const verifyModal = !!document.querySelector('[class*="verify-bar"], [class*="captcha-verify"]');
        const captcha = captchaIframes.length > 0 || verifyModal;
        const loginPanel = !!document.querySelector('#login-full-panel, #douyin_login_comp_flat_panel');
        const userInfo = !!document.querySelector('[class*="user-info"], [class*="UserInfo"], [data-e2e="user-info"]');
        const avatar = !!document.querySelector('[class*="avatar"]:not([class*="placeholder"])');
        return JSON.stringify({title, captcha, loginPanel, userInfo, avatar});
    })()"""
    r = subprocess.run(
        f"agent-browser eval \"$(cat <<'EOF'\n{check_js}\nEOF\n)\"",
        capture_output=True, text=True, timeout=10, shell=True,
    )
    if r.returncode != 0 or not r.stdout.strip():
        err(f"ab eval 失败: {r.stderr[:200]}")
        return False
    out = r.stdout.strip()
    # 剥 ab eval 的 shell 引用
    if out.startswith('"'):
        try:
            out = ast.literal_eval(out)
        except (ValueError, SyntaxError):
            pass
    try:
        info = json.loads(out)
    except Exception:
        err(f"无法解析登录状态: {out[:200]}")
        return False
    if info.get("captcha") or "验证码" in info.get("title", ""):
        err(f"页面是验证码中间页: {info.get('title')}")
        return False
    if info.get("loginPanel"):
        err("页面弹出登录 panel — cookie 未注入")
        return False
    # userInfo 或 avatar 至少一个出现算登录
    if info.get("userInfo") or info.get("avatar"):
        ok(f"登录态验证通过 (title: {info.get('title', '?')[:50]})")
        return True
    # 如果都没出现,可能是页面还没渲染完,但也没 captcha / login panel
    # 这种情况下,我们看 title 是否含 抖音
    if "抖音" in info.get("title", ""):
        # title 是 抖音-记录美好生活 这种未登录首页 title
        if "记录美好" in info.get("title", "") or info.get("title", "").strip() in ("抖音", "抖音-记录美好生活"):
            err(f"页面是未登录首页 (title: {info.get('title')}) — cookie 没注入")
            return False
        # 否则可能是视频页但没抓到 userInfo / avatar,放行
        ok(f"未明确识别登录元素,放行 (title: {info.get('title', '?')[:50]})")
        return True
    err(f"页面状态不明: {info}")
    return False


def main():
    ap = argparse.ArgumentParser(description="douyin skill cookie/state 管理")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("setup", help="打印 setup 流程说明")
    p = sub.add_parser("inject", help="把 raw 格式转 Netscape")
    sub.add_parser("check", help="验证 cookie 是否有效 (调一次搜索 API)")
    p = sub.add_parser("state", help="ab state 管理 (给 video 命令用)")
    p.add_argument("state_cmd", choices=["save", "load", "check"])

    args = ap.parse_args()
    if args.cmd == "setup":
        cmd_setup(args)
    elif args.cmd == "inject":
        cmd_inject(args)
    elif args.cmd == "check":
        cmd_check(args)
    elif args.cmd == "state":
        cmd_state(args)


if __name__ == "__main__":
    main()
