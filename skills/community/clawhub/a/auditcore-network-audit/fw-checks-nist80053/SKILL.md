---
name: fw-checks-nist80053
description: >-
  Framework checks NIST SP 800-53 Rev 5. Layer 2 — cargar por framework, uno a la vez.
  Evalúa ~187 controles en familias AC, AU, CM, IA, SC, SI usando dominios del vendor KB.
  Descargar antes de cargar el siguiente framework. Guardar findings a disco antes de descargar.
metadata:
  safety: read-only
  author: auditcore
  version: "2.0.0"
  openclaw: '{"emoji":"📋","safetyTier":"read-only","requires":{"bins":[],"env":[]},"tags":["framework","nist","800-53","layer2","checks"]}'
---

# Framework Checks: NIST SP 800-53 Rev 5

Controles evaluados: ~187 | Familias: 20
Instrucción: Para cada control, usar domain → vendor KB → ejecutar comando → evaluar.

---

## Familia AC — Access Control

### AC-2 — Account Management
Dominio: ACCOUNTS
CUMPLE: No cuentas con password por defecto, roles mínimos asignados, sin cuentas compartidas
FALLA: Cuenta admin/admin, cuentas sin rol, cuentas de servicio con privilegio admin
ADVERTENCIA: Cuentas inactivas >90 días detectadas
Severidad: High

### AC-3 — Access Enforcement
Dominio: ACCOUNTS + AUTH_SOURCE
CUMPLE: RBAC implementado, acceso mínimo por rol
FALLA: Usuarios con acceso total sin justificación
Severidad: High

### AC-6 — Least Privilege
Dominio: ACCOUNTS
CUMPLE: Roles asignados al mínimo necesario para la función
FALLA: Cuentas de operación con privilegio admin completo
Severidad: High

### AC-7 — Unsuccessful Login Attempts
Dominio: PASSWORD_POLICY
CUMPLE: max-login-failures ≤ 5, lockout configurado
FALLA: lockout deshabilitado, o threshold > 10
ADVERTENCIA: threshold entre 6 y 10
Severidad: High

### AC-8 — System Use Notification
Dominio: BANNER
CUMPLE: Banner con texto de autorización presente
FALLA: Banner ausente o vacío
Severidad: Medium

### AC-12 — Session Termination
Dominio: SESSION_TIMEOUT
CUMPLE: timeout ≤ 600 segundos (10 min)
FALLA: timeout = 0 (nunca expira), o timeout > 1800
ADVERTENCIA: timeout entre 601 y 1800 segundos
Severidad: High

### AC-17 — Remote Access
Dominio: SSH_HARDENING + HTTPS_CONFIG
CUMPLE: SSH restringido a IPs de mgmt, HTTPS habilitado, HTTP deshabilitado
FALLA: SSH allow = All (sin restricción), HTTP habilitado sin redirect
ADVERTENCIA: SSH accesible desde subnet amplia, no desde any
Severidad: High

---

## Familia AU — Audit and Accountability

### AU-2 — Event Logging
Dominio: LOGGING
CUMPLE: Logging habilitado para auth, config changes, admin actions
FALLA: Logging deshabilitado o solo local
ADVERTENCIA: Logging habilitado pero sin forward remoto
Severidad: High

### AU-4 — Audit Log Storage
Dominio: LOGGING
CUMPLE: Destino remoto configurado y activo, buffer local con rotación
FALLA: Sin almacenamiento remoto, sin política de retención
Severidad: Medium

### AU-6 — Audit Review
Dominio: LOGGING
CUMPLE: SIEM destino configurado, log level ≥ informational
FALLA: Sin destino SIEM, log level = emergency (demasiado silencioso)
Severidad: High

### AU-8 — Time Stamps
Dominio: NTP
CUMPLE: NTP sincronizado, stratum ≤ 4, servers definidos
FALLA: NTP no configurado o out of sync
ADVERTENCIA: NTP configurado pero stratum > 4
Severidad: Medium

---

