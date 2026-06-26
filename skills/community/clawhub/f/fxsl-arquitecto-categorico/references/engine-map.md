# Engine Map

Usar este mapa para despachar la solicitud al playbook minimo.

## Dispatch Table

| Modo | Senal dominante | Leer primero | Leer despues | Salida principal |
|---|---|---|---|---|
| `static` | entidades, constraints, schema, DDL, tipos declarativos | `static-modeling.md` | `artifact-mappings.md` | modelo + DDL/schema/diagrama |
| `dynamic` | estado, transiciones, observaciones, API stateful, DAL | `dynamic-modeling.md` | `artifact-mappings.md` | modelo dinamico + API/DAL |
| `integration` | multiples fuentes, tenants, zonas, multimodelo, lake | `integration-modeling.md` | `artifact-mappings.md` | esquema global + wrappers/query |
| `audit` | diagnostico, drift, inconsistencias, versionado, deuda | `evolution-audit.md` | `kb-map.md` si audita corpus | informe por severidad |
| `consult` | duda teorica o justificativa | `kb-map.md` | uno o dos playbooks maximo | explicacion formal corta |

## Dispatch Rules

- Elegir `static` cuando el problema central sea un modelo declarativo o un schema.
- Elegir `dynamic` cuando importe el comportamiento observable mas que la estructura interna.
- Elegir `integration` cuando el reto sea componer o federar esquemas heterogeneos.
- Elegir `audit` cuando el usuario entregue artefactos existentes y pida diagnostico o migracion.
- Elegir `consult` cuando la salida principal sea una explicacion teorica y no un artefacto.

## Mode Hand-Offs

- Saltar de `static` a `dynamic` si aparecen estados, observaciones o efectos.
- Saltar de `dynamic` a `integration` si el comportamiento depende de multiples fuentes o modelos.
- Mantener `audit` si ya existe un artefacto; solo cambiar de modo para proponer la correccion.
- Entrar a `consult` solo para justificar o desambiguar; volver luego al modo operativo.

## Clarification Gate

Si faltan decisiones de alto impacto, leer `clarification-taxonomy.md` y preguntar una sola cosa:

- entidad vs evento
- SQL vs documento
- lens vs coalgebra vs monada
- federacion vs esquema global
- fusion vs restriccion

No emitir el artefacto final hasta colapsar esa tension.
