#!/usr/bin/env python3
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import subprocess
import os
import sys

BASE = Path('/root/.openclaw/workspace/skills/eda-spec2gds/eda-runs').resolve()
OUT = BASE / '_dashboard'


def refresh():
    subprocess.run(['python3', '/root/.openclaw/workspace/skills/eda-spec2gds/scripts/generate_multi_project_dashboard.py'], check=True)


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ['/', '/index.html'] or self.path.endswith('.html'):
            refresh()
        return super().do_GET()


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8766
    OUT.mkdir(parents=True, exist_ok=True)
    refresh()
    os.chdir(str(BASE))
    server = ThreadingHTTPServer(('0.0.0.0', port), Handler)
    print(f'Serving multi-project dashboard on http://0.0.0.0:{port}/_dashboard/index.html')
    server.serve_forever()


if __name__ == '__main__':
    main()