## Familia CM — Configuration Management

### CM-2 — Baseline Configuration
Dominio: CONFIG_BACKUP
CUMPLE: Backup/UCS reciente (<30 días), config validation PASS
FALLA: Sin backup en >30 días, config validation con errores
Severidad: High

### CM-7 — Least Functionality
Dominio: SERVICES
CUMPLE: Solo servicios necesarios habilitados, mgmt en VLAN dedicada
FALLA: Servicios innecesarios activos (telnet, http, ftp)
ADVERTENCIA: Servicios no críticos sin justificación documentada
Severidad: Medium

### CM-8 — System Component Inventory
Dominio: VERSION
CUMPLE: Versión, hardware, módulos documentados
CAPTURAR: platform, OS version, serial, licensed modules, HA role
Severidad: Info

---

## Familia IA — Identification and Authentication

### IA-2 — Identification and Authentication (Organizational Users)
Dominio: AUTH_SOURCE
CUMPLE: type = tacacs o radius (no local)
FALLA: type = local (sin AAA centralizada)
ADVERTENCIA: AAA configurado pero sin fallback correctamente definido
Severidad: Critical

### IA-2(1) — MFA para acceso privilegiado
Dominio: AUTH_SOURCE
CUMPLE: MFA habilitado para cuentas admin via AAA
FALLA: Solo password, sin segundo factor
Severidad: Critical

### IA-5 — Authenticator Management
Dominio: PASSWORD_POLICY + SNMP
CUMPLE: min-length ≥ 12, complejidad (upper+lower+num+special), SNMP sin comunidades v1/v2c
FALLA: min-length < 8, sin complejidad, SNMP community "public" activa
ADVERTENCIA: min-length 8-11, complejidad parcial
Severidad: High

---

## Familia SC — System and Communications Protection

### SC-5 — Denial of Service Protection
Dominio: SERVICES
CUMPLE: Rate limiting, SYN protection configurados
ADVERTENCIA: Sin configuración explícita de DoS protection
Severidad: Medium

### SC-7 — Boundary Protection
Dominio: PACKET_FILTERS + ACL
CUMPLE: Packet filters/ACLs protegen management plane
FALLA: Management plane accesible sin restricción
Severidad: High

### SC-8 — Transmission Confidentiality and Integrity
Dominio: TLS_PROFILES + SSH_HARDENING
CUMPLE: TLS 1.2+ únicamente, sin TLS 1.0/1.1/SSL
FALLA: TLS 1.0 o TLS 1.1 habilitado
ADVERTENCIA: TLS 1.1 como versión mínima (no TLS 1.0, pero no ideal)
Severidad: High

### SC-13 — Cryptographic Protection
Dominio: IPSEC + TLS_PROFILES
CUMPLE: AES-128+, SHA-256+, IKEv2, PFS habilitado
FALLA: DES, 3DES, MD5, IKEv1 en uso
ADVERTENCIA: AES-128 con SHA-1 (débil pero aceptable transitoriamente)
Severidad: Medium

---

## Familia SI — System and Information Integrity

### SI-2 — Flaw Remediation
Dominio: VERSION
CUMPLE: OS en versión soportada, sin advisories críticos/altos activos
FALLA: OS EOL, CVE crítico activo (CVSS ≥ 9.0) sin parche
ADVERTENCIA: CVE alto activo (CVSS 7.0–8.9) pendiente de parche
Severidad: Critical (si CVE CVSS ≥ 9.0), High (si CVSS 7.0–8.9)

### SI-3 — Malware Protection
Dominio: THREAT_INTEL
CUMPLE: Firmas de threat intelligence actualizadas, IPS activo
ADVERTENCIA: IPS no habilitado o firmas desactualizadas (>7 días)
Severidad: Medium

### SI-4 — System Monitoring
Dominio: THREAT_INTEL
CUMPLE: sFlow/NetFlow configurado hacia colector, SIEM recibiendo
FALLA: Sin visibilidad de tráfico
Severidad: Medium
