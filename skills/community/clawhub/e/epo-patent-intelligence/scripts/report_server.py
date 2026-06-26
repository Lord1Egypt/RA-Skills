#!/usr/bin/env python3
"""
Simple HTTP server for serving patent reports
Serves static HTML reports on port 8080
"""

import http.server
import socketserver
import os
import sys

# Configuration
PORT = 8080
DIRECTORY = "/root/.openclaw/workspace/skills/epo-patent-intelligence/reports"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def log_message(self, format, *args):
        # Custom logging
        print(f"[REPORT SERVER] {self.client_address[0]} - {format % args}")

# Ensure reports directory exists
os.makedirs(DIRECTORY, exist_ok=True)

# Create index.html if it doesn't exist
index_path = os.path.join(DIRECTORY, "index.html")
if not os.path.exists(index_path):
    with open(index_path, "w") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Patent Intelligence Reports</title>
    <style>
        body { font-family: system-ui, -apple-system, sans-serif; max-width: 1200px; margin: 0 auto; padding: 40px; }
        h1 { color: #1a1a2e; }
        .report-list { list-style: none; padding: 0; }
        .report-item { 
            background: #f8f9fa; 
            border-radius: 8px; 
            padding: 20px; 
            margin: 10px 0;
            border-left: 4px solid #4361ee;
        }
        .report-item a { 
            color: #4361ee; 
            text-decoration: none; 
            font-weight: 600;
            font-size: 1.1em;
        }
        .report-item a:hover { text-decoration: underline; }
        .report-meta { 
            color: #666; 
            font-size: 0.9em; 
            margin-top: 5px;
        }
        .status { 
            display: inline-block; 
            padding: 4px 12px; 
            border-radius: 20px; 
            font-size: 0.8em; 
            font-weight: 500;
            margin-left: 10px;
        }
        .status.pending { background: #ffd700; color: #333; }
        .status.ready { background: #28a745; color: white; }
    </style>
</head>
<body>
    <h1>📊 Patent Intelligence Reports</h1>
    <p>Weekly competitive intelligence reports for DMG Mori</p>
    
    <ul class="report-list">
        <li class="report-item">
            <a href="weekly_report_20260404.html">Week 14, 2026 - Competitive Analysis</a>
            <span class="status pending">Generating...</span>
            <div class="report-meta">Last updated: Loading from database...</div>
        </li>
    </ul>
    
    <script>
        // Auto-refresh every 30 seconds to check for new reports
        setTimeout(() => location.reload(), 30000);
    </script>
</body>
</html>""")

# Start server
with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print(f"[REPORT SERVER] Serving reports at http://localhost:{PORT}")
    print(f"[REPORT SERVER] Reports directory: {DIRECTORY}")
    print(f"[REPORT SERVER] Press Ctrl+C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[REPORT SERVER] Shutting down...")
        sys.exit(0)
