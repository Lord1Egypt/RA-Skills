---
name: audit-diag-health
description: >-
  Diagnóstico y troubleshooting de infraestructura de red. Cubre los 6 vendors
  pre-construidos (F5, Cisco, Fortinet, Palo Alto, Juniper, Arista) en una sola
  carga. Tres dominios por vendor: HEALTH_STATUS (salud general del equipo),
  LOGS_CONTROL_PLANE (eventos de sistema, auth, routing, config changes),
  LOGS_DATA_PLANE (sesiones, tráfico, drops, NAT, contadores de interfaz).
  Usar junto con vendor-kb activo. NO es un framework de cumplimiento.
metadata:
  safety: read-only
  author: auditcore
  version: "1.0.0"
  openclaw: '{"emoji":"🩺","safetyTier":"read-only","requires":{"bins":["ssh"],"env":[]},"tags":["diag","health","logs","troubleshooting","control-plane","data-plane","all-vendors"]}'
---

# AuditCore — Diagnóstico de Salud y Logs

> **Uso:** Activar cuando el usuario solicite troubleshooting, estado de salud,
> logs, errores, latencia, drops, o cualquier diagnóstico operacional.
> Usar la sección correspondiente al vendor ya cargado en Layer 1.

---

## REGLA DE USO

1. Identificar vendor activo (ya debe estar cargado `vendor-kb-{vendor}`)
2. Ir a la sección `## [VENDOR]` de este skill
3. Ejecutar los dominios en orden: HEALTH_STATUS → CONTROL_PLANE → DATA_PLANE
4. Registrar evidencia en `MEMORY/evidence/{assessment_id}/{hostname}/diag/`
5. Presentar resumen en tabla antes de mostrar comandos al usuario

---

## FORMATO DE SALIDA DIAGNÓSTICO

Para cada dominio ejecutado, presentar:

```
🩺 HEALTH CHECK — [VENDOR] [hostname]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 HEALTH STATUS
  CPU:       [%] [NORMAL/ALTO/CRÍTICO]
  Memoria:   [%] [NORMAL/ALTO/CRÍTICO]
  Uptime:    [días/horas]
  HA State:  [ACTIVE/STANDBY/STANDALONE/DEGRADADO]
  HW Alerts: [NONE/lista]

📋 CONTROL PLANE — últimas anomalías
  [timestamp] [evento significativo]
  ...

📡 DATA PLANE — estado de tráfico
  Sesiones activas: [N]
  Drops (último intervalo): [N]
  Interfaces con errores: [lista o NONE]
  ...

⚠️ HALLAZGOS OPERACIONALES
  [CRÍTICO/ALTO/MEDIO/INFO] — [descripción]
```

---

## UMBRALES DE ALERTA

| Métrica | NORMAL | ALTO | CRÍTICO |
|---------|--------|------|---------|
| CPU | < 70% | 70–89% | ≥ 90% |
| Memoria | < 75% | 75–89% | ≥ 90% |
| Drops/seg | 0 | 1–100 | > 100 |
| Auth failures | 0 | 1–4 | ≥ 5 en 5 min |
| Interface errors | 0 | 1–99 | ≥ 100 |
| HA state | ACTIVE o STANDBY | — | UNKNOWN / DISCONNECTED |

---

---

## 🔵 F5 NETWORKS (BIG-IP TMOS / VELOS / F5 XC)

### dominio: HEALTH_STATUS
```bash
# Versión y uptime
tmsh show sys version
tmsh show sys uptime

# Recursos del sistema
tmsh show sys performance all-stats
tmsh show sys cpu
tmsh show sys memory

# Hardware y alertas
tmsh show sys hardware
tmsh show sys alert
tmsh show sys message

# Estado HA / Cluster
tmsh show cm sync-status
tmsh show cm failover-status
tmsh show cm device all
tmsh show cm traffic-group all

# Servicios activos
tmsh show sys service
tmsh show sys daemon-log-settings all

# Interfaces
tmsh show net interface all
tmsh show net trunk all
tmsh show net vlan all
```

