#!/usr/bin/env python3
"""
Simplified Web UI server using only standard library
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timedelta
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
import os

DB_PATH = Path.home() / ".openclaw" / "audit.db"

class AuditAPIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.directory = Path(__file__).parent.parent / "assets" / "templates"
        super().__init__(*args, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        # Serve dashboard
        if parsed.path == '/' or parsed.path == '/dashboard.html':
            self.serve_dashboard()
        elif parsed.path.startswith('/api/'):
            self.handle_api_get(parsed)
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path.startswith('/api/'):
            self.handle_api_post(parsed)
        else:
            self.send_error(404)

    def serve_dashboard(self):
        dashboard_path = self.directory / "dashboard.html"
        if dashboard_path.exists():
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(dashboard_path, 'r') as f:
                self.wfile.write(f.read().encode())
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_simple_dashboard().encode())

    def get_simple_dashboard(self):
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Claw Audit Center</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, sans-serif; background: #0d1117; color: #c9d1d9; padding: 20px; }
        h1 { color: #00ff9f; margin-bottom: 20px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 8px; }
        .stat-label { color: #8b949e; font-size: 12px; text-transform: uppercase; margin-bottom: 8px; }
        .stat-value { color: #00ff9f; font-size: 32px; font-weight: bold; }
        .section { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .section h2 { margin-bottom: 15px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #30363d; }
        th { color: #8b949e; font-size: 12px; text-transform: uppercase; }
        code { background: #21262d; padding: 2px 6px; border-radius: 4px; }
        .badge { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
        .badge-success { background: #238636; color: white; }
        .badge-danger { background: #da3633; color: white; }
    </style>
</head>
<body>
    <h1>⚡ Claw Audit Center (Simplified)</h1>
    <div class="stats" id="stats"></div>
    <div class="section">
        <h2>🔧 Recent Operations</h2>
        <table id="operations"></table>
    </div>
    <div class="section">
        <h2>🚨 Alerts</h2>
        <div id="alerts"></div>
    </div>
    <script>
        fetch('/api/stats').then(r => r.json()).then(stats => {
            document.getElementById('stats').innerHTML = `
                <div class="stat-card"><div class="stat-label">Total Operations</div><div class="stat-value">${stats.total_operations}</div></div>
                <div class="stat-card"><div class="stat-label">Failed Operations</div><div class="stat-value">${stats.failed_operations}</div></div>
                <div class="stat-card"><div class="stat-label">Unresolved Alerts</div><div class="stat-value">${stats.unresolved_alerts}</div></div>
                <div class="stat-card"><div class="stat-label">Activity (24h)</div><div class="stat-value">${stats.recent_24h}</div></div>
            `;
        });

        fetch('/api/operations?limit=10').then(r => r.json()).then(ops => {
            let html = '<tr><th>Time</th><th>Tool</th><th>Action</th><th>Status</th></tr>';
            ops.forEach(op => {
                const time = new Date(op.timestamp).toLocaleString();
                const status = op.success ? '<span class="badge badge-success">✓</span>' : '<span class="badge badge-danger">✗</span>';
                html += `<tr><td>${time}</td><td><code>${op.tool_name}</code></td><td>${op.action}</td><td>${status}</td></tr>`;
            });
            document.getElementById('operations').innerHTML = html;
        });

        fetch('/api/alerts?resolved=false').then(r => r.json()).then(alerts => {
            if (alerts.length === 0) {
                document.getElementById('alerts').innerHTML = '<p>✅ No active alerts</p>';
            } else {
                let html = '';
                alerts.forEach(alert => {
                    html += `<div style="padding: 10px; margin-bottom: 10px; background: #21262d; border-left: 4px solid #00ff9f;">
                        <strong>${alert.alert_type}</strong>: ${alert.message}<br>
                        <small style="color: #8b949e;">${new Date(alert.timestamp).toLocaleString()}</small>
                    </div>`;
                });
                document.getElementById('alerts').innerHTML = html;
            }
        });

        setInterval(() => location.reload(), 30000);
    </script>
</body>
</html>
        """

    def handle_api_get(self, parsed):
        response = self.get_api_response(parsed.path, parsed.query)
        self.send_json(response)

    def handle_api_post(self, parsed):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        response = self.post_api_response(parsed.path, post_data)
        self.send_json(response)

    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def get_db_connection(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def get_api_response(self, path, query):
        conn = self.get_db_connection()
        cursor = conn.cursor()

        try:
            if path == '/api/stats':
                cursor.execute("SELECT COUNT(*) as count FROM operations")
                total = cursor.fetchone()["count"]

                cursor.execute("SELECT COUNT(*) as count FROM operations WHERE success = 0")
                failed = cursor.fetchone()["count"]

                cursor.execute("SELECT COUNT(*) as count FROM audit_alerts WHERE resolved = 0")
                alerts = cursor.fetchone()["count"]

                since = (datetime.now() - timedelta(hours=24)).isoformat()
                cursor.execute("SELECT COUNT(*) as count FROM operations WHERE timestamp >= ?", (since,))
                recent = cursor.fetchone()["count"]

                return {
                    "total_operations": total,
                    "failed_operations": failed,
                    "unresolved_alerts": alerts,
                    "recent_24h": recent
                }

            elif path == '/api/operations':
                params = urllib.parse.parse_qs(query)
                limit = int(params.get('limit', [50])[0])

                cursor.execute("""
                    SELECT * FROM operations
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (limit,))

                return [dict(row) for row in cursor.fetchall()]

            elif path == '/api/alerts':
                params = urllib.parse.parse_qs(query)
                resolved = params.get('resolved', ['false'])[0] == 'true'

                cursor.execute("""
                    SELECT a.*, o.tool_name, o.action
                    FROM audit_alerts a
                    LEFT JOIN operations o ON a.operation_id = o.id
                    WHERE a.resolved = ?
                    ORDER BY a.timestamp DESC
                """, (resolved,))

                return [dict(row) for row in cursor.fetchall()]

            else:
                return {"error": "Unknown endpoint"}

        finally:
            conn.close()

    def post_api_response(self, path, data):
        if path.startswith('/api/alerts/') and path.endswith('/resolve'):
            alert_id = int(path.split('/')[-2])
            conn = self.get_db_connection()
            cursor = conn.cursor()

            cursor.execute("UPDATE audit_alerts SET resolved = 1 WHERE id = ?", (alert_id,))
            conn.commit()
            conn.close()

            return {"success": True}

        return {"error": "Unknown endpoint"}

    def log_message(self, format, *args):
        return  # Suppress log messages

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8080), AuditAPIHandler)
    print("🚀 Starting Audit Center Web UI (Simplified)...")
    print(f"📊 Dashboard: http://localhost:8080")
    print("⚠️  Note: Install Flask for full-featured UI:")
    print("   pip3 install flask watchdog plotly")
    print()
    server.serve_forever()
