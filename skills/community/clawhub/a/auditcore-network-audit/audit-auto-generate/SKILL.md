---
name: audit-auto-generate
description: >-
  Auto-genera skills de auditoría para cualquier vendor o plataforma sin skill
  pre-construido: dispositivos de red desconocidos, sistemas operativos servidor
  (Ubuntu, RHEL, Windows Server, Debian, Rocky Linux, etc.), plataformas cloud
  (AWS, Azure, GCP), contenedores (Docker, Kubernetes) o cualquier otro objetivo.
  Investiga documentación, genera checks mapeados al framework, valida estructura,
  y persiste el nuevo skill tras aprobación del usuario.
metadata:
  safety: read-only
  author: auditcore
  version: "1.0.0"
  openclaw: '{"emoji":"🔧","safetyTier":"read-only","requires":{"bins":["ssh"],"env":[]},"tags":["auto-generate","vendor","skill","dynamic"]}'
---

# AuditCore — Auto-Generación de Skills para Vendors Desconocidos

Este skill se activa cuando el usuario solicita auditar un vendor que no
tiene skill pre-construido en la biblioteca. El proceso es:

1. Investigar documentación del vendor
2. Generar mapeo de controles
3. Obtener aprobación del usuario
4. Persistir skill en disco
5. Ejecutar auditoría con el skill recién creado

---

## Cuándo Activar Este Skill

Activar cuando el objetivo solicitado NO tiene skill pre-construido. Los skills disponibles son:

**Dispositivos de red:**
```
skills/vendor-kb-f5/        → F5 BIG-IP / TMOS / VELOS
skills/vendor-kb-cisco/     → Cisco IOS / NX-OS / ACI
skills/vendor-kb-fortinet/  → Fortinet FortiOS
skills/vendor-kb-paloalto/  → Palo Alto PAN-OS
skills/vendor-kb-juniper/   → Juniper JunOS
skills/vendor-kb-arista/    → Arista EOS
```

**Todo lo demás activa este skill:**
- Servidores Linux (Ubuntu, RHEL, CentOS, Debian, Rocky, Alma, Kali…)
- Servidores Windows (Windows Server, IIS, Active Directory…)
- Cloud Platforms (AWS, Azure, GCP…)
- Contenedores y orquestación (Docker, Kubernetes, OpenShift…)
- Cualquier otro vendor o plataforma desconocida

---

## Proceso de Generación

### Fase 1 — Research del Vendor

Investigar y extraer:

1. **CLI Reference**
   - Comandos de lectura disponibles (`show`, `get`, `display`, `list`)
   - Comandos prohibidos (write, configure, delete, reload)
   - Formato de salida (texto plano, JSON, XML)
   - Versiones de OS soportadas

2. **API REST** (si existe)
   - Endpoint base
   - Autenticación (token, basic, session)
   - Endpoints de configuración de solo lectura
   - Rate limits relevantes

3. **Benchmarks Disponibles**
   - Verificar si existe CIS Benchmark oficial para el vendor
   - Buscar STIG/NIST guidance específico del vendor
   - Documentación de hardening del fabricante

4. **CVEs Conocidos**
   - Últimos 12 meses, CVSS ≥ 7.0
   - Advisory URL del fabricante
   - Versiones afectadas

---

### Fase 2 — Mapeo de Controles

Para cada framework solicitado, generar checks con esta estructura:

```yaml
control:
  id: "[NIST/CIS/PCI/ISO control ID]"
  name: "[Nombre del control]"
  command: "[comando read-only de verificación]"
  pass_condition: "[condición para PASS]"
  fail_condition: "[condición para FAIL]"
  remediation: "[comando de corrección]"
  rollback: "[comando de rollback]"
  severity: "[Critical/High/Medium/Low]"
  evidence_type: "[cli_output/api_response/config_file]"
```

**Dominios mínimos a cubrir por framework:**

