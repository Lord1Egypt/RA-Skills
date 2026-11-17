#!/usr/bin/env python3
"""
api_server.py - Local open query API (BidHunter v3.0, zero-cloud subset).

Exposes BidHunter's data over a local HTTP API so other local tools / your own
scripts can query verdicts, rules and reports without the cloud. NO external
server, NO paid infra — binds to 127.0.0.1 only.

Endpoints:
  GET /health
  GET /query?title=...            -> verdict for a single title
  GET /rules                      -> current qual_rules.json
  GET /report?date=YYYY-MM-DD    -> text report for a date (if cached)
  GET /analytics?days=30         -> local portrait summary (JSON)

v3.0 cloud/SaaS parts (multi-tenant, third-party plugin marketplace, data
marketplace, Salesforce/金蝶 connectors) are DEFERRED per the cost constraint
(require paid cloud infra). This local API is the zero-cost "开放能力" subset.

Usage:
  python3 api_server.py [--port 8765]
"""
import os
import sys
import json
import re
import glob
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT_DIR = os.path.dirname(HERE)
RULES_PATH = os.path.join(SCRIPT_DIR, "qual_rules.json")
CACHE_DIR = os.path.join(SCRIPT_DIR, "bid_cache")
REPORT_DIR = os.path.join(SCRIPT_DIR, "bid_reports")


def _verdict_for(title):
    sys.path.insert(0, SCRIPT_DIR)
    from qual_check import evaluate_announcement, load_rules
    rules = load_rules(RULES_PATH)
    ann = {"title": title, "id": "api", "url": "", "source": "api"}
    return evaluate_announcement(ann, rules)


class Handler(BaseHTTPRequestHandler):
    def _j(self, obj, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "http://127.0.0.1")
        self.end_headers()
        self.wfile.write(json.dumps(obj, ensure_ascii=False).encode("utf-8"))

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path == "/health":
            return self._j({"status": "ok", "service": "bidhunter-api", "ts": datetime.now().isoformat()})
        if u.path == "/query":
            title = (q.get("title") or [""])[0]
            if not title:
                return self._j({"error": "missing title"}, 400)
            return self._j(_verdict_for(title))
        if u.path == "/rules":
            try:
                with open(RULES_PATH, "r", encoding="utf-8") as f:
                    return self._j(json.load(f))
            except Exception as e:
                return self._j({"error": str(e)}, 500)
        if u.path == "/report":
            d = (q.get("date") or [datetime.now().strftime("%Y-%m-%d")])[0]
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", d):
                return self._j({"error": "invalid date format, expected YYYY-MM-DD"}, 400)
            p = os.path.join(REPORT_DIR, f"report_{d}.txt")
            if not os.path.exists(p):
                return self._j({"error": "no report for " + d}, 404)
            with open(p, "r", encoding="utf-8") as f:
                return self._j({"date": d, "report": f.read()})
        if u.path == "/analytics":
            days = int((q.get("days") or ["30"])[0])
            # lightweight: count by verdict from qual cache
            from collections import Counter
            c = Counter()
            for f in glob.glob(os.path.join(CACHE_DIR, "qual_*.jsonl")):
                for line in open(f, encoding="utf-8"):
                    try:
                        c[json.loads(line).get("verdict", "x")] += 1
                    except Exception:
                        pass
            return self._j({"days": days, "verdicts": dict(c)})
        self.send_error(404)

    def log_message(self, *a):
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()
    print(f"BidHunter 本地 API 已启动: http://127.0.0.1:{args.port}  (Ctrl+C 退出)")
    print("仅本机访问，无云端依赖。v3.0 云/SaaS 部分因成本约束未启用。")
    HTTPServer(("127.0.0.1", args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
