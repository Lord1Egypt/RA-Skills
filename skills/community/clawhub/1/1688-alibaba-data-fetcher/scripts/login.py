#!/usr/bin/env python3
"""
1688 Data Claw - 登录脚本 (v6)
==================================
特性 (v6):
  - 脚本永不退出（除非登录成功或达到 --max-time 上限）
  - 单次 wait_timeout 后自动刷新二维码，继续等待
  - 模型侧只需 poll 一次，无需循环 re-exec

输出标记:
  [QR_UPDATED]       — 二维码已生成/已刷新（含大小+裁剪坐标）
  [LOGIN_SUCCESS]    — 登录成功（→ sys.exit(0)）
  [TIMEOUT]          — 单次等待超时（脚本继续，不退出）
  [MAX_TIME_REACHED] — 总等待超时，超出 --max-time（→ sys.exit(1)）

用法:
  python3 login.py                              # 首次登录（清Cookie + 导航 + 生成二维码）
  python3 login.py --refresh                    # 刷新二维码（复用当前会话）
  python3 login.py --wait-timeout 300           # 单次二维码等待超时（默认 300s，禁止 < 180s）
  python3 login.py --max-time 1800              # 总等待超时（默认 0=无限）

退出码: 0=登录成功, 1=达到 max-time 或浏览器未就绪
"""

import sys
import json
import time
import os
import subprocess
import base64
import platform
from pathlib import Path

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR / 'scripts'))

from cdp_client import CdpClient, _cdp_call, _cdp_eval

OUTPUT = SKILL_DIR / '1688_qrcode.png'
WAIT_TIMEOUT = 100      # 默认 100s（1688 二维码有效期约 120s）
MIN_WAIT_TIMEOUT = 90   # 硬下界：留 30s 余量，避免刷新太频繁浪费
MAX_WAIT_TIMEOUT = 110  # 硬上界：超过 110s 会扫不上（⛔ 安全区 90–110s）
DEFAULT_MAX_TIME = 0    # 默认无限（=永不退出）


def _start_browser():
    if platform.system() == 'Windows':
        script = SKILL_DIR / 'scripts' / 'start-browser.ps1'
        cmd = f'powershell -ExecutionPolicy Bypass -File "{script}"'
    else:
        script = SKILL_DIR / 'scripts' / 'start-browser.sh'
        cmd = f'bash "{script}"'
    result = subprocess.run(cmd, shell=True, check=False)
    return result.returncode == 0


def _find_qr_canvas(sock):
    qr_info = _cdp_eval(sock, """
    (function() {
        var canvases = document.querySelectorAll('canvas');
        for (var c of canvases) {
            var r = c.getBoundingClientRect();
            if (r.width > 50 && r.height > 50 && r.x >= 0 && r.y >= 0) {
                var ctx = c.getContext && c.getContext('2d');
                if (ctx) {
                    try {
                        var imgData = ctx.getImageData(0, 0, c.width, c.height);
                        var nonWhite = 0;
                        for (var i = 0; i < imgData.data.length; i += 16) {
                            if (imgData.data[i] < 200) nonWhite++;
                        }
                        if (nonWhite < 5) continue;
                    } catch(e) {}
                }
                if (r.width >= 100 && r.width <= 350 && r.height >= 100 && r.height <= 350) {
                    return JSON.stringify({
                        x: Math.round(r.x) - 20,
                        y: Math.round(r.y) - 20,
                        width: Math.round(r.width) + 40,
                        height: Math.round(r.height) + 40
                    });
                }
            }
        }
        var selectors = [
            '.qrcode-img', '#qrcode', '.qr-code', '.login-qrcode',
            '[class*="qrcode"]', '[class*="qr_code"]', '[id*="qrcode"]',
            'div[class*="QR"]', 'div[class*="qr"]'
        ];
        for (var sel of selectors) {
            var el = document.querySelector(sel);
            if (el) {
                var r = el.getBoundingClientRect();
                if (r.width > 50 && r.height > 50) {
                    return JSON.stringify({
                        x: Math.round(r.x) - 15,
                        y: Math.round(r.y) - 15,
                        width: Math.round(r.width) + 30,
                        height: Math.round(r.height) + 30
                    });
                }
            }
        }
        var imgs = document.querySelectorAll('img[src*="qrcode"], img[src*="qr"], img[src*="QR"]');
        for (var img of imgs) {
            var r = img.getBoundingClientRect();
            if (r.width > 50 && r.height > 50) {
                return JSON.stringify({
                    x: Math.round(r.x) - 10,
                    y: Math.round(r.y) - 10,
                    width: Math.round(r.width) + 20,
                    height: Math.round(r.height) + 20
                });
            }
        }
        var allImgs = document.querySelectorAll('canvas, img');
        var best = null, bestArea = 0;
        for (var el of allImgs) {
            var r = el.getBoundingClientRect();
            if (r.width > 50 && r.height > 50 && r.x > 200) {
                var area = r.width * r.height;
                if (area > bestArea && area < 400 * 400) {
                    bestArea = area;
                    best = el;
                }
            }
        }
        if (best) {
            var r = best.getBoundingClientRect();
            return JSON.stringify({
                x: Math.round(r.x) - 20,
                y: Math.round(r.y) - 20,
                width: Math.round(r.width) + 40,
                height: Math.round(r.height) + 40
            });
        }
        return null;
    })()
    """)
    if qr_info:
        return json.loads(qr_info)
    return None


