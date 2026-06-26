#!/usr/bin/env python3
"""
财经简报 PDF 生成脚本

将 Markdown 财经简报转换为正式 PDF，包含封面页和正文。
使用 Chrome headless 进行 HTML→PDF 转换（macOS/Linux 均支持）。

用法:
    python3 generate_pdf.py --input <md文件路径> --output <pdf输出路径>
"""

import argparse
import subprocess
import sys
import shutil
from datetime import datetime
from pathlib import Path


def install_if_missing(package: str, import_name=None):
    import_name = import_name or package
    try:
        __import__(import_name)
    except ImportError:
        print(f"正在安装依赖: {package} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])


def find_chrome():
    """在常见路径寻找 Chrome 可执行文件"""
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium",
        "/usr/bin/google-chrome",
        shutil.which("chromium") or "",
        shutil.which("google-chrome") or "",
    ]
    for path in candidates:
        if path and Path(path).exists():
            return path
    return None


def md_to_html(md_text: str) -> str:
    install_if_missing("markdown")
    import sys as _sys
    import site
    _sys.path.insert(0, site.getusersitepackages())
    import markdown
    return markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "nl2br"],
    )


def build_full_html(body_html: str, report_date: str) -> str:
    template_path = Path(__file__).parent / "template.html"
    template = template_path.read_text(encoding="utf-8")
    return template.replace("{{REPORT_DATE}}", report_date).replace("{{BODY}}", body_html)


