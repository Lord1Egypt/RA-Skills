#!/usr/bin/env python3
"""
Browser control adapter — provides a unified CLI for browser automation.
Controls the user's existing Google Chrome via Chrome DevTools Protocol (CDP).

浏览器控制适配器 — 提供统一的命令行接口来控制浏览器。
通过 Chrome DevTools Protocol (CDP) 控制用户已有的 Google Chrome，无检测横幅。

=== Setup / 初始设置 ===

Step 1: Start Chrome with remote debugging enabled / 启动 Chrome 并启用远程调试:

  Windows:
    chrome.exe --remote-debugging-port=9222

  macOS:
    /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222

  Linux:
    google-chrome --remote-debugging-port=9222

  Or add --remote-debugging-port=9222 to your Chrome shortcut properties.
  或在 Chrome 快捷方式属性中添加 --remote-debugging-port=9222。

Step 2: Install dependency / 安装依赖:
    pip install playwright

Step 3: Use this script / 使用本脚本:
    python browser.py navigate <url>
    python browser.py screenshot [url] [--output path.png] [--full]
    python browser.py dom
    python browser.py text
    python browser.py click <x> <y>
    python browser.py type <text>
    python browser.py key <key_name>
    python browser.py scroll <direction> [amount]
    python browser.py resize <width> <height>
    python browser.py network
    python browser.py console
    python browser.py status
    python browser.py lock          # Block user input (prevent interference)
    python browser.py unlock        # Restore user input

=== Why no "controlled by automated software" banner? ===
=== 为什么没有"正受到自动测试软件的控制"横幅？===

This script connects to your EXISTING Chrome via CDP (same as Antigravity).
It does NOT launch a new Chrome instance in automation mode.
Your Chrome is a normal user-launched browser — CDP just attaches to it.

本脚本通过 CDP 连接到你已有的 Chrome（与 Antigravity 相同方式）。
不会启动新的自动化模式 Chrome 实例。
你的 Chrome 是正常用户启动的浏览器 — CDP 只是附加连接。
"""

import argparse
import asyncio
import json
import sys
import os
from datetime import datetime

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("ERROR: playwright not installed.")
    print("  Install: pip install playwright")
    print("  Note: No need to run 'playwright install' — we connect to your existing Chrome, not Playwright's bundled browser.")
    print()
    print("ERROR: 未安装 playwright。")
    print("  安装: pip install playwright")
    print("  注意: 无需运行 'playwright install' — 我们连接你已有的 Chrome，不使用 Playwright 自带浏览器。")
    sys.exit(1)

CDP_ENDPOINT = os.environ.get("BROWSER_CDP_ENDPOINT", "http://localhost:9222")


async def get_browser():
    """Connect to existing Chrome via CDP. Never launches a new browser."""
    p = await async_playwright().start()
    try:
        browser = await p.chromium.connect_over_cdp(CDP_ENDPOINT)
    except Exception as e:
        print(f"ERROR: Cannot connect to Chrome at {CDP_ENDPOINT}")
        print(f"  {e}")
        print()
        print("Make sure Chrome is running with remote debugging:")
        print(f'  chrome.exe --remote-debugging-port=9222')
        print()
        print(f"ERROR: 无法连接到 Chrome ({CDP_ENDPOINT})")
        print("请确保 Chrome 已启用远程调试:")
        print(f'  chrome.exe --remote-debugging-port=9222')
        sys.exit(1)
    return p, browser


async def get_page(browser):
    """Get the active page or create one."""
    contexts = browser.contexts
    if not contexts:
        context = await browser.new_context()
    else:
        context = contexts[0]

    pages = context.pages
    if not pages:
        page = await context.new_page()
    else:
        page = pages[-1]

    return page