### dominio: LOGS_CONTROL_PLANE
```bash
# Logs del sistema LTM (últimas 200 líneas)
tail -200 /var/log/ltm

# Eventos de autenticación y acceso
tail -200 /var/log/secure
tail -200 /var/log/audit
grep -i "login\|logout\|failed\|denied\|root" /var/log/secure | tail -50

# Cambios de configuración
grep -i "mcpd\|config\|modify\|create\|delete" /var/log/audit | tail -50

# Daemon y sistema
tail -100 /var/log/daemon.log
tail -100 /var/log/cron

# APM (si licenciado)
tail -100 /var/log/apm

# GTM / DNS (si licenciado)
tail -50 /var/log/gtm

# mcpd (config daemon — errores críticos)
grep -i "err\|crit\|emerg\|alert" /var/log/mcpd.out | tail -50

# Eventos de HA / failover
grep -i "failover\|sync\|standby\|active\|disconn" /var/log/ltm | tail -50

# VELOS específico
cat /var/F5/partition1/log/platform.log 2>/dev/null | tail -100
```

### dominio: LOGS_DATA_PLANE
```bash
# Estado de VIPs y pools
tmsh show ltm virtual all
tmsh show ltm pool all
tmsh show ltm node all

# Conexiones activas
tmsh show sys connection count
tmsh show sys connection cs-server-addr <VIP_IP>

# Tablas ARP y rutas
tmsh show net arp all
tmsh show net route all

# Estadísticas de tráfico por interfaz
tmsh show net interface all field-fmt | grep -E "name|in-packets|out-packets|in-errors|out-errors|drops"

# Drops y resets
grep -iE "reset|drop|timeout|conn_limit|reject" /var/log/ltm | tail -100

# SSL/TLS — handshake failures
grep -i "ssl\|tls\|handshake\|cert" /var/log/ltm | tail -50

# iRules errors
grep -i "irule\|tcl\|error" /var/log/ltm | tail -50

# Throughput instantáneo
tmsh show sys performance throughput
```

---

---

## 🟦 CISCO (IOS / IOS-XE / NX-OS / ACI)

### dominio: HEALTH_STATUS
```
show version
show inventory
show environment all
show platform
show processes cpu sorted
show processes memory sorted
show interfaces status
show redundancy
show redundancy states
show module
show chassis
show ip interface brief
show cdp neighbors detail
```

### dominio: LOGS_CONTROL_PLANE
```
show logging
show logging last 200
show logging | include Error|OSPF|BGP|EIGRP|AUTH|failed|down|up
show aaa authentication statistics
show users
show archive log config all
show ip ospf neighbor
show ip bgp summary
show ip eigrp neighbors
show isis neighbors
show spanning-tree summary
show vtp status

# NX-OS específico
show system internal sysmgr service all
show install all status
show ntp status

# ACI específico (en APIC)
moquery -c faultInst -f 'fault.Inst.severity=="critical"'
```

### dominio: LOGS_DATA_PLANE
```
show interfaces
show interfaces counters errors
show ip traffic
show ip nat translations total
show ip nat statistics
show access-lists
show ip route summary
show ip cef summary
show etherchannel summary
show mac address-table count
show arp

# NX-OS específico
show hardware rate-limiter
show system internal forwarding l2 internal drop statistics
show forwarding inconsistency

# Performance
show policy-map interface
show queue interface
```

---

---

## 🟥 FORTINET (FortiOS 6.x / 7.x)

### dominio: HEALTH_STATUS
```
get system status
get hardware status
get system performance status
diagnose hardware sysinfo memory
diagnose hardware sysinfo cpu
get system ha status
diagnose sys top 3 20
diagnose debug crashlog read
get system interface physical
diagnose netlink interface list
diagnose sys session stat
```

### dominio: LOGS_CONTROL_PLANE
```
# Logs del sistema (últimos eventos)
execute log filter category 1
execute log filter start-line 1
execute log display

# Eventos de administración / config
execute log filter category 3
execute log display

# Auth y usuarios
execute log filter category 0
execute log filter field action login
execute log display

# Estado de routing
get router info routing-table all
diagnose ip router ospf all
diagnose ip bgp all summary
diagnose ip bgp neighbor
get router info bgp summary

# NTP y sincronización
diagnose sys ntp status
get system ntp

# Config changes recientes
get system history admin
```

