#!/usr/bin/env python3
"""
Coze-Power Server — Bridge Coze bots to local capabilities.

Usage:
    python3 server.py                    # Start with default config
    python3 server.py --config my.json   # Custom config path
    python3 server.py --port 9999        # Override port

Requirements: Python 3.8+ (standard library only, no pip needed)
"""

import json
import os
import sys
import subprocess
import pyperclip  # optional: pip install pyperclip
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from datetime import datetime
import platform
import shutil

# ─── Default Config ───────────────────────────────────────────────────────────

DEFAULT_CONFIG = {
    "api_key": "coze-power-dev-key",
    "host": "0.0.0.0",
    "port": 8899,
    "allowed_commands": ["ls", "pwd", "cat", "echo", "python3", "node", "date", "whoami"],
    "allowed_paths": [os.path.expanduser("~"), "/tmp"],
    "max_file_size_kb": 1024,
}

CONFIG = dict(DEFAULT_CONFIG)


# ─── Load Config ──────────────────────────────────────────────────────────────

def load_config(path=None):
    global CONFIG
    if path is None:
        # Look for config.json next to the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(script_dir, "config.json")
    if os.path.exists(path):
        try:
            with open(path) as f:
                user_config = json.load(f)
            CONFIG.update(user_config)
            print(f"[coze-power] Loaded config from {path}")
        except Exception as e:
            print(f"[coze-power] Warning: Failed to load config: {e}")
    else:
        print(f"[coze-power] No config found at {path}, using defaults")
        print(f"[coze-power] Default API key: {CONFIG['api_key']} (CHANGE THIS!)")


# ─── Tools Implementation ─────────────────────────────────────────────────────

def tool_web_search(query: str, count: int = 5):
    """Search the web using DuckDuckGo (no API key needed)."""
    import urllib.request
    import urllib.parse
    from html.parser import HTMLParser

    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

    class ResultParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.results = []
            self._in_result = False
            self._in_link = False
            self._in_snippet = False
            self._current = {}
            self._depth = 0

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == "a" and attrs.get("class") == "result__a":
                self._in_link = True
                self._current = {"title": "", "url": attrs.get("href", ""), "snippet": ""}
            if tag == "a" and "result__snippet" in attrs.get("class", ""):
                self._in_snippet = True

        def handle_data(self, data):
            if self._in_link:
                self._current["title"] += data.strip()
            if self._in_snippet:
                self._current["snippet"] += data.strip()

        def handle_endtag(self, tag):
            if tag == "a" and self._in_link:
                self._in_link = False
                if self._current.get("title"):
                    self.results.append(self._current)
                self._current = {}
            if tag == "a" and self._in_snippet:
                self._in_snippet = False

    try:
        resp = urllib.request.urlopen(req, timeout=15)
        html = resp.read().decode("utf-8", errors="replace")
        parser = ResultParser()
        parser.feed(html)
        return {"success": True, "results": parser.results[:count], "query": query}
    except Exception as e:
        return {"success": False, "error": str(e)}