async def set_input_lock(page, ignore: bool):
    """Lock/unlock user input via visual overlay (same approach as Antigravity).
    When locked: injects a full-screen overlay that intercepts all user input,
    shows 'AI is controlling' message, and provides a Stop button.
    锁定/解锁用户输入（与 Antigravity 相同的覆盖层方式）。
    锁定时：注入全屏覆盖层拦截所有用户操作，显示控制状态，提供停止按钮。"""
    if ignore:
        await page.evaluate("""() => {
            if (document.getElementById('__browser_automation_overlay')) return;

            const overlay = document.createElement('div');
            overlay.id = '__browser_automation_overlay';
            overlay.style.cssText = `
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                z-index: 2147483647;
                background: rgba(0, 0, 0, 0.45);
                display: flex; flex-direction: column;
                align-items: center; justify-content: center;
                cursor: not-allowed;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            `;

            // Pulsing border glow
            const borderEl = document.createElement('div');
            borderEl.style.cssText = `
                position: fixed; top: 0; left: 0; right: 0; bottom: 0;
                border: 3px solid rgba(59, 130, 246, 0.8);
                box-shadow: inset 0 0 30px rgba(59, 130, 246, 0.15);
                pointer-events: none;
                animation: __ba_pulse 2s ease-in-out infinite;
            `;
            overlay.appendChild(borderEl);

            // Status card
            const card = document.createElement('div');
            card.style.cssText = `
                background: rgba(15, 23, 42, 0.95);
                border: 1px solid rgba(59, 130, 246, 0.5);
                border-radius: 16px;
                padding: 32px 48px;
                text-align: center;
                box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
                backdrop-filter: blur(12px);
            `;

            const icon = document.createElement('div');
            icon.textContent = '🤖';
            icon.style.cssText = 'font-size: 48px; margin-bottom: 16px;';
            card.appendChild(icon);

            const title = document.createElement('div');
            title.textContent = 'AI is controlling the browser';
            title.style.cssText = `
                color: #e2e8f0; font-size: 18px; font-weight: 600;
                margin-bottom: 8px;
            `;
            card.appendChild(title);

            const subtitle = document.createElement('div');
            subtitle.textContent = 'AI 正在控制浏览器';
            subtitle.style.cssText = 'color: #94a3b8; font-size: 14px; margin-bottom: 24px;';
            card.appendChild(subtitle);

            // Animated dots
            const dots = document.createElement('div');
            dots.id = '__ba_dots';
            dots.style.cssText = `
                display: flex; gap: 8px; justify-content: center; margin-bottom: 24px;
            `;
            for (let i = 0; i < 3; i++) {
                const dot = document.createElement('div');
                dot.style.cssText = `
                    width: 10px; height: 10px; border-radius: 50%;
                    background: #3b82f6;
                    animation: __ba_bounce 1.4s ease-in-out ${i * 0.16}s infinite;
                `;
                dots.appendChild(dot);
            }
            card.appendChild(dots);

            // Stop button
            const btn = document.createElement('button');
            btn.textContent = '⏹ Stop / 停止';
            btn.style.cssText = `
                background: rgba(239, 68, 68, 0.15);
                border: 1px solid rgba(239, 68, 68, 0.5);
                color: #fca5a5; padding: 10px 28px;
                border-radius: 8px; font-size: 14px; font-weight: 500;
                cursor: pointer; transition: all 0.2s;
            `;
            btn.onmouseenter = () => {
                btn.style.background = 'rgba(239, 68, 68, 0.3)';
                btn.style.borderColor = '#ef4444';
                btn.style.color = '#fff';
            };
            btn.onmouseleave = () => {
                btn.style.background = 'rgba(239, 68, 68, 0.15)';
                btn.style.borderColor = 'rgba(239, 68, 68, 0.5)';
                btn.style.color = '#fca5a5';
            };
            btn.onclick = (e) => {
                e.stopPropagation();
                const el = document.getElementById('__browser_automation_overlay');
                if (el) el.remove();
                const style = document.getElementById('__ba_styles');
                if (style) style.remove();
                window.__browser_automation_stopped = true;
            };
            card.appendChild(btn);
            overlay.appendChild(card);

            // Keyframes
            const style = document.createElement('style');
            style.id = '__ba_styles';
            style.textContent = `
                @keyframes __ba_pulse {
                    0%, 100% { border-color: rgba(59, 130, 246, 0.8); }
                    50% { border-color: rgba(59, 130, 246, 0.3); }
                }
                @keyframes __ba_bounce {
                    0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
                    40% { transform: scale(1); opacity: 1; }
                }
            `;
            document.head.appendChild(style);
            document.body.appendChild(overlay);
            window.__browser_automation_stopped = false;
        }""")
    else:
        await page.evaluate("""() => {
            const el = document.getElementById('__browser_automation_overlay');
            if (el) el.remove();
            const style = document.getElementById('__ba_styles');
            if (style) style.remove();
            window.__browser_automation_stopped = false;
        }""")

async def cmd_status(args):
    p, browser = await get_browser()
    page = await get_page(browser)
    print(json.dumps({
        "status": "connected",
        "cdp": CDP_ENDPOINT,
        "url": page.url,
        "title": await page.title(),
        "viewport": page.viewport_size,
    }, ensure_ascii=False))


async def cmd_navigate(args):
    p, browser = await get_browser()
    page = await get_page(browser)
    await page.goto(args.url, wait_until="domcontentloaded")
    print(json.dumps({
        "status": "ok",
        "url": page.url,
        "title": await page.title()
    }, ensure_ascii=False))


async def cmd_screenshot(args):
    p, browser = await get_browser()
    page = await get_page(browser)

    if args.url:
        await page.goto(args.url, wait_until="domcontentloaded")

    output = args.output or f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    await page.screenshot(path=output, full_page=args.full)
    print(json.dumps({
        "status": "ok",
        "path": os.path.abspath(output),
        "url": page.url,
        "title": await page.title()
    }, ensure_ascii=False))


async def cmd_dom(args):
    p, browser = await get_browser()
    page = await get_page(browser)
    content = await page.content()
    print(content)


async def cmd_text(args):
    p, browser = await get_browser()
    page = await get_page(browser)
    text = await page.inner_text("body")
    print(text)


async def cmd_lock(args):
    p, browser = await get_browser()
    page = await get_page(browser)
    await set_input_lock(page, True)
    print(json.dumps({"status": "ok", "input": "locked",
                      "note": "Overlay active — user input blocked / 覆盖层已激活，用户输入已锁定"}))


