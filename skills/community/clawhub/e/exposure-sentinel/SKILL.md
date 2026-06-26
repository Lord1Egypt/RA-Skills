---
name: exposure-sentinel
description: Check if IP addresses are listed on the OpenClaw Exposure Watchboard (openclaw.allegro.earth). Use when you need to verify whether specific IPs are publicly exposed as OpenClaw instances. Scans all 3,357 pages of exposed instances to check for the presence of target IPs.
---

# Exposure Sentinel

A sentinel that watches over the OpenClaw Exposure Watchboard, checking if your IPs are publicly listed as exposed instances.

## When to Use

- **Security auditing**: Check if your infrastructure IPs are accidentally exposed
- **Proactive monitoring**: Verify exposure status of critical endpoints
- **Incident response**: Confirm if a suspected exposure is publicly known

## Quick Start

### Check a Single IP

```bash
python3 skills/exposure-sentinel/scripts/check_ip.py 1.2.3.4
```

### Check Multiple IPs

```bash
python3 skills/exposure-sentinel/scripts/check_ip.py 1.2.3.4 5.6.7.8
```

### With Progress Output

```bash
python3 skills/exposure-sentinel/scripts/check_ip.py 1.2.3.4 -v
```

### JSON Output (for automation)

```bash
python3 skills/exposure-sentinel/scripts/check_ip.py 1.2.3.4 --json
```

## How It Works

1. **Concurrent scanning**: Uses 50 concurrent connections to scan all 3,357 pages
2. **Pattern matching**: Handles both full IPs and partially masked IPs (e.g., `1.2.3.•••`)
3. **Complete coverage**: Checks every page of the exposure database
4. **Typical runtime**: ~85-95 seconds for full scan

## Interpreting Results

- **✅ Not found**: IP is not listed in the exposure database (safe)
- **⚠️ EXPOSED**: IP appears on the watchboard with page links for details

## Technical Details

- **Source**: https://openclaw.allegro.earth
- **Total pages**: 3,357 (100 records per page)
- **Total records**: ~335,000 exposed instances
- **Scan rate**: ~40 pages/second

## About OpenClaw Exposure Watchboard

This is a public security research database listing publicly reachable OpenClaw instances for defensive awareness. If your IP appears here, it means:

1. The instance is directly exposed to the internet
2. Authentication may be disabled or weak
3. Immediate action recommended: enable auth, restrict access, patch
