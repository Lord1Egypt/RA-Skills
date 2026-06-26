# FXSL Corpus Map

Usar este mapa para cargar el corpus teorico de solo lectura bajo:

`{baseDir}/references/kb`

No editar esos archivos desde esta skill. Tratarlos como autoridad de dominio del workspace.

## Static Modeling

- `{baseDir}/references/kb/categorical-data-structures.md`
  Usar para schema como categoria, instancia como funtor y C-Sets.
- `{baseDir}/references/kb/constraint-logic.md`
  Usar para path equations, constraints y preservacion por migraciones.
- `{baseDir}/references/kb/action-primary-key.md`
  Usar cuando la identidad real sea la accion o el episodio.
- `{baseDir}/references/kb/seven-sketches.md`
  Usar para el modelo clasico de bases como funtores y Delta/Sigma/Pi.

## Dynamic Modeling

- `{baseDir}/references/kb/coalgebras.md`
  Usar para comportamiento observable, final coalgebra y bisimulacion.
- `{baseDir}/references/kb/categorical-systems-theory.md`
  Usar para lenses, sistemas dinamicos y wiring.
- `{baseDir}/references/kb/cognitive-toolkit.md`
  Usar cuando el problema mezcle agentes, episodios o razonamiento operacional.
- `{baseDir}/references/kb/data-access-layers.md`
  Usar cuando el foco sea storage/API/repository/ORM/pipeline.

## Integration and Lakes

- `{baseDir}/references/kb/cql-data-integration.md`
  Usar para integracion algebraica y CQL.
- `{baseDir}/references/kb/data-lakes-ct.md`
  Usar para enfoque categorico de lakes.
- `{baseDir}/references/kb/formal-framework-data-lakes-ct.md`
  Usar para formalizacion adicional de zonas y flujos.
- `{baseDir}/references/kb/unified-multimodel.md`
  Usar para unificacion de modelos heterogeneos.
- `{baseDir}/references/kb/unified-representation-transformation-multimodel.md`
  Usar para transformaciones entre representaciones.
- `{baseDir}/references/kb/algebraic-model-management.md`
  Usar cuando el cambio de modelo sea parte del problema.
- `{baseDir}/references/kb/multicategory-multimodel-query-processing.md`
  Usar si la consulta multimodelo es el centro.

## Evolution and Audit

- `{baseDir}/references/kb/schema-evolution.md`
  Usar para evolucion temporal de esquemas.
- `{baseDir}/references/kb/audit-patterns.md`
  Usar para sintomas y patrones de reparacion.
- `{baseDir}/references/kb/mbse-consistency.md`
  Usar para consistencia entre modelos y vistas.
- `{baseDir}/references/kb/formal-framework-multimodel-data-transformations.md`
  Usar para migraciones entre modelos distintos.
- `{baseDir}/references/kb/kb-category.md`
  Usar para auditar el propio corpus, URNs, manifests y relaciones.

## Meta and Foundations

- `{baseDir}/references/kb/algebraic-databases.md`
  Usar para profunctors, bimodules, Data double category y queries.
- `{baseDir}/references/kb/exploring-category-theoretic-approaches-to-databases.md`
  Usar para comparativas y contexto de bases.
- `{baseDir}/references/kb/mathematical-modelling.md`
  Usar para justificar la formalizacion matematica.

## Loading Rule

- Empezar siempre por un playbook del bundle.
- Cargar del corpus solo 1 a 3 archivos por turno.
- Preferir archivos directamente conectados con el modo activo.
- Si el pedido es teorico, cargar corpus primero y luego volver al playbook operativo minimo.
