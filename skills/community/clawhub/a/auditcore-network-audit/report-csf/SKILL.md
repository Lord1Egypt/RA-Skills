---
name: report-csf
description: >-
  Report skill NIST CSF 2.0. Layer 3 — cargar DESPUÉS de fw-checks-csf.
  Lee findings-csf.json desde disco y genera: reporte HTML técnico con radar chart por función,
  resumen ejecutivo con Tier de madurez (1-4), roadmap hacia siguiente Tier.
metadata:
  safety: read-only
  author: auditcore
  version: "2.0.0"
  openclaw: '{"emoji":"📄","safetyTier":"read-only","requires":{"bins":[],"env":[]},"tags":["report","nist","csf","layer3","html"]}'
---

# Report Skill: NIST CSF 2.0

Este skill se carga DESPUÉS de la auditoría. Lee findings desde disco.
NO cargarlo durante la evaluación — reemplaza al framework-checks en contexto.

---

## Input

Leer desde disco: `MEMORY/assessments/{assessment_id}/findings-csf.json`

---

## Estructura del Reporte HTML Técnico

### Sección 1 — Header
- Título: "NIST Cybersecurity Framework 2.0 — Posture Assessment"
- Vendor + hostname + fecha
- Nivel de madurez objetivo: Tier 1–4

### Sección 2 — Scorecard por Función CSF

Tabla de las 6 funciones:
```
| Función  | Subcategorías | PASS | FAIL | WARNING | Score | Tier estimado |
|----------|---------------|------|------|---------|-------|---------------|
| GOVERN   | [N]           | [N]  | [N]  | [N]     | [X]%  | Tier [1-4]    |
| IDENTIFY | [N]           | [N]  | [N]  | [N]     | [X]%  | Tier [1-4]    |
| PROTECT  | [N]           | [N]  | [N]  | [N]     | [X]%  | Tier [1-4]    |
| DETECT   | [N]           | [N]  | [N]  | [N]     | [X]%  | Tier [1-4]    |
| RESPOND  | [N]           | [N]  | [N]  | [N]     | [X]%  | Tier [1-4]    |
| RECOVER  | [N]           | [N]  | [N]  | [N]     | [X]%  | Tier [1-4]    |
```

CSF Tiers de Madurez:
- Tier 1 (Partial): < 40% — Procesos ad-hoc, no formalizados
- Tier 2 (Risk Informed): 40–59% — Algunos procesos definidos
- Tier 3 (Repeatable): 60–79% — Procesos establecidos y practicados
- Tier 4 (Adaptive): ≥ 80% — Mejora continua integrada

### Sección 3 — Radar Chart
Gráfica de araña (radar) con SVG puro mostrando score por función.

### Sección 4 — Hallazgos Detallados por Función

Para cada hallazgo FAIL/WARNING:
```
[Función] → [Subcategoría ID] — [Nombre]
  Status: [PASS|FAIL|WARNING|N/A]
  Evidence: [output]
  Gap: [descripción]
  CSF Reference: [link a la subcategoría en NIST]
```

---

## Estructura del Reporte Ejecutivo HTML

1. Tier actual del dispositivo: Tier [1-4] — [nombre]
2. Radar chart de madurez por función (visual)
3. Brecha vs Tier objetivo del cliente
4. Top 3 áreas de mejora inmediata
5. Roadmap hacia Tier [N+1]: acciones específicas y timeframes

---

## Archivos a Generar

```
MEMORY/reports/{client}/{assessment_id}/
├── report-csf-technical.html
├── report-csf-executive.html
└── remediation/
    ├── csf-{subcategory}-remediate.sh
    └── csf-{subcategory}-rollback.sh
```
