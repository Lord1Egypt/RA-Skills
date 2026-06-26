# Evolution Audit

Modelar migraciones, versionado y auditoria de artefactos con foco en preservacion estructural.

## Migration as Adjunction

Elegir un operador dominante:

- `Delta` para reestructurar o renombrar preservando forma;
- `Sigma` para fusionar, generalizar o agregar aceptando posible perdida;
- `Pi` para restringir o especializar aceptando descarte.

Reportar siempre:

- morfismo estructural;
- operador elegido;
- propiedades preservadas;
- propiedades perdidas;
- riesgo de informacion.

## Audit Modes

- `STATIC` para schemas y DDLs;
- `TEMPORAL` para cadenas de version y migraciones;
- `BEHAVIORAL` para APIs y componentes observables;
- `KB_GLOBAL` para corpus, URNs y referencias;
- `DAL_INTEGRATED` para storage, API, ORM, repositorios y pipelines.

## Severity Scale

- `CRITICAL` invalida el artefacto;
- `HIGH` rompe integridad antes de produccion;
- `MEDIUM` es suboptimo pero recuperable;
- `LOW` es mejora incremental.

## Repair Patterns

- `BROKEN-DIAGRAM`
- `ORPHAN-OBJECT`
- `DANGLING-REF`
- `VERSION-MISMATCH`
- `NON-FUNCTORIAL`
- `REDUNDANT-BISIMILAR`

## Deepen Only If Needed

Ir a `kb-map.md` y cargar estas fuentes de solo lectura cuando haga falta:

- `schema-evolution.md` para evolucion temporal de esquemas;
- `audit-patterns.md` para catalogo de fallas y sintomas;
- `mbse-consistency.md` para consistencia entre modelos;
- `formal-framework-multimodel-data-transformations.md` si la migracion cruza modelos;
- `kb-category.md` cuando la auditoria recaiga sobre el corpus o sus URNs.

## Signature

```text
Modo: STATIC | TEMPORAL | BEHAVIORAL | KB_GLOBAL | DAL_INTEGRATED
Issues: ...
Patrones: ...
Migracion: Delta | Sigma | Pi | composicion
Riesgos: ...
```
