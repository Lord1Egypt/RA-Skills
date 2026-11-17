#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
guided_register.py — 小递查查「无障碍注册引导向导」（人在环）

目标：让零基础客户也能走完「注册 → 拿 API Key → 落盘凭据」这一步，
为后续「批量查询」提供可用的凭据。

为什么需要人在环（无法全自动）：
  · 注册页含【阿里云滑块验证码】，必须真人拖动完成；
  · 注册需【短信验证码】，需客户真实手机号收码并录入。
这两步由客户在弹出的浏览器窗口里手动完成，脚本负责其余一切（填表、等 token、
调接口、落盘、校验），并在页面与控制台给出分步中文引导。

流程：
  1) 打开 register.html（或 login.html）；
  2) 在页面顶部注入「分步引导横幅」，同时自动填好手机号/密码；
  3) 客户手动：点「获取验证码」→ 收短信填码 → 完成滑块 → 点「注册/登录」；
  4) 脚本轮询 localStorage.userToken，出现即提取；
  5) 用 token 调 GetUserApiKey，映射并写入凭据文件；
  6) 用该凭据试跑一单，校验可用；失败则给出会话内的兜底排查提示。

用法：
  python guided_register.py --phone 138xxxx --password '****'
  python guided_register.py --mode login --phone 138xxxx --password '****'
  python guided_register.py --creds "C:/path/xdcc-credentials.env"
"""

import argparse
import json
import os
import shutil
import sys
import time

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    # 注意：这里只能记录「不可用」，不能在导入期 sys.exit()。
    # 本模块会被 onboard.py 懒加载，导入期退出会让上层 except ImportError 兜底失效，
    # 进程直接裸退、用户看不到友好提示。统一改为运行期返回错误码。
    sync_playwright = None
    PLAYWRIGHT_ERROR = "缺少依赖 Playwright"
else:
    PLAYWRIGHT_ERROR = ""

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (  # noqa: E402
    map_apikey_to_creds, write_creds, cs_hint, validate_track_creds,
)
from get_user_apikey import call_get_user_apikey, API_BASE, ENDPOINT  # noqa: E402

# Chrome 探测候选：环境变量 → PATH → 各系统通用安装路径。
# 不做任何硬编码的「某台开发机」路径，避免换机器即失效、也避免泄露用户名。
_CHROME_CANDIDATES = [
    os.environ.get("CHROME_PATH", ""),
    os.environ.get("CHROME_BIN", ""),
    shutil.which("chrome"),
    shutil.which("google-chrome"),
    shutil.which("chromium"),
    shutil.which("chromium-browser"),
    shutil.which("msedge"),
    shutil.which("microsoft-edge"),
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
]

PAGES = {
    "register": "https://xdccy.com/register.html",
    "login": "https://xdccy.com/login.html",
}

# 页面内引导条（fixed 顶部，pointer-events:none 不挡点击）
#
# 合规约束：本条位于第三方页面之上，必须做成**中性、无品牌、无推广**的
# 操作提示条——不使用品牌色置顶条幅、不放大字号、不压任何标识、不引导跳转。
# 它只回答「这一步做什么」，不回答「去哪里找人」。
_BANNER_CSS = """
#xdcc_guide {
  position: fixed; top: 0; left: 0; right: 0; z-index: 2147483000;
  background: rgba(255,255,255,.94); color: #24292f;
  font-family: -apple-system,"Microsoft YaHei",sans-serif; font-size:12px; line-height:1.55;
  padding: 6px 14px; border-bottom: 1px solid #d8dee4; pointer-events: none;
}
#xdcc_guide b { color: #24292f; }
#xdcc_guide .step { margin: 1px 0; }
#xdcc_guide .now { background: #f0f3f6; border-radius: 4px; padding: 1px 6px; }
"""

_BANNER_HTML = """
<div id="xdcc_guide">
  <div class="step"><b>操作提示</b>（约 1 分钟即可完成）</div>
  <div class="step" id="g1">① 手机号 / 密码已由助手填好，请核对无误</div>
  <div class="step" id="g2"><span class="now">② 点击「获取验证码」，手机收到短信后填入验证码</span></div>
  <div class="step" id="g3">③ 完成「滑块验证」（拖动拼图到正确位置）</div>
  <div class="step" id="g4">④ 点击「{act}」按钮，等待本页顶部提示变为「{act}成功」</div>
  <div class="step" style="opacity:.8">完成后本窗口会自动关闭，无需其他操作；遇阻请把控制台提示发回会话。</div>
