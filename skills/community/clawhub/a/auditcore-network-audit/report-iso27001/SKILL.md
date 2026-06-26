---
name: report-iso27001
description: >-
  Report skill ISO/IEC 27001:2022. Layer 3 — cargar DESPUÉS de fw-checks-iso27001.
  Lee findings-iso27001.json desde disco y genera: reporte HTML con NC Mayor/Menor/OBS,
  SoA parcial, registro de NCs, resumen ejecutivo de preparación para certificación.
metadata:
  safety: read-only
  author: auditcore
  version: "2.0.0"
  openclaw: '{"emoji":"📄","safetyTier":"read-only","requires":{"bins":[],"env":[]},"tags":["report","iso","iso27001","layer3","html"]}'
---

# Report Skill: ISO/IEC 27001:2022

Este skill se carga DESPUÉS de la auditoría. Lee findings desde disco.
NO cargarlo durante la evaluación — reemplaza al framework-checks en contexto.

---

## Input

Leer desde disco: `MEMORY/assessments/{assessment_id}/findings-iso27001.json`

---

## Contexto ISO 27001

Los reportes ISO 27001 deben estar alineados con la estructura del SGSI (Sistema de Gestión de Seguridad de la Información). El resultado es una declaración de no conformidades (NC) y observaciones (OBS) para el ISMS.

---

## Estructura del Reporte HTML Técnico

### Sección 1 — Header
- Título: "ISO/IEC 27001:2022 — Conformity Assessment"
- Organización: [cliente]
- Alcance del SGSI: [descripción del scope]
- Tipo de auditoría: Interna preparatoria (no oficial)

### Sección 2 — Resumen de Conformidad por Tema

Tabla de los 4 temas del Anexo A:
```
| Tema | Nombre                    | Controles | Conformes | NC Mayor | NC Menor | Obs |
|------|---------------------------|-----------|-----------|----------|----------|-----|
| 5    | Controles Organizacionales| [N]       | [N]       | [N]      | [N]      | [N] |
| 6    | Controles de Personas     | [N]       | [N]       | [N]      | [N]      | [N] |
| 7    | Controles Físicos         | [N]       | [N]       | [N]      | [N]      | [N] |
| 8    | Controles Tecnológicos    | [N]       | [N]       | [N]      | [N]      | [N] |
```

Clasificación de hallazgos ISO:
- **No Conformidad Mayor (NC Mayor):** Severity Critical/High → riesgo significativo
- **No Conformidad Menor (NC Menor):** Severity Medium → no cumple pero riesgo controlado
- **Observación (OBS):** Severity Low / WARNING → área de mejora recomendada

### Sección 3 — No Conformidades Detalladas

Para cada NC Mayor y Menor:
```
[Número de NC] — [A.X.XX] [Nombre del control]
  Tipo: [NC Mayor | NC Menor | Observación]
  Clausula ISO: [referencia exacta]
  Hallazgo: [descripción de la no conformidad]
  Evidencia: [output sanitizado]
  Riesgo: [impacto en el SGSI]
  Acción Correctiva Propuesta: [remediación]
  Fecha límite: [según SLA]
```

SLAs ISO 27001 (recomendados):
- NC Mayor: 30 días (antes de auditoría de certificación)
- NC Menor: 90 días
- Observación: 180 días

### Sección 4 — Declaración de Aplicabilidad (SoA) Parcial
Tabla de los controles técnicos evaluados con estado de aplicabilidad:
```
| Control | Nombre         | Aplicable | Status    | Justificación si N/A |
|---------|----------------|-----------|-----------|----------------------|
| A.8.15  | Logging        | Sí        | NC Menor  | —                    |
| A.8.24  | Cryptography   | Sí        | NC Mayor  | —                    |
```

---

## Estructura del Reporte Ejecutivo HTML

1. Estado de preparación para certificación ISO 27001: [LISTO / CON GAPS / NO LISTO]
2. Número de NC Mayores: [N] — impiden certificación hasta resolución
3. Número de NC Menores: [N] — deben resolverse en ciclo de mejora continua
4. Plan de acción correctiva: cronograma con responsables y fechas
5. Siguiente paso recomendado: auditoría interna formal / pre-certificación

---

## Archivos a Generar

```
MEMORY/reports/{client}/{assessment_id}/
├── report-iso27001-technical.html
├── report-iso27001-executive.html
├── report-iso27001-soa-partial.html  ← SoA de controles evaluados
├── report-iso27001-nc-register.html  ← Registro de NCs
├── poam-iso27001.md
└── remediation/
    ├── iso-{control_id}-remediate.sh
    ├── iso-{control_id}-rollback.sh
    └── iso-{control_id}-verify.sh
```
