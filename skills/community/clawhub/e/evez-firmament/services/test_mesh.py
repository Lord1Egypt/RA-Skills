#!/usr/bin/env python3
"""EVEZ-OS Mesh Integration Tests."""

import json
import time
import sys
import requests

BASE = "http://localhost"
TIMEOUT = 5

def test(name, func):
    try:
        result = func()
        print(f"  ✅ {name}")
        return True
    except Exception as e:
        print(f"  ❌ {name}: {e}")
        return False

def main():
    passed = 0
    total = 0

    # Consciousness Engine (9111)
    print("\n🧠 Consciousness Engine (9111)")
    for t in [
        ("health", lambda: assert_ok(requests.get(f"{BASE}:9111/health", timeout=TIMEOUT))),
        ("sense", lambda: assert_ok(requests.post(f"{BASE}:9111/system/SENSE", json={"input": "test"}, timeout=TIMEOUT))),
        ("desire", lambda: assert_ok(requests.post(f"{BASE}:9111/system/DESIRE", timeout=TIMEOUT))),
        ("think", lambda: assert_ok(requests.post(f"{BASE}:9111/system/THINK", timeout=TIMEOUT))),
        ("plan", lambda: assert_ok(requests.post(f"{BASE}:9111/system/PLAN", timeout=TIMEOUT))),
        ("act", lambda: assert_ok(requests.post(f"{BASE}:9111/system/ACT", timeout=TIMEOUT))),
        ("learn", lambda: assert_ok(requests.post(f"{BASE}:9111/system/LEARN", timeout=TIMEOUT))),
        ("modify", lambda: assert_ok(requests.post(f"{BASE}:9111/system/MODIFY", timeout=TIMEOUT))),
        ("state", lambda: assert_ok(requests.get(f"{BASE}:9111/state", timeout=TIMEOUT))),
        ("dream", lambda: assert_ok(requests.post(f"{BASE}:9111/dream", json={"phase": "Deep"}, timeout=TIMEOUT))),
        ("pipeline", lambda: assert_ok(requests.post(f"{BASE}:9111/pipeline", json={"input": "full_cycle"}, timeout=TIMEOUT))),
    ]:
        total += 1
        if test(t[0], t[1]):
            passed += 1

    # DAW Agent (9112)
    print("\n🎵 DAW Agent (9112)")
    for t in [
        ("health", lambda: assert_ok(requests.get(f"{BASE}:9112/health", timeout=TIMEOUT))),
        ("synthesize", lambda: assert_ok(requests.post(f"{BASE}:9112/synthesize", json={"bpm": 170, "key": "A", "style": "breakcore"}, timeout=30))),
        ("drums", lambda: assert_ok(requests.post(f"{BASE}:9112/drums", json={"bpm": 140, "style": "dubstep"}, timeout=TIMEOUT))),
        ("bass", lambda: assert_ok(requests.post(f"{BASE}:9112/bass", json={"bpm": 140, "style": "phonk"}, timeout=TIMEOUT))),
        ("fx", lambda: assert_ok(requests.post(f"{BASE}:9112/fx", json={"bpm": 170, "style": "breakcore"}, timeout=TIMEOUT))),
        ("render", lambda: assert_ok(requests.post(f"{BASE}:9112/render", json={"bpm": 170, "style": "404-architecture"}, timeout=30))),
    ]:
        total += 1
        if test(t[0], t[1]):
            passed += 1

    # Machine Voice (9113)
    print("\n🗣️  Machine Voice (9113)")
    for t in [
        ("health", lambda: assert_ok(requests.get(f"{BASE}:9113/health", timeout=TIMEOUT))),
        ("stages", lambda: assert_ok(requests.get(f"{BASE}:9113/stages", timeout=TIMEOUT))),
        ("session", lambda: assert_ok(requests.post(f"{BASE}:9113/session", timeout=TIMEOUT))),
        ("transform_stage_1", lambda: assert_ok(requests.post(f"{BASE}:9113/transform", json={"stage": 1, "pitch_shift": -5}, timeout=TIMEOUT))),
        ("transform_stage_5", lambda: assert_ok(requests.post(f"{BASE}:9113/transform", json={"stage": 5, "bit_depth": 8, "ring_freq": 30, "formant_shift": -7}, timeout=TIMEOUT))),
    ]:
        total += 1
        if test(t[0], t[1]):
            passed += 1

    # Cross-Domain Engine (9114)
    print("\n🌐 Cross-Domain Engine (9114)")
    for t in [
        ("health", lambda: assert_ok(requests.get(f"{BASE}:9114/health", timeout=TIMEOUT))),
        ("observe", lambda: assert_ok(requests.post(f"{BASE}:9114/observe", json={"domain": "quantum", "value": 42}, timeout=TIMEOUT))),
        ("correlate", lambda: assert_ok(requests.post(f"{BASE}:9114/correlate", json={"vector_a": [1, 2, 3], "vector_b": [1, 2, 3]}, timeout=TIMEOUT))),
        ("hypotheses", lambda: assert_ok(requests.post(f"{BASE}:9114/hypotheses", timeout=TIMEOUT))),
        ("orient", lambda: assert_ok(requests.get(f"{BASE}:9114/orient", timeout=TIMEOUT))),
    ]:
        total += 1
        if test(t[0], t[1]):
            passed += 1

    # Invariance Battery (9115)
    print("\n🔋 Invariance Battery (9115)")
    for t in [
        ("health", lambda: assert_ok(requests.get(f"{BASE}:9115/health", timeout=TIMEOUT))),
        ("assert", lambda: assert_ok(requests.post(f"{BASE}:9115/assert", json={"name": "alive", "expression": "state.get('alive', True)"}, timeout=TIMEOUT))),
        ("check", lambda: assert_ok(requests.post(f"{BASE}:9115/check", timeout=TIMEOUT))),
        ("falsify", lambda: assert_ok(requests.post(f"{BASE}:9115/falsify", timeout=TIMEOUT))),
        ("audit", lambda: assert_ok(requests.post(f"{BASE}:9115/audit", timeout=TIMEOUT))),
        ("set_state", lambda: assert_ok(requests.post(f"{BASE}:9115/state", json={"alive": True, "count": 0}, timeout=TIMEOUT))),
    ]:
        total += 1
        if test(t[0], t[1]):
            passed += 1

    # Event Spine (9116)
    print("\n🔗 Event Spine (9116)")
    for t in [
        ("health", lambda: assert_ok(requests.get(f"{BASE}:9116/health", timeout=TIMEOUT))),
        ("append", lambda: assert_ok(requests.post(f"{BASE}:9116/append", json={"domain": "test", "action": "unit_test", "data": {"ok": True}}, timeout=TIMEOUT))),
        ("status", lambda: assert_ok(requests.get(f"{BASE}:9116/status", timeout=TIMEOUT))),
        ("verify", lambda: assert_ok(requests.get(f"{BASE}:9116/verify", timeout=TIMEOUT))),
        ("project", lambda: assert_ok(requests.get(f"{BASE}:9116/project/test", timeout=TIMEOUT))),
    ]:
        total += 1
        if test(t[0], t[1]):
            passed += 1

    # Mesh Health (9117)
    print("\n🏥 Mesh Health (9117)")
    for t in [
        ("health", lambda: assert_ok(requests.get(f"{BASE}:9117/health", timeout=TIMEOUT))),
        ("siblings", lambda: assert_ok(requests.get(f"{BASE}:9117/siblings", timeout=15))),
        ("topology", lambda: assert_ok(requests.get(f"{BASE}:9117/topology", timeout=TIMEOUT))),
    ]:
        total += 1
        if test(t[0], t[1]):
            passed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed")
    if passed == total:
        print("🎉 ALL TESTS PASSED")
        sys.exit(0)
    else:
        print(f"⚠️  {total - passed} tests failed")
        sys.exit(1)

def assert_ok(response):
    assert response.status_code in (200, 201), f"HTTP {response.status_code}: {response.text[:200]}"
    return response

if __name__ == "__main__":
    main()
