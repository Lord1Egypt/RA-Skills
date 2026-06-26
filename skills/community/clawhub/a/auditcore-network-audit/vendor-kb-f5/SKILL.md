---
name: vendor-kb-f5
description: >-
  Knowledge Base de F5 Networks. Layer 1 — cargar al iniciar auditoría F5, mantener
  hasta Fase 7. Contiene: dominios READ_COMMANDS (tmsh/bash), FORBIDDEN_COMMANDS,
  SEVERITY_MAP y REMEDIATION_FORMAT para BIG-IP TMOS 13.x–17.x, VELOS y F5 XC.
  Cargarlo con system-methodology + system-index.
metadata:
  safety: read-only
  author: auditcore
  version: "2.0.0"
  openclaw: '{"emoji":"🔵","safetyTier":"read-only","requires":{"bins":["ssh"],"env":[]},"tags":["vendor-kb","f5","bigip","tmos","velos","xc","layer1"]}'
---

# Vendor KB: F5 Networks

OS: BIG-IP TMOS 13.x–17.x | VELOS (F5OS + tenant TMOS) | XC (SaaS/API)
Access: SSH + tmsh | XC: REST API read-only
HA: active/standby pairs — evaluar AMBOS nodos independientemente

## COMANDOS_PROHIBIDOS
tmsh create | tmsh modify | tmsh delete | tmsh save | tmsh load
tmsh install | rm | mv | dd | chmod | reboot | shutdown

---

## COMANDOS_LECTURA

### dominio: VERSION
```
tmsh show sys version
tmsh show sys hardware
tmsh show sys provision
tmsh show sys software status
tmsh show sys uptime
```

### dominio: HA_STATUS
```
tmsh show cm sync-status
tmsh show cm failover-status
tmsh show cm device
tmsh show cm device-group
tmsh show cm traffic-group
```

### dominio: ACCOUNTS
```
tmsh list auth user
tmsh list auth user role
tmsh list auth remote-user
tmsh list auth partition
```

### dominio: AUTH_SOURCE
```
tmsh list auth source
tmsh list auth tacacs
tmsh list auth radius
tmsh list auth ldap
tmsh list auth remote-role
```

### dominio: PASSWORD_POLICY
```
tmsh list auth password-policy
```

### dominio: SESSION_TIMEOUT
```
tmsh list sys sshd inactivity-timeout
tmsh list sys httpd auth-pam-idle-timeout
```

### dominio: BANNER
```
tmsh list sys sshd banner
tmsh list sys sshd banner-text
```

### dominio: SSH_HARDENING
```
tmsh list sys sshd
tmsh list sys sshd allow
```

### dominio: HTTPS_CONFIG
```
tmsh list sys httpd
tmsh list sys httpd ssl-port
```

### dominio: LOGGING
```
tmsh list sys syslog
tmsh list sys syslog remote-servers
tmsh list sys log config
tmsh list sys syslog local-syslog
```

### dominio: NTP
```
tmsh list sys ntp
tmsh show sys ntp status
tmsh list sys ntp restrict
```

### dominio: SNMP
```
tmsh list sys snmp communities
tmsh list sys snmp users
tmsh list sys snmp traps
```

### dominio: CONFIG_BACKUP
```
tmsh verify sys config
tmsh list sys ucs
tmsh show sys ucs
```

### dominio: SERVICES
```
tmsh list sys service
tmsh list sys management-ip
tmsh list sys httpd
tmsh list sys sshd
```

### dominio: PACKET_FILTERS
```
tmsh list net packet-filter
tmsh show net packet-filter
```

### dominio: IPSEC
```
tmsh list net ipsec ike-peer
tmsh list net ipsec ipsec-policy
tmsh show net ipsec ipsec-sa
```

### dominio: TLS_PROFILES
```
tmsh list ltm profile ssl-client | grep -i "ciphers\|options\|ssl-protocol"
tmsh list ltm profile ssl-server | grep -i "ciphers\|options"
```

### dominio: THREAT_INTEL
```
tmsh list sys software update
tmsh show sys sflow
tmsh list sys sflow receiver
```

### dominio: INTERFACES
```
tmsh show net interface
tmsh show net lldp
```

---

## TABLA_SEVERIDAD (F5-específico)

| Condición | Severidad |
|-----------|-----------|
| auth source = local (sin AAA) | Critical |
| HA out of sync | Critical |
| SSH allow = All (sin restricción IP) | High |
| SNMPv2c community activa | High |
| TLS 1.0/1.1 habilitado | High |
| SSH inactivity-timeout = 0 | High |
| Sin syslog remoto | High |
| Sin UCS backup reciente | High |
| Sin banner SSH | Medium |
| NTP sin sincronizar | Medium |
| SSH ciphers débiles (3des, arcfour) | Medium |
| IKEv1 o 3DES en IPsec | Medium |

---

## FORMATO_REMEDIACION (F5 TMOS)

```bash
#!/bin/bash
# WARNING: Revisar antes de aplicar. Probar en lab primero.
# Device: {hostname}  Framework: {fw}  Fecha: {date}  Assessor: AuditCore

# BACKUP (obligatorio antes de cualquier cambio):
tmsh save sys config

# {CONTROL_ID}: {título del hallazgo}
{remediation_cmd}

# VERIFY:
{verify_cmd}

# ROLLBACK (script separado):
# {rollback_cmd}
# tmsh save sys config
```
