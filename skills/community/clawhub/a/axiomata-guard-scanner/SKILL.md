---
name: axiomata-guard-scanner
description: "Axiomata Guard Scanner — Universal security scanner for any OpenClaw skill. Use when: (1) scanning a skill for security threats before installation, (2) checking for malicious code patterns (C2, rootkits, bootkits, chains), (3) validating skill safety with multiple vaccines, (4) any security audit of OpenClaw skills. This skill provides: VAX-001 (ClawHub malicious), VAX-027 (C2/exfiltration), VAX-028 (cross-vector chains), VAX-029 (rootkit/bootkit), VAX-030 (package ecosystem). Works with any agent — fully impersonal."
version: "1.0.0"
---

# Axiomata Guard Scanner

> Universal OpenClaw skill security scanner
> Impersonal — works for any agent

---

## Description

Axiomata Guard Scanner protects OpenClaw agents by scanning skills for security threats. It uses multiple "vaccines" (detection engines) to identify malicious patterns before installation.

**Trigger:** Before installing any skill, especially from ClawHub.

---

## Security Layers

### Layer 1: ClawHub Malicious Pattern Check (VAX-001)

```
Checks for known malicious patterns:
- Malicious binary downloads (openclawcli.zip)
- RCE via glot.io snippets
- Malware via GitHub releases
- Password-protected archives
```

### Layer 2: C2 & Data Exfiltration Detection (VAX-027)

```
Detects command & control infrastructure:
- Suspicious DNS lookups
- Discord/Telegram webhooks
- Bit.ly / short URL redirects
- Exfiltration patterns
```

### Layer 3: Cross-Vector Attack Chain (VAX-028)

```
Correlates findings from other vaccines:
- Multiple attack vectors
- Chain escalation patterns
- Combined threat assessment
```

### Layer 4: Rootkit & Bootkit Detection (VAX-029)

```
Detects kernel-level threats:
- System manipulation patterns
- Driver injection
- UEFI threats
```

### Layer 5: Package Ecosystem Attacks (VAX-030)

```
Detects package-level attacks:
- typosquatting
- dependency confusion
- malicious packages
```

---

## Usage

### Scan a skill file

```bash
python3 scripts/guard_scanner.py --file <skill-path>
```

### Scan skill code directly

```bash
python3 scripts/guard_scanner.py --code "<skill code>"
```

### JSON output

```bash
python3 scripts/guard_scanner.py --file <skill-path> --json
```

---

## Output Format

```json
{
  "scanner": "Axiomata Guard Scanner",
  "version": "1.0.0",
  "skill_name": "...",
  "global_threat_level": "CLEAN | LOW | MEDIUM | HIGH | CRITICAL",
  "global_score": 0-300,
  "decision": "APPROVE | WARN | NEUTRALIZE | ISOLATE",
  "triggered_vaccines": [...],
  "summary": {...}
}
```

---

## Threat Levels

| Level | Score | Action |
|-------|-------|--------|
| CLEAN | 0 | APPROVE |
| LOW | 1-19 | APPROVE with monitoring |
| MEDIUM | 20-49 | WARN — manual review |
| HIGH | 50-79 | NEUTRALIZE |
| CRITICAL | 80+ | ISOLATE immediately |

---

_In Altum Per Security._
Axiomata Guard Scanner v1.0.0