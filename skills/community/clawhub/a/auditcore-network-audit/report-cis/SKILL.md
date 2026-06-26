---
name: report-cis
description: >-
  Report skill CIS Controls v8. Layer 3 — cargar DESPUÉS de fw-checks-cis.
  Lee findings-cis.json desde disco y genera: reporte HTML técnico con score por control,
  tabla de Quick Wins priorizada (esfuerzo × impacto), resumen ejecutivo con IG level.
metadata:
  safety: read-only
  author: auditcore
  version: "2.0.0"
  openclaw: '{"emoji":"📄","safetyTier":"read-only","requires":{"bins":[],"env":[]},"tags":["report","cis","cis-v8","layer3","html"]}'
---

# Report Skill: CIS Controls v8

Este skill se carga DESPUÉS de la auditoría. Lee findings desde disco.
NO cargarlo durante la evaluación — reemplaza al framework-checks en contexto.

---

## Input

Leer desde disco: `MEMORY/assessments/{assessment_id}/findings-cis.json`

---

## Estructura del Reporte HTML Técnico

### Sección 1 — Header
- Título: "CIS Controls v8 — Implementation Assessment"
- Vendor + hostname + fecha
- CIS Implementation Group evaluado: IG1 (básico) / IG2 (empresa) / IG3 (avanzado)

### Sección 2 — Resumen por Control

Tabla de los 18 controles CIS:
```
| Control | Nombre                                    | Safeguards | PASS | FAIL | Score |
|---------|-------------------------------------------|------------|------|------|-------|
| 1       | Inventory and Control of Enterprise Assets| [N]        | [N]  | [N]  | [X]%  |
| 2       | Inventory and Control of Software Assets  | [N]        | [N]  | [N]  | [X]%  |
| 3       | Data Protection                           | [N]        | [N]  | [N]  | [X]%  |
| 4       | Secure Configuration                      | [N]        | [N]  | [N]  | [X]%  |
| 5       | Account Management                        | [N]        | [N]  | [N]  | [X]%  |
| 6       | Access Control Management                 | [N]        | [N]  | [N]  | [X]%  |
| 7       | Continuous Vulnerability Management       | [N]        | [N]  | [N]  | [X]%  |
| 8       | Audit Log Management                      | [N]        | [N]  | [N]  | [X]%  |
| 12      | Network Infrastructure Management         | [N]        | [N]  | [N]  | [X]%  |
| 13      | Network Monitoring and Defense            | [N]        | [N]  | [N]  | [X]%  |
```

### Sección 3 — Hallazgos Detallados

Para cada safeguard FAIL/WARNING:
```
CIS [X.X] — [Nombre del safeguard]
  Implementation Group: IG[1|2|3]
  Status: IMPLEMENTED / PARTIAL / NOT IMPLEMENTED
  Evidence: [output del comando]
  Gap: [descripción]
  Priority: [Essential/Foundational/Organizational]
```

### Sección 4 — Priorización por Quick Wins

Tabla ordenada por Esfuerzo (bajo→alto) × Impacto (alto→bajo):
```
| Safeguard | Esfuerzo | Impacto | Tiempo est. | Ganancia score |
|-----------|----------|---------|-------------|----------------|
| CIS 8.4   | Bajo     | Alto    | < 1h        | +5 puntos      |
| CIS 4.3   | Bajo     | Alto    | < 30min     | +5 puntos      |
| CIS 5.2   | Medio    | Alto    | 2h          | +5 puntos      |
```

---

## Estructura del Reporte Ejecutivo HTML

1. CIS Implementation Level actual: IG1 [X]% / IG2 [X]% / IG3 [X]%
2. Comparación con benchmark de la industria (si disponible)
3. Top 5 Quick Wins: remediaciones de bajo esfuerzo y alto impacto
4. Inversión estimada para alcanzar IG2 completo

---

## Archivos a Generar

```
MEMORY/reports/{client}/{assessment_id}/
├── report-cis-technical.html
├── report-cis-executive.html
├── report-cis-quickwins.html    ← tabla de quick wins priorizada
├── poam-cis.md
└── remediation/
    ├── cis-{x_x}-remediate.sh
    ├── cis-{x_x}-rollback.sh
    └── cis-{x_x}-verify.sh
```
