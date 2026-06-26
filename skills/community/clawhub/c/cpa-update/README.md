# CPA Update - Secure CLI Proxy API Maintenance

## Overview
This skill provides a secure and reliable workflow for updating and maintaining CLI Proxy API (CPA) deployments, specifically designed for Docker installations.

## Problem Solved
Official CPA containers have common issues that this skill addresses:
- **Auth directory permission problems**: Container's `/root/.cli-proxy-api` directory permissions prevent proper OAuth token storage
- **Read-only config mounting**: Default mounting restricts WebUI configuration modifications  
- **Version compatibility issues**: Direct upgrades between versions may lose authentication data
- **Lack of standardized update process**: Users need to manually handle backup, testing, and rollback steps

## Features
- ✅ Complete auth directory permission fix
- ✅ Writable config file mounting (supports WebUI modifications)
- ✅ Standardized backup → test → production → rollback workflow
- ✅ Automated baseline recording and version verification
- ✅ Safe configuration changes without service interruption

## Usage
1. Install via ClawHub: `clawhub install cpa-update`
2. Follow the detailed workflow in `SKILL.md`
3. Execute updates safely with built-in rollback capability

## Directory Structure
```
cpa-update/
├── SKILL.md          # Complete update workflow documentation
├── README.md         # This file
└── (no sensitive data included)
```

## Security Guarantees
- All operations include automatic backup before changes
- New versions are tested on alternate ports before production deployment
- Full rollback support to any previous version
- Persistent storage of configuration and authentication files
- Config files mounted in writable mode (fixed from previous read-only issues)

## Version
2.2.1

## Tags
cpa, cli-proxy-api, maintenance, security, docker, update