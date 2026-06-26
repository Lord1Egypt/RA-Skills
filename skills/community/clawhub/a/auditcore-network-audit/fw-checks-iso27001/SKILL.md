---
name: fw-checks-iso27001
description: >-
  Framework checks ISO/IEC 27001:2022. Layer 2 — cargar por framework, uno a la vez.
  Evalúa ~35 controles técnicos del Anexo A (Temas 5, 6, 8) aplicables a dispositivos de red.
  Produce clasificación NC Mayor / NC Menor / Observación. Descargar antes del siguiente.
metadata:
  safety: read-only
  author: auditcore
  version: "2.0.0"
  openclaw: '{"emoji":"📋","safetyTier":"read-only","requires":{"bins":[],"env":[]},"tags":["framework","iso","iso27001","layer2","checks"]}'
---

# Framework Checks: ISO/IEC 27001:2022

Controles evaluados: Anexo A — 93 controles en 4 temas
Aplicables a dispositivos de red: ~35 controles técnicos
Instrucción: Para cada control, usar domain → vendor KB → ejecutar → evaluar.

---

## Tema 5 — Controles Organizacionales

### A.5.15 — Access Control
Dominio: ACCOUNTS + AUTH_SOURCE
CUMPLE: RBAC implementado, política de mínimo privilegio, AAA centralizada
FALLA: Sin control de acceso formal, auth local únicamente
Severidad: High

### A.5.16 — Identity Management
Dominio: ACCOUNTS
CUMPLE: Identidades únicas por usuario, sin cuentas compartidas ni genéricas
FALLA: Cuentas compartidas, cuentas genéricas sin propietario
Severidad: High

### A.5.17 — Authentication Information
Dominio: PASSWORD_POLICY + SNMP + BANNER
CUMPLE: Política de password robusta, SNMP v3, banner de acceso
FALLA: Sin política de password, SNMP v1/v2c, sin banner
Severidad: High

### A.5.18 — Access Rights
Dominio: ACCOUNTS
CUMPLE: Derechos asignados por rol, revisión periódica documentada
FALLA: Derechos excesivos, sin proceso de revisión
Severidad: High

### A.5.19 — Information Security in Supplier Relationships
Dominio: VERSION
EVALUAR: ¿El firmware tiene soporte activo del fabricante?
CUMPLE: OS en soporte activo
FALLA: OS EOL (fabricante sin parches)
Severidad: High

### A.5.23 — Information Security for Use of Cloud Services
Dominio: HTTPS_CONFIG + TLS_PROFILES
CUMPLE: Comunicaciones hacia cloud cifradas con TLS 1.2+
FALLA: Comunicaciones no cifradas o con TLS débil
Severidad: High

---

## Tema 6 — Controles de Personas

### A.6.7 — Remote Working
Dominio: SSH_HARDENING + HTTPS_CONFIG + AUTH_SOURCE
CUMPLE: Acceso remoto solo por SSH/HTTPS con AAA, MFA habilitado
FALLA: Telnet activo, acceso sin MFA, SSH sin restricción IP
Severidad: High

---

## Tema 7 — Controles Físicos

*No aplican directamente a configuración lógica de dispositivos.*
*Verificar mediante evidencia documental o inspección física.*

---

## Tema 8 — Controles Tecnológicos

### A.8.1 — User Endpoint Devices
Dominio: SESSION_TIMEOUT
CUMPLE: Sesiones de mgmt con timeout ≤ 600 segundos
FALLA: timeout = 0, sesiones sin expiración
Severidad: Medium

### A.8.2 — Privileged Access Rights
Dominio: ACCOUNTS + AUTH_SOURCE
CUMPLE: Cuentas privilegiadas con MFA, auditadas, separadas de cuentas normales
FALLA: Sin segregación de cuentas privilegiadas, sin MFA
Severidad: Critical

### A.8.4 — Access to Source Code
Dominio: CONFIG_BACKUP
CUMPLE: Backup de configuración protegida, acceso restringido
FALLA: Sin backup, configuración expuesta
Severidad: Medium

### A.8.5 — Secure Authentication
Dominio: AUTH_SOURCE + PASSWORD_POLICY
CUMPLE: AAA centralizada, MFA, política de passwords robusta
FALLA: Auth local, sin MFA, política débil
Severidad: High

### A.8.7 — Protection Against Malware
Dominio: THREAT_INTEL + VERSION
CUMPLE: Firmas de threat intel actualizadas, OS sin vulnerabilidades conocidas
FALLA: OS con CVE crítico activo, sin protección contra amenazas
Severidad: High

### A.8.8 — Management of Technical Vulnerabilities
Dominio: VERSION
CUMPLE: OS en versión soportada, CVEs parcheados dentro de SLA
FALLA: CVE crítico (CVSS ≥ 9.0) activo, OS EOL
ADVERTENCIA: CVE alto (7.0–8.9) sin parche dentro de SLA
Severidad: Critical/High

### A.8.9 — Configuration Management
Dominio: CONFIG_BACKUP + SERVICES + BANNER
CUMPLE: Baseline documentada, backup reciente, solo servicios necesarios
FALLA: Sin baseline, sin backup, servicios no autorizados activos
Severidad: High

### A.8.12 — Data Leakage Prevention
Dominio: LOGGING + PACKET_FILTERS
CUMPLE: Logging de tráfico activo, filtros de paquetes configurados
ADVERTENCIA: Sin visibilidad de flujos de datos salientes
Severidad: Medium

### A.8.15 — Logging
Dominio: LOGGING + NTP
CUMPLE: Eventos de auth, config changes, y admin actions logueados; NTP sincronizado
FALLA: Logging deshabilitado, NTP sin sincronizar
Severidad: High

### A.8.16 — Monitoring Activities
Dominio: THREAT_INTEL + LOGGING
CUMPLE: SIEM activo, alertas configuradas, flujos de red monitoreados
FALLA: Sin monitoreo centralizado, sin alertas
Severidad: High

### A.8.17 — Clock Synchronization
Dominio: NTP
CUMPLE: NTP configurado y sincronizado, stratum ≤ 4
FALLA: NTP no configurado o desincronizado
Severidad: Medium

### A.8.19 — Installation of Software on Operational Systems
Dominio: VERSION + SERVICES
CUMPLE: Solo software autorizado instalado, versión documentada
FALLA: Módulos o servicios no autorizados activos
Severidad: Medium

### A.8.20 — Networks Security
Dominio: ACL + PACKET_FILTERS + SSH_HARDENING
CUMPLE: Segmentación de red implementada, management plane protegido
FALLA: Sin segmentación, management plane expuesto
Severidad: High

### A.8.21 — Security of Network Services
Dominio: TLS_PROFILES + IPSEC
CUMPLE: Servicios de red con cifrado fuerte (TLS 1.2+, IKEv2)
FALLA: Servicios sin cifrado o con protocolos débiles
Severidad: High

### A.8.24 — Use of Cryptography
Dominio: TLS_PROFILES + IPSEC + SSH_HARDENING
CUMPLE: AES-128+, SHA-256+, IKEv2, PFS, TLS 1.2+, ciphers SSH fuertes
FALLA: DES, 3DES, MD5, RC4, IKEv1, TLS ≤ 1.1 en uso
Severidad: High
