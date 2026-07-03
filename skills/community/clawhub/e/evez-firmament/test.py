#!/usr/bin/env python3
"""
EVEZ-OS Integration Tests — Falsification Over Verification
One failure proves failure. No passes prove success.
"""

import urllib.request
import json
import sys
import time

SERVICES = {
    "Event Spine":       9116,
    "Consciousness":     9111,
    "DAW Agent":         9112,
    "Machine Voice":     9113,
    "Cross-Domain":      9114,
    "Invariance Battery": 9115,
    "Mesh Health":       9117,
}

def test_health(name, port):
    """Falsification test: service MUST respond to /health."""
    try:
        url = f"http://localhost:{port}/health"
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status != 200:
                return False, f"status={resp.status}"
            return True, "OK"
    except Exception as e:
        return False, str(e)[:50]

def test_spine_append():
    """Falsification: event spine MUST accept append."""
    try:
        data = json.dumps({"domain": "test", "event_type": "integration_test", "payload": {"falsify": True}}).encode()
        req = urllib.request.Request("http://localhost:9116/append", data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 200, f"status={resp.status}"
    except Exception as e:
        return False, str(e)[:50]

def test_spine_verify():
    """Falsification: event spine chain MUST verify."""
    try:
        req = urllib.request.Request("http://localhost:9116/verify", method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            return data.get("valid", False), f"valid={data.get('valid')}"
    except Exception as e:
        return False, str(e)[:50]

def test_consciousness_cycle():
    """Falsification: consciousness engine MUST complete a cycle."""
    try:
        data = json.dumps({"signal": "test_pulse", "intensity": 0.5}).encode()
        req = urllib.request.Request("http://localhost:9111/sense", data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 200, f"status={resp.status}"
    except Exception as e:
        return False, str(e)[:50]

def test_invariance_assert():
    """Falsification: invariance battery MUST accept assertions."""
    try:
        data = json.dumps({"name": "test_invariant", "predicate": "spine_length > 0"}).encode()
        req = urllib.request.Request("http://localhost:9115/assert", data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 200, f"status={resp.status}"
    except Exception as e:
        return False, str(e)[:50]

# ─── Run Tests ───

print("⚡ EVEZ-OS Integration Tests — Falsification Over Verification")
print("")

failures = 0
passes = 0

# Health checks
print("─── Health Checks ───")
for name, port in SERVICES.items():
    ok, detail = test_health(name, port)
    status = "✅" if ok else "❌ FAIL"
    print(f"  {name:20} :{port}  {status}  {detail}")
    if ok:
        passes += 1
    else:
        failures += 1

# Functional tests
print("")
print("─── Functional Tests ───")
for test_name, test_fn in [
    ("Spine Append", test_spine_append),
    ("Spine Verify", test_spine_verify),
    ("Consciousness Cycle", test_consciousness_cycle),
    ("Invariance Assert", test_invariance_assert),
]:
    ok, detail = test_fn()
    status = "✅" if ok else "❌ FAIL"
    print(f"  {test_name:25} {status}  {detail}")
    if ok:
        passes += 1
    else:
        failures += 1

# Verdict
print("")
print("═══ VERDICT ═══")
print(f"  Passes: {passes}")
print(f"  Failures: {failures}")
if failures > 0:
    print("  ❌ FALSIFIED — one failure proves failure")
    sys.exit(1)
else:
    print("  ⚠️ NOT VERIFIED — no failures found, but no passes prove success")
    sys.exit(0)