def _capture_qr(sock, output_path):
    clip = _find_qr_canvas(sock)
    if clip is None:
        clip = {'x': 476, 'y': 168, 'width': 180, 'height': 180}
    result = _cdp_call(sock, 'Page.captureScreenshot', {
        'format': 'png',
        'clip': {
            'x': clip['x'], 'y': clip['y'],
            'width': clip['width'], 'height': clip['height'],
            'scale': 1
        }
    })
    img = base64.b64decode(result['data'])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(str(output_path), 'wb') as f:
        f.write(img)
    return len(img), clip


def _refresh_qr_on_page(sock):
    """刷新页面上的二维码：通过 CDP Page.reload 完整重载页面"""
    _cdp_call(sock, 'Page.reload')
    time.sleep(1)


def _switch_to_qr_login(sock):
    """切换到扫码登录模式"""
    result = _cdp_eval(sock, """
    (function() {
        var all = document.querySelectorAll('*');
        for (var el of all) {
            if (el.offsetParent === null) continue;
            var text = (el.textContent || '').trim();
            if (text === '扫码' || text === '扫码登录' || text === '二维码') {
                return text;
            }
        }
        for (var el of all) {
            if (el.offsetParent === null) continue;
            var text = (el.textContent || '').trim();
            if (text.includes('扫码') && text.length < 10) {
                el.click();
                return 'clicked: ' + text;
            }
        }
        return 'already_qr';
    })()
    """)
    return result


def _wait_for_login(sock, wait_timeout, start_time, max_time):
    """
    轮询等待登录成功。返回:
      True  — 登录成功（已 sys.exit(0)）
      False — 单次超时但未达 max-time，调用方应刷新二维码继续等
    v6 起永不因"单次超时"sys.exit，进程继续运行。
    """
    for i in range(wait_timeout):
        time.sleep(1)
        url = _cdp_eval(sock, 'window.location.href') or ''
        if 'work.1688.com' in url and 'login' not in url.lower():
            print(f"[LOGIN_SUCCESS] 登录成功！耗时 {i + 1}s")
            return True
        if (i + 1) % 30 == 0:
            print(f"[INFO] 等待登录中... {i + 1}s / {wait_timeout}s")
            sys.stdout.flush()
        # max-time 检查
        if max_time > 0 and (time.time() - start_time) >= max_time:
            print(f"[MAX_TIME_REACHED] 总等待时间达到 {max_time}s")
            return False
    print(f"[TIMEOUT] 单次等待超时（{wait_timeout}s），将自动刷新二维码...")
    return False