| Dominio | NIST 800-53 | CIS v8 | PCI DSS | ISO 27001 |
|---------|------------|--------|---------|-----------|
| Autenticación | IA-2, IA-5 | 5.2 | 8.2, 8.3 | A.5.17 |
| Acceso remoto | AC-17 | 12.7 | 2.2.7 | A.6.7 |
| Sesiones | AC-12 | 4.3 | 8.1.8 | A.8.1 |
| Logging | AU-2, AU-8 | 8.2 | 10.2 | A.8.15 |
| Config baseline | CM-2 | 4.1 | 2.2 | A.8.9 |
| Versión/Parches | SI-2 | 7.3 | 6.3.3 | A.8.8 |
| Cifrado | SC-8, SC-13 | 3.10 | 4.2.1 | A.8.24 |
| SNMP/Servicios | CM-7 | 4.8 | 2.2.4 | A.8.9 |
| Banner/AC-8 | AC-8 | — | — | A.5.17 |

---

### Fase 3 — Estructura del Skill Generado

El skill generado se persiste como:

```
skills/audit-[vendor-slug]/
└── SKILL.md
```

**Formato del SKILL.md generado:**

```markdown
---
name: audit-[vendor-slug]
description: >-
  [Descripción generada automáticamente]
metadata:
  safety: read-only
  author: auditcore-autogen
  version: "1.0.0-autogen"
  generated: "[fecha ISO]"
  confidence: "auto-generated — validar en primera ejecución"
---

# AuditCore — [VENDOR] Assessment (Auto-Generated)

⚠️ Este skill fue generado automáticamente. Los checks son funcionales
pero pueden requerir ajuste fino tras la primera ejecución real.

## Platform Scope

[tabla de plataformas, OS, y métodos de acceso]

## Safety Rule

[lista de comandos permitidos y prohibidos]

## CLI Commands — [VENDOR] Read-Only

[por cada dominio: comando + check de evaluación]

## Control Framework Mapping

[tabla de mapeo vendor-específico]

## Severity Classification

[tabla de hallazgos comunes y su severidad]

## Remediation Script Format

[ejemplo de script con rollback]

## Advisory Source

[URL oficial de avisos de seguridad del vendor]
```

---

### Fase 4 — Validaciones Pre-Aprobación

Antes de mostrar el skill al usuario para aprobación, ejecutar:

1. **Validación estructural:** ¿Todos los campos requeridos presentes?
2. **Validación de contenido:** ¿Los comandos son read-only? (verificar contra lista de verbos peligrosos)
3. **Validación de seguridad:** ¿No hay comandos que modifiquen configuración?
4. **Validación de cobertura:** ¿Al menos 5 dominios cubiertos?

**Verbos prohibidos en comandos generados:**
```
create, modify, delete, save, load, write, configure, set,
install, upgrade, downgrade, reload, reboot, shutdown, reset,
rm, mv, chmod, chown, dd
```

Si algún check falla → corregir antes de mostrar al usuario.

---

### Fase 5 — Flujo de Aprobación

```
¿Apruebas el skill? *(sí / editar / rechazar)*
```

**Si "sí":**
- Persistir `SKILL.md` en `skills/audit-[vendor-slug]/`
- Confirmar persistencia
- Continuar con flujo normal de auditoría

**Si "editar":**
- Preguntar qué cambiar específicamente
- Aplicar cambios
- Volver a mostrar el skill actualizado
- Repetir aprobación

**Si "rechazar":**
- "Entendido. No guardé el skill. Puedes pedirme intentarlo de nuevo
  con diferentes parámetros cuando quieras."
- No ejecutar auditoría

---

## Notas de Confianza

Los skills auto-generados llevan una marca de confianza:

| Confianza | Condición |
|-----------|-----------|
| ⚠️ auto-generated | Primera versión, sin ejecución real validada |
| ✅ validado | Ejecutado al menos una vez exitosamente |
| ✅✅ maduro | Múltiples ejecuciones, ajustes aplicados |

La marca se actualiza en el frontmatter del SKILL.md después de cada ejecución exitosa.
