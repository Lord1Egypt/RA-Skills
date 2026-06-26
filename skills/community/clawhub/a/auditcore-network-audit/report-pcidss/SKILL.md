---
name: report-pcidss
description: >-
  Report skill PCI DSS v4.0. Layer 3 — cargar DESPUÉS de fw-checks-pcidss.
  Lee findings-pcidss.json desde disco y genera: reporte HTML técnico por requisito,
  gap matrix, tabla de CVEs en scope PCI, resumen ejecutivo con estado IN PLACE / NOT IN PLACE.
metadata:
  safety: read-only
  author: auditcore
  version: "2.0.0"
  openclaw: '{"emoji":"📄","safetyTier":"read-only","requires":{"bins":[],"env":[]},"tags":["report","pci","pcidss","layer3","html"]}'
---

# Report Skill: PCI DSS v4.0

Este skill se carga DESPUÉS de la auditoría. Lee findings desde disco.
NO cargarlo durante la evaluación — reemplaza al framework-checks en contexto.

---

## Input

Leer desde disco: `MEMORY/assessments/{assessment_id}/findings-pcidss.json`

---

## Contexto PCI DSS

Los reportes PCI DSS deben estar listos para presentación a QSA (Qualified Security Assessor).
Cada hallazgo FAIL debe tener: evidencia, control específico del v4.0, y plan de remediación fechado.

---

## Estructura del Reporte HTML Técnico

### Sección 1 — Header PCI
- Título: "PCI DSS v4.0 — SAQ / ROC Assessment"
- Merchant/Service Provider: [cliente]
- Assessment scope: CDE + sistemas conectados
- Período de evaluación: [fecha]
- Assessor: AuditCore | QSA Reference: pendiente validación humana

### Sección 2 — Resumen de Requisitos

Tabla por requisito PCI (1–12):
```
| Req | Nombre                              | Controles | PASS | FAIL | Compliance |
|-----|-------------------------------------|-----------|------|------|------------|
| 1   | Network Security Controls           | [N]       | [N]  | [N]  | [X]%       |
| 2   | Secure Configurations               | [N]       | [N]  | [N]  | [X]%       |
| 4   | Cryptography in Transit             | [N]       | [N]  | [N]  | [X]%       |
| 6   | Vulnerability Management            | [N]       | [N]  | [N]  | [X]%       |
| 7   | Access Control                      | [N]       | [N]  | [N]  | [X]%       |
| 8   | Authentication                      | [N]       | [N]  | [N]  | [X]%       |
| 10  | Logging and Monitoring              | [N]       | [N]  | [N]  | [X]%       |
```

### Sección 3 — Hallazgos por Requisito

Para cada hallazgo FAIL/WARNING con formato PCI:
```
Req [X.X.X] — [Nombre del sub-requisito]
  Status: IN PLACE / NOT IN PLACE / NOT APPLICABLE
  Testing Procedure: [comando ejecutado]
  Evidence: [output sanitizado]
  Gap: [descripción de qué falta]
  Remediation Due: [fecha según SLA]
```

SLAs PCI DSS v4.0:
- Vulnerabilidades críticas: 1 mes
- Vulnerabilidades altas: 3 meses
- Media: 6 meses

### Sección 4 — Compensating Controls
Si algún control no puede implementarse exactamente:
Documentar control compensatorio propuesto con justificación.

### Sección 5 — CVEs en Scope PCI
Tabla de CVEs detectados en dispositivos dentro del CDE:
```
| CVE          | CVSS | Vendor | Versión afectada | Parche disponible | SLA vence |
|--------------|------|--------|------------------|-------------------|-----------|
| CVE-XXXX-XXX | 9.8  | F5     | TMOS 15.1.x      | Sí (17.x)         | 30 días   |
```

---

## Estructura del Reporte Ejecutivo HTML

1. Estado de compliance PCI: IN SCOPE / AT RISK / NON-COMPLIANT
2. Requisitos IN PLACE vs NOT IN PLACE (semáforo por req)
3. Riesgo de multas y consecuencias para el negocio (lenguaje ejecutivo)
4. Roadmap de remediación con fechas y responsables
5. Nota de disclaimer: "Este reporte es preparatorio — la validación oficial requiere QSA certificado"

---

## Archivos a Generar

```
MEMORY/reports/{client}/{assessment_id}/
├── report-pcidss-technical.html
├── report-pcidss-executive.html
├── report-pcidss-gap-matrix.html  ← tabla de gaps por req
├── poam-pcidss.md
└── remediation/
    ├── {req_id}-remediate.sh
    ├── {req_id}-rollback.sh
    └── {req_id}-verify.sh
```
