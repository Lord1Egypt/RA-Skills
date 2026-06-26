"""
Crypto Wave Scanner — Local Server
Serves the dashboard at http://localhost:7890/wave-scanner.html
"""
import http.server, socketserver, webbrowser, os, threading, time

PORT = 7890
ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets')

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args): pass  # silent

def open_browser():
    time.sleep(1.2)
    webbrowser.open(f"http://localhost:{PORT}/wave-scanner.html")

os.chdir(ASSETS_DIR)
threading.Thread(target=open_browser, daemon=True).start()

print(f"🌊 Cedars Wave Scanner running at http://localhost:{PORT}/wave-scanner.html")
print("Press Ctrl+C to stop.")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
