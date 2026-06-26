---
name: vendor-kb-juniper
description: >-
  Knowledge Base de Juniper Networks. Layer 1 — cargar al iniciar auditoría Juniper,
  mantener hasta Fase 7. Contiene: dominios READ_COMMANDS (JunOS CLI/NETCONF),
  FORBIDDEN_COMMANDS, SEVERITY_MAP y REMEDIATION_FORMAT.
  Soporta JunOS 18.x–23.x: SRX, QFX, EX, MX.
metadata:
  safety: read-only
  author: auditcore
  version: "2.0.0"
  openclaw: '{"emoji":"🟩","safetyTier":"read-only","requires":{"bins":["ssh"],"env":[]},"tags":["vendor-kb","juniper","junos","srx","qfx","mx","layer1"]}'
---

# Vendor KB: Juniper Networks

OS: JunOS 18.x–23.x | SRX (firewall) | QFX/EX (switching) | MX (routing)
Access: SSH + CLI (operational/configuration mode) | NETCONF read-only
HA: Chassis Cluster (SRX), Virtual Chassis (QFX/EX) — evaluar ambos nodos

## COMANDOS_PROHIBIDOS
set | delete | rollback (sin número) | request system reboot | load | merge | override | replace | commit

---

## COMANDOS_LECTURA

### dominio: VERSION
```
show version
show chassis hardware
show system storage
show system software
```

### dominio: HA_STATUS
```
show chassis cluster status
show chassis cluster interfaces
show virtual-chassis
show redundancy
```

### dominio: ACCOUNTS
```
show configuration system login | display set
show configuration system login user | display set
show system login
```

### dominio: AUTH_SOURCE
```
show configuration system authentication-order | display set
show configuration system radius-server | display set
show configuration system tacplus-server | display set
```

### dominio: PASSWORD_POLICY
```
show configuration system login password | display set
show system login user | grep tries
```

### dominio: SESSION_TIMEOUT
```
show configuration system services ssh | display set | grep connection-limit
show configuration system login retry-options | display set
```

### dominio: BANNER
```
show configuration system login message | display set
show configuration system login announcement | display set
```

### dominio: SSH_HARDENING
```
show configuration system services ssh | display set
show configuration system services | display set
```

### dominio: HTTPS_CONFIG
```
show configuration system services web-management | display set
show configuration system services | display set | grep https
```

### dominio: LOGGING
```
show configuration system syslog | display set
show log messages | last 20
```

### dominio: NTP
```
show ntp status
show configuration system ntp | display set
```

### dominio: SNMP
```
show configuration snmp | display set
show snmp statistics
```

### dominio: CONFIG_BACKUP
```
show configuration | display set | count
show system commit
show rollback 0 | count
```

### dominio: SERVICES
```
show configuration system services | display set
show configuration interfaces | display set | grep management
```

### dominio: SECURITY_POLICY
```
show security policies
show configuration security policies | display set
```

### dominio: TLS_PROFILES
```
show configuration security pki | display set
show ssl
show configuration system services web-management https | display set
```

### dominio: IPSEC
```
show security ike security-associations
show security ipsec security-associations
show configuration security ike | display set
show configuration security ipsec | display set
```

### dominio: INTERFACES
```
show interfaces terse
show lldp neighbors
show arp
```

---

## TABLA_SEVERIDAD (Juniper-específico)

| Condición | Severidad |
|-----------|-----------|
| Authentication-order = password (solo local) | Critical |
| Telnet habilitado (services telnet) | Critical |
| SNMP community "public" activa | High |
| Sin syslog host (remoto) | High |
| SSH protocol-version = v1 | High |
| Sin login message (banner) | Medium |
| NTP no configurado | Medium |
| Cluster out of sync | Critical |
| IKEv1 en security ike proposal | Medium |
| JunOS EOL / sin soporte activo | Critical |

---

## FORMATO_REMEDIACION (JunOS)

```
# WARNING: Revisar antes de aplicar. Probar en lab.
# Device: {hostname}  Framework: {fw}  Fecha: {date}

# BACKUP: request system snapshot

[edit]
# {CONTROL_ID}: {título}
set {remediation_cmd}

commit confirmed 5

# VERIFY: {verify_cmd}
# ROLLBACK: rollback 1 / commit
```
