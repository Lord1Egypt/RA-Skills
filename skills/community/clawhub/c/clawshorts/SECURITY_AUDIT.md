# ClawShorts — Security Audit Report

**Audited by:** cisco/software-security tile + manual review
**Date:** 2026-04-01
**Version:** 1.3.0
**Files audited:** SKILL.md, scripts/clawshorts.sh, scripts/clawshorts-daemon.py, scripts/clawshorts_db.py, src/clawshorts/cli.py, src/clawshorts/validators.py, src/clawshorts/detection.py

---

## Severity Scale

| Rating | Meaning |
|--------|---------|
| 🔴 CRITICAL | Remote code execution, credential exposure, data destruction |
| 🟠 HIGH | Significant exploit path, network-level attack |
| 🟡 MEDIUM | Limited impact, requires local access or user cooperation |
| 🟢 LOW | Hardening opportunity, defense-in-depth |

---

## Findings

### 🟡 MEDIUM — No restriction to private IP ranges

**File:** `src/clawshorts/validators.py`

`validate_ipv4()` only checks that each octet is 0–255. It does **not** verify the IP is in a private range (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16). A user could accidentally add a public IP and the system would attempt ADB connections to it.

**Exploit scenario:** User mistypes IP as `192.168.1.999` → rejected by octet check. But `192.168.1.1` (a router admin panel) would be accepted and the daemon would attempt ADB connections to it.

**Impact:** Limited — ADB connections to unintended local devices. No remote exploit.

**Recommendation:** Add private IP validation:

```python
import ipaddress

def validate_ipv4(ip: str) -> bool:
    if not isinstance(ip, str):
        return False
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback
    except ValueError:
        return False
```

---

### 🟡 MEDIUM — ADB has no authentication (inherent to ADB, documented)

**File:** `clawshorts.sh` (install instructions)

ADB debugging on Fire TV has **no built-in authentication**. Anyone on the same network who enables ADB debugging can connect to the device without a password.

**This is an ADB design limitation, not a code defect.** The install instructions warn users to only enable ADB on trusted home networks.

**Recommendation (documentation):** Add a prominent warning in SKILL.md:
> ⚠️ **Security:** ADB has no authentication. Only enable ADB Debugging on a trusted, password-protected home network. Never on public WiFi.

---

### 🟡 MEDIUM — No confirmation before force-stopping YouTube

**File:** `scripts/clawshorts-daemon.py` (`_force_stop_youtube`)

When the daily limit is reached, YouTube is force-stopped with `am force-stop` with no user notification beyond a log line. The user who configured the device implicitly consented, but there's no:

- OS notification to the user before stopping
- Configurable grace period
- Dry-run / audit mode

**Impact:** Abrupt app termination with no warning on-screen.

**Recommendation:** Add a configurable grace/warning period (e.g., show a 30-second warning notification on the TV before stopping). This would require a Fire TV notification API, which ADB can send via `am start -a android.intent.action.WARNING`.

---

### 🟢 LOW — `cmd_stop` uses broad `pkill -f` pattern

**File:** `scripts/clawshorts.sh` (`cmd_stop`)

```bash
pids=$(pgrep -f "clawshorts-daemon" 2>/dev/null || true)
```

`pgrep -f` matches against the full command line. A process whose working directory or args contain the string "clawshorts-daemon" could be matched. Unlikely to cause issues in practice.

**Recommendation:** Use a more specific PID file approach:

```bash
echo "$pids" > "$STATE_DIR/daemon.pid"
# Stop: kill $(cat "$STATE_DIR/daemon.pid")
```

---

### 🟢 LOW — `cmd_stop` sends SIGKILL after 2s without checking if graceful shutdown succeeded

**File:** `scripts/clawshorts.sh` (`cmd_stop`)

```bash
kill -TERM $pids 2>/dev/null || true
sleep 2
pkill -f "clawshorts-daemon" 2>/dev/null || true
```

Always sends SIGKILL after 2 seconds regardless of whether the process exited cleanly. Minor — the daemon handles SIGTERM gracefully, but there's no check for actual exit.

**Recommendation:** Check if process exited before SIGKILL:

```bash
kill -TERM $pids 2>/dev/null || true
sleep 2
for pid in $pids; do
    kill -0 $pid 2>/dev/null && kill -9 $pid
done
```

---

### 🟢 LOW — No automatic cleanup of stale UI XML files

**File:** `scripts/clawshorts-daemon.py` (`_dump_ui`)

Temporary UI XML files are downloaded to `~/.clawshorts/ui-*.xml` and read back, but never deleted. Over many days of polling, these accumulate.

**Impact:** Low — one file per IP per daemon session, rarely restarted.

**Recommendation:** Add cleanup on daemon startup or on file read failure.

---

### 🟡 MEDIUM — Daemon runs as user with no resource limits

**File:** `clawshorts-daemon.sh`, LaunchAgent plist

The daemon has no CPU, memory, or file descriptor limits set in the LaunchAgent plist. A bug causing an infinite loop could consume resources.

**Impact:** Denial of service on the host machine.

**Recommendation:** Add to plist:

```xml
<key>HardResourceLimits</key>
<dict>
    <key>CPULimit</key>
    <integer>10</integer>
</dict>
```

---

## ✅ Security Strengths

| Area | Status |
|------|--------|
| Path traversal in UI dump | ✅ Protected — validates resolved path stays within STATE_DIR |
| SQL injection | ✅ Parameterized queries throughout |
| Command injection in ADB calls | ✅ Commands passed as list args, not shell strings |
| Credential exposure | ✅ No credentials stored; no secrets in code |
| Signal handling | ✅ Clean SIGINT/SIGTERM handlers |
| File permissions on DB | ✅ `os.chmod(DB_PATH, 0o600)` restricts SQLite file |
| Log rotation | ✅ RotatingFileHandler with 1MB cap + 3 backups |
| Input validation on IP | ✅ IPv4 format validated before ADB calls |
| LaunchAgent plist | ✅ User-level only, no system-wide modifications |
| No remote fetch | ✅ No `curl`/`wget` to external URLs in daemon |

---

## Summary

| Severity | Count |
|----------|-------|
| 🔴 CRITICAL | 0 |
| 🟠 HIGH | 0 |
| 🟡 MEDIUM | 4 |
| 🟢 LOW | 3 |

**Overall:** The codebase is well-structured with security fundamentals in place — no injection vulnerabilities, no credential leaks, no path traversal. The main risks are **configuration/environment** rather than code defects: ADB's inherent lack of auth, and the ability to point the tool at unintended IPs on the local network.

**Top 3 fixes to implement:**
1. Add private IP validation to `validate_ipv4()`
2. Add explicit ADB network trust warning to SKILL.md
3. Add a grace-period notification before force-stopping YouTube