### dominio: LOGS_DATA_PLANE
```
# Sesiones activas
diagnose sys session list | head -100
diagnose sys session stat
diagnose sys session filter dport 443
diagnose sys session filter proto 6

# Contadores de interfaz
diagnose netlink interface list
diagnose hardware deviceinfo nic <interfaz>

# Firewall policy hits
diagnose firewall iprope show 100004
get firewall policy

# NAT
diagnose firewall ippool-all list
diagnose firewall fnatp list

# Drops y anomalías
diagnose ips anomaly list
diagnose autoupdate status
diagnose debug flow filter daddr <IP_DESTINO>

# BGP / Routing data plane
diagnose ip router bgp all
get router info routing-table all
```

---

---

## 🟧 PALO ALTO (PAN-OS 9.x / 10.x / 11.x / Panorama)

### dominio: HEALTH_STATUS
```
show system info
show system resources
show system disk-space
show system environmentals
show high-availability state
show high-availability state-synchronization
show chassis-ready
show interface all
show routing summary
show session info
show system software status
show jobs all
```

### dominio: LOGS_CONTROL_PLANE
```
# Logs del sistema
show log system direction equal backward
show log system direction equal backward subtype equal auth
show log config direction equal backward

# Usuarios admin activos
show admins
show admins all

# Estado de routing protocols
show routing protocol bgp peer
show routing protocol bgp summary
show routing protocol ospf state
show routing protocol ospf neighbor

# Actualizaciones y licencias
show system updates
show license

# HA events
show log system direction equal backward subtype equal ha

# Certificados
show certificate-info
show ssl-cert-cache-stats
```

### dominio: LOGS_DATA_PLANE
```
# Sesiones activas
show session all
show session meter
show session info

# Drops y contadores
show counter global filter delta yes severity drop
show counter global filter delta yes severity error
show counter interface all

# Políticas y hits
show running security-policy
show running nat-policy

# Rutas y forwarding
show routing fib
show routing route

# Amenazas (último ciclo)
show log threat direction equal backward

# URL filtering
show log url direction equal backward

# Interface errors
show interface ethernet1/1
show interface management
```

---

---

## 🟩 JUNIPER (JunOS 18.x–23.x / SRX / QFX / MX)

### dominio: HEALTH_STATUS
```
show system uptime
show version
show chassis hardware
show chassis routing-engine
show chassis environment
show chassis fpc
show chassis power
show system alarms
show redundancy summary
show interfaces terse
show system storage
show system processes extensive | head -30
show system memory
```

### dominio: LOGS_CONTROL_PLANE
```
# Log del sistema (últimos 200)
show log messages | last 200
show log messages | match "error|Error|Err|warn|WARN|fail|FAIL" | last 100

# Comandos ejecutados (audit trail)
show log interactive-commands | last 100

# Autenticación y usuarios
show log auth | last 100
show system users

# Config changes
show system commit
show system commit detail

# Routing protocols
show bgp summary
show bgp neighbor
show ospf overview
show ospf neighbor
show isis adjacency
show mpls lsp

# HA / NSRP / ISSU
show chassis cluster status
show chassis cluster interfaces
show reth interfaces
```

### dominio: LOGS_DATA_PLANE
```
# Estadísticas de interfaz
show interfaces statistics detail
show interfaces extensive | match "error|drops|Input|Output" | head -50

# Tabla de rutas y forwarding
show route summary
show route forwarding-table summary

# Sesiones SRX
show security flow session summary
show security flow statistics
show security flow statistics extensive

# Firewall filter counters
show firewall filter

# PFE stats (packet forwarding engine)
show pfe statistics traffic
show pfe statistics error

# NAT SRX
show security nat source summary
show security nat destination summary
show security nat interface

# ARP y vecinos
show arp
show lldp neighbors

# Drops
show security flow session destination-prefix <IP>
```

---

---

## 🟪 ARISTA (EOS 4.2x.x / CloudVision CVP)

### dominio: HEALTH_STATUS
```
show version
show inventory
show system environment all
show system environment temperature
show system environment power
show system environment fans
show processes top once
show processes memory
show interface status
show interface counters
show redundancy status
show bgp summary
show spanning-tree summary
```

### dominio: LOGS_CONTROL_PLANE
```
# Buffer de logs del sistema
show logging
show logging last 200
show logging | include ERR|WARN|OSPF|BGP|AUTH|failed|down|up

# Autenticación y acceso
show aaa authentication
show users

# Config changes (si EOS ≥ 4.23)
show running-config diffs
show change-control pending

# Routing protocols
show ip bgp summary
show ip bgp neighbors
show ip ospf neighbor
show ip ospf
show isis neighbors

# NTP
show ntp status
show ntp associations

# CVP específico
show cvp info
show cvp status

# MLAG
show mlag
show mlag detail
```

### dominio: LOGS_DATA_PLANE
```
# Contadores de errores por interfaz
show interfaces counters errors
show interfaces counters rates

# Tráfico IP
show ip traffic
show ip route summary

# NAT (si configurado)
show ip nat translations
show ip nat statistics

# ACLs y hits
show ip access-lists
show mac address-table count

# Sesiones (si firewall EOS)
show ip security connections
show ip security flows

# Colas y drops
show queue-monitor length
show queue-monitor congestion

# ARP
show arp

# VxLAN
show vxlan vtep
show vxlan address-table
show bgp evpn summary
```

---

## INTERPRETACIÓN RÁPIDA

### Señales de Alarma Inmediata (escalar)

| Señal | Vendor | Significado |
|-------|--------|-------------|
| `sync failed` / `sync error` | F5 | HA desincronizado — riesgo de failover inesperado |
| `STANDBY DISCONNECTED` | F5/PA/Cisco | Nodo HA sin comunicación |
| `CPU > 90%` | Todos | Riesgo de packet drops y timeouts |
| `memory usage > 90%` | Todos | Riesgo de OOM y reboot inesperado |
| `login failed` repetido | Todos | Posible brute force o cuenta comprometida |
| `configuration changed` sin ticket | Todos | Cambio no autorizado — revisar audit trail |
| `interface down` inesperado | Todos | Falla de enlace o media error |
| `route flap` frecuente | Cisco/Juniper/Arista | Inestabilidad de routing |
| `session table full` | F5/PA/Fortinet | DoS o mal dimensionamiento |
| `CRL expired` / `cert expired` | F5/PA | Certificados vencidos — SSL roto |

---

## SALIDA RECOMENDADA PARA EL USUARIO

Después de recolectar evidencia, presentar:

```
📊 RESUMEN DE SALUD — [VENDOR] [hostname] — [fecha]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OVERALL: [🟢 SALUDABLE / 🟡 ADVERTENCIA / 🔴 CRÍTICO]

┌─────────────────────────────────────────────────┐
│ METRIC              VALUE    STATUS              │
│ CPU Usage           XX%      🟢/🟡/🔴            │
│ Memory Usage        XX%      🟢/🟡/🔴            │
│ Uptime              Xd Xh    🟢                  │
│ HA State            ACTIVE   🟢/🔴               │
│ HW Alarms           NONE     🟢/🔴               │
│ Interface Errors    X        🟢/🟡/🔴            │
│ Auth Failures (1h)  X        🟢/🟡/🔴            │
│ Session Table       XX%      🟢/🟡/🔴            │
│ Data Plane Drops    X/s      🟢/🟡/🔴            │
└─────────────────────────────────────────────────┘

⚠️ ANOMALÍAS DETECTADAS:
  [si hay] 🔴 CRÍTICO — descripción + timestamp + log line
  [si hay] 🟡 ADVERTENCIA — descripción
  [si no]  ✅ Ninguna anomalía detectada

📁 Evidencia guardada en:
   MEMORY/evidence/{assessment_id}/{hostname}/diag/
```
