#!/usr/bin/env python3
"""Start/stop a simple HTTP server to serve local PDF files

This serves the pdfs directory so that PDFs can be linked in Zotero
with a local URL that you can access directly.

⚠️  SECURITY NOTICE: This server is designed for INTRANET/PRIVATE NETWORK use only.
Do NOT expose this server directly to the public internet.
Always run it behind a authenticated reverse proxy if external access is needed.

Usage:
    python scripts/start_pdf_server.py start [port] [host]
    python scripts/start_pdf_server.py stop
    python scripts/start_pdf_server.py status

Arguments:
    start: Start server in background
    stop: Stop running server
    status: Show if server is running

    port: Port number to listen on (default: 8000)
    host: Host/IP to listen on (default: 0.0.0.0 = all interfaces)
           Use '内网' or 'private' for all private network addresses

Examples:
    python scripts/start_pdf_server.py start 8000 0.0.0.0
    python scripts/start_pdf_server.py start 8000 192.168.1.100
    python scripts/start_pdf_server.py stop
"""

import http.server
import socketserver
import os
import sys
import signal
import socket
from urllib.parse import unquote

# Get the pdfs directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
PDF_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pdfs'))
PID_FILE = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.pdf_server.pid'))

class SecurePDFRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Secure request handler that only serves PDF files from pdfs directory.

    Security features:
    - Only serves .pdf files
    - Sandboxed to PDF_DIR - no access outside this directory
    - Directory listing disabled
    - Path sanitization to prevent path traversal
    """

    def translate_path(self, path):
        """Sanitize path and ensure it stays within PDF_DIR"""
        # Decode the path
        path = unquote(path)
        # Strip leading slashes
        path = path.lstrip('/')
        # Join with PDF_DIR
        full_path = os.path.abspath(os.path.join(PDF_DIR, path))

        # Security check: ensure the final path is within PDF_DIR
        if not full_path.startswith(PDF_DIR + os.sep):
            # Path traversal attempt
            self.send_error(403, "Forbidden")
            return None

        # Security check: only serve .pdf files
        if not full_path.lower().endswith('.pdf'):
            self.send_error(403, "Forbidden - only PDF files are served")
            return None

        # Check if file exists
        if not os.path.exists(full_path) or not os.path.isfile(full_path):
            self.send_error(404, "Not Found")
            return None

        return full_path

    def list_directory(self, path):
        """Disable directory listing"""
        self.send_error(403, "Forbidden - directory listing disabled")
        return None

def get_private_ips():
    """Get all private network IP addresses"""
    private_ips = []
    try:
        hostname = socket.gethostname()
        addr_info = socket.getaddrinfo(hostname, None)
        for addr in addr_info:
            ip = addr[4][0]
            # Check for private network ranges
            if ip.startswith('10.') or ip.startswith('172.16.') or ip.startswith('192.168.') or ip == 'localhost':
                if ip not in private_ips:
                    private_ips.append(ip)
    except:
        pass
    return private_ips

def is_running():
    """Check if server is running"""
    if not os.path.exists(PID_FILE):
        return False
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        os.kill(pid, 0)
        return True
    except:
        return False

def get_pid():
    """Get PID from pid file"""
    if not os.path.exists(PID_FILE):
        return None
    try:
        with open(PID_FILE, 'r') as f:
            return int(f.read().strip())
    except:
        return None

def start_server(port: int, host: str):
    """Start server in background"""
    if is_running():
        pid = get_pid()
        print(f"PDF server is already running (PID: {pid}) on port {port}")
        print(f"Stop it first with: python {sys.argv[0]} stop")
        sys.exit(1)

    # Create pdfs directory if it doesn't exist
    if not os.path.exists(PDF_DIR):
        os.makedirs(PDF_DIR)

    # Change to pdfs directory
    os.chdir(PDF_DIR)

    # Fork to background
    pid = os.fork()
    if pid > 0:
        # Parent: save pid and exit
        with open(PID_FILE, 'w') as f:
            f.write(str(pid))
        print(f"Starting PDF server in background on {host}:{port}")
        print(f"Serving directory: {PDF_DIR}")
        print()
        print("Configure your base URL in .env file:")
        if host == "0.0.0.0":
            # Get local IPs for user reference
            private_ips = get_private_ips()
            if private_ips:
                for ip in private_ips:
                    print(f"PDF_BASE_URL=http://{ip}:{port}/")
            else:
                print(f"PDF_BASE_URL=http://your-server-ip:{port}/")
        else:
            print(f"PDF_BASE_URL=http://{host}:{port}/")
        print()
        print(f"Server PID: {pid} saved to {PID_FILE}")
        print(f"Stop with: python {sys.argv[0]} stop")
        sys.exit(0)

    # Child: run server
    try:
        with socketserver.TCPServer((host, port), SecurePDFRequestHandler) as httpd:
            print(f"Serving PDFs at http://{host}:{port}")
            print("Security: only .pdf files are served, directory listing disabled")
            httpd.serve_forever()
    except Exception as e:
        print(f"Server error: {e}")
        sys.exit(1)

def stop_server():
    """Stop the running server"""
    if not is_running():
        print("PDF server is not running")
        return
    pid = get_pid()
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"Stopped PDF server (PID: {pid})")
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
    except Exception as e:
        print(f"Error stopping server: {e}")
        # Force remove pid file
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)

def status_server():
    """Show server status"""
    if is_running():
        pid = get_pid()
        print(f"PDF server is running (PID: {pid})")
    else:
        print("PDF server is not running")

def show_help():
    """Show help"""
    print(__doc__)

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == 'start':
        # Get port
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
        # Get host
        if len(sys.argv) > 3:
            host = sys.argv[3]
        else:
            # Default to all interfaces (accessible from any IP)
            host = "0.0.0.0"

        # Handle "内网" or "private" alias
        if host.lower() in ['内网', 'private', 'lan']:
            # Still listen on 0.0.0.0 for all interfaces
            # User can access from any private IP
            host = "0.0.0.0"

        start_server(port, host)

    elif command == 'stop':
        stop_server()

    elif command == 'status':
        status_server()

    elif command in ['-h', '--help', 'help']:
        show_help()

    else:
        print(f"Unknown command: {command}")
        print()
        show_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
