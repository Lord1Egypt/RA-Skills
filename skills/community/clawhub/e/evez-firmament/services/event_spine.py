#!/usr/bin/env python3
"""EVEZ-OS Event Spine — Append-only hash-linked event log on port 9116."""

import json
import time
import hashlib
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# ── Hash-Linked Event Log ──────────────────────────────────────────

class EventSpine:
    def __init__(self):
        self.lock = threading.Lock()
        self.events = []
        self.index = {}        # domain → [event indices]
        self.chain_valid = True

    def append(self, domain, action, data, timestamp=None):
        with self.lock:
            prev_hash = self.events[-1]["hash"] if self.events else "0" * 64
            seq = len(self.events)
            ts = timestamp or time.time()
            # Build event
            event = {
                "seq": seq,
                "domain": domain,
                "action": action,
                "data": data,
                "timestamp": ts,
                "prev_hash": prev_hash,
            }
            # Compute hash: SHA-256 of (seq + prev_hash + domain + action + data_json)
            hash_input = f"{seq}:{prev_hash}:{domain}:{action}:{json.dumps(data, sort_keys=True, default=str)}"
            event["hash"] = hashlib.sha256(hash_input.encode()).hexdigest()
            self.events.append(event)
            # Index by domain
            self.index.setdefault(domain, []).append(seq)
        return event

    def project(self, domain):
        with self.lock:
            indices = self.index.get(domain, [])
            return [self.events[i] for i in indices if i < len(self.events)]

    def replay(self, domain):
        events = self.project(domain)
        return {
            "domain": domain,
            "events": events,
            "count": len(events),
        }

    def verify(self):
        """Verify chain integrity — check all hash links."""
        with self.lock:
            events = list(self.events)
        
        if not events:
            return {"valid": True, "events_checked": 0, "errors": []}

        errors = []
        for i, event in enumerate(events):
            if i == 0:
                if event["prev_hash"] != "0" * 64:
                    errors.append({"seq": i, "error": "genesis prev_hash mismatch"})
            else:
                if event["prev_hash"] != events[i - 1]["hash"]:
                    errors.append({"seq": i, "error": "chain link broken"})

            # Recompute hash
            hash_input = f"{event['seq']}:{event['prev_hash']}:{event['domain']}:{event['action']}:{json.dumps(event['data'], sort_keys=True, default=str)}"
            computed = hashlib.sha256(hash_input.encode()).hexdigest()
            if computed != event["hash"]:
                errors.append({"seq": i, "error": "hash mismatch", "expected": computed, "actual": event["hash"]})

        return {
            "valid": len(errors) == 0,
            "events_checked": len(events),
            "errors": errors,
            "head_hash": events[-1]["hash"] if events else None,
        }

    def stats(self):
        with self.lock:
            domains = {d: len(idxs) for d, idxs in self.index.items()}
            return {
                "total_events": len(self.events),
                "domains": domains,
                "domain_count": len(domains),
                "head_hash": self.events[-1]["hash"] if self.events else None,
                "first_event": self.events[0]["timestamp"] if self.events else None,
                "last_event": self.events[-1]["timestamp"] if self.events else None,
            }

SPINE = EventSpine()

# ── HTTP Handler ─────────────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):
    def _json(self, code, data):
        body = json.dumps(data, default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length:
            return json.loads(self.rfile.read(length))
        return {}

    def do_GET(self):
        if self.path == "/health":
            self._json(200, {"status": "alive", "service": "event_spine", "port": 9116})
        elif self.path == "/status":
            self._json(200, SPINE.stats())
        elif self.path == "/verify":
            self._json(200, SPINE.verify())
        elif self.path.startswith("/project/"):
            domain = self.path.split("/project/", 1)[1]
            self._json(200, {"domain": domain, "events": SPINE.project(domain)})
        elif self.path.startswith("/replay/"):
            domain = self.path.split("/replay/", 1)[1]
            self._json(200, SPINE.replay(domain))
        elif self.path == "/events":
            # Last 50 events
            with SPINE.lock:
                events = SPINE.events[-50:]
            self._json(200, {"events": events, "showing": len(events)})
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/health":
            self._json(200, {"status": "alive", "service": "event_spine", "port": 9116})
            return

        body = self._read_body()

        if self.path == "/append":
            domain = body.get("domain", "unknown")
            action = body.get("action", "event")
            data = body.get("data", {})
            timestamp = body.get("timestamp")
            event = SPINE.append(domain, action, data, timestamp)
            self._json(201, event)
        elif self.path == "/project":
            domain = body.get("domain", "")
            if not domain:
                self._json(400, {"error": "domain required"})
                return
            self._json(200, {"domain": domain, "events": SPINE.project(domain)})
        elif self.path == "/replay":
            domain = body.get("domain", "")
            if not domain:
                self._json(400, {"error": "domain required"})
                return
            self._json(200, SPINE.replay(domain))
        elif self.path == "/verify":
            self._json(200, SPINE.verify())
        else:
            self._json(404, {"error": "not found"})

    def log_message(self, *a):
        pass

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 9116), Handler)
    print("Event Spine running on :9116")
    server.serve_forever()
