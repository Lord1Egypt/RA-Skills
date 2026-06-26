---
name: fw-checks-cis
description: >-
  Framework checks CIS Controls v8. Layer 2 — cargar por framework, uno a la vez.
  Evalúa safeguards de los controles CIS 1-8, 12, 13 aplicables a dispositivos de red.
  18 controles, 153 safeguards. Descargar antes del siguiente framework.
metadata:
  safety: read-only
  author: auditcore
  version: "2.0.0"
  openclaw: '{"emoji":"📋","safetyTier":"read-only","requires":{"bins":[],"env":[]},"tags":["framework","cis","cis-v8","layer2","checks"]}'
---

# Framework Checks: CIS Controls v8

Controles evaluados: 18 controles, 153 safeguards
Instrucción: Para cada safeguard, usar domain → vendor KB → ejecutar → evaluar.

---

## CIS Control 1 — Inventory and Control of Enterprise Assets

### CIS 1.1 — Establish and Maintain Detailed Asset Inventory
Dominio: VERSION
CUMPLE: Hostname, versión OS, hardware, módulos, rol HA documentados
FALLA: Versión OS desconocida o datos de inventario incompletos
Severidad: Medium

---

## CIS Control 2 — Inventory and Control of Software Assets

### CIS 2.2 — Ensure Authorized Software is Currently Supported
Dominio: VERSION
CUMPLE: OS con soporte activo del fabricante
FALLA: OS en EOL (End of Life) — sin actualizaciones de seguridad disponibles
Severidad: Critical

---

## CIS Control 3 — Data Protection

### CIS 3.10 — Encrypt Sensitive Data in Transit
Dominio: TLS_PROFILES + IPSEC + SSH_HARDENING
CUMPLE: TLS 1.2+, AES-256, no protocolos débiles
FALLA: TLS 1.0/1.1, DES, 3DES, MD5 activos
Severidad: High

---

## CIS Control 4 — Secure Configuration of Enterprise Assets and Software

### CIS 4.1 — Establish and Maintain a Secure Configuration Process
Dominio: CONFIG_BACKUP
CUMPLE: Backup reciente (<30 días), proceso de change management evidenciado
FALLA: Sin backup, sin evidencia de baseline
Severidad: High

### CIS 4.3 — Configure Automatic Session Locking
Dominio: SESSION_TIMEOUT
CUMPLE: timeout ≤ 600 segundos
FALLA: timeout = 0 o no configurado
Severidad: High

### CIS 4.8 — Uninstall or Disable Unnecessary Services
Dominio: SERVICES
CUMPLE: Solo servicios requeridos habilitados
FALLA: Telnet, HTTP, FTP, o servicios inseguros habilitados
Severidad: High

---

## CIS Control 5 — Account Management

### CIS 5.1 — Establish and Maintain an Inventory of Accounts
Dominio: ACCOUNTS
CUMPLE: Todas las cuentas tienen propietario y rol documentado
FALLA: Cuentas genéricas, cuentas sin rol asignado
Severidad: High

### CIS 5.2 — Use Unique Passwords
Dominio: PASSWORD_POLICY
CUMPLE: min-length ≥ 14, complejidad completa (upper+lower+num+special)
FALLA: min-length < 8, sin política de complejidad
ADVERTENCIA: min-length 8-13
Severidad: High

### CIS 5.3 — Disable Dormant Accounts
Dominio: ACCOUNTS
CUMPLE: Sin cuentas inactivas >90 días
ADVERTENCIA: Cuentas inactivas detectadas >90 días
Severidad: Medium

### CIS 5.4 — Restrict Administrator Privileges
Dominio: ACCOUNTS + AUTH_SOURCE
CUMPLE: Cuentas admin separadas de cuentas de usuario, MFA en cuentas privilegiadas
FALLA: Cuentas de usuario con privilegios admin, sin MFA en admin
Severidad: Critical

---

## CIS Control 6 — Access Control Management

### CIS 6.3 — Require MFA for Externally-Exposed Applications
Dominio: AUTH_SOURCE + SSH_HARDENING
CUMPLE: MFA habilitado para acceso externo/remoto
FALLA: Acceso remoto con solo password
Severidad: Critical

### CIS 6.4 — Require MFA for Remote Network Access
Dominio: AUTH_SOURCE
CUMPLE: AAA centralizada con MFA para acceso de administración
FALLA: Solo auth local, sin MFA
Severidad: Critical

---

## CIS Control 7 — Continuous Vulnerability Management

### CIS 7.3 — Perform Automated Operating System Patch Management
Dominio: VERSION
CUMPLE: OS en versión actual o N-1, CVEs críticos parcheados
FALLA: OS con CVE CVSS ≥ 9.0 activo, >90 días sin parche de seguridad
ADVERTENCIA: OS en N-2 o mayor antigüedad
Severidad: Critical/High según CVSS

---

## CIS Control 8 — Audit Log Management

### CIS 8.2 — Collect Audit Logs
Dominio: LOGGING
CUMPLE: Logging de auth, config changes, y admin actions habilitado
FALLA: Logging deshabilitado
Severidad: High

### CIS 8.4 — Standardize Time Synchronization
Dominio: NTP
CUMPLE: NTP configurado y sincronizado, mismo servidor NTP en toda la infraestructura
FALLA: NTP no configurado o out of sync
Severidad: Medium

### CIS 8.9 — Centralize Audit Logs
Dominio: LOGGING
CUMPLE: Logs enviados a SIEM o syslog centralizado
FALLA: Solo logs locales, sin destino remoto
Severidad: High

---

## CIS Control 12 — Network Infrastructure Management

### CIS 12.7 — Manage Default Accounts on Enterprise Assets
Dominio: ACCOUNTS + AUTH_SOURCE
CUMPLE: Cuentas por defecto deshabilitadas o con password cambiado y MFA
FALLA: Cuenta admin con credenciales por defecto, sin cambio post-instalación
Severidad: Critical

---

## CIS Control 13 — Network Monitoring and Defense

### CIS 13.6 — Collect Network Traffic Flow Logs
Dominio: THREAT_INTEL
CUMPLE: NetFlow/sFlow configurado hacia colector activo
ADVERTENCIA: Sin colección de flujos de red
Severidad: Medium
