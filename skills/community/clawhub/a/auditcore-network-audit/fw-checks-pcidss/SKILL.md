---
name: fw-checks-pcidss
description: >-
  Framework checks PCI DSS v4.0. Layer 2 — cargar por framework, uno a la vez.
  Evalúa ~89 controles técnicos en 12 requisitos aplicables a dispositivos en el CDE.
  Listo para presentación a QSA. Descargar antes del siguiente framework.
metadata:
  safety: read-only
  author: auditcore
  version: "2.0.0"
  openclaw: '{"emoji":"📋","safetyTier":"read-only","requires":{"bins":[],"env":[]},"tags":["framework","pci","pcidss","layer2","checks"]}'
---

# Framework Checks: PCI DSS v4.0

Requisitos evaluados: 12 requisitos, ~89 controles técnicos aplicables a dispositivos de red.
Instrucción: Para cada control, usar domain → vendor KB → ejecutar → evaluar.
Alcance: Solo aplicable a dispositivos en el CDE (Cardholder Data Environment) o conectados a él.

---

## Req 1 — Install and Maintain Network Security Controls

### PCI 1.2.1 — Security features defined and implemented
Dominio: FIREWALL_POLICY + ACL + PACKET_FILTERS
CUMPLE: Políticas con reglas explícitas de deny, no reglas "any any allow"
FALLA: Regla "permit any any" activa, sin política de denegación por defecto
Severidad: Critical

### PCI 1.3.1 — Inbound traffic restricted to CDE
Dominio: FIREWALL_POLICY + ACL
CUMPLE: Solo tráfico autorizado hacia CDE, denegación implícita para el resto
FALLA: Sin restricción de inbound al CDE
Severidad: Critical

### PCI 1.3.2 — Outbound traffic restricted from CDE
Dominio: FIREWALL_POLICY + ACL
CUMPLE: Outbound desde CDE restringido solo a destinos necesarios
FALLA: CDE puede iniciar tráfico a cualquier destino
Severidad: High

---

## Req 2 — Apply Secure Configurations to All System Components

### PCI 2.2.1 — Configuration standards established
Dominio: CONFIG_BACKUP + SERVICES
CUMPLE: Baseline de configuración documentada, backup reciente
FALLA: Sin configuración hardened documentada
Severidad: High

### PCI 2.2.4 — Only necessary services/protocols enabled
Dominio: SERVICES
CUMPLE: Solo servicios necesarios activos, telnet/http deshabilitados
FALLA: Telnet, HTTP, o servicios inseguros habilitados
Severidad: High

### PCI 2.2.7 — Non-console admin access encrypted
Dominio: SSH_HARDENING + HTTPS_CONFIG
CUMPLE: SSH habilitado, telnet deshabilitado, HTTPS para web mgmt
FALLA: Telnet activo en líneas VTY, HTTP sin HTTPS
Severidad: Critical

---

## Req 4 — Protect Cardholder Data with Strong Cryptography

### PCI 4.2.1 — Strong cryptography for data in transit
Dominio: TLS_PROFILES + IPSEC + SSH_HARDENING
CUMPLE: TLS 1.2+ únicamente, AES-128+, SHA-256+, sin protocolos débiles
FALLA: TLS 1.0/1.1 habilitado, DES/3DES/RC4 en uso
ADVERTENCIA: TLS 1.1 como mínimo (debe migrarse a TLS 1.2+)
Severidad: Critical

---

## Req 6 — Develop and Maintain Secure Systems and Software

### PCI 6.3.3 — Security patches installed
Dominio: VERSION
CUMPLE: Parches críticos aplicados dentro de 1 mes, altos dentro de 3 meses
FALLA: CVE crítico activo (CVSS ≥ 9.0) sin parche por más de 30 días
ADVERTENCIA: CVE alto (7.0–8.9) sin parche por más de 90 días
Severidad: Critical

---

## Req 7 — Restrict Access to System Components and Cardholder Data

### PCI 7.1 — Access control model defined
Dominio: ACCOUNTS + AUTH_SOURCE
CUMPLE: RBAC implementado, acceso mínimo necesario
FALLA: Sin modelo de acceso, usuarios con privilegio total por defecto
Severidad: High

### PCI 7.2.1 — Appropriate access assigned to users
Dominio: ACCOUNTS
CUMPLE: Roles asignados acorde a función laboral
FALLA: Cuentas con privilegios no justificados
Severidad: High

---

## Req 8 — Identify Users and Authenticate Access

### PCI 8.1.1 — User IDs managed
Dominio: ACCOUNTS
CUMPLE: Cuentas únicas por usuario, sin cuentas compartidas, sin cuentas por defecto activas
FALLA: Cuentas genéricas activas, cuenta "admin" con password por defecto
Severidad: Critical

### PCI 8.1.6 — Account lockout after failed attempts
Dominio: PASSWORD_POLICY
CUMPLE: Lockout tras ≤ 6 intentos fallidos
FALLA: Lockout deshabilitado o threshold > 10
Severidad: High

### PCI 8.1.8 — Re-authentication after idle time
Dominio: SESSION_TIMEOUT
CUMPLE: Sesión expira en ≤ 15 minutos de inactividad
FALLA: timeout = 0 o > 900 segundos
Severidad: High

### PCI 8.2 — Proper identification and authentication
Dominio: AUTH_SOURCE
CUMPLE: AAA centralizada, autenticación única por sesión
FALLA: Auth local sin AAA, sesiones compartidas
Severidad: High

### PCI 8.3 — Multi-factor authentication for admin access
Dominio: AUTH_SOURCE
CUMPLE: MFA habilitado para todos los accesos admin
FALLA: Sin MFA para acceso administrativo
Severidad: Critical

### PCI 8.3.9 — Password requirements met
Dominio: PASSWORD_POLICY
CUMPLE: min-length ≥ 12, complejidad completa, historial ≥ 4
FALLA: min-length < 7, sin complejidad
Severidad: High

---

## Req 10 — Log and Monitor All Access

### PCI 10.2 — Audit logs implemented
Dominio: LOGGING
CUMPLE: Logs de: auth (éxito y fallo), acceso admin, cambios de config, acceso a datos
FALLA: Logging no configurado o incompleto
Severidad: Critical

### PCI 10.3.3 — Audit logs protected from modification
Dominio: LOGGING
CUMPLE: Logs enviados a syslog remoto inmediatamente (no solo local)
FALLA: Solo logs locales (modificables por un atacante con acceso al device)
Severidad: High

### PCI 10.6 — Time synchronization
Dominio: NTP
CUMPLE: NTP configurado y sincronizado con fuente confiable
FALLA: NTP no configurado, tiempo no sincronizado
Severidad: Medium

---

## Req 11 — Test Security of Systems and Networks

### PCI 11.4 — External and internal penetration testing
Dominio: THREAT_INTEL + VERSION
CUMPLE: Evidencia de vulnerability scanning reciente, CVEs activos documentados
ADVERTENCIA: Sin evidencia de escaneo de vulnerabilidades en últimos 6 meses
Severidad: Medium
