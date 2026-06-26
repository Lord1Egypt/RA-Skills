# Dynamic Modeling

Modelar comportamiento, APIs stateful y DALs cuando la dinamica importa mas que la forma estatica.

## Decision Principal

Elegir una sola estructura dominante:

- `lens` para exponer y actualizar entre dos vistas;
- `coalgebra` para comportamiento observable y sustituibilidad;
- `monada` para efectos, fallo, no determinismo, estado o trazas.

## Lens

Usar `expose: S -> O` y `update: S x I -> S` cuando haya:

- CQRS o read model derivado;
- sincronizacion SQL a documento;
- interfaces que leen y reescriben el mismo estado.

## Coalgebra

Usar `c: U -> F(U)` cuando haya:

- servicios reactivos;
- objetos con estado oculto;
- componentes que deban compararse por comportamiento externo.

Verificar bisimulacion si la pregunta real es sustituibilidad.

## Monada

Usar una monada dominante si el sistema se organiza por efecto:

- `Maybe` para fallo;
- `List` para no determinismo;
- `Dist` para probabilidad;
- `State` para estado mutable;
- `Writer` para trazabilidad y auditoria.

## DAL Guidance

- `SQL` cuando mandan limites, integridad y joins;
- `NoSQL` cuando mandan colimites, fusion y flexibilidad;
- `Mixto` cuando conviene un lens asimetrico entre write model y read model.

Tratar:

- la API como un funtor del dominio al estilo de interfaz elegido;
- el repository como coalgebra;
- el ORM como adjuncion cuyo drift aparece cuando el round-trip deja de aproximar identidad.

## Deepen Only If Needed

Ir a `kb-map.md` y cargar estas fuentes de solo lectura cuando haga falta:

- `coalgebras.md` para comportamiento, final coalgebra y bisimulacion;
- `categorical-systems-theory.md` para lenses, wiring diagrams y sistemas dinamicos;
- `cognitive-toolkit.md` si la interfaz modela episodios, agentes o reasoning operacional;
- `data-access-layers.md` cuando el foco real sea la DAL;
- `action-primary-key.md` si la accion estructura la identidad del sistema.

## Signature

```text
Subsistema: Lens | Coalgebra | Monada
Estados/Observaciones: ...
Persistencia: SQL | NoSQL | Mixto
API: REST | GraphQL | gRPC | Streams
Sustituibilidad: verificada | pendiente
```
