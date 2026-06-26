---
name: report-nist80053
description: >-
  Report skill NIST SP 800-53 Rev 5. Layer 3 — cargar DESPUÉS de fw-checks-nist80053,
  nunca simultáneo. Lee findings-nist80053.json desde disco y genera: reporte HTML técnico,
  resumen ejecutivo HTML, POA&M con SLAs, scripts remediate/rollback/verify por control.
metadata:
  safety: read-only
  author: auditcore
  version: "2.0.0"
  openclaw: '{"emoji":"📄","safetyTier":"read-only","requires":{"bins":[],"env":[]},"tags":["report","nist","800-53","layer3","html"]}'
---

# Report Skill: NIST SP 800-53 Rev 5

Este skill se carga DESPUÉS de la auditoría. Lee findings desde disco.
NO cargarlo durante la evaluación — reemplaza al framework-checks en contexto.

---

## Input

Leer desde disco: `MEMORY/assessments/{assessment_id}/findings-nist80053.json`

---

## Estructura del Reporte HTML Técnico

### Sección 1 — Header
- Título: "NIST SP 800-53 Rev 5 — Compliance Assessment"
- Vendor + hostname + IP + fecha
- Assessor: AuditCore | Organización: OXM Tech
- ID de assessment + SHA-256 del reporte
- Estado: CONFIDENTIAL

### Sección 2 — Executive Dashboard
Tabla de métricas globales:
```
| Controles evaluados | [N]      |
| ✅ PASS             | [N] [X]% |
| ❌ FAIL             | [N] [X]% |
| ⚠️ WARNING          | [N] [X]% |
| ➖ N/A              | [N] [X]% |
| Compliance Score    | [X]%     |
| Postura             | [DEFICIENT < 60% | PARTIAL 60-79% | COMPLIANT ≥ 80%] |
```

Gráfica de barras por familia (AC, AU, CM, IA, SC, SI) — usar CSS puro.

### Sección 3 — Top Hallazgos Críticos
Tabla con los 5-10 hallazgos de mayor riesgo:
```
| ID        | Control | Título                          | Severidad  | CVE          |
|-----------|---------|----------------------------------|------------|--------------|
| FIND-001  | IA-2    | Sin AAA centralizada             | 🔴 Critical | —            |
| FIND-002  | SC-8    | TLS 1.0 habilitado               | 🔴 Critical | CVE-XXXX     |
```

### Sección 4 — Hallazgos Detallados (por familia)
Para cada hallazgo en findings-nist80053.json:
```html
<div class="finding severity-{severity}">
  <h3>[control_id] — [title]</h3>
  <table>
    <tr><td>Status</td><td>[FAIL|WARNING|PASS|N/A]</td></tr>
    <tr><td>Severidad</td><td>[severity]</td></tr>
    <tr><td>Impacto negocio</td><td>[business_impact]</td></tr>
    <tr><td>Evidencia</td><td><code>[evidence]</code></td></tr>
    <tr><td>Comando</td><td><code>[command]</code></td></tr>
    <tr><td>Remediación</td><td><code>[remediation_cmd]</code></td></tr>
    <tr><td>CVE</td><td>[cve] CVSS [cvss]</td></tr>
  </table>
</div>
```

### Sección 5 — POA&M (Plan of Action & Milestones)
Tabla con SLAs por severidad:
```
| ID       | Control | Título | Severidad | SLA    | Fecha límite          | Owner |
|----------|---------|--------|-----------|--------|-----------------------|-------|
| FIND-001 | IA-2    | ...    | Critical  | 30 días | {fecha + 30 días}    | TBD   |
```

SLAs estándar NIST 800-53:
- Critical: 30 días
- High: 90 días
- Medium: 180 días
- Low: 365 días

### Sección 6 — Scripts de Remediación
Índice de scripts generados con links a archivos en `remediation/`:
```
remediation/{control_id}-remediate.sh
remediation/{control_id}-rollback.sh
remediation/{control_id}-verify.sh
```

---

## Estructura del Reporte Ejecutivo HTML

1. Resumen en 3 oraciones: qué se auditó, cuál es la postura, cuál es el riesgo principal
2. Semáforo de postura: 🔴 DEFICIENT / 🟡 PARTIAL / 🟢 COMPLIANT
3. Top 3 riesgos en lenguaje de negocio (sin tecnicismos)
4. Tabla de inversión: esfuerzo vs impacto por remediación crítica
5. Próximos pasos: 3 acciones concretas con fechas

---

## Archivos a Generar

```
MEMORY/reports/{client}/{assessment_id}/
├── report-nist80053-technical.html
├── report-nist80053-executive.html
├── poam-nist80053.md
└── remediation/
    ├── {control_id}-remediate.sh
    ├── {control_id}-rollback.sh
    └── {control_id}-verify.sh
```

---

## CSS — Clases de Severidad

```css
.severity-Critical { border-left: 4px solid #dc2626; background: #fef2f2; }
.severity-High     { border-left: 4px solid #f97316; background: #fff7ed; }
.severity-Medium   { border-left: 4px solid #eab308; background: #fefce8; }
.severity-Low      { border-left: 4px solid #22c55e; background: #f0fdf4; }
.severity-PASS     { border-left: 4px solid #16a34a; }
```