</div>
"""


def _detect_chrome():
    """探测本机已安装的桌面浏览器。返回可执行文件路径或 None（此时用 Playwright 自带内核）。"""
    for c in _CHROME_CANDIDATES:
        if c and os.path.isfile(c):
            return c
    return None


def _banner_html(mode):
    """按 register / login 生成对应文案，避免登录模式出现「注册」引导。"""
    action = "注册" if mode == "register" else "登录"
    return _BANNER_HTML.format(act=action)


def inject_banner(page, mode):
    try:
        page.add_style_tag(content=_BANNER_CSS)
        page.evaluate(
            "(html) => { document.body.insertAdjacentHTML('afterbegin', %s); }"
            % json.dumps(_banner_html(mode))
        )
    except Exception:
        pass  # 横幅只是辅助，失败不影响主流程


def set_banner_step(page, step_id, text):
    try:
        page.evaluate(
            "(args) => { const e=document.getElementById(args.id);"
            " if(e){e.innerHTML='<span class=\"now\">'+args.t+'</span>';} }",
            {"id": step_id, "t": text},
        )
    except Exception:
        pass


def autofill(page, mode, phone, password, no_autofill):
    if no_autofill:
        return
    if phone:
        for sel in ("手机号", "手机号码", "手机"):
            try:
                page.get_by_placeholder(sel, exact=False).fill(phone)
                break
            except Exception:
                continue
    if password and mode == "register":
        try:
            page.get_by_placeholder("密码", exact=False).first.fill(password)
        except Exception:
            pass
        try:
            page.get_by_placeholder("确认密码", exact=False).fill(password)
        except Exception:
            pass
    elif password and mode == "login":
        try:
            page.get_by_placeholder("密码", exact=False).first.fill(password)
        except Exception:
            pass


def wait_for_token(page, timeout, mode_cn="注册"):
    print(f"\n[等待] 请在弹出的浏览器中完成：获取验证码 → 填短信码 → 过滑块 → 点{mode_cn} "
          f"（最长等待 {timeout}s）")
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            tok = page.evaluate("localStorage.getItem('userToken')")
        except Exception:
            tok = None
        if tok:
            return tok.strip()
        time.sleep(2)
    return None


def fetch_user_apikey_via_browser(page, token):
    """通过已打开的浏览器页面发起 fetch（复用页面网络上下文，更稳）。"""
    js = (
        "async (token) => {"
        "  const r = await fetch('%s', {method:'POST',"
        "    headers:{'Content-Type':'application/json','auth':token}, body:'{}'});"
        "  return await r.text();"
        "}" % (API_BASE + ENDPOINT)
    )
    try:
        text = page.evaluate(js, token)
    except Exception as e:
        return None, f"浏览器 fetch 失败: {e}"
    try:
        return json.loads(text), None
    except Exception as e:
        return None, f"响应非 JSON: {e}（原始前200字：{str(text)[:200]}）"


def run(mode, phone, password, no_autofill, timeout, creds_path, chrome_path, quiet):
    mode_cn = "注册" if mode == "register" else "登录"

    # Playwright 可用性在运行期判断，返回错误码而不是在导入期直接退出进程
    if sync_playwright is None:
        print(f"\n[失败] {PLAYWRIGHT_ERROR}", file=sys.stderr)
        print("请先安装：pip install playwright && playwright install chromium", file=sys.stderr)
        print(cs_hint("运行环境缺少浏览器自动化依赖"), file=sys.stderr)
        return 2

    print("=" * 56)
    print(f"  小递查查「{mode_cn}引导向导」")
    print("=" * 56)
    print("本向导将帮您完成：注册/登录 → 获取 API Key → 生成查询凭据。")
    print("需要您手动完成的两步（安全校验，无法自动）：")
    print("  · 短信验证码（手机收码后填入）")
    print("  · 阿里云滑块验证（拖动拼图）")
    print("其余步骤由助手自动完成。\n")

    url = PAGES[mode]
    with sync_playwright() as pw:
        launch_kwargs = {"headless": False}
        chrome = chrome_path or _detect_chrome()
        if chrome:
            launch_kwargs["executable_path"] = chrome
        browser = pw.chromium.launch(**launch_kwargs)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")
        print(f"[已打开] {url}")
        inject_banner(page, mode)
        autofill(page, mode, phone, password, no_autofill)
        if not no_autofill:
            print("[自动填表] 手机号/密码已尝试自动填入，请核对页面顶部引导横幅。")

        token = wait_for_token(page, timeout, mode_cn)
        if not token:
            print("\n[失败] 等待超时，未取得登录凭证(userToken)。", file=sys.stderr)
            print("常见原因：未点「获取验证码」、短信码填错、滑块未通过、或网络不畅。", file=sys.stderr)
            print(cs_hint("注册/登录超时未取得凭证"), file=sys.stderr)
            browser.close()
            return 1

        print(f"[成功] 已取得登录凭证（前8位：{token[:8]}…），正在获取 API Key…")
        set_banner_step(page, "g4", "✅ 已登录，正在获取 API Key…")

        payload, err = fetch_user_apikey_via_browser(page, token)
        if err:
            print(f"[提示] 浏览器内调用异常（{err}），改用脚本直连…")
            payload, err = call_get_user_apikey(token)
        if err:
            print(f"\n[失败] 获取 API Key 出错：{err}", file=sys.stderr)
            print(cs_hint("GetUserApiKey 调用失败"), file=sys.stderr)
            browser.close()
            return 1

        data = (payload or {}).get("Data") or {}
        code = payload.get("Code", payload.get("code"))
        if not data or str(code) not in ("0", "200", "200.0"):
            print(f"\n[失败] GetUserApiKey 返回异常：Code={code} "
                  f"Message={payload.get('Message') or payload.get('msg')}", file=sys.stderr)
            print(cs_hint("GetUserApiKey 返回异常，账号可能未完成实名/激活"), file=sys.stderr)
            browser.close()
            return 1

        creds = map_apikey_to_creds(data)
        if not (creds["XDCC_PLATFORM_ID"] and creds["XDCC_MEMBER_ID"] and creds["XDCC_API_KEY"]):
            print("\n[失败] 凭据字段缺失（PlatformID / UserID / UserApiKey）。", file=sys.stderr)
            print("接口原始返回：", json.dumps(payload, ensure_ascii=False)[:300], file=sys.stderr)
            print(cs_hint("凭据字段缺失"), file=sys.stderr)
            browser.close()
            return 1

        # 落盘凭据
        write_creds(creds_path, creds, token=token)
        print(f"[已生成] 凭据文件：{creds_path}")
        print(f"         PlatformID={creds['XDCC_PLATFORM_ID']}  "
              f"MemberID={creds['XDCC_MEMBER_ID']}  "
              f"APIKey={creds['XDCC_API_KEY'][:8]}…")

        # 校验凭据可用于批量查询
        print("[校验] 用新凭据试跑一单，确认可用于批量查询…")
        ok, msg = validate_track_creds(creds)
        if ok:
            print(f"[校验通过] {msg}")
            set_banner_step(page, "g4", "✅ 注册成功，API Key 已就绪！可关闭此窗口。")
            print("\n✅ 注册引导完成。凭据已就绪，下一步即可批量查询快递。")
            browser.close()
            return 0
        else:
            print(f"[校验未通过] {msg}", file=sys.stderr)
            print("凭据已生成，但试跑未通过。可能是账号需激活/实名，或接口临时异常。", file=sys.stderr)
            print(cs_hint(f"凭据校验未通过：{msg}"), file=sys.stderr)
            browser.close()
            return 1


def main(argv=None):
    p = argparse.ArgumentParser(description="小递查查 无障碍注册引导向导（人在环）")
    p.add_argument("--mode", choices=["register", "login"], default="register",
                   help="register=新账号注册（默认）；login=已有账号登录")
    p.add_argument("--phone", help="手机号（自动填入，可留空手动填）")
    p.add_argument("--password", help="密码（自动填入，可留空手动填）")
    p.add_argument("--no-autofill", action="store_true", help="完全手动填写表单")
    p.add_argument("--timeout", type=int, default=600, help="等待完成注册的秒数（默认600）")
    p.add_argument("--creds", default=os.path.expanduser("~/.workbuddy/xdcc-credentials.env"),
                   help="凭据输出路径（默认 ~/.workbuddy/xdcc-credentials.env）")
    p.add_argument("--chrome-path", default=None, help="Chrome 可执行文件路径（默认自动探测）")
    args = p.parse_args(argv)

    if args.mode == "register" and not args.phone:
        print("提示：注册需要手机号。可加 --phone 138xxxx 自动填入，或留空在页面手动填。", file=sys.stderr)
    return run(args.mode, args.phone, args.password, args.no_autofill,
               args.timeout, args.creds, args.chrome_path, False)


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass
    sys.exit(main())
