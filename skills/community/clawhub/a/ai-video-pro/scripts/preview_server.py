"""
本地视频预览服务器

零外部依赖，仅使用 Python 标准库。
提供 HTML5 视频播放器，支持播放控制。
仅绑定 localhost，不对外暴露。
"""

import argparse
import http.server
import mimetypes
import os
import sys
import threading
import webbrowser
from pathlib import Path
from urllib.parse import unquote

# HTML 模板
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Video Pro - 视频预览</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #0a0a0a;
            color: #e0e0e0;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .header h1 {{
            font-size: 24px;
            font-weight: 300;
            color: #fff;
            margin-bottom: 8px;
        }}
        .header .badge {{
            display: inline-block;
            background: #ff6b00;
            color: #fff;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }}
        .player-container {{
            max-width: 960px;
            width: 100%;
            background: #1a1a1a;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0,0,0,0.5);
        }}
        video {{
            width: 100%;
            display: block;
            background: #000;
        }}
        .controls {{
            padding: 16px 20px;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
            border-top: 1px solid #333;
        }}
        .controls button {{
            background: #2a2a2a;
            border: 1px solid #444;
            color: #e0e0e0;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            transition: all 0.2s;
        }}
        .controls button:hover {{
            background: #3a3a3a;
            border-color: #666;
        }}
        .controls button.active {{
            background: #0066ff;
            border-color: #0066ff;
            color: #fff;
        }}
        .info {{
            padding: 16px 20px;
            border-top: 1px solid #333;
            font-size: 13px;
            color: #888;
        }}
        .info table {{
            width: 100%;
        }}
        .info td {{
            padding: 4px 0;
        }}
        .info td:first-child {{
            color: #666;
            width: 100px;
        }}
        .speed-group {{
            display: flex;
            gap: 4px;
        }}
        .speed-group button {{
            padding: 6px 10px;
            font-size: 12px;
        }}
        .frame-info {{
            margin-left: auto;
            font-size: 13px;
            color: #888;
            font-variant-numeric: tabular-nums;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>AI Video Pro Preview</h1>
        <span class="badge">BETA</span>
    </div>

    <div class="player-container">
        <video id="player" controls preload="auto">
            <source src="/video/{filename}" type="{mimetype}">
            您的浏览器不支持 HTML5 视频播放。
        </video>

        <div class="controls">
            <button onclick="togglePlay()">播放/暂停</button>
            <button onclick="stepFrame(-1)">上一帧</button>
            <button onclick="stepFrame(1)">下一帧</button>
            <button onclick="restart()">重播</button>
            <button onclick="toggleLoop()" id="loopBtn">循环: 关</button>

            <div class="speed-group">
                <button onclick="setSpeed(0.25)">0.25x</button>
                <button onclick="setSpeed(0.5)">0.5x</button>
                <button onclick="setSpeed(1)" class="active" id="speed1">1x</button>
                <button onclick="setSpeed(2)">2x</button>
            </div>

            <span class="frame-info" id="frameInfo">00:00.000</span>
        </div>

        <div class="info">
            <table>
                <tr><td>文件名</td><td>{filename}</td></tr>
                <tr><td>文件大小</td><td>{filesize}</td></tr>
                <tr><td>路径</td><td>{filepath}</td></tr>
            </table>
        </div>
    </div>

    <script>
        const player = document.getElementById('player');
        const frameInfo = document.getElementById('frameInfo');

        function togglePlay() {{
            player.paused ? player.play() : player.pause();
        }}

        function stepFrame(direction) {{
            player.pause();
            // 假设 30fps
            player.currentTime += direction * (1/30);
        }}

        function restart() {{
            player.currentTime = 0;
            player.play();
        }}

        function toggleLoop() {{
            player.loop = !player.loop;
            document.getElementById('loopBtn').textContent =
                '循环: ' + (player.loop ? '开' : '关');
            document.getElementById('loopBtn').classList.toggle('active', player.loop);
        }}

        function setSpeed(speed) {{
            player.playbackRate = speed;
            document.querySelectorAll('.speed-group button').forEach(btn => {{
                btn.classList.toggle('active', btn.textContent === speed + 'x');
            }});
        }}

        function updateFrameInfo() {{
            const t = player.currentTime;
            const m = Math.floor(t / 60);
            const s = Math.floor(t % 60);
            const ms = Math.floor((t % 1) * 1000);
            frameInfo.textContent =
                String(m).padStart(2, '0') + ':' +
                String(s).padStart(2, '0') + '.' +
                String(ms).padStart(3, '0');
            requestAnimationFrame(updateFrameInfo);
        }}
        requestAnimationFrame(updateFrameInfo);

        // 快捷键
        document.addEventListener('keydown', (e) => {{
            switch(e.key) {{
                case ' ': e.preventDefault(); togglePlay(); break;
                case 'ArrowLeft': stepFrame(-1); break;
                case 'ArrowRight': stepFrame(1); break;
                case 'r': restart(); break;
                case 'l': toggleLoop(); break;
            }}
        }});
    </script>
</body>
</html>"""


class PreviewHandler(http.server.BaseHTTPRequestHandler):
    """视频预览 HTTP 请求处理器。"""

    video_path = None
    video_filename = None

    def do_GET(self):
        path = unquote(self.path)

        if path == "/" or path == "/index.html":
            self._serve_html()
        elif path.startswith("/video/"):
            self._serve_video()
        else:
            self.send_error(404)

    def _serve_html(self):
        video_path = Path(self.__class__.video_path)
        file_size = video_path.stat().st_size
        size_str = f"{file_size / (1024*1024):.1f} MB" if file_size > 1024*1024 else f"{file_size / 1024:.1f} KB"

        mime_type, _ = mimetypes.guess_type(str(video_path))
        mime_type = mime_type or "video/mp4"

        html = HTML_TEMPLATE.format(
            filename=self.__class__.video_filename,
            mimetype=mime_type,
            filesize=size_str,
            filepath=str(video_path),
        )

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _serve_video(self):
        video_path = Path(self.__class__.video_path)
        if not video_path.exists():
            self.send_error(404, "视频文件不存在")
            return

        mime_type, _ = mimetypes.guess_type(str(video_path))
        mime_type = mime_type or "video/mp4"
        file_size = video_path.stat().st_size

        # 支持 Range 请求（视频拖拽）
        range_header = self.headers.get("Range")
        if range_header:
            range_start, range_end = self._parse_range(range_header, file_size)
            self.send_response(206)
            self.send_header("Content-Range", f"bytes {range_start}-{range_end}/{file_size}")
            self.send_header("Content-Length", str(range_end - range_start + 1))
        else:
            range_start, range_end = 0, file_size - 1
            self.send_response(200)
            self.send_header("Content-Length", str(file_size))

        self.send_header("Content-Type", mime_type)
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()

        with open(video_path, "rb") as f:
            f.seek(range_start)
            remaining = range_end - range_start + 1
            chunk_size = 65536
            while remaining > 0:
                chunk = f.read(min(chunk_size, remaining))
                if not chunk:
                    break
                self.wfile.write(chunk)
                remaining -= len(chunk)

    def _parse_range(self, range_header: str, file_size: int):
        """解析 HTTP Range 头。"""
        range_spec = range_header.replace("bytes=", "")
        parts = range_spec.split("-")
        start = int(parts[0]) if parts[0] else 0
        end = int(parts[1]) if parts[1] else file_size - 1
        return start, min(end, file_size - 1)

    def log_message(self, format, *args):
        """静默日志，避免刷屏。"""
        pass


def start_preview_server(video_path: str, port: int = 8765,
                         open_browser: bool = True) -> None:
    """
    启动视频预览服务器。

    Args:
        video_path: 视频文件路径
        port: 服务器端口
        open_browser: 是否自动打开浏览器
    """
    video_path = Path(video_path).resolve()
    if not video_path.exists():
        print(f"错误: 视频文件不存在: {video_path}")
        sys.exit(1)

    PreviewHandler.video_path = str(video_path)
    PreviewHandler.video_filename = video_path.name

    server = http.server.HTTPServer(("127.0.0.1", port), PreviewHandler)

    url = f"http://localhost:{port}"
    print(f"预览服务器已启动: {url}")
    print(f"视频文件: {video_path}")
    print("按 Ctrl+C 停止服务器")

    if open_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n预览服务器已停止")
        server.shutdown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Video Pro 视频预览服务器")
    parser.add_argument("--file", required=True, help="视频文件路径")
    parser.add_argument("--port", type=int, default=8765, help="服务器端口 (默认: 8765)")
    parser.add_argument("--no-browser", action="store_true", help="不自动打开浏览器")

    args = parser.parse_args()
    start_preview_server(args.file, args.port, not args.no_browser)
