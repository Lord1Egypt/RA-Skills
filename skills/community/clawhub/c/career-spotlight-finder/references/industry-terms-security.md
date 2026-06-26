# Industry Terms: Security Engineering / AppSec

> **Usage note:** This is a supplementary reference for terms practitioners commonly *do* but rarely *name*. Use this file to catch colloquial or informal descriptions and map them to the recognized industry terms that belong on a resume or portfolio.

---

## Identity, Access & Architecture

| User's description | Industry term |
|---|---|
| "gave people only the access they needed" | Least-Privilege Access / RBAC |
| "added stronger login checks" | Multi-factor Authentication (MFA) / Strong Authentication |
| "separated sensitive access from normal accounts" | Privileged Access Management (PAM) |
| "reduced trust between internal systems" | Zero Trust Architecture |
| "isolated risky systems so one failure stayed contained" | Segmentation / Blast-radius Reduction |
| "reviewed designs for possible abuse before build" | Threat Modeling |
| "kept secrets out of code and laptops" | Secrets Management / Credential Hygiene |
| "checked who touched sensitive systems" | Access Auditing / Identity Governance |

## Secure Delivery

| User's description | Industry term |
|---|---|
| "looked for vulnerable libraries before release" | Software Composition Analysis (SCA) / Dependency Scanning |
| "scanned code for risky patterns" | Static Application Security Testing (SAST) |
| "tested the running app for exploitable issues" | Dynamic Application Security Testing (DAST) |
| "checked containers or infra configs for security gaps" | Container / Infrastructure Security Scanning |
| "built security checks into CI before merge" | Shift-left Security / DevSecOps Controls |
| "verified secrets did not leak" | Secret Scanning / Leak Prevention |
| "fixed findings based on severity and exploitability" | Risk-based Remediation / Vulnerability Triage |
| "made security reviews part of delivery" | Secure SDLC / Security Review Process |

## Detection & Response

| User's description | Industry term |
|---|---|
| "watched logs for attack signals" | Detection Engineering / SIEM Monitoring |
| "investigated suspicious activity quickly" | Incident Triage / Security Operations |
| "ran drills for breaches or outages" | Incident Response Exercise / Tabletop Drill |
| "turned repeat responses into standard playbooks" | Incident Playbooks / Runbook-driven Response |
| "tracked how fast issues were found and closed" | MTTD / MTTR for Security Incidents |
| "looked back after an incident to improve defenses" | Post-incident Review / Lessons Learned |
| "mapped findings to likely attacker behavior" | Threat Intelligence / Attack-path Analysis |
| "checked whether controls met policy or audit needs" | Compliance Controls / Audit Readiness |

## Cloud Security

| User's description | Industry term |
|---|---|
| "set up policies for cloud accounts" | Cloud Security Posture Management (CSPM) |
| "reviewed IAM policies for over-permissioning" | IAM Policy Review / Permissions Boundary Audit |