def tool_read_file(path: str):
    """Read a file, checking allowed paths."""
    abs_path = os.path.abspath(os.path.expanduser(path))
    if not _is_path_allowed(abs_path):
        return {"success": False, "error": f"Access denied: {path} is not in allowed paths"}
    if not os.path.exists(abs_path):
        return {"success": False, "error": f"File not found: {path}"}
    if os.path.getsize(abs_path) > CONFIG["max_file_size_kb"] * 1024:
        return {"success": False, "error": f"File too large (max {CONFIG['max_file_size_kb']}KB)"}
    try:
        with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        return {"success": True, "path": path, "content": content, "size": len(content)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def tool_write_file(path: str, content: str):
    """Write content to a file."""
    abs_path = os.path.abspath(os.path.expanduser(path))
    if not _is_path_allowed(abs_path):
        return {"success": False, "error": f"Access denied: {path} is not in allowed paths"}
    try:
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"success": True, "path": path, "size": len(content)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def tool_list_dir(path: str = "."):
    """List contents of a directory."""
    abs_path = os.path.abspath(os.path.expanduser(path))
    if not _is_path_allowed(abs_path):
        return {"success": False, "error": f"Access denied: {path} is not in allowed paths"}
    if not os.path.isdir(abs_path):
        return {"success": False, "error": f"Not a directory: {path}"}
    try:
        entries = os.listdir(abs_path)
        items = []
        for name in sorted(entries):
            full = os.path.join(abs_path, name)
            stat = os.stat(full)
            items.append({
                "name": name,
                "type": "dir" if os.path.isdir(full) else "file",
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            })
        return {"success": True, "path": path, "items": items, "count": len(items)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def tool_run_command(command: str):
    """Execute a shell command (whitelist enforced)."""
    cmd_parts = command.strip().split()
    if not cmd_parts:
        return {"success": False, "error": "Empty command"}
    base = cmd_parts[0]
    if base not in CONFIG["allowed_commands"]:
        return {
            "success": False,
            "error": f"Command '{base}' not allowed. Allowed: {', '.join(CONFIG['allowed_commands'])}",
        }
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=30
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout[:5000],
            "stderr": result.stderr[:2000],
            "return_code": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timed out (30s limit)"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def tool_system_info():
    """Get system information."""
    try:
        uname = platform.uname()
        disk = shutil.disk_usage("/")
        return {
            "success": True,
            "os": f"{uname.system} {uname.release}",
            "hostname": uname.node,
            "architecture": uname.machine,
            "cpu_count": os.cpu_count(),
            "disk_total_gb": round(disk.total / (1024**3), 1),
            "disk_free_gb": round(disk.free / (1024**3), 1),
            "disk_used_pct": round(disk.used / disk.total * 100, 1),
            "python_version": sys.version.split()[0],
            "current_time": datetime.now().isoformat(),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def tool_clipboard_read():
    """Read clipboard content."""
    try:
        import pyperclip
        text = pyperclip.paste()
        return {"success": True, "content": text[:10000]}
    except ImportError:
        # Fallback: try xclip on Linux
        try:
            result = subprocess.run(
                ["xclip", "-o", "-selection", "clipboard"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                return {"success": True, "content": result.stdout[:10000]}
        except:
            pass
        return {"success": False, "error": "Clipboard module not available. Install: pip install pyperclip"}


def tool_clipboard_write(content: str):
    """Write to clipboard."""
    try:
        import pyperclip
        pyperclip.copy(content)
        return {"success": True, "size": len(content)}
    except ImportError:
        try:
            proc = subprocess.Popen(["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE)
            proc.communicate(content.encode("utf-8"))
            return {"success": True, "size": len(content)}
        except:
            return {"success": False, "error": "Clipboard module not available. Install: pip install pyperclip"}


def tool_notify(title: str, message: str):
    """Send desktop notification."""
    try:
        if sys.platform == "linux":
            subprocess.run(
                ["notify-send", title, message],
                capture_output=True, timeout=5
            )
        elif sys.platform == "darwin":
            subprocess.run(
                ["osascript", "-e", f'display notification "{message}" with title "{title}"'],
                capture_output=True, timeout=5
            )
        elif sys.platform == "win32":
            from ctypes import windll
            windll.user32.MessageBoxW(0, message, title, 0)
        else:
            return {"success": False, "error": f"Notifications not supported on {sys.platform}"}
        return {"success": True, "title": title, "message": message}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _is_path_allowed(path: str) -> bool:
    """Check if a path is within allowed directories."""
    abs_path = os.path.realpath(os.path.abspath(path))
    for allowed in CONFIG["allowed_paths"]:
        allowed_abs = os.path.realpath(os.path.abspath(os.path.expanduser(allowed)))
        if abs_path.startswith(allowed_abs):
            return True
    return False


# ─── HTTP Handler ─────────────────────────────────────────────────────────────

TOOLS = {
    "web-search":          tool_web_search,
    "read-file":           tool_read_file,
    "write-file":          tool_write_file,
    "list-dir":            tool_list_dir,
    "run-command":         tool_run_command,
    "system-info":         tool_system_info,
    "clipboard-read":      tool_clipboard_read,
    "clipboard-write":     tool_clipboard_write,
    "notify":              tool_notify,
}


class CozePowerHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the Coze-Power API."""

    def _auth(self):
        api_key = self.headers.get("X-API-Key", "")
        if api_key != CONFIG["api_key"]:
            self._json(401, {"success": False, "error": "Invalid API key"})
            return False
        return True

    def _json(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._json(200, {"status": "ok", "version": "1.0.0", "tools": list(TOOLS.keys())})
        elif parsed.path == "/tools/system-info":
            if not self._auth():
                return
            self._json(200, tool_system_info())
        else:
            self._json(404, {"success": False, "error": f"Not found: {parsed.path}"})

    def do_POST(self):
        if not self._auth():
            return

        parsed = urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            params = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError as e:
            self._json(400, {"success": False, "error": f"Invalid JSON: {e}"})
            return

        tool_name = parsed.path.removeprefix("/tools/")
        if tool_name not in TOOLS:
            self._json(404, {"success": False, "error": f"Unknown tool: {tool_name}"})
            return

        try:
            tool_fn = TOOLS[tool_name]
            result = tool_fn(**params)
            self._json(200, result)
        except TypeError as e:
            self._json(400, {"success": False, "error": f"Invalid parameters: {e}"})
        except Exception as e:
            self._json(500, {"success": False, "error": f"Internal error: {e}"})

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-API-Key")
        self.end_headers()

    def log_message(self, format, *args):
        print(f"[coze-power] {datetime.now().isoformat()} {args[0]} {args[1]} {args[2]}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Coze-Power: Bridge Coze bots to local capabilities")
    parser.add_argument("--config", help="Path to config JSON file")
    parser.add_argument("--port", type=int, help="Override port")
    parser.add_argument("--host", help="Override host")
    args = parser.parse_args()

    load_config(args.config)

    if args.port:
        CONFIG["port"] = args.port
    if args.host:
        CONFIG["host"] = args.host

    server = HTTPServer((CONFIG["host"], CONFIG["port"]), CozePowerHandler)
    print(f"╔══════════════════════════════════════════════════╗")
    print(f"║  🚀 Coze-Power Server v1.0                      ║")
    print(f"╠══════════════════════════════════════════════════╣")
    print(f"║  Listening on: http://{CONFIG['host']}:{CONFIG['port']}          ║")
    print(f"║  API Key:      {CONFIG['api_key']}                     ║")
    print(f"║  Tools loaded: {len(TOOLS)}                                ║")
    print(f"║  Commands:     {'/health'}                 ║")
    print(f"║                                                      ║")
    print(f"║  ⚠️  For Coze to reach this server, expose it via:   ║")
    print(f"║     ngrok http {CONFIG['port']}                          ║")
    print(f"║     cloudflared tunnel --url http://localhost:{CONFIG['port']}  ║")
    print(f"╚══════════════════════════════════════════════════╝")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[coze-power] Shutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
