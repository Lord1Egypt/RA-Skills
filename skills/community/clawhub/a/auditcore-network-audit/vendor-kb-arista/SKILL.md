---
name: vendor-kb-arista
description: >-
  Knowledge Base de Arista Networks. Layer 1 — cargar al iniciar auditoría Arista,
  mantener hasta Fase 7. Contiene: dominios READ_COMMANDS (EOS CLI/eAPI),
  FORBIDDEN_COMMANDS, SEVERITY_MAP y REMEDIATION_FORMAT.
  Soporta EOS 4.2x.x y CloudVision Portal (CVP).
metadata:
  safety: read-only
  author: auditcore
  version: "2.0.0"
  openclaw: '{"emoji":"🟪","safetyTier":"read-only","requires":{"bins":["ssh"],"env":[]},"tags":["vendor-kb","arista","eos","cloudvision","cvp","layer1"]}'
---

# Vendor KB: Arista Networks

OS: EOS 4.2x.x | CloudVision Portal (CVP)
Access: SSH + CLI | eAPI (JSON/HTTP read-only)
HA: MLAG, BGP EVPN — evaluar peers

## COMANDOS_PROHIBIDOS
configure | conf t | write | copy run | no | reload | delete | debug | bash (excepto show bash)

---

## COMANDOS_LECTURA

### dominio: VERSION
```
show version
show inventory
show module
show platform
```

### dominio: HA_STATUS
```
show mlag
show mlag detail
show lacp
show spanning-tree
```

### dominio: ACCOUNTS
```
show running-config | section username
show users
show role
```

### dominio: AUTH_SOURCE
```
show running-config | section aaa
show running-config | section tacacs
show running-config | section radius
show aaa methods
```

### dominio: PASSWORD_POLICY
```
show running-config | include aaa root
show running-config | section security
```

### dominio: SESSION_TIMEOUT
```
show running-config | include exec-timeout
show running-config | section management ssh
```

### dominio: BANNER
```
show running-config | section banner
```

### dominio: SSH_HARDENING
```
show management ssh
show running-config | section management ssh
```

### dominio: HTTPS_CONFIG
```
show management api http-commands
show running-config | section management api
```

### dominio: LOGGING
```
show logging
show running-config | section logging
```

### dominio: NTP
```
show ntp status
show ntp associations
show running-config | section ntp
```

### dominio: SNMP
```
show snmp community
show snmp user
show running-config | section snmp-server
```

### dominio: CONFIG_BACKUP
```
show running-config checksum
show event-handler
show running-config | section eos-sdk
```

### dominio: SERVICES
```
show running-config | section management
show ip interface brief
```

### dominio: ACL
```
show ip access-lists
show running-config | section ip access-list
```

### dominio: TLS_PROFILES
```
show running-config | section ssl
show management security
```

### dominio: INTERFACES
```
show interfaces status
show lldp neighbors detail
show arp
```

---

## TABLA_SEVERIDAD (Arista-específico)

| Condición | Severidad |
|-----------|-----------|
| AAA no configurado (sin aaa new-model) | Critical |
| Telnet habilitado | Critical |
| eAPI habilitado en HTTP (sin HTTPS) | High |
| SNMP community "public" | High |
| Sin syslog remoto | High |
| exec-timeout = 0 | High |
| MLAG inconsistency | High |
| Sin banner login | Medium |
| NTP no configurado | Medium |
| CDP/LLDP en interfaces uplink con externos | Low |

---

## FORMATO_REMEDIACION (Arista EOS)

```
! WARNING: Revisar antes de aplicar. Probar en lab.
! Device: {hostname}  Framework: {fw}  Fecha: {date}

! BACKUP: copy running-config tftp://{server}/{hostname}-{date}.cfg

configure
   ! {CONTROL_ID}: {título}
   {remediation_cmd}
end
write memory

! VERIFY: {verify_cmd}
! ROLLBACK: configure / {rollback_cmd} / end / write memory
```
