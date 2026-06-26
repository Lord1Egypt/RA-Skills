#!/usr/bin/env python3
"""
LAN Upload Server — Accept file uploads over LAN and store in shared media directory.
Companion to the LAN Media Server. Saves files to the same MEDIA_ROOT.
"""
import http.server
import socketserver
import os
import cgi
import json
from pathlib import Path

PORT = int(os.getenv('UPLOAD_PORT', '18802'))
MEDIA_ROOT = Path(os.getenv('UPLOAD_ROOT', os.path.expanduser('~/projects/shared-media')))
HOST = os.getenv('BIND_ADDR', '0.0.0.0')  # Bind address (default: all interfaces). Set to specific LAN IP for tighter security.

os.makedirs(MEDIA_ROOT, exist_ok=True)

class UploadHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        # Serve the upload page (same origin)
        if self.path == '/' or self.path == '/upload.html':
            try:
                # Look for upload.html in the same directory as this script
                script_dir = os.path.dirname(os.path.abspath(__file__))
                html_path = os.path.join(script_dir, 'upload.html')
                with open(html_path, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(f'Error loading page: {e}'.encode())
                return
        # Simple status for /upload (GET)
        if self.path == '/upload':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'LAN Upload Server is running. Use POST /upload to send a file.')
            return
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'Not found.')

    def do_POST(self):
        if self.path != '/upload':
            self.send_response(404)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            return

        # Parse multipart form data
        try:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers.get('Content-Type')}
            )
        except Exception as e:
            self.send_response(400)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Invalid form data'}).encode())
            return

        if 'file' not in form:
            self.send_response(400)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'No file field provided'}).encode())
            return

        file_item = form['file']
        if not file_item.filename:
            self.send_response(400)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'No file selected'}).encode())
            return

        # Secure filename
        filename = os.path.basename(file_item.filename)
        dest_path = MEDIA_ROOT / filename

        try:
            with open(dest_path, 'wb') as f:
                # Read in chunks to handle large files
                while True:
                    chunk = file_item.file.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
        except Exception as e:
            self.send_response(500)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': f'Failed to save: {str(e)}'}).encode())
            return

        # Success response
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        # Return both direct download and view URLs (view uses media server)
        server_addr = self.server.server_address
        host = self.headers.get('Host', f'{server_addr[0]}:{PORT}')
        # Media server runs on port 18801
        download_url = f'http://{host.split(":")[0]}:18801/{filename}'
        view_url = download_url  # same endpoint; media server decides content-type
        self.wfile.write(json.dumps({
            'filename': filename,
            'size': dest_path.stat().st_size,
            'download_url': download_url,
            'view_url': view_url,
            'saved_to': str(dest_path)
        }).encode())

    def log_message(self, format, *args):
        # Log to stderr ( Quiet by default, but will show errors)
        return

if __name__ == '__main__':
    # Allow immediate reuse of the address after the server stops (avoid "Address already in use")
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), UploadHandler) as httpd:
        print(f"LAN Upload Server running on http://{HOST}:{PORT}/upload")
        print(f"Files will be saved to: {MEDIA_ROOT}")
        print("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down.")
            httpd.server_close()
