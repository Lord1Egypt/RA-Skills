# Provenance

Esta skill fue reconstruida desde el agente fuente `AGENTS/fxsl/arquitecto-categorico` para que otro agente pueda adquirir la misma capacidad sin depender de un bootstrap dedicado.

## Fuentes Del Agente

- `AGENTS/fxsl/arquitecto-categorico/SOUL.md`
- `AGENTS/fxsl/arquitecto-categorico/AGENTS.md`
- `AGENTS/fxsl/arquitecto-categorico/TOOLS.md`
- `AGENTS/fxsl/arquitecto-categorico/USER.md`
- `AGENTS/fxsl/arquitecto-categorico/config.json`

## Motores Destilados En El Bundle

- `AGENTS/fxsl/arquitecto-categorico/skills/CM-STRUCTURE-ENGINE.md`
- `AGENTS/fxsl/arquitecto-categorico/skills/CM-BEHAVIOR-ENGINE.md`
- `AGENTS/fxsl/arquitecto-categorico/skills/CM-INTEGRATION-ENGINE.md`
- `AGENTS/fxsl/arquitecto-categorico/skills/CM-AUDIT-ENGINE.md`
- `AGENTS/fxsl/arquitecto-categorico/skills/CM-TENSION-EXPLORER.md`
- `AGENTS/fxsl/arquitecto-categorico/skills/CM-ARTIFACT-GENERATOR.md`
- `AGENTS/fxsl/arquitecto-categorico/skills/CM-DAL-ENGINE.md`
- `AGENTS/fxsl/arquitecto-categorico/skills/CM-MIGRATION-ENGINE.md`

## Corpus FXSL De Solo Lectura

El corpus esta incluido en `{baseDir}/references/kb`. La skill no modifica esos archivos.

- `{baseDir}/references/kb-map.md` indica que archivos leer segun el modo activo.
- Los playbooks del bundle son la guia operativa compacta.
- El corpus en `references/kb` es la autoridad teorica y de trazabilidad cuando se necesita mayor profundidad.

## Nota

El runtime normal debe cargar primero los playbooks del skill y solo despues los archivos del corpus que correspondan al problema.
