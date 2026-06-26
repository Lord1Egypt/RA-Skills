#!/usr/bin/env python3
"""OpenClaw Harness Dashboard Server - Python version"""

import http.server
import json
import os
import re
import urllib.parse
import socketserver

PORT = 8765
# BASE_DIR is the directory containing this server.py.
# When copied to a project root, it serves files from that root.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REQUESTS_DIR = os.path.join(BASE_DIR, 'requests')

MIME_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.js': 'application/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.svg': 'image/svg+xml',
}

def find_project_states():
    projects = []
    for root, dirs, files in os.walk(BASE_DIR):
        if 'node_modules' in root:
            continue
        if 'project-state.json' in files:
            full = os.path.join(root, 'project-state.json')
            try:
                with open(full, 'r') as f:
                    state = json.load(f)
                rel = os.path.relpath(full, BASE_DIR)
                project_dir = os.path.dirname(rel)
                project_id = 'default' if project_dir == '.' else project_dir
                modules = state.get('modules', [])
                if isinstance(modules, dict):
                    modules = list(modules.values())
                total = len(modules)
                completed = sum(1 for m in modules if m.get('status') in ('accepted', 'passed') or m.get('state') in ('accepted', 'passed'))
                top_status = state.get('status')
                if top_status and top_status != 'unknown':
                    inferred = top_status
                elif completed == total and total > 0:
                    inferred = 'completed'
                elif any(m.get('status') == 'in_progress' or m.get('state') == 'in_progress' for m in modules):
                    inferred = 'in_progress'
                elif all(m.get('status') == 'pending' or m.get('state') == 'pending' for m in modules):
                    inferred = 'pending'
                else:
                    inferred = 'in_progress'
                projects.append({
                    'id': project_id,
                    'path': '/projects/' + rel,
                    'name': state.get('project_name') or state.get('name', project_id),
                    'status': inferred,
                    'progress': round(completed / total * 100) if total > 0 else 0,
                    'total_modules': total,
                    'completed_modules': completed,
                    'description': state.get('description', ''),
                    'outputDir': project_dir,
                })
            except Exception as e:
                print('Error loading ' + full + ': ' + str(e))

    archive_dir = os.path.join(BASE_DIR, 'archive')
    if os.path.isdir(archive_dir):
        for af in sorted(os.listdir(archive_dir)):
            if af.endswith('.json'):
                try:
                    with open(os.path.join(archive_dir, af), 'r') as f:
                        state = json.load(f)
                    modules = state.get('modules', [])
                    if isinstance(modules, dict):
                        modules = list(modules.values())
                    total = len(modules)
                    completed = sum(1 for m in modules if m.get('status') in ('accepted', 'passed') or m.get('state') in ('accepted', 'passed'))
                    name = state.get('project_name') or state.get('name', af)
                    stem = os.path.splitext(af)[0]
                    for s in ['-2026-04-06', '-2026-04-07']:
                        stem = stem.replace(s, '')
                    projects.append({
                        'id': 'archived-' + os.path.splitext(af)[0],
                        'path': '/archive/' + af,
                        'name': name,
                        'status': 'completed',
                        'progress': round(completed / total * 100) if total > 0 else 0,
                        'total_modules': total,
                        'completed_modules': completed,
                        'description': state.get('description', ''),
                        'outputDir': stem,
                    })
                except Exception as e:
                    print('Error loading archive ' + af + ': ' + str(e))

    if os.path.isdir(REQUESTS_DIR):
        for rf in sorted(os.listdir(REQUESTS_DIR)):
            if rf.endswith('.json'):
                try:
                    with open(os.path.join(REQUESTS_DIR, rf), 'r') as f:
                        req = json.load(f)
                    req_name = req.get('name', os.path.splitext(rf)[0])
                    if not any(p['name'] == req_name for p in projects):
                        mods = req.get('modules', [])
                        projects.append({
                            'id': 'req-' + os.path.splitext(rf)[0],
                            'path': None,
                            'name': '[待启动] ' + req_name,
                            'status': 'pending',
                            'progress': 0,
                            'total_modules': len(mods),
                            'completed_modules': 0,
                            'description': req.get('description', ''),
                            'is_request': True,
                        })
                except Exception as e:
                    print('Error loading request ' + rf + ': ' + str(e))

    return projects


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        pathname = parsed.path

        if pathname == '/api/projects':
            data = json.dumps(find_project_states())
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(data.encode())))
            self.end_headers()
            self.wfile.write(data.encode())
            return

        if pathname.startswith('/api/logs/'):
            project_id = urllib.parse.unquote(pathname[len('/api/logs/'):])
            logs_dir = os.path.join(BASE_DIR, project_id, 'logs')
            parsed_logs = []
            if os.path.isdir(logs_dir):
                # Read all .log files and merge by timestamp
                for log_file in sorted(os.listdir(logs_dir)):
                    if not log_file.endswith('.log'):
                        continue
                    # Extract agent name from filename
                    agent_name = log_file.replace('.log', '')
                    fp = os.path.join(logs_dir, log_file)
                    if os.path.isfile(fp):
                        with open(fp, 'r') as f:
                            for line in f:
                                line = line.strip()
                                if not line:
                                    continue
                                # Parse: [timestamp] message
                                m = re.match(r'^\[([^\]]+)\]\s+(.*)', line)
                                if m:
                                    timestamp = m[1]
                                    rest = m[2]
                                    # Legacy timeline.log format: [timestamp] [agent_name] message
                                    agent_match = re.match(r'^\[([^\]]+)\]\s+(.*)', rest)
                                    if agent_match:
                                        agent_name = agent_match[1]
                                        message = agent_match[2]
                                    else:
                                        message = rest
                                    # Truncate timestamp microseconds to seconds
                                    if '.' in timestamp:
                                        base, tz = timestamp.split('.')
                                        tz_start = tz.find('+') if '+' in tz else tz.find('Z')
                                        if tz_start >= 0:
                                            timestamp = base + tz[tz_start:]
                                        else:
                                            timestamp = base + tz[-6:] if len(tz) > 6 else base + tz
                                    parsed_logs.append({
                                        'timestamp': timestamp,
                                        'agent': agent_name,
                                        'message': message
                                    })
            # Sort by timestamp (newest first)
            parsed_logs.sort(key=lambda x: x['timestamp'], reverse=True)
            data = json.dumps(parsed_logs)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(data.encode())))
            self.end_headers()
            self.wfile.write(data.encode())
            return

        if pathname.startswith('/projects/'):
            rel = urllib.parse.unquote(pathname[len('/projects/'):])
            fp = os.path.join(BASE_DIR, rel)
            if os.path.isfile(fp) and self.safe_path(fp):
                self.send_file(fp)
            else:
                self.send_404()
            return

        if pathname.startswith('/archive/'):
            af = urllib.parse.unquote(pathname[len('/archive/'):])
            fp = os.path.join(BASE_DIR, 'archive', af)
            if os.path.isfile(fp) and self.safe_path(fp):
                with open(fp, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_404()
            return

        if pathname == '/':
            fp = os.path.join(BASE_DIR, 'dashboard.html')
        else:
            fp = os.path.join(BASE_DIR, pathname.lstrip('/'))

        if os.path.isfile(fp) and self.safe_path(fp):
            self.send_file(fp)
        else:
            self.send_404()

    def safe_path(self, fp):
        """Ensure filepath is within BASE_DIR (prevent path traversal)."""
        real = os.path.realpath(fp)
        return real.startswith(os.path.realpath(BASE_DIR) + os.sep) or real == os.path.realpath(BASE_DIR)

    def send_file(self, fp):
        ext = os.path.splitext(fp)[1].lower()
        ct = MIME_TYPES.get(ext, 'application/octet-stream')
        with open(fp, 'rb') as f:
            content = f.read()
        self.send_response(200)
        self.send_header('Content-Type', ct)
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def send_404(self):
        body = b'<h1>404 Not Found</h1>'
        self.send_response(404)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def main():
    # Bind to localhost only — never expose to public network
    with ReusableTCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print('\n🦞 OpenClaw Harness Dashboard (Python)')
        print('=' * 40)
        print('📂 Serving from: ' + BASE_DIR)
        print('🌐 Dashboard:    http://localhost:' + str(PORT))
        print('📊 API:         http://localhost:' + str(PORT) + '/api/projects')
        print('\nPress Ctrl+C to stop\n')
        httpd.serve_forever()


if __name__ == '__main__':
    main()
