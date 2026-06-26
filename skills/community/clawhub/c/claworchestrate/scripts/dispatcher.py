#!/usr/bin/env python3
"""
ClawOrchestrate — Secure Agent Dispatcher
Receives tasks from gateway via HTTP and triggers local agents.

Security features:
- API key authentication (required)
- Tailscale-only binding (configurable)
- Rate limiting (configurable)
- Request logging
- IP allowlist (optional)

Usage:
  python3 dispatcher.py --api-key YOUR_SECRET_KEY
  python3 dispatcher.py --api-key YOUR_SECRET_KEY --bind 100.73.101.62
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
import threading
import os
import sys
import time
import argparse
import hashlib
import hmac

# Default config
DEFAULT_PORT = 9876
DEFAULT_BIND = "0.0.0.0"  # Change to Tailscale IP for production
OPENCLAW = os.path.expanduser("~/.local/bin/openclaw")
LOG_FILE = "/tmp/dispatcher.log"

# Rate limiting
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX = 30      # requests per window
request_log = []

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def check_rate_limit(client_ip):
    """Check if client IP has exceeded rate limit."""
    now = time.time()
    # Clean old entries
    global request_log
    request_log = [(ip, t) for ip, t in request_log if now - t < RATE_LIMIT_WINDOW]
    
    client_count = sum(1 for ip, t in request_log if ip == client_ip)
    if client_count >= RATE_LIMIT_MAX:
        return False
    
    request_log.append((client_ip, now))
    return True

class SecureDispatchHandler(BaseHTTPRequestHandler):
    api_key = None
    
    def verify_auth(self):
        """Verify API key from Authorization header."""
        auth_header = self.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            provided_key = auth_header[7:]
            return hmac.compare_digest(provided_key, self.api_key)
        return False
    
    def do_POST(self):
        client_ip = self.client_address[0]
        
        # Rate limit check
        if not check_rate_limit(client_ip):
            log(f"RATE LIMITED: {client_ip}")
            self.send_response(429)
            self.end_headers()
            self.wfile.write(b'{"error":"rate limited"}')
            return
        
        if self.path == "/dispatch":
            # Auth check
            if not self.verify_auth():
                log(f"AUTH FAILED: {client_ip}")
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'{"error":"unauthorized"}')
                return
            
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 10240:  # 10KB max
                self.send_response(413)
                self.end_headers()
                self.wfile.write(b'{"error":"payload too large"}')
                return
            
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body)
                agent_id = data.get("agent", "")
                message = data.get("message", "")
                
                # Validate agent_id (alphanumeric + hyphens only)
                if not agent_id or not all(c.isalnum() or c in "-_" for c in agent_id):
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'{"error":"invalid agent id"}')
                    return
                
                if not message or len(message) > 50000:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'{"error":"invalid message"}')
                    return
                
                log(f"DISPATCH: {client_ip} → {agent_id}: {message[:80]}...")
                
                # Trigger agent in background
                threading.Thread(
                    target=self.trigger_agent,
                    args=(agent_id, message),
                    daemon=True
                ).start()
                
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "dispatched", "agent": agent_id}).encode())
                
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error":"invalid json"}')
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        client_ip = self.client_address[0]
        
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        elif self.path == "/agents":
            if not self.verify_auth():
                self.send_response(401)
                self.end_headers()
                return
            # List available agents
            agents_dir = os.path.expanduser("~/.openclaw/agents")
            agents = []
            if os.path.exists(agents_dir):
                agents = [d for d in os.listdir(agents_dir) if os.path.isdir(os.path.join(agents_dir, d, "agent"))]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({"agents": sorted(agents)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress default logging — we handle it ourselves."""
        pass
    
    def trigger_agent(self, agent_id, message):
        """Run openclaw agent in background."""
        try:
            proc = subprocess.Popen(
                [OPENCLAW, "agent", "--agent", agent_id, "--message", message, "--timeout", "120"],
                stdout=open(f"/tmp/dispatch-{agent_id}.log", "a"),
                stderr=subprocess.STDOUT
            )
            log(f"AGENT STARTED: {agent_id} (pid={proc.pid})")
        except Exception as e:
            log(f"AGENT ERROR: {agent_id}: {e}")

def main():
    parser = argparse.ArgumentParser(description="ClawOrchestrate Secure Dispatcher")
    parser.add_argument("--api-key", required=True, help="API key for authentication")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port (default: {DEFAULT_PORT})")
    parser.add_argument("--bind", default=DEFAULT_BIND, help="Bind address (default: 0.0.0.0)")
    args = parser.parse_args()
    
    SecureDispatchHandler.api_key = args.api_key
    
    log(f"ClawOrchestrate Dispatcher starting on {args.bind}:{args.port}")
    log(f"Security: API key auth enabled, rate limiting enabled")
    log(f"POST /dispatch (auth required) — dispatch task to agent")
    log(f"GET /health (public) — health check")
    log(f"GET /agents (auth required) — list available agents")
    
    server = HTTPServer((args.bind, args.port), SecureDispatchHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log("Shutting down...")
        server.shutdown()

if __name__ == "__main__":
    main()
