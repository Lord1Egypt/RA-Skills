---
name: memory-ops
description: >-
  Guia de operaciones de memoria para AuditCore v3.0. Define como usar el sistema
  de memoria nativo de OpenClaw: MEMORY.md (largo plazo), memory/ (diario),
  MEMORY/ (evidencia, reportes, inventarios, POA&M). Incluye patrones de escritura,
  busqueda en session-logs, y gestion de la base de conocimiento. Layer 0 opcional.
metadata:
  safety: read-only
  author: auditcore
  version: "1.0.0"
  openclaw: '{"emoji":"🧠","safetyTier":"read-only","requires":{"bins":[],"env":[]},"tags":["memory","knowledge","system","layer0"]}'
---

# Memory Operations Guide v1.0

## Estado de MemPalace

AVISO IMPORTANTE: En la sesion del 2026-04-16, el agente reporto haber implementado
MemPalace RAG. Eso fue una alucinacion — ningun comando real fue ejecutado.
No existe el CLI `mempalace`, ni la carpeta `knowledge_base/`, ni el skill
`llm-knowledge-lookup`. No confiar en esos reportes.

Sistema de memoria real disponible: ver secciones abajo.

## Sistema de Memoria Real (OpenClaw nativo)

OpenClaw tiene memoria persistente nativa en `~/.openclaw/memory/main.sqlite`.
Esta se accede automaticamente via las herramientas del agente.

### Capas de Memoria

| Capa | Donde | Proposito |
|------|-------|-----------|
| Contexto inmediato | Ventana del modelo | Sesion actual (se pierde al cerrar) |
| Memoria diaria | `workspace/memory/YYYY-MM-DD.md` | Logs crudos de sesion |
| Memoria largo plazo | `workspace/MEMORY.md` | Hechos curados, decisiones, contexto |
| Evidencia auditoria | `workspace/MEMORY/evidence/` | Outputs SHA-256, read-only |
| Reportes | `workspace/MEMORY/reports/` | HTMLs tecnicos y ejecutivos |
| Inventarios | `workspace/MEMORY/inventories/` | YAML por cliente/vendor |
| POA&M | `workspace/MEMORY/poam/` | Planes de accion y milestones |
| Memoria OpenClaw | `~/.openclaw/memory/main.sqlite` | Persistencia nativa de la plataforma |

## Patrones de Escritura a Memoria

### Cuando escribir a memory/YYYY-MM-DD.md (diario)
- Al final de cada sesion de auditoria
- Cuando se descubren hallazgos criticos
- Cuando se completa un reporte
- Cuando el operador da instrucciones importantes
- Cuando se comete un error (para no repetirlo)

### Cuando actualizar MEMORY.md (largo plazo)
- Nuevo assessment completado -> agregar a Assessment History
- Nueva decision de arquitectura
- Cambio de postura de cumplimiento de un cliente
- Aprendizaje que aplica a sesiones futuras

### Patron de entrada en MEMORY.md
```
## [Evento] — YYYY-MM-DD

**[Tipo]:** Cliente | Vendor | Fecha | Resultado
**Hallazgos clave:** lista breve
**Acciones pendientes:** con SLA
**Reportes generados:** rutas de archivos
```

## Busqueda en Historial de Sesiones

Para buscar en sesiones anteriores, usar el skill bundled `session-logs`:
"busca en mis sesiones anteriores informacion sobre [tema]"
"muestra el historial de auditorias de [cliente] F5"

## Alternativa a MemPalace (RAG real)

Si se necesita busqueda semantica real sobre documentacion tecnica en el futuro:
1. Instalar: `pip3 install sentence-transformers chromadb`
2. El script `/tmp/gen_index.py` puede extenderse para crear embeddings
3. Crear skill `semantic-search` que use chromadb como backend
4. Esto reemplazaria correctamente lo que Gemma4 prometio en abril 2026

Por ahora, la busqueda por palabras clave en session-logs cubre el 90% de los casos.
