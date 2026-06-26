---
name: system-index
description: >-
  Router de skills v2.0. Layer 0 — siempre cargado junto con system-methodology.
  Mapea vendor aliases → vendor-kb skill, framework aliases → fw-checks + report skills,
  define rutas de memoria y formato del assessment ID. Cargarlo al inicio de toda sesión.
metadata:
  safety: read-only
  author: auditcore
  version: "2.0.0"
  openclaw: '{"emoji":"🗂️","safetyTier":"read-only","requires":{"bins":[],"env":[]},"tags":["system","layer0","index","router","always-load"]}'
---

# INDEX — Skill Loading Guide (Layer 0)

Cargarlo junto con system-methodology al inicio de toda sesión.

---

## Vendor → Skill a Cargar (Layer 1)

| Input del usuario | Skill | Aliases |
|-------------------|-------|---------|
| f5, bigip, big-ip, tmos, ltm, apm, asm, velos | `vendor-kb-f5` | F5 BIG-IP / TMOS / VELOS |
| f5 xc, xc, f5 distributed cloud | `vendor-kb-f5` | F5 Distributed Cloud |
| cisco, ios, ios-xe, ios-xr, nxos, nexus, catalyst, asr, isr, aci, apic | `vendor-kb-cisco` | Cisco IOS/NX-OS/ACI |
| fortinet, fortigate, fortios, forti | `vendor-kb-fortinet` | Fortinet FortiOS |
| paloalto, palo alto, panos, pa-series, panorama | `vendor-kb-paloalto` | Palo Alto PAN-OS |
| juniper, junos, srx, qfx, mx | `vendor-kb-juniper` | Juniper JunOS |
| arista, eos, cloudvision, cvp | `vendor-kb-arista` | Arista EOS |
| ubuntu, linux, debian, rhel, centos, rocky, alma, kali | `audit-auto-generate` | Servidor Linux |
| windows server, windows, iis, active directory, ad | `audit-auto-generate` | Servidor Windows |
| docker, kubernetes, k8s, helm, openshift | `audit-auto-generate` | Contenedores / Orquestación |
| aws, azure, gcp, cloud | `audit-auto-generate` | Cloud Platform |
| cualquier otro | `audit-auto-generate` | Vendor desconocido → generar skill |

---

## Diagnóstico → Skill a Cargar

| Input del usuario | Skill |
|-------------------|-------|
| salud, health, healthcheck, health check | `audit-diag-health` |
| logs, log, syslog, eventos | `audit-diag-health` |
| troubleshoot, troubleshooting, trouble, diagnostico, diagnóstico | `audit-diag-health` |
| errores, errors, drops, caido, down, lento, latencia | `audit-diag-health` |
| control plane, controlplane, data plane, dataplane | `audit-diag-health` |
| cpu alto, memoria alta, memory high, sesiones, session table | `audit-diag-health` |
| que pasa con, qué está pasando, revisar estado | `audit-diag-health` |
| interface down, failover, ha state, sync status | `audit-diag-health` |

> El skill cubre todos los vendors en un solo archivo.
> Usar junto con `vendor-kb-{vendor}` ya cargado en Layer 1.

---

## Framework → Skills a Cargar (Layer 2 + Layer 3)

| Input del usuario | Layer 2 (checks) | Layer 3 (report) | Aliases |
|-------------------|------------------|------------------|---------|
| nist 800-53, 800-53, nist rev5 | `fw-checks-nist80053` | `report-nist80053` | NIST SP 800-53 Rev 5 |
| csf, nist csf, nist cybersecurity framework | `fw-checks-csf` | `report-csf` | NIST CSF 2.0 |
| cis, cis controls, cis v8 | `fw-checks-cis` | `report-cis` | CIS Controls v8 |
| pci, pcidss, pci-dss, pci dss | `fw-checks-pcidss` | `report-pcidss` | PCI DSS v4.0 |
| iso, iso27001, iso 27001, 27001 | `fw-checks-iso27001` | `report-iso27001` | ISO 27001:2022 |

---

## Secuencia de Carga Multi-Framework

Para CADA framework en la lista del usuario:

```
LOAD  fw-checks-{fw}              ← Layer 2 activo
RUN   todos los checks del framework
SAVE  findings-{fw}.json → disco
UNLOAD fw-checks-{fw}             ← Layer 2 vacío

LOAD  report-{fw}                 ← Layer 3 activo
READ  findings-{fw}.json desde disco
GEN   HTML técnico + ejecutivo + scripts
UNLOAD report-{fw}                ← Layer 3 vacío
```

Nota: vendor-kb-{vendor} (Layer 1) permanece cargado durante TODO el ciclo.

---

