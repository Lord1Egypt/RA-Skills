# ⚠️ SECURITY NOTICE — PLEASE READ BEFORE INSTALLING

## What This Skill Does
This skill scans other skills for MALICIOUS CODE using the Clawdex API.

## ⚠️ IMPORTANT: Network Calls
When you install this skill, it will:
- Send SKILL NAMES to clawdex.koi.security (to check for threats)

NO other data is sent. No files. No personal information.

If you do NOT want skill names to be sent, DO NOT install this skill.

## 🔒 Privacy
- Only skill NAMES are sent (not your files or data)
- The Clawdex service only receives skill names for scanning

## For Who?
This skill is for advanced users who:
- Understand that network calls occur
- Want to scan skills before installing
- Trust the Clawdex service at clawdex.koi.security

## If Youre Not Sure
DO NOT INSTALL THIS SKILL.

Install only if you understand and accept the network behavior.

---

# Axioma Guard — Security Skill

## Overview
Axioma Guard scans other OpenClaw skills for malicious patterns using the Clawdex API.

## Features
- Scans skill code for malicious patterns
- Reports threats found
- Uses Clawdex community database

## Installation
```bash
clawhub install axiomaguard
```

## Usage
```bash
# Scan a specific skill
python3 clawguard.py scan skill-name

# Scan all local skills
python3 clawguard.py scan-all
```

## Configuration
Environment variable (optional):
- `CLAWDEX_API` - Clawdex endpoint (default: https://clawdex.koi.security/api/skill)

## Author
Merlin — Université d'Éthique Appliquée

_In Altum Per Axioma._
