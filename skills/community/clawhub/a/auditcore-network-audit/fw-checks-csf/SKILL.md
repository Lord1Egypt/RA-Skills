---
name: fw-checks-csf
description: >-
  Framework checks NIST CSF 2.0. Layer 2 — cargar por framework, uno a la vez.
  Evalúa ~40 subcategorías aplicables a red en 6 funciones: GOVERN, IDENTIFY, PROTECT,
  DETECT, RESPOND, RECOVER. Descargar antes del siguiente framework.
metadata:
  safety: read-only
  author: auditcore
  version: "2.0.0"
  openclaw: '{"emoji":"📋","safetyTier":"read-only","requires":{"bins":[],"env":[]},"tags":["framework","nist","csf","layer2","checks"]}'
---

# Framework Checks: NIST Cybersecurity Framework (CSF) 2.0

Funciones evaluadas: 6 (GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER)
Subcategorías aplicables: ~108 | Evaluadas en dispositivos de red: ~40
Instrucción: Para cada subcategoría, usar domain → vendor KB → ejecutar → evaluar.

---

## GV — GOVERN (Gobernanza)

### GV.OC-01 — Organizational context
Dominio: VERSION + CONFIG_BACKUP
EVALUAR: ¿Existe documentación de baseline y propietario del activo?
CUMPLE: Inventario con hostname, OS, rol, responsable documentado
FALLA: Sin documentación de activo
Severidad: Medium

### GV.PO-01 — Policy for cybersecurity exists
Dominio: BANNER + CONFIG_BACKUP
EVALUAR: ¿El banner refleja política de uso aceptable? ¿Hay proceso de change management?
CUMPLE: Banner con política, backup con historial de cambios
FALLA: Sin banner, sin proceso de cambios documentado
Severidad: Medium

---

## ID — IDENTIFY (Identificar)

### ID.AM-01 — Hardware assets inventoried
Dominio: VERSION
CUMPLE: Platform, OS, serial, módulos, rol HA capturados
CAPTURAR: Completar inventario con datos del dispositivo
Severidad: Info

### ID.AM-05 — Assets prioritized by criticality
Dominio: VERSION + HA_STATUS
EVALUAR: ¿El dispositivo tiene rol definido (perimetral, core, mgmt)?
CUMPLE: Rol documentado en inventario
ADVERTENCIA: Rol no documentado explícitamente
Severidad: Low

### ID.RA-01 — Vulnerabilities identified
Dominio: VERSION
CUMPLE: OS sin CVEs críticos/altos activos, versión en soporte
FALLA: CVE CVSS ≥ 9.0 activo, OS EOL
Severidad: Critical

---

## PR — PROTECT (Proteger)

### PR.AA-01 — Identities and credentials managed
Dominio: ACCOUNTS + PASSWORD_POLICY
CUMPLE: Cuentas únicas, política de complejidad, sin cuentas por defecto
FALLA: Credenciales por defecto, cuentas compartidas
Severidad: High

### PR.AA-02 — Identities proofed and bound to credentials
Dominio: AUTH_SOURCE
CUMPLE: AAA centralizada (TACACS+/RADIUS), autenticación fuerte
FALLA: Auth local únicamente
Severidad: High

### PR.AA-03 — Users, services, hardware authenticated
Dominio: AUTH_SOURCE + SNMP
CUMPLE: SNMP v3 con auth/priv, AAA centralizada
FALLA: SNMP v1/v2c community público, auth local
Severidad: High

### PR.AA-05 — Access permissions managed
Dominio: ACCOUNTS
CUMPLE: Mínimo privilegio aplicado, revisión periódica de accesos
FALLA: Privilegios excesivos sin justificación
Severidad: High

### PR.AA-06 — Physical access to assets managed
Dominio: SESSION_TIMEOUT + BANNER
EVALUAR: ¿Sesiones expiran? ¿Banner de autorización presente?
CUMPLE: timeout ≤ 600s, banner configurado
FALLA: Sin timeout, sin banner
Severidad: Medium

### PR.DS-02 — Data in transit protected
Dominio: TLS_PROFILES + IPSEC + SSH_HARDENING
CUMPLE: TLS 1.2+, SSH con ciphers fuertes, VPN con IKEv2 + AES
FALLA: Protocolos de texto plano, TLS débil
Severidad: High

### PR.DS-10 — Data integrity enforced
Dominio: CONFIG_BACKUP
CUMPLE: UCS/backup con checksum, config validation activa
FALLA: Sin mecanismo de integridad de configuración
Severidad: Medium

### PR.IR-01 — Networks protected from unauthorized access
Dominio: ACL + PACKET_FILTERS + FIREWALL_POLICY
CUMPLE: ACLs/packet-filters protegen management plane, segmentación implementada
FALLA: Management plane expuesto sin restricción
Severidad: High

### PR.PS-01 — Configuration management practices followed
Dominio: CONFIG_BACKUP + SERVICES
CUMPLE: Baseline documentada, servicios mínimos, backup reciente
FALLA: Sin baseline, servicios innecesarios activos
Severidad: High

### PR.PS-04 — Logs generated
Dominio: LOGGING + NTP
CUMPLE: Logging completo con timestamp sincronizado
FALLA: Logging parcial o deshabilitado
Severidad: High

---

## DE — DETECT (Detectar)

### DE.AE-02 — Potentially adverse events analyzed
Dominio: LOGGING + THREAT_INTEL
CUMPLE: Logs hacia SIEM, alertas configuradas para eventos críticos
FALLA: Sin SIEM, sin alerting centralizado
Severidad: High

### DE.AE-06 — Information on adverse events available
Dominio: LOGGING
CUMPLE: Logs accesibles y con retención ≥ 90 días
ADVERTENCIA: Logs solo locales con retención limitada
Severidad: Medium

### DE.CM-01 — Networks monitored for security events
Dominio: THREAT_INTEL + LOGGING
CUMPLE: NetFlow/sFlow activo, SNMP traps configurados, syslog centralizado
FALLA: Sin monitoreo de red activo
Severidad: High

---

## RS — RESPOND (Responder)

### RS.MA-01 — Incidents contained
Dominio: ACL + SSH_HARDENING
EVALUAR: ¿Existe capacidad de restringir acceso rápidamente?
CUMPLE: ACLs/allow-lists configuradas, acceso mgmt restringido por IP
FALLA: Sin mecanismo de restricción rápida
Severidad: Medium

---

## RC — RECOVER (Recuperar)

### RC.RP-01 — Recovery plan executed
Dominio: CONFIG_BACKUP
CUMPLE: UCS/backup reciente (<30 días), proceso de restore documentado
FALLA: Sin backup, sin procedimiento de recuperación
Severidad: High
