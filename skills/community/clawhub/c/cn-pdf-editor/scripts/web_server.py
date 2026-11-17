#!/usr/bin/env python3
"""
PDF Editor - Web Server
Launch with: python3 web_server.py [--port 8711] [--file document.pdf]
Then open http://localhost:8711 in your browser.
"""

import os
import sys
import json
import tempfile
import argparse
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Add scripts dir to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "templates")
sys.path.insert(0, SCRIPT_DIR)

from pdf_editor import PDFEditor


class EditorState:
    """Global editor state."""
    editor = None
    filepath = None
    tmp_dir = None

    @classmethod
    def open(cls, filepath):
        cls.filepath = filepath
        cls.editor = PDFEditor(filepath)

    @classmethod
    def ensure(cls):
        if not cls.editor:
            raise ValueError("No PDF opened")


class Handler(BaseHTTPRequestHandler):
    """HTTP request handler for PDF Editor."""

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, path):
        with open(path, 'rb') as f:
            content = f.read()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.wfile.write(content)

    def _send_image(self, data, content_type='image/png'):
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(data))
        self.end_headers()
        self.wfile.write(data)

    def _send_binary(self, data, filename):
        self.send_response(200)
        self.send_header('Content-Type', 'application/pdf')
        self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
        self.send_header('Content-Length', len(data))
        self.end_headers()
        self.wfile.write(data)

    def _read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        return self.rfile.read(length) if length > 0 else b''

    def _parse_multipart(self):
        """Parse multipart form data. Returns dict of {field_name: (filename, bytes)} for files, {field_name: bytes_value} for fields."""
        content_type = self.headers.get('Content-Type', '')
        boundary = content_type.split('boundary=')[1]
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        boundary_b = ('--' + boundary).encode()
        parts = body.split(boundary_b)
        result = {}
        for part in parts:
            if not part or part.strip() in (b'', b'--', b'--\r\n', b'\r\n'):
                continue
            # Split headers from body
            if b'\r\n\r\n' not in part:
                continue
            header_data, content = part.split(b'\r\n\r\n', 1)
            if content.endswith(b'\r\n'):
                content = content[:-2]
            # Parse Content-Disposition
            header_str = header_data.decode('utf-8', errors='replace')
            if 'Content-Disposition' not in header_str:
                continue
            name_match = None
            filename_match = None
            for line in header_str.split('\r\n'):
                if 'name="' in line:
                    import re
                    name_match = re.search(r'name="([^"]+)"', line)
                if 'filename=' in line:
                    import re
                    filename_match = re.search(r'filename="?([^"\r\n]+)"?', line)
            if name_match:
                name = name_match.group(1)
                if filename_match:
                    result[name] = (filename_match.group(1), content)
                else:
                    result[name] = content
        return result

    def _read_json(self):
        return json.loads(self._read_body().decode('utf-8'))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == '/' or path == '/index.html':
            self._send_html(os.path.join(TEMPLATES_DIR, 'editor.html'))

        elif path.startswith('/api/page/'):
            try:
                page_num = int(path.split('/')[-1])
                dpi = int(params.get('dpi', ['150'])[0])
                EditorState.ensure()
                data = EditorState.editor.get_page_thumbnail(page_num, dpi)
                self._send_image(data)
            except Exception as e:
                self._send_json({"error": str(e)}, 400)

        elif path == '/api/info':
            try:
                EditorState.ensure()
                self._send_json(EditorState.editor.info())
            except Exception as e:
                self._send_json({"error": str(e)}, 400)

        elif path.startswith('/api/text-blocks/'):
            # Return text blocks with positions for inline editing UI
            try:
                page_num = int(path.split('/')[-1])
                EditorState.ensure()
                spans = EditorState.editor.get_page_text(page_num)
                blocks = []
                for sp in spans:
                    bbox = sp['bbox']
                    blocks.append({
                        'text': sp['text'],
                        'x0': bbox[0], 'y0': bbox[1],
                        'x1': bbox[2], 'y1': bbox[3],
                        'font': sp.get('font', ''),
                        'size': sp.get('size', 12),
                    })
                self._send_json(blocks)
            except Exception as e:
                self._send_json({"error": str(e)}, 400)

        elif path.startswith('/api/text-at/'):
            # Return text at a specific coordinate (for click-to-edit fallback)
            try:
                page_num = int(path.split('/')[-1])
                click_x = float(params.get('x', [0])[0])
                click_y = float(params.get('y', [0])[0])
                EditorState.ensure()
                spans = EditorState.editor.get_page_text(page_num)
                best = None
                best_dist = float('inf')
                for sp in spans:
                    bbox = sp['bbox']
                    # Check if point is inside or near the bounding box
                    cx = (bbox[0] + bbox[2]) / 2
                    cy = (bbox[1] + bbox[3]) / 2
                    dist = ((click_x - cx) ** 2 + (click_y - cy) ** 2) ** 0.5
                    if dist < best_dist:
                        best_dist = dist
                        best = {
                            'text': sp['text'],
                            'x0': bbox[0], 'y0': bbox[1],
                            'x1': bbox[2], 'y1': bbox[3],
                            'width': bbox[2] - bbox[0],
                            'height': bbox[3] - bbox[1],
                        }
                if best and best_dist < 50:  # within 50pt radius
                    self._send_json(best)
                else:
                    self._send_json({"text": None})
            except Exception as e:
                self._send_json({"error": str(e)}, 400)

        else:
            self._send_json({"error": "Not found"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        try:
            if path == '/api/open':
                form = self._parse_multipart()
                file_item = form.get('file')
                if file_item and isinstance(file_item, tuple) and len(file_item) == 2:
                    filename, file_data = file_item
                    tmp_file = os.path.join(EditorState.tmp_dir, 'document.pdf')
                    with open(tmp_file, 'wb') as f:
                        f.write(file_data)
                    EditorState.open(tmp_file)
                    self._send_json(EditorState.editor.info())
                else:
                    self._send_json({"error": "No file uploaded"}, 400)

            elif path == '/api/edit-text-at-rect':
                try:
                    data = self._read_json()
                    EditorState.ensure()
                    new_rect = EditorState.editor.edit_text_at_rect(
                        page_num=data['page'],
                        x0=data['x0'], y0=data['y0'],
                        x1=data['x1'], y1=data['y1'],
                        new_text=data['new_text'])
                    self._send_json({"ok": True, "new_rect": new_rect})
                except Exception as e:
                    self._send_json({"error": str(e)}, 500)

            elif path == '/api/add-text':
                data = self._read_json()
                EditorState.ensure()
                EditorState.editor.add_text(
                    data['page'], data['text'], data.get('x', 72),
                    data.get('y', 72), data.get('font_size', 12))
                self._send_json({"ok": True})

            elif path == '/api/insert-image':
                EditorState.ensure()
                form = self._parse_multipart()
                page = int(form.get('page', b'0')) if isinstance(form.get('page'), bytes) else 0
                img_item = form.get('image')
                if img_item and isinstance(img_item, tuple) and len(img_item) == 2:
                    filename, img_data = img_item
                    img_path = os.path.join(EditorState.tmp_dir, 'upload_image')
                    with open(img_path, 'wb') as f:
                        f.write(img_data)
                    EditorState.editor.insert_image(page, img_path, 72, 72)
                    self._send_json({"ok": True})
                else:
                    self._send_json({"error": "No image"}, 400)

            elif path == '/api/watermark':
                data = self._read_json()
                EditorState.ensure()
                count = EditorState.editor.add_watermark(
                    text=data.get('text'),
                    opacity=data.get('opacity', 0.3),
                    font_size=data.get('font_size', 50),
                    angle=data.get('angle', 45),
                    pages=data.get('pages', 'all'))
                self._send_json({"count": count})

            elif path == '/api/highlight':
                data = self._read_json()
                EditorState.ensure()
                count = EditorState.editor.add_highlight(
                    data['page'], data['text'])
                self._send_json({"count": count})

            elif path == '/api/annotation':
                data = self._read_json()
                EditorState.ensure()
                EditorState.editor.add_annotation(
                    data['page'], data['text'],
                    data.get('x', 200), data.get('y', 200))
                self._send_json({"ok": True})

            elif path == '/api/rotate':
                parts = path.split('/')
                page_num = int(parts[-1])
                EditorState.ensure()
                EditorState.editor.rotate_page(page_num)
                self._send_json({"ok": True})

            elif path == '/api/save':
                EditorState.ensure()
                saved = EditorState.editor.save()
                self._send_json({"path": saved})

            elif path == '/api/download':
                EditorState.ensure()
                import io
                buf = io.BytesIO()
                EditorState.editor.doc.save(buf)
                buf.seek(0)
                filename = os.path.basename(EditorState.filepath or 'edited.pdf')
                if not filename.endswith('.pdf'):
                    filename += '.pdf'
                self._send_binary(buf.read(), filename)

            else:
                self._send_json({"error": "Not found"}, 404)

        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path

        try:
            if path.startswith('/api/delete-page/'):
                page_num = int(path.split('/')[-1])
                EditorState.ensure()
                EditorState.editor.delete_pages([page_num])
                self._send_json({"pages": len(EditorState.editor.doc)})
            else:
                self._send_json({"error": "Not found"}, 404)
        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    def log_message(self, format, *args):
        # Suppress request logs for cleaner output
        pass


def main():
    parser = argparse.ArgumentParser(description="PDF Editor Web Server")
    parser.add_argument('--port', type=int, default=8711, help='Port number')
    parser.add_argument('--file', '-f', help='PDF file to open on startup')
    args = parser.parse_args()

    # Create temp directory
    EditorState.tmp_dir = tempfile.mkdtemp(prefix='pdf_editor_')
    print(f"📎 Temp dir: {EditorState.tmp_dir}")

    server = HTTPServer(('0.0.0.0', args.port), Handler)

    url = f'http://localhost:{args.port}'
    print(f"\n📄 PDF Editor 已启动!")
    print(f"🌐 地址: {url}")
    print(f"⌨️  按 Ctrl+C 退出\n")

    # Open browser
    webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 PDF Editor 已关闭")
        server.server_close()
        # Cleanup temp files
        import shutil
        if EditorState.tmp_dir:
            shutil.rmtree(EditorState.tmp_dir, ignore_errors=True)


if __name__ == '__main__':
    main()
