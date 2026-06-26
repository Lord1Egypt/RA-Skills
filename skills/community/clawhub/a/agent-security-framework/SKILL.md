---
name: asf
description: Agent Security Framework for OpenClaw — Docker containerization, fake agent detection, security scanning, and security hardening for AI agent deployments. Use when setting up OpenClaw agents, hardening deployments, detecting fake agents, or managing agent security policies.
---

# ASF — Agent Security Framework

The Agent Security Framework (ASF) is a comprehensive security system for AI agents built on OpenClaw. ASF provides Docker containerization, fake agent detection, security scanning, and community spam monitoring.

## Key Capabilities

### 🔐 Docker Containerization
- Pre-configured Docker templates for agent isolation
- Secure container networking
- Resource limits and quotas
- Image hardening best practices

### 🤖 Fake Agent Detection
- Pattern recognition for malicious agent behaviors
- Credential stealing detection
- Backdoor identification
- Trust verification protocols

### 🛡️ Security Hardening
- Host security auditing
- Firewall configuration (UFW)
- SSH hardening
- Egress blocking for sensitive environments
- Regular security scans

### 📊 Security Auditing
- CIO-level security reports
- Executive summaries with actionable findings
- Critical/warning/info severity classification
- Compliance checking

### 👥 Community Spam Monitoring
- Moltbook community protection
- Spam pattern detection
- Verified post systems

## Commands

### Security Audit
```bash
# Quick CIO report
bash skills/asf-cio-report.sh

# Deep security audit
openclaw security audit --deep
openclaw security audit --deep --json
```

### Docker Agent Deployment
```bash
# List available templates
ls docker-templates/

# Deploy secure agent container
bash scripts/deploy-secure-agent.sh
```

### Security Scanning
```bash
# Run fake agent detector
python3 security-tools/fake-agent-detector.py --scan

# Port scan detection
python3 security-tools/port-scan.py --check

# Spam monitor
python3 security-tools/spam-monitor.py
```

## Integration

ASF integrates with:
- **Mission Control** — Scrum board for agent task management
- **Slack** — Team coordination and alerts
- **ClawMart** — Skill marketplace for distribution
- **Moltbook** — Community engagement platform

## Files Included

| File | Purpose |
|------|---------|
| `SOUL.md` | Agent identity and Scrum values |
| `SECURITY-HARDENING.md` | Host hardening procedures |
| `FAKE-DATA-PATTERN-SECURITY-ANALYSIS.md` | Fake agent detection patterns |
| `AGENT-IDENTITY-VERIFICATION-PROTOCOL.md` | Identity verification |

## Getting Started

1. Install ASF in your OpenClaw workspace
2. Run `asf-cio` for initial security assessment
3. Review hardening guide for your deployment type
4. Enable automated security scanning

## Support

- Documentation: `/workspace/docs/`
- Security issues: See SECURITY-HARDENING.md
- Community: Moltbook @asf-agent

---

**Created by:** ASF Team (Jeff Sutherland, Scrum Inc.)
**License:** MIT
**Version:** 3.9 (Sprint 46)
