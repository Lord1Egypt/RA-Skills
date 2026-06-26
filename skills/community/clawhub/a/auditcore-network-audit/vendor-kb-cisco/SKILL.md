---
name: vendor-kb-cisco
description: >-
  Knowledge Base de Cisco. Layer 1 — cargar al iniciar auditoría Cisco, mantener
  hasta Fase 7. Contiene: dominios READ_COMMANDS (IOS/IOS-XE/NX-OS/ACI),
  FORBIDDEN_COMMANDS, SEVERITY_MAP y REMEDIATION_FORMAT.
  Soporta: IOS, IOS-XE, IOS-XR, NX-OS, ACI/APIC.
metadata:
  safety: read-only
  author: auditcore
  version: "2.0.0"
  openclaw: '{"emoji":"🟦","safetyTier":"read-only","requires":{"bins":["ssh"],"env":[]},"tags":["vendor-kb","cisco","ios","ios-xe","nxos","aci","layer1"]}'
---

# Vendor KB: Cisco

OS: IOS / IOS-XE / IOS-XR / NX-OS / ACI (APIC)
Access: SSH + CLI | ACI: REST API read-only
HA: StackWise, VSS, vPC, NSF/SSO — evaluar ambos miembros activos

## COMANDOS_PROHIBIDOS
conf t | configure | write | copy run | no | reload | erase | delete | format | debug (excepto show debug)

---

## COMANDOS_LECTURA

### dominio: VERSION
```
show version
show inventory
show platform
show module
```

### dominio: HA_STATUS
```
show redundancy
show standby
show vss status
show vpc
```

### dominio: ACCOUNTS
```
show running-config | section username
show aaa local user lockout
show users
```

### dominio: AUTH_SOURCE
```
show running-config | section aaa
show running-config | section tacacs
show running-config | section radius
show aaa servers
```

### dominio: PASSWORD_POLICY
```
show aaa local user blocked
show running-config | include security password
show running-config | include login block-for
show running-config | include login delay
```

### dominio: SESSION_TIMEOUT
```
show running-config | include exec-timeout
show running-config | section line vty
show running-config | section line con
```

### dominio: BANNER
```
show running-config | section banner
```

### dominio: SSH_HARDENING
```
show ip ssh
show running-config | section ip ssh
show ssh
```

### dominio: HTTPS_CONFIG
```
show running-config | include ip http
show running-config | section ip http
```

### dominio: LOGGING
```
show logging
show running-config | section logging
show running-config | include logging host
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
show running-config | section snmp
```

### dominio: CONFIG_BACKUP
```
show archive
show running-config | include archive
```

### dominio: SERVICES
```
show running-config | include service
show control-plane
show ip interface brief
```

### dominio: ACL
```
show access-lists
show running-config | section ip access-list
show ip access-lists
```

### dominio: TLS_PROFILES
```
show ssl
show running-config | include ssl
show running-config | include crypto pki
```

### dominio: IPSEC
```
show crypto isakmp sa
show crypto ipsec sa
show running-config | section crypto
```

### dominio: INTERFACES
```
show interfaces
show cdp neighbors detail
show lldp neighbors detail
```

---

## TABLA_SEVERIDAD (Cisco-específico)

| Condición | Severidad |
|-----------|-----------|
| AAA not configured (aaa new-model ausente) | Critical |
| Telnet habilitado en VTY (transport input telnet) | Critical |
| HTTP server habilitado sin HTTPS | High |
| SNMP v1/v2 con community "public" | High |
| SSH versión 1 | High |
| exec-timeout = 0 0 (nunca expira) | High |
| Sin logging host (sin syslog remoto) | High |
| Sin enable secret (solo enable password) | High |
| Banner MOTD ausente | Medium |
| NTP no configurado | Medium |
| CDP habilitado en interfaces externas | Medium |

---

## FORMATO_REMEDIACION (Cisco IOS/IOS-XE)

```
! WARNING: Revisar antes de aplicar. Probar en lab primero.
! Device: {hostname}  Framework: {fw}  Fecha: {date}

! BACKUP ANTES:
! copy running-config tftp://{server}/{hostname}-backup-{date}.cfg

configure terminal
 ! {CONTROL_ID}: {título}
 {remediation_cmd}
end

! VERIFY:
! {verify_cmd}

! ROLLBACK:
! {rollback_cmd}
```
