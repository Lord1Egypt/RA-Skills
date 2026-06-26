---
name: vendor-kb-paloalto
description: >-
  Knowledge Base de Palo Alto Networks. Layer 1 — cargar al iniciar auditoría PA, mantener
  hasta Fase 7. Contiene: dominios READ_COMMANDS (PAN-OS CLI/API), FORBIDDEN_COMMANDS,
  SEVERITY_MAP y REMEDIATION_FORMAT. Soporta PAN-OS 9.x/10.x/11.x y Panorama.
metadata:
  safety: read-only
  author: auditcore
  version: "2.0.0"
  openclaw: '{"emoji":"🟧","safetyTier":"read-only","requires":{"bins":["ssh"],"env":[]},"tags":["vendor-kb","paloalto","panos","panorama","layer1"]}'
---

# Vendor KB: Palo Alto Networks

OS: PAN-OS 9.x / 10.x / 11.x | Panorama (centralizado)
Access: SSH + CLI | REST API (read-only API key)
HA: Active/Passive, Active/Active — evaluar ambos nodos

## COMANDOS_PROHIBIDOS
set | delete | rename | move | commit | revert | request system reboot | debug

---

## COMANDOS_LECTURA

### dominio: VERSION
```
show system info
show system resources
show system disk-space
```

### dominio: HA_STATUS
```
show high-availability state
show high-availability all
show high-availability transitions
```

### dominio: ACCOUNTS
```
show admins all
show config running | match admin
show user account-locked-out
```

### dominio: AUTH_SOURCE
```
show config running | match authentication-profile
show config running | match server-profile
show authentication setting
```

### dominio: PASSWORD_POLICY
```
show config running | match password-complexity
show config running | match minimum-password-complexity
```

### dominio: SESSION_TIMEOUT
```
show config running | match idle-timeout
show config running | match max-session
```

### dominio: BANNER
```
show config running | match login-banner
show config running | match motd
```

### dominio: SSH_HARDENING
```
show config running | match ssh
show system setting
show config running | match management-interface
```

### dominio: HTTPS_CONFIG
```
show config running | match permitted-ip
show config running | match interface management
```

### dominio: LOGGING
```
show config running | match syslog
show log-settings profile
show config running | match log-forwarding
```

### dominio: NTP
```
show config running | match ntp
show ntp
```

### dominio: SNMP
```
show config running | match snmp
show config running | match v3-user
```

### dominio: CONFIG_BACKUP
```
show config saved
show jobs all | match export
show system setting management
```

### dominio: SERVICES
```
show config running | match services
show system setting
```

### dominio: SECURITY_POLICY
```
show running security-policy
show config running | match security rule
```

### dominio: TLS_PROFILES
```
show config running | match ssl-tls-service-profile
show config running | match protocol-settings
show config running | match min-version
```

### dominio: IPSEC
```
show vpn ike-sa
show vpn ipsec-sa
show config running | match ike-crypto-profile
show config running | match ipsec-crypto-profile
```

### dominio: INTERFACES
```
show interface all
show arp all
show lldp neighbors all
```

---

## TABLA_SEVERIDAD (Palo Alto-específico)

| Condición | Severidad |
|-----------|-----------|
| Sin authentication-profile en admin accounts | Critical |
| Management interface accesible desde any | Critical |
| Syslog no configurado | High |
| HA no sincronizado | High |
| SNMP v2c community "public" | High |
| idle-timeout = 0 | High |
| Regla de seguridad "any any allow" activa | Critical |
| SSL/TLS min-version = tls1-0 | High |
| Sin login banner | Medium |
| NTP sin configurar | Medium |
| IKEv1 en crypto profile | Medium |

---

## FORMATO_REMEDIACION (PAN-OS CLI)

```
# WARNING: Revisar antes de aplicar. Probar en lab.
# Device: {hostname}  Framework: {fw}  Fecha: {date}

# BACKUP: scp export configuration from {hostname} to {server}

# {CONTROL_ID}: {título}
set {remediation_cmd}
commit

# VERIFY: {verify_cmd}
# ROLLBACK: set {rollback_cmd} / commit
```
