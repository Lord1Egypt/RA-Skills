#!/usr/bin/env python3
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import subprocess
import sys
import os

ROOT = Path('/root/.openclaw/workspace/skills/eda-spec2gds/eda-runs/simple_fifo_demo').resolve()
REPORTS = ROOT / 'reports'


def latest_metrics_path():
    candidates = sorted(ROOT.glob('constraints/runs/*/final/metrics.json'))
    return candidates[-1] if candidates else None


def refresh_artifacts():
    metrics = latest_metrics_path()
    if metrics is not None:
        subprocess.run([
            'python3',
            '/root/.openclaw/workspace/skills/eda-spec2gds/scripts/extract_ppa.py',
            str(metrics),
            str(REPORTS / 'ppa.json')
        ], check=False)
    subprocess.run([
        'python3',
        '/root/.openclaw/workspace/skills/eda-spec2gds/scripts/extract_progress.py',
        str(ROOT),
        str(REPORTS / 'progress.json')
    ], check=False)
    subprocess.run([
        'python3',
        '/root/.openclaw/workspace/skills/eda-spec2gds/scripts/list_artifacts.py',
        str(ROOT),
        str(REPORTS / 'artifacts-index.json')
    ], check=False)
    subprocess.run([
        'python3',
        '/root/.openclaw/workspace/skills/eda-spec2gds/scripts/generate_artifact_index.py'
    ], check=True)


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ['/', '/index.html']:
            refresh_artifacts()
        return super().do_GET()


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    REPORTS.mkdir(parents=True, exist_ok=True)
    refresh_artifacts()
    os.chdir(str(REPORTS))
    server = ThreadingHTTPServer(('0.0.0.0', port), Handler)
    print(f'Serving {REPORTS} on http://0.0.0.0:{port}/')
    print(f'Open http://<server-ip>:{port}/index.html')
    server.serve_forever()


if __name__ == '__main__':
    main()
