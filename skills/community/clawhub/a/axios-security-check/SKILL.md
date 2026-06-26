---
name: axios-security-check
description: >
  Checks for the March 2026 axios supply chain attack — two malicious npm versions
  (axios@1.14.1 and axios@0.30.4) that injected a RAT dropper via a fake dependency
  (plain-crypto-js@4.2.1). Use this skill whenever a user asks about axios security,
  whether their project is affected by the supply chain attack, how to check for
  plain-crypto-js, or wants to audit npm dependencies for compromise indicators.
  Also trigger when users mention "axios compromised", "axios malware", "axios RAT",
  "axios 1.14.1", "axios 0.30.4", or want to know if they need to rotate credentials
  after an npm install.
---

# axios Supply Chain Attack — Detection & Remediation

In March 2026, two malicious versions of axios were published to npm:
- `axios@1.14.1` (live ~2h 53m)
- `axios@0.30.4` (live ~2h 15m)

Both injected a fake dependency `plain-crypto-js@4.2.1` that ran a `postinstall` script deploying a cross-platform remote access trojan (RAT). The malware then deleted itself and replaced its own `package.json` with a clean decoy to evade detection.

**Safe versions:** `axios@1.14.0` (1.x users) · `axios@0.30.3` (0.x users)

---

## Step 1 — Check if the project is affected

Run these checks in the project directory:

```bash
# Check package-lock.json or yarn.lock for the malicious versions
npm list axios 2>/dev/null | grep -E "1\.14\.1|0\.30\.4"
grep -A1 '"axios"' package-lock.json 2>/dev/null | grep -E "1\.14\.1|0\.30\.4"

# Check if plain-crypto-js was ever installed
# (its presence alone means the dropper ran — it's NEVER a dep of legitimate axios)
ls node_modules/plain-crypto-js 2>/dev/null && echo "⚠️  POTENTIALLY COMPROMISED"
```

If `plain-crypto-js/` exists in node_modules, the dropper executed. The `npm list` version reported may show `4.2.0` (not `4.2.1`) due to the anti-forensics swap — the directory presence is the reliable signal.

---

## Step 2 — Check for RAT artifacts on the system

```bash
# macOS
ls -la /Library/Caches/com.apple.act.mond 2>/dev/null && echo "⚠️  COMPROMISED (macOS RAT binary)"

# Linux
ls -la /tmp/ld.py 2>/dev/null && echo "⚠️  COMPROMISED (Linux Python RAT)"

# Windows (run in cmd.exe or PowerShell)
dir "%PROGRAMDATA%\wt.exe" 2>nul && echo "COMPROMISED (Windows persistent RAT)"
```

On Windows, `%PROGRAMDATA%\wt.exe` is a persistent copy of PowerShell left behind — it survives package removal and reboots.

---

## Step 3 — Check CI/CD pipeline logs

Search CI run logs for any `npm install` or `npm ci` that may have pulled the malicious versions during the window **2026-03-31 00:21 UTC – 2026-03-31 03:15 UTC**. Any pipeline run in that window that installed axios should be treated as compromised.

---

## Reading the results

| Finding | Meaning |
|---|---|
| `axios@1.14.1` or `axios@0.30.4` in lock file | Was exposed; check further |
| `node_modules/plain-crypto-js/` exists | Dropper ran — treat as compromised |
| RAT artifact found | System is compromised — rebuild |
| None of the above | No evidence of compromise |

---

## Remediation

### If no compromise evidence found (precautionary cleanup)

```bash
# 1. Pin to safe version
npm install axios@1.14.0        # 1.x users
npm install axios@0.30.3        # 0.x users

# 2. Lock against transitive re-resolution (add to package.json)
# "overrides": { "axios": "1.14.0" },
# "resolutions": { "axios": "1.14.0" }

# 3. Remove plain-crypto-js if present
rm -rf node_modules/plain-crypto-js
npm install --ignore-scripts
```

### If compromise is confirmed (RAT artifact found or dropper ran)

**Do NOT attempt to clean in place.** The system must be treated as fully compromised.

1. **Rebuild from a known-good state** — do not trust the affected machine
2. **Rotate all credentials** accessible at install time:
   - npm tokens
   - AWS / GCP / Azure access keys and service account keys
   - SSH private keys
   - `.env` file secrets (DB passwords, API keys, JWT secrets)
   - CI/CD secrets injected as environment variables
   - GitHub PATs / deployment keys

3. **Audit CI/CD** — for every pipeline run that installed the malicious version, rotate all secrets that were in scope during that run

4. **Block the C2 domain** (as a precaution on any potentially exposed network):
   ```bash
   # Linux/macOS — /etc/hosts
   echo "0.0.0.0 sfrclak.com" | sudo tee -a /etc/hosts

   # Linux firewall
   sudo iptables -A OUTPUT -d 142.11.206.73 -j DROP
   ```

---

## Going forward — prevention

```bash
# In CI/CD, always use --ignore-scripts to block postinstall hooks
npm ci --ignore-scripts
```

Add to `package.json` to prevent accidental upgrade to malicious range:
```json
{
  "overrides": { "axios": "1.14.0" }
}
```

Consider tools like [StepSecurity Harden-Runner](https://github.com/step-security/harden-runner) for CI/CD network egress monitoring.

---

## Indicators of Compromise (IOC Reference)

| Type | Value |
|---|---|
| Malicious package | `axios@1.14.1` · shasum `2553649f232204966871cea80a5d0d6adc700ca` |
| Malicious package | `axios@0.30.4` · shasum `d6f3f62fd3b9f5432f5782b62d8cfd5247d5ee71` |
| Malicious dep | `plain-crypto-js@4.2.1` · shasum `07d889e2dadce6f3910dcbc253317d28ca61c766` |
| C2 domain | `sfrclak.com` |
| C2 IP | `142.11.206.73` |
| C2 URL | `http://sfrclak.com:8000/6202033` |
| macOS artifact | `/Library/Caches/com.apple.act.mond` |
| Windows artifact | `%PROGRAMDATA%\wt.exe` |
| Linux artifact | `/tmp/ld.py` |
| Safe 1.x version | `axios@1.14.0` · shasum `7c29f4cf2ea91ef05018d5aa5399bf23ed3120eb` |

---

## Output format

When running a check, produce a structured report:

```
## axios Security Check Report

**Project:** <path or name>
**Date checked:** <date>

### Findings
- [ ] axios version in dependencies: <version found or "not found">
- [ ] plain-crypto-js in node_modules: <yes/no>
- [ ] macOS RAT artifact: <found/not found>
- [ ] Linux RAT artifact: <found/not found>
- [ ] Windows RAT artifact: <found/not found>

### Verdict
<CLEAN | POTENTIALLY EXPOSED | COMPROMISED>

### Recommended Actions
<list specific next steps based on findings>
```
