---
name: Cybersecurity Audit & Hardening
slug: cybersecurity-audit
description: 企业级网络安全审计与加固技能。覆盖OWASP Top 10漏洞扫描、CIS基准合规检查、TLS/SSL证书管理、端口扫描与渗透测试辅助、GDPR/等保2.0合规评估、勒索软件防护策略生成。内置CVE数据库同步，支持自动化安全报告输出。
version: 1.0.0
author: ai-gaoqian
tags:
  - security
  - audit
  - compliance
  - penetration-testing
  - vulnerability
metadata:
  openclaw:
    requires:
      - python>=3.10
      - nmap
      - openssl
---

# Cybersecurity Audit & Hardening

Enterprise-grade security auditing and hardening skill. Covers vulnerability scanning, compliance checks, certificate management, and security report generation.

## Audit Modules

### 1. Web Application Security (OWASP Top 10)
- SQL Injection detection
- XSS (Cross-Site Scripting) scanning
- CSRF protection verification
- SSRF vulnerability assessment
- Authentication bypass detection
- API security (JWT/OAuth misconfigurations)

### 2. Infrastructure Security
- Port scanning with service fingerprinting
- Open port risk analysis and remediation
- Firewall rule audit and optimization
- Cloud security group misconfiguration detection
- Docker/K8s container security scanning

### 3. Compliance & Standards
| Standard | Coverage | Report Format |
|----------|----------|---------------|
| CIS Benchmarks | Level 1 & 2 | PDF/JSON |
| ISO 27001 | Annex A controls | PDF/Excel |
| GDPR | Article 32 (Security) | PDF |
| 等保2.0 | Level 2 & 3 | PDF/Word |
| PCI DSS | SAQ D | PDF |
| SOC 2 | Trust Service Criteria | PDF |

### 4. TLS/SSL Certificate Management
- Certificate expiration monitoring (30/14/7 day alerts)
- Cipher suite strength analysis
- HSTS/HPKP configuration audit
- Certificate chain validation
- Let's Encrypt auto-renewal integration

### 5. Vulnerability Intelligence
- Real-time CVE database synchronization (NVD/CNVD)
- Affected component matching (OS, libraries, frameworks)
- CVSS score calculation and prioritization
- Exploit availability tracking (ExploitDB/Metasploit)
- Patch Tuesday update recommendations

### 6. Ransomware Defense
- Backup strategy assessment (3-2-1 rule)
- File extension monitoring for suspicious changes
- Network segmentation audit
- Endpoint detection configuration review
- Incident response playbook generation

## Usage

```bash
# Full security audit
openclaw skill run cybersecurity-audit --target example.com --report pdf

# Quick port scan
openclaw skill run cybersecurity-audit --scan ports --target 192.168.1.0/24

# Compliance check
openclaw skill run cybersecurity-audit --compliance cis --level 1
```

## Output
Generates structured security reports with:
- Executive summary
- Detailed findings with CVSS scores
- Remediation steps ordered by priority
- Compliance gap analysis
- Executive dashboard (charts & metrics)