async def cmd_unlock(args):
    p, browser = await get_browser()
    page = await get_page(browser)
    await set_input_lock(page, False)
    print(json.dumps({"status": "ok", "input": "unlocked", "note": "User input restored / 用户输入已恢复"}))


async def cmd_click(args):
    p, browser = await get_browser()
    page = await get_page(browser)
    await page.mouse.click(args.x, args.y)
    print(json.dumps({"status": "ok", "clicked": [args.x, args.y]}))


async def cmd_type(args):
    p, browser = await get_browser()
    page = await get_page(browser)
    await page.keyboard.type(args.text)
    print(json.dumps({"status": "ok", "typed": args.text}))


async def cmd_key(args):
    p, browser = await get_browser()
    page = await get_page(browser)
    await page.keyboard.press(args.key_name)
    print(json.dumps({"status": "ok", "key": args.key_name}))


async def cmd_scroll(args):
    p, browser = await get_browser()
    page = await get_page(browser)
    delta = args.amount or 500
    dx, dy = 0, 0
    if args.direction == "down":
        dy = delta
    elif args.direction == "up":
        dy = -delta
    elif args.direction == "right":
        dx = delta
    elif args.direction == "left":
        dx = -delta
    await page.mouse.wheel(dx, dy)
    print(json.dumps({"status": "ok", "direction": args.direction, "amount": delta}))


async def cmd_resize(args):
    p, browser = await get_browser()
    page = await get_page(browser)
    await page.set_viewport_size({"width": args.width, "height": args.height})
    print(json.dumps({"status": "ok", "width": args.width, "height": args.height}))


async def cmd_network(args):
    p, browser = await get_browser()
    page = await get_page(browser)
    requests_log = []

    def on_response(response):
        requests_log.append({
            "url": response.url,
            "status": response.status,
            "method": response.request.method,
        })

    page.on("response", on_response)
    await page.reload(wait_until="domcontentloaded")
    await page.wait_for_timeout(2000)
    print(json.dumps({"status": "ok", "requests": requests_log}, ensure_ascii=False))


async def cmd_console(args):
    p, browser = await get_browser()
    page = await get_page(browser)
    logs = []

    def on_console(msg):
        logs.append({"type": msg.type, "text": msg.text})

    page.on("console", on_console)
    await page.reload(wait_until="domcontentloaded")
    await page.wait_for_timeout(2000)
    print(json.dumps({"status": "ok", "logs": logs}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="Browser automation CLI — controls existing Chrome via CDP\n"
                    "浏览器自动化 CLI — 通过 CDP 控制已有的 Chrome",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--cdp", default=None,
                        help="CDP endpoint (default: http://localhost:9222)")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="Check browser connection / 检查浏览器连接")

    p_nav = sub.add_parser("navigate", help="Navigate to URL / 导航到 URL")
    p_nav.add_argument("url")

    p_ss = sub.add_parser("screenshot", help="Capture screenshot / 截图")
    p_ss.add_argument("url", nargs="?", default=None)
    p_ss.add_argument("--output", "-o", default=None)
    p_ss.add_argument("--full", action="store_true", help="Full page / 全页截图")

    sub.add_parser("dom", help="Get page HTML / 获取页面 HTML")
    sub.add_parser("text", help="Get page text / 获取页面文本")

    p_click = sub.add_parser("click", help="Click at coordinates / 点击坐标")
    p_click.add_argument("x", type=float)
    p_click.add_argument("y", type=float)

    p_type = sub.add_parser("type", help="Type text / 输入文字")
    p_type.add_argument("text")

    p_key = sub.add_parser("key", help="Press a key / 按键")
    p_key.add_argument("key_name")

    p_scroll = sub.add_parser("scroll", help="Scroll page / 滚动页面")
    p_scroll.add_argument("direction", choices=["up", "down", "left", "right"])
    p_scroll.add_argument("amount", type=int, nargs="?", default=500)

    p_resize = sub.add_parser("resize", help="Resize viewport / 调整视口")
    p_resize.add_argument("width", type=int)
    p_resize.add_argument("height", type=int)

    sub.add_parser("network", help="Capture network requests / 捕获网络请求")
    sub.add_parser("console", help="Capture console logs / 捕获控制台日志")

    sub.add_parser("lock", help="Block user input (exclusive model control) / 锁定用户输入")
    sub.add_parser("unlock", help="Restore user input / 解锁用户输入")

    args = parser.parse_args()

    if args.cdp:
        global CDP_ENDPOINT
        CDP_ENDPOINT = args.cdp

    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmd_map = {
        "status": cmd_status,
        "navigate": cmd_navigate, "screenshot": cmd_screenshot,
        "dom": cmd_dom, "text": cmd_text, "click": cmd_click,
        "type": cmd_type, "key": cmd_key, "scroll": cmd_scroll,
        "resize": cmd_resize, "network": cmd_network, "console": cmd_console,
        "lock": cmd_lock, "unlock": cmd_unlock,
    }
    asyncio.run(cmd_map[args.command](args))


if __name__ == "__main__":
    main()
