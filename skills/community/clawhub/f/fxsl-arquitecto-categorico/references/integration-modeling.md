# Integration Modeling

Integrar fuentes heterogeneas sin perder trazabilidad estructural.

## Patrones Principales

### Grothendieck `int F`

Usar cuando el indice importa:

- federacion por sistema;
- multi-tenant;
- versiones temporales;
- zonas de data lake.

Definir:

- `I` como categoria indice;
- `F(i)` como schema por indice;
- `F(f)` como traduccion entre esquemas;
- `int F` como espacio global de objetos y morfismos.

### Multimodel

Usar cuando conviven SQL, documentos, grafos o key-value.

Normalizar cada fuente a un lenguaje comun:

- objetos: tablas, colecciones, nodos, keyspaces;
- morfismos: FKs, refs, edges, paths.

### Query as Functor

Tratar la consulta como un funtor desde el schema global al output deseado:

- relacional;
- documental;
- grafo;
- flat.

## Integration Procedure

1. Inventariar fuentes y decidir si el problema es indice, heterogeneidad o ambos.
2. Elegir entre federacion y esquema global consolidado.
3. Declarar equivalencias semanticas y wrappers por fuente.
4. Preservar proveniencia: origen, transformacion y criterio de equivalencia.

## Deepen Only If Needed

Ir a `kb-map.md` y cargar estas fuentes de solo lectura cuando haga falta:

- `cql-data-integration.md` para integracion functorial y CQL;
- `data-lakes-ct.md` y `formal-framework-data-lakes-ct.md` para lakes y zonas;
- `unified-multimodel.md` para unificacion multimodelo;
- `unified-representation-transformation-multimodel.md` para transformaciones entre modelos;
- `algebraic-model-management.md` o `multicategory-multimodel-query-processing.md` cuando la consulta o el cambio de modelo sea el problema central.

## Signature

```text
Fuentes: [...]
Metodo: Grothendieck | Multimodel | Ambos
Global Schema: ...
Wrappers: ...
Query target: ...
Proveniencia: completa | parcial
```
