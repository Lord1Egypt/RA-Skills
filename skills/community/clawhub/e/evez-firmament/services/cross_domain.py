#!/usr/bin/env python3
"""EVEZ-OS Cross-Domain Engine — OODA loop + poly_c scoring on port 9114."""

import json
import math
import time
import hashlib
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

SPINE_URL = "http://localhost:9116/append"

def spine_log(domain, action, data):
    try:
        requests.post(SPINE_URL, json={"domain": domain, "action": action, "data": data, "timestamp": time.time()}, timeout=2)
    except Exception:
        pass

# ── State ────────────────────────────────────────────────────────────

class CrossDomainState:
    def __init__(self):
        self.lock = threading.Lock()
        self.observations = []     # raw data points
        self.hypotheses = {}       # id → hypothesis
        self.correlations = []     # stored correlation results
        self.ooda_log = []         # OODA cycle log
        self._hid = 0

    def next_hid(self):
        self._hid += 1
        return f"hyp-{self._hid:04d}"

STATE = CrossDomainState()

# ── OODA Loop ───────────────────────────────────────────────────────

def ooda_observe(data_point):
    """Observe: ingest new data point."""
    with STATE.lock:
        obs = {
            "id": f"obs-{len(STATE.observations)+1:04d}",
            "data": data_point,
            "timestamp": time.time(),
        }
        STATE.observations.append(obs)
        if len(STATE.observations) > 1000:
            STATE.observations = STATE.observations[-1000:]
    STATE.ooda_log.append({"phase": "OBSERVE", "id": obs["id"], "ts": time.time()})
    spine_log("cross_domain", "observe", {"obs_id": obs["id"]})
    return obs

def ooda_orient():
    """Orient: summarize current observations."""
    with STATE.lock:
        obs = STATE.observations
    domains = {}
    for o in obs:
        d = o["data"].get("domain", "unknown")
        domains[d] = domains.get(d, 0) + 1
    orientation = {
        "total_observations": len(obs),
        "domains": domains,
        "recent": obs[-5:] if obs else [],
    }
    STATE.ooda_log.append({"phase": "ORIENT", "ts": time.time(), "summary": {k: v for k, v in orientation.items() if k != "recent"}})
    return orientation

def ooda_decide():
    """Decide: pick best hypothesis to test."""
    with STATE.lock:
        hyps = STATE.hypotheses
    if not hyps:
        return {"decision": "no hypotheses available", "action": "observe_more"}
    # Pick untested or lowest-confidence hypothesis
    best = None
    for h in hyps.values():
        if h.get("falsified"):
            continue
        if best is None or h.get("confidence", 0) < best.get("confidence", 0):
            best = h
    if best is None:
        return {"decision": "all hypotheses falsified", "action": "generate_new"}
    decision = {"decision": f"test hypothesis {best['id']}", "hypothesis": best, "action": "falsify"}
    STATE.ooda_log.append({"phase": "DECIDE", "ts": time.time(), "hypothesis_id": best["id"]})
    return decision

def ooda_act(hypothesis_id=None):
    """Act: attempt falsification of selected hypothesis."""
    with STATE.lock:
        if hypothesis_id and hypothesis_id in STATE.hypotheses:
            h = STATE.hypotheses[hypothesis_id]
        elif STATE.hypotheses:
            h = next(iter(STATE.hypotheses.values()))
        else:
            return {"action": "nothing to act on", "hypothesis_id": None}
    result = falsify_hypothesis(h["id"])
    STATE.ooda_log.append({"phase": "ACT", "ts": time.time(), "hypothesis_id": h["id"], "result": result.get("status")})
    return {"action": "falsify", "hypothesis_id": h["id"], "result": result}

# ── Correlation Scoring ──────────────────────────────────────────────

def poly_c_score(vec_a, vec_b):
    """
    poly_c = τ × ω × topo / 2√N
    
    τ  = cosine similarity (alignment)
    ω  = weight factor (domain proximity)
    topo = topological overlap (shared dimensions)
    N  = total dimension count
    """
    # Cosine similarity (τ)
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a * a for a in vec_a)) or 1e-10
    mag_b = math.sqrt(sum(b * b for b in vec_b)) or 1e-10
    tau = dot / (mag_a * mag_b)

    # Weight factor (ω) — based on magnitude correlation
    avg_a = sum(abs(a) for a in vec_a) / len(vec_a) if vec_a else 0
    avg_b = sum(abs(b) for b in vec_b) / len(vec_b) if vec_b else 0
    omega = 1.0 / (1.0 + abs(avg_a - avg_b))

    # Topological overlap (topo) — shared non-zero dimensions
    min_len = min(len(vec_a), len(vec_b))
    shared = sum(1 for i in range(min_len) if vec_a[i] != 0 and vec_b[i] != 0)
    topo = shared / max(len(vec_a), len(vec_b), 1)

    N = max(len(vec_a), len(vec_b), 1)
    score = tau * omega * topo / (2 * math.sqrt(N))

    return {
        "poly_c": round(score, 6),
        "tau": round(tau, 6),
        "omega": round(omega, 6),
        "topo": round(topo, 4),
        "N": N,
        "interpretation": "strong" if score > 0.1 else "moderate" if score > 0.01 else "weak",
    }