def main():
    refresh_mode = '--refresh' in sys.argv

    output_path = OUTPUT
    wait_timeout = WAIT_TIMEOUT
    max_time = DEFAULT_MAX_TIME

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == '--output' and i + 1 < len(args):
            output_path = Path(args[i + 1])
            i += 2
        elif args[i] == '--wait-timeout' and i + 1 < len(args):
            wait_timeout = int(args[i + 1])
            i += 2
        elif args[i] == '--max-time' and i + 1 < len(args):
            max_time = int(args[i + 1])
            i += 2
        elif args[i] == '--refresh':
            i += 1
        else:
            i += 1

    # ── wait_timeout 硬下界检查（⛔ 二维码有效期 ~120s，禁止越界）──
    if wait_timeout < MIN_WAIT_TIMEOUT:
        print(f"[WARN] --wait-timeout {wait_timeout}s 低于硬下界 {MIN_WAIT_TIMEOUT}s，"
              f"已强制为 {MIN_WAIT_TIMEOUT}s")
        wait_timeout = MIN_WAIT_TIMEOUT
    elif wait_timeout > MAX_WAIT_TIMEOUT:
        print(f"[WARN] --wait-timeout {wait_timeout}s 超出硬上界 {MAX_WAIT_TIMEOUT}s "
              f"（1688 二维码有效期约 120s，超出会扫不上），已强制为 {MAX_WAIT_TIMEOUT}s")
        wait_timeout = MAX_WAIT_TIMEOUT

    # ── 检查/启动浏览器 ──
    if not CdpClient.is_running():
        print("[INFO] 浏览器未运行，启动中...")
        if not _start_browser():
            print("[ERROR] 浏览器启动失败")
            sys.exit(2)
        time.sleep(3)

    start_time = time.time()  # 总等待起始时间

    with CdpClient() as c:
        try:
            c.ensure_tab(retries=3)
        except RuntimeError:
            print("[INFO] 没有 1688 标签页，创建中...")
            c.create_tab("https://work.1688.com/?_path_=sellerPro/sellberBaseNew_Index/seller2018IndexPage")
            time.sleep(4)
            c.ensure_tab(retries=5)

        sock = c._sock

        # ── 首次准备页面（仅第一轮）：正常模式清 Cookie+导航；refresh 模式直接刷新 ──
        if refresh_mode:
            print("[INFO] 刷新模式：完整刷新页面获取新二维码...")
            _refresh_qr_on_page(sock)
            print("[INFO] 页面已完整刷新，等待加载...")
            time.sleep(5)
        else:
            print("[INFO] 清除 Cookie...")
            _cdp_call(sock, 'Network.clearBrowserCookies')

            print("[INFO] 导航到 1688 工作台...")
            _cdp_call(sock, 'Page.navigate', {
                'url': 'https://work.1688.com/?_path_=sellerPro/sellberBaseNew_Index/seller2018IndexPage'
            })
            time.sleep(5)

            url = _cdp_eval(sock, 'window.location.href') or ''
            print(f"[INFO] 当前 URL: {url[:100]}")

            if 'login' not in url.lower() and 'work.1688.com' in url.lower():
                print("[LOGIN_SUCCESS] 已登录，无需扫码")
                sys.exit(0)

            print("[INFO] 切换到扫码登录...")
            switch_result = _switch_to_qr_login(sock)
            print(f"[INFO] 切换结果: {switch_result}")
            time.sleep(3)

            print("[INFO] 完整刷新页面以获取干净二维码...")
            _refresh_qr_on_page(sock)
            time.sleep(5)

        # 截取二维码（首次）
        file_size, clip = _capture_qr(sock, output_path)
        print(f"[QR_UPDATED] 大小={file_size}bytes, "
              f"裁剪=[x={clip['x']} y={clip['y']} w={clip['width']} h={clip['height']}]")
        print(f"[INFO] 二维码文件: {output_path}")
        sys.stdout.flush()

        # ── 大循环：v6 永不因单次超时退出 ──
        round_idx = 0
        while True:
            round_idx += 1
            max_time_note = "" if max_time == 0 else f"，max-time={max_time}s"
            print(f"[INFO] 第 {round_idx} 轮等待扫码（最长 {wait_timeout}s{max_time_note}）...")
            sys.stdout.flush()

            success = _wait_for_login(sock, wait_timeout, start_time, max_time)
            if success:
                sys.exit(0)

            # 单次超时但未达 max-time：刷新二维码，继续等
            if max_time > 0 and (time.time() - start_time) >= max_time:
                print("[MAX_TIME_REACHED] 总等待超时，退出")
                sys.exit(1)

            print(f"[INFO] 自动刷新二维码（round {round_idx + 1}）...")
            _refresh_qr_on_page(sock)
            time.sleep(5)

            file_size, clip = _capture_qr(sock, output_path)
            print(f"[QR_UPDATED] 大小={file_size}bytes, "
                  f"裁剪=[x={clip['x']} y={clip['y']} w={clip['width']} h={clip['height']}]")
            print(f"[INFO] 二维码文件: {output_path}")
            sys.stdout.flush()


if __name__ == '__main__':
    main()