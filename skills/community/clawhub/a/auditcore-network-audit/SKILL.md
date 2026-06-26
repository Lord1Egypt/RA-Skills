---
name: auditcore-network-audit
description: >-
  AuditCore — Suite completa de auditoría de seguridad para infraestructura de red.
  Cubre 6 vendors (F5, Cisco, Fortinet, Palo Alto, Juniper, Arista), 5 frameworks
  (NIST 800-53, NIST CSF 2.0, CIS Controls v8, PCI DSS v4.0, ISO 27001:2022),
  generación automática de scripts de remediación con rollback, reportes HTML
  ejecutivos y técnicos, y diagnóstico de salud de infraestructura.
  Arquitectura en capas (Layer 0→1→2→3) optimizada para ventanas de contexto reducidas.
metadata:
  safety: read-only
  author: auditcore
  version: "2.0.0"
  openclaw: >-
    {"emoji":"🛡️","safetyTier":"read-only","tags":["audit","network","compliance","nist","cis","pcidss","iso27001","f5","cisco","fortinet","paloalto","juniper","arista"]}
---

# AuditCore — Network Security Audit Suite v2.0

Suite completa de auditoría de ciberseguridad para infraestructura de red crítica.
Diseñada para OpenClaw con gestión de contexto por capas.

---

## Arquitectura de Capas

```
Layer 0 — Siempre cargado (constitución + router)
  system-methodology    → 7 fases, reglas de oro, formato de hallazgos
  system-index          → Routing vendor→skill, framework→skill, rutas de memoria
  memory-ops            → Gestión del sistema de memoria (opcional)

Layer 1 — Un vendor a la vez (F1 → F7 completo)
  vendor-kb-f5          → F5 BIG-IP TMOS 13.x-17.x, VELOS, XC
  vendor-kb-cisco       → Cisco IOS / IOS-XE / NX-OS / ACI
  vendor-kb-fortinet    → Fortinet FortiOS 6.x/7.x
  vendor-kb-paloalto    → Palo Alto PAN-OS 9.x/10.x/11.x + Panorama
  vendor-kb-juniper     → Juniper JunOS 18.x-23.x (SRX, QFX, EX, MX)
  vendor-kb-arista      → Arista EOS 4.2x / CloudVision

Layer 2 — Un framework a la vez (cargar → evaluar → descargar)
  fw-checks-nist80053   → NIST SP 800-53 Rev 5 (~187 controles, 20 familias)
  fw-checks-csf         → NIST CSF 2.0 (6 funciones, ~40 subcategorías)
  fw-checks-cis         → CIS Controls v8 (18 controles, 153 safeguards)
  fw-checks-pcidss      → PCI DSS v4.0 (~89 controles técnicos, 12 requisitos)
  fw-checks-iso27001    → ISO/IEC 27001:2022 (Anexo A temas 5, 6, 8)

Layer 3 — Reemplaza Layer 2 en Fase 6 (generación de reportes)
  report-nist80053      → Reporte NIST 800-53: dashboard ejecutivo + POA&M + scripts
  report-csf            → Reporte CSF 2.0: radar chart + scorecard + maturity tier
  report-cis            → Reporte CIS v8: HTML técnico + quick wins + scripts
  report-pcidss         → Reporte PCI DSS: gap matrix + CVE CDE scope + QSA-ready
  report-iso27001       → Reporte ISO 27001: SoA parcial + NC register + cert readiness

Skills especializados (cargar según necesidad):
  audit-diag-health     → Diagnóstico de salud para los 6 vendors (health + logs)
  audit-auto-generate   → Auto-genera skills para vendors sin KB pre-construido
  tools-secops          → Inventario de herramientas SecOps locales instaladas
  community-cybersec-index → Router hacia 754 skills comunitarios de ciberseguridad
```

---

## Cómo Usar Esta Suite

### Inicio de sesión (siempre)
```
Cargar: system-methodology + system-index
```

### Auditoría de un dispositivo
```
1. Cargar vendor-kb-{vendor}                    → Layer 1 activo
2. Cargar fw-checks-{framework}                 → Layer 2 activo
3. Ejecutar checks → guardar findings-{fw}.json → disco
4. Descargar fw-checks-{framework}              → Layer 2 vacío
5. Cargar report-{framework}                    → Layer 3 activo
6. Leer findings desde disco → generar reporte  → Layer 3 vacío
7. Repetir pasos 2-6 para cada framework
8. Descargar vendor-kb-{vendor}                 → ciclo completo
```

### Diagnóstico rápido
```
Cargar: audit-diag-health (cubre todos los vendors)
```

### Vendor sin KB pre-construido
```
Cargar: audit-auto-generate
```

### Operaciones fuera de red (forensics, threat intel, cloud, etc.)
```
Cargar: community-cybersec-index → identifica skill específico
Nota: Requiere instalar la librería comunitaria por separado.
```

---

## Frameworks Cubiertos

| Framework | Skills | Alcance |
|-----------|--------|---------|
| NIST SP 800-53 Rev 5 | fw-checks-nist80053 + report-nist80053 | ~187 controles, familias AC/AU/CM/IA/SC/SI |
| NIST CSF 2.0 | fw-checks-csf + report-csf | 6 funciones: GOVERN/IDENTIFY/PROTECT/DETECT/RESPOND/RECOVER |
| CIS Controls v8 | fw-checks-cis + report-cis | 18 controles, 153 safeguards |
| PCI DSS v4.0 | fw-checks-pcidss + report-pcidss | ~89 controles técnicos, 12 requisitos |
| ISO/IEC 27001:2022 | fw-checks-iso27001 + report-iso27001 | Anexo A: temas 5, 6, 8 |

---

## Vendors Soportados

| Vendor | KB | OS/Platform |
|--------|----|-------------|
| F5 Networks | vendor-kb-f5 | BIG-IP TMOS 13.x–17.x, VELOS, XC |
| Cisco | vendor-kb-cisco | IOS, IOS-XE, IOS-XR, NX-OS, ACI |
| Fortinet | vendor-kb-fortinet | FortiOS 6.x/7.x |
| Palo Alto Networks | vendor-kb-paloalto | PAN-OS 9.x/10.x/11.x, Panorama |
| Juniper Networks | vendor-kb-juniper | JunOS 18.x–23.x (SRX, QFX, EX, MX) |
| Arista Networks | vendor-kb-arista | EOS 4.2x, CloudVision |
| Cualquier otro vendor | audit-auto-generate | Auto-generación dinámica |

---

## Reglas de Oro

1. **READ-ONLY** — Nunca ejecutar comandos de escritura en producción
2. **EVIDENCIA REAL** — Nunca inventar ni asumir output de comandos
3. **N/A sobre PASS falso** — Sin evidencia = N/A, nunca PASS
4. **CREDENCIALES EFÍMERAS** — Nunca persistir en disco
5. **HA WORST-CASE** — Resultado del cluster = peor miembro individual
6. **CONFIRMACIÓN SIEMPRE** — Resumen de hallazgos antes de generar reportes
7. **SCRIPTS SOLO REVISIÓN** — Generar scripts, nunca auto-ejecutar

---

## Gestión de Contexto

| Layer | Skills | ~Tokens | Vigencia |
|-------|--------|---------|----------|
| 0 | system-methodology + system-index | ~2,400 | Siempre |
| 1 | vendor-kb-{vendor} | ~1,500 | F1 → F7 |
| 2 | fw-checks-{framework} | ~1,200 | Un framework a la vez |
| 3 | report-{framework} | ~800 | Reemplaza Layer 2 en F6 |

Pico máximo de contexto: ~5,100 tokens (sin community skills).