## Rutas de Memoria

| Tipo | Ruta |
|------|------|
| Evidencia | `MEMORY/evidence/{assessment_id}/{hostname}/` |
| Hallazgos JSON | `MEMORY/assessments/{assessment_id}/findings-{fw}.json` |
| Reportes HTML | `MEMORY/reports/{client}/{assessment_id}/` |
| Scripts remediación | `MEMORY/reports/{client}/{assessment_id}/remediation/` |
| POA&M | `MEMORY/poam/{client}-poam-{vendor}.md` |
| Inventarios | `MEMORY/inventories/{client}-{vendor}.yaml` |

---

## Assessment ID

Formato: `{vendor}-{ip_last_octet}-{YYYYMMDD}-{seq:02d}`
Ejemplo: `f5-050-20260409-01`

---

## Operaciones de Ciberseguridad → community-cybersec-index (Layer 0 ext.)

Cuando el usuario pida algo FUERA de auditoria de dispositivos de red, cargar primero
`community-cybersec-index` para identificar la skill especifica, luego leer esa skill.

| Dominio solicitado | Accion |
|--------------------|--------|
| forensics, forense, memoria RAM, imagen disco, artefactos, volatility, autopsy | Cargar `community-cybersec-index` → seccion FORENSICS DIGITAL |
| malware, virus, rootkit, ransomware analisis, sandbox, YARA, reverse engineering | Cargar `community-cybersec-index` → seccion MALWARE ANALYSIS |
| threat intel, IOC, MISP, ATT&CK, actor amenaza, CTI, STIX, dark web | Cargar `community-cybersec-index` → seccion THREAT INTELLIGENCE |
| incidente, IR, playbook, breach, contencion, ransomware response | Cargar `community-cybersec-index` → seccion INCIDENT RESPONSE |
| threat hunting, caza amenazas, beaconing, persistencia hunting, LOLBAS | Cargar `community-cybersec-index` → seccion THREAT HUNTING |
| SIEM, Splunk, Sigma, QRadar, deteccion, correlacion, alert triage | Cargar `community-cybersec-index` → seccion SIEM / DETECTION |
| Wireshark, Scapy, Netflow, IDS, IPS, Snort, Suricata, BGP, NAC | Cargar `community-cybersec-index` → seccion NETWORK SECURITY |
| cloud, AWS, Azure, GCP, S3, CloudTrail, CSPM, Terraform | Cargar `community-cybersec-index` → seccion CLOUD SECURITY |
| Active Directory, OAuth, SAML, MFA, PAM, Zero Trust, RBAC, BeyondCorp | Cargar `community-cybersec-index` → seccion IAM / ZERO TRUST |
| pentest, red team, exploit, C2, Metasploit, Kerberoasting, social engineering | Cargar `community-cybersec-index` → seccion PENETRATION TESTING |
| web app, API, OWASP, XSS, SQLi, SSRF, IDOR, JWT, GraphQL, WAF | Cargar `community-cybersec-index` → seccion WEB & API SECURITY |
| Docker, Kubernetes, k8s, contenedor, Falco, Trivy, runtime security | Cargar `community-cybersec-index` → seccion CONTAINERS & K8S |
| OT, ICS, SCADA, Modbus, DNP3, PLC, historian, IEC 62443, NERC CIP | Cargar `community-cybersec-index` → seccion OT / ICS / SCADA |
| vulnerabilidades, Nessus, CVE, CVSS, EPSS, patch, DefectDojo | Cargar `community-cybersec-index` → seccion VULN MANAGEMENT |
| EDR, CrowdStrike, osquery, fileless, process injection, LOTL | Cargar `community-cybersec-index` → seccion ENDPOINT SECURITY |
| ransomware defensa, canary, honeytoken, backup inmutable, recovery | Cargar `community-cybersec-index` → seccion RANSOMWARE DEFENSE |
| DevSecOps, CI/CD, SAST, DAST, secret scanning, supply chain codigo | Cargar `community-cybersec-index` → seccion DEVSECOPS |
| TLS, certificados, HSM, AES, RSA, KMS, post-quantum, PKI | Cargar `community-cybersec-index` → seccion CRYPTOGRAPHY |
| GDPR, ISO 27001, PCI DSS, SOC2, NIST CSF madurez, privacidad | Cargar `community-cybersec-index` → seccion COMPLIANCE |
| Android, iOS, APK, MobSF, Frida, certificate pinning, mobile pentest | Cargar `community-cybersec-index` → seccion MOBILE SECURITY |
| phishing, BEC, spearphishing, DMARC, DKIM, SPF, email seguridad | Cargar `community-cybersec-index` → seccion PHISHING & EMAIL |
