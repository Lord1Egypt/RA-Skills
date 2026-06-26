---
name: vendor-kb-fortinet
description: >-
  Knowledge Base de Fortinet. Layer 1 — cargar al iniciar auditoría Fortinet, mantener
  hasta Fase 7. Contiene: dominios READ_COMMANDS (FortiOS CLI/API), FORBIDDEN_COMMANDS,
  SEVERITY_MAP y REMEDIATION_FORMAT. Soporta FortiOS 6.x/7.x, FortiManager, FortiAnalyzer.
metadata:
  safety: read-only
  author: auditcore
  version: "2.0.0"
  openclaw: '{"emoji":"🟥","safetyTier":"read-only","requires":{"bins":["ssh"],"env":[]},"tags":["vendor-kb","fortinet","fortigate","fortios","layer1"]}'
---

# Vendor KB: Fortinet FortiGate

OS: FortiOS 6.x / 7.x | FortiManager / FortiAnalyzer
Access: SSH + CLI | REST API (read-only token)
HA: Active-Passive / Active-Active — evaluar ambos nodos

## COMANDOS_PROHIBIDOS
config | set | unset | delete | execute | diag sys reboot | diag debug reset

---

## COMANDOS_LECTURA

### dominio: VERSION
```
get system status
get hardware status
diagnose sys flash list
```

### dominio: HA_STATUS
```
get system ha status
diagnose sys ha checksum show
diagnose sys ha dump-by vcluster
```

### dominio: ACCOUNTS
```
show system admin
get system admin
show system accprofile
```

### dominio: AUTH_SOURCE
```
show user tacacs+
show user radius
show user ldap
show user setting
get user setting
```

### dominio: PASSWORD_POLICY
```
show system password-policy
get system password-policy
```

### dominio: SESSION_TIMEOUT
```
get system global | grep admintimeout
show system global | grep admintimeout
```

### dominio: BANNER
```
get system global | grep pre-login-banner
get system global | grep post-login-banner
show system global | grep banner
```

### dominio: SSH_HARDENING
```
get system global | grep admin-ssh
show system interface | grep allowaccess
get system interface | grep allowaccess
```

### dominio: HTTPS_CONFIG
```
get system global | grep admin-https
get system global | grep admin-http
```

### dominio: LOGGING
```
show log syslogd setting
show log syslogd2 setting
get log syslogd setting
get log setting
```

### dominio: NTP
```
show system ntp
get system ntp
```

### dominio: SNMP
```
show system snmp sysinfo
show system snmp community
show system snmp user
get system snmp community
```

### dominio: CONFIG_BACKUP
```
get system backup | grep schedule
diagnose sys confsync status
```

### dominio: SERVICES
```
get system global | grep admin-sport
show system service
show firewall policy | grep action
```

### dominio: FIREWALL_POLICY
```
show firewall policy
get firewall policy
show firewall address
```

### dominio: TLS_PROFILES
```
show firewall ssl-ssh-profile
get vpn ssl settings | grep cipher
show vpn ssl settings
```

### dominio: IPSEC
```
show vpn ipsec phase1-interface
show vpn ipsec phase2-interface
get vpn ipsec tunnel summary
```

### dominio: INTERFACES
```
get system interface physical
diagnose ip address list
```

---

## TABLA_SEVERIDAD (Fortinet-específico)

| Condición | Severidad |
|-----------|-----------|
| Auth source = local (sin TACACS+/RADIUS) | Critical |
| HTTP admin acceso habilitado | High |
| SNMP v1/v2 community "public" activa | High |
| admintimeout = 0 (nunca expira) | High |
| Sin syslog remoto configurado | High |
| Política "permit any any" activa | High |
| SSH acceso desde any en interface WAN | High |
| Sin pre-login-banner | Medium |
| NTP no configurado | Medium |
| FortiOS fuera de soporte (EOL) | Critical |
| IKEv1 en VPN IPsec | Medium |

---

## FORMATO_REMEDIACION (FortiOS CLI)

```
# WARNING: Revisar antes de aplicar. Probar en lab.
# Device: {hostname}  Framework: {fw}  Fecha: {date}

# BACKUP ANTES:
# execute backup config ftp {server} {path}

config system global
    # {CONTROL_ID}: {título}
    set {remediation_cmd}
end

# VERIFY: {verify_cmd}
# ROLLBACK: config system global / set {rollback_cmd} / end
```