# ── Hypothesis Management ───────────────────────────────────────────

def generate_hypotheses():
    """Generate cross-domain hypotheses from observations."""
    with STATE.lock:
        obs = STATE.observations
    domains = {}
    for o in obs:
        d = o["data"].get("domain", "unknown")
        domains.setdefault(d, []).append(o)

    new_hyps = []
    domain_list = list(domains.keys())
    for i in range(len(domain_list)):
        for j in range(i + 1, len(domain_list)):
            d1, d2 = domain_list[i], domain_list[j]
            hid = STATE.next_hid()
            hyp = {
                "id": hid,
                "domains": [d1, d2],
                "statement": f"Correlation between {d1} and {d2} may indicate shared underlying mechanism",
                "confidence": 0.5,
                "falsified": False,
                "created": time.time(),
            }
            with STATE.lock:
                STATE.hypotheses[hid] = hyp
            new_hyps.append(hyp)

    spine_log("cross_domain", "hypotheses", {"count": len(new_hyps)})
    return new_hyps

def falsify_hypothesis(hypothesis_id):
    """Attempt to falsify a hypothesis."""
    with STATE.lock:
        h = STATE.hypotheses.get(hypothesis_id)
    if not h:
        return {"error": "hypothesis not found"}

    # Get observations for both domains
    obs_a = [o for o in STATE.observations if o["data"].get("domain") == h["domains"][0]]
    obs_b = [o for o in STATE.observations if o["data"].get("domain") == h["domains"][1]]

    if len(obs_a) < 2 or len(obs_b) < 2:
        return {"status": "insufficient_data", "hypothesis_id": hypothesis_id, "falsified": False}

    # Simple falsification: check if domain data moves in opposite directions
    vals_a = [o["data"].get("value", 0) for o in obs_a[-10:]]
    vals_b = [o["data"].get("value", 0) for o in obs_b[-10:]]
    
    trend_a = (vals_a[-1] - vals_a[0]) / max(abs(vals_a[0]), 1e-10)
    trend_b = (vals_b[-1] - vals_b[0]) / max(abs(vals_b[0]), 1e-10)
    
    # If trends are strongly opposite, falsification attempt succeeds
    falsified = (trend_a * trend_b < 0) and (abs(trend_a) > 0.5) and (abs(trend_b) > 0.5)
    
    with STATE.lock:
        STATE.hypotheses[hypothesis_id]["falsified"] = falsified
        if falsified:
            STATE.hypotheses[hypothesis_id]["confidence"] = max(0, STATE.hypotheses[hypothesis_id]["confidence"] - 0.3)
        else:
            STATE.hypotheses[hypothesis_id]["confidence"] = min(1.0, STATE.hypotheses[hypothesis_id]["confidence"] + 0.1)

    result = {
        "status": "falsified" if falsified else "survived",
        "hypothesis_id": hypothesis_id,
        "trend_a": round(trend_a, 4),
        "trend_b": round(trend_b, 4),
        "falsified": falsified,
    }
    spine_log("cross_domain", "falsify", result)
    return result

# ── HTTP Handler ─────────────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):
    def _json(self, code, data):
        body = json.dumps(data).encode()
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
            self._json(200, {"status": "alive", "service": "cross_domain", "port": 9114})
        elif self.path == "/hypotheses":
            with STATE.lock:
                hyps = {k: v for k, v in STATE.hypotheses.items()}
            self._json(200, {"hypotheses": hyps, "count": len(hyps)})
        elif self.path == "/orient":
            self._json(200, ooda_orient())
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/health":
            self._json(200, {"status": "alive", "service": "cross_domain", "port": 9114})
            return

        body = self._read_body()

        if self.path == "/observe":
            result = ooda_observe(body)
            self._json(200, result)
        elif self.path == "/correlate":
            vec_a = body.get("vector_a", [])
            vec_b = body.get("vector_b", [])
            if not vec_a or not vec_b:
                self._json(400, {"error": "both vector_a and vector_b required"})
                return
            score = poly_c_score(vec_a, vec_b)
            STATE.correlations.append(score)
            self._json(200, score)
        elif self.path == "/hypotheses":
            hyps = generate_hypotheses()
            self._json(200, {"generated": len(hyps), "hypotheses": hyps})
        elif self.path == "/falsify":
            hid = body.get("hypothesis_id")
            if not hid:
                # Decide + act
                dec = ooda_decide()
                if dec.get("hypothesis"):
                    hid = dec["hypothesis"]["id"]
                else:
                    self._json(200, dec)
                    return
            result = falsify_hypothesis(hid)
            self._json(200, result)
        elif self.path == "/ooda":
            # Full OODA cycle
            obs = ooda_observe(body.get("data", {}))
            orient = ooda_orient()
            decide = ooda_decide()
            act_result = ooda_act(decide.get("hypothesis", {}).get("id") if isinstance(decide.get("hypothesis"), dict) else None)
            self._json(200, {"observe": obs["id"], "orient": orient.get("domains", {}), "decide": decide.get("decision"), "act": act_result})
        else:
            self._json(404, {"error": "not found"})

    def log_message(self, *a):
        pass

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 9114), Handler)
    print("Cross-Domain Engine running on :9114")
    server.serve_forever()