def html_to_pdf_chrome(html_path: Path, pdf_path: Path, chrome: str):
    """
    用 Chrome CDP (DevTools Protocol) 生成 PDF。
    通过 --remote-debugging-pipe 与 Chrome 通信，精确控制打印参数，
    彻底去掉页眉页脚（URL、页码等）。
    """
    import http.server
    import threading
    import socket
    import functools
    import json
    import os
    import tempfile
    import time

    # 1. 起临时 HTTP server，从 html 所在目录服务文件
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        http_port = s.getsockname()[1]

    serve_dir = str(html_path.parent)
    handler_cls = functools.partial(
        http.server.SimpleHTTPRequestHandler,
        directory=serve_dir,
    )
    handler_cls.log_message = lambda *a: None
    http_server = http.server.HTTPServer(("127.0.0.1", http_port), handler_cls)
    http_thread = threading.Thread(target=http_server.serve_forever)
    http_thread.daemon = True
    http_thread.start()

    page_url = f"http://127.0.0.1:{http_port}/{html_path.name}"

    # 2. 找一个空闲的远程调试端口
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        debug_port = s.getsockname()[1]

    # 3. 启动 Chrome，开启远程调试
    chrome_proc = subprocess.Popen(
        [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-extensions",
            f"--remote-debugging-port={debug_port}",
            "--no-first-run",
            "--no-default-browser-check",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        # 4. 等 Chrome 启动，获取 WebSocket 调试地址
        import urllib.request
        ws_url = None
        for _ in range(20):
            time.sleep(0.3)
            try:
                resp = urllib.request.urlopen(
                    f"http://127.0.0.1:{debug_port}/json/version", timeout=2
                )
                info = json.loads(resp.read())
                ws_url = info.get("webSocketDebuggerUrl")
                if ws_url:
                    break
            except Exception:
                continue

        if not ws_url:
            raise RuntimeError("Chrome 远程调试未就绪")

        import base64, struct, re

        def _ws_connect(ws_url_str):
            """建立 WebSocket 连接并完成握手，返回 socket。"""
            m = re.match(r"ws://([^/:]+):(\d+)(/.+)", ws_url_str)
            host, port, path = m.group(1), int(m.group(2)), m.group(3)
            s = socket.create_connection((host, port), timeout=30)
            key = base64.b64encode(os.urandom(16)).decode()
            s.sendall((
                f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\n"
                "Upgrade: websocket\r\nConnection: Upgrade\r\n"
                f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
            ).encode())
            buf = b""
            while b"\r\n\r\n" not in buf:
                buf += s.recv(4096)
            return s

        def _ws_send(s, data: str):
            p = data.encode(); mask = os.urandom(4); n = len(p)
            hdr = struct.pack("!BB", 0x81, 0x80 | n) if n < 126 else struct.pack("!BBH", 0x81, 0x80 | 126, n)
            s.sendall(hdr + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(p)))

        def _ws_recv(s) -> str:
            h = b""
            while len(h) < 2: h += s.recv(2 - len(h))
            n = h[1] & 0x7F
            if n == 126:
                e = b""
                while len(e) < 2: e += s.recv(2 - len(e))
                n = struct.unpack("!H", e)[0]
            elif n == 127:
                e = b""
                while len(e) < 8: e += s.recv(8 - len(e))
                n = struct.unpack("!Q", e)[0]
            d = b""
            while len(d) < n: d += s.recv(n - len(d))
            return d.decode("utf-8")

        # 5. 从浏览器级 ws 创建一个新 page target，获取页面级 ws URL
        browser_sock = _ws_connect(ws_url)
        mid = [0]

        def browser_cdp(method, params=None):
            mid[0] += 1
            _ws_send(browser_sock, json.dumps({"id": mid[0], "method": method, "params": params or {}}))
            while True:
                obj = json.loads(_ws_recv(browser_sock))
                if obj.get("id") == mid[0]:
                    return obj.get("result", {})

        target = browser_cdp("Target.createTarget", {"url": "about:blank"})
        target_id = target["targetId"]
        page_ws_url = f"ws://127.0.0.1:{debug_port}/devtools/page/{target_id}"
        browser_sock.close()

        # 6. 连到页面级 WebSocket
        page_sock = _ws_connect(page_ws_url)
        pmid = [0]

        def cdp(method, params=None):
            pmid[0] += 1
            _ws_send(page_sock, json.dumps({"id": pmid[0], "method": method, "params": params or {}}))
            while True:
                obj = json.loads(_ws_recv(page_sock))
                if obj.get("id") == pmid[0]:
                    return obj.get("result", {})

        # 7. 导航并等待加载完成
        cdp("Page.enable")
        cdp("Page.navigate", {"url": page_url})
        for _ in range(40):
            time.sleep(0.2)
            r = cdp("Runtime.evaluate", {"expression": "document.readyState"})
            if r.get("result", {}).get("value") == "complete":
                break
        time.sleep(0.5)  # 等待字体/样式渲染

        # 8. 打印 PDF，关闭页眉页脚
        # margin 设为 0，由 CSS .content padding 控制正文留白；
        # 封面 min-height:100vh 保证全出血背景
        result = cdp("Page.printToPDF", {
            "printBackground": True,
            "displayHeaderFooter": False,   # 精确关闭页眉页脚（URL、页码等）
            "paperWidth": 8.27,             # A4 宽（英寸）
            "paperHeight": 11.69,           # A4 高（英寸）
            "marginTop": 0,
            "marginBottom": 0,
            "marginLeft": 0,
            "marginRight": 0,
            "preferCSSPageSize": False,     # 由 CDP 控制纸张尺寸
        })

        page_sock.close()

        if "data" not in result:
            raise RuntimeError(f"Page.printToPDF 未返回数据: {result}")

        # 9. 解码并写入 PDF
        pdf_data = base64.b64decode(result["data"])
        pdf_path.write_bytes(pdf_data)

    finally:
        chrome_proc.terminate()
        http_server.shutdown()


def main():
    parser = argparse.ArgumentParser(description="财经简报 Markdown → PDF 转换工具")
    parser.add_argument("--input",  "-i", required=True, help="输入 Markdown 文件路径")
    parser.add_argument("--output", "-o", help="输出 PDF 文件路径（默认与输入同目录）")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"错误：找不到输入文件 {input_path}")
        sys.exit(1)

    output_path = Path(args.output).resolve() if args.output else input_path.with_suffix(".pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y年%m月%d日")

    print(f"正在读取: {input_path}")
    md_text = input_path.read_text(encoding="utf-8")

    print("正在转换 Markdown → HTML ...")
    body_html = md_to_html(md_text)

    full_html = build_full_html(body_html, today)

    tmp_html = output_path.with_suffix(".html")
    tmp_html.write_text(full_html, encoding="utf-8")
    print(f"HTML 中间文件: {tmp_html}")

    # 尝试 Chrome headless
    chrome = find_chrome()
    if chrome:
        print(f"正在用 Chrome 生成 PDF: {output_path}")
        try:
            html_to_pdf_chrome(tmp_html, output_path, chrome)
            size_kb = output_path.stat().st_size // 1024
            print(f"\n PDF 已生成: {output_path} ({size_kb} KB)")
            return
        except Exception as e:
            print(f"Chrome 转换失败: {e}，尝试其他方案...")

    # 回退：提示用户手动转换
    print("\n未找到 Chrome，请手动将 HTML 转为 PDF：")
    print(f"  打开浏览器 → 文件 → 打印 → 保存为 PDF")
    print(f"  HTML 文件位置: {tmp_html}")
    print("\n或安装 Chrome 后重新运行此脚本。")
    sys.exit(1)


if __name__ == "__main__":
    main()
