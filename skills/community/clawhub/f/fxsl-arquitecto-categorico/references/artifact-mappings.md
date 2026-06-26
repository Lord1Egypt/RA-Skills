# Artifact Mappings

Usar este archivo despues de fijar el modelo categorico para elegir y emitir el artefacto target.

## Mapping Table

| Categorico | PostgreSQL | GraphQL | OpenAPI | JSON Schema | Prisma | Mermaid | PlantUML |
|---|---|---|---|---|---|---|---|
| objeto | tabla | `type` | `components.schemas.*` | `object` | `model` | nodo o entity | class/entity |
| morfismo | `FOREIGN KEY` | field tipado | `$ref` o relation path | `$ref` | `@relation` | edge | arrow |
| identidad | `PRIMARY KEY` | `id: ID!` | propiedad requerida | propiedad requerida | `@id` | etiqueta clave | atributo clave |
| limite | `JOIN`, `CHECK`, `UNIQUE` | nested type o campo derivado | `allOf` | `allOf` | `@@unique` | subgrafo conmutativo | asociacion estructurada |
| colimite | `UNION`, merge | `union` | `oneOf` | `oneOf` | patron explicito | union de ramas | jerarquia o merge |

## Emission Rules

- Emitir `PostgreSQL DDL` cuando la integridad, las FKs y los joins sean la prioridad.
- Emitir `JSON Schema` u `OpenAPI` cuando el target sea intercambio o contrato de API.
- Emitir `GraphQL SDL` cuando el dominio se consuma por navegacion tipada.
- Emitir `Prisma` cuando el usuario quiera un schema ORM declarativo.
- Emitir `Mermaid` o `PlantUML` cuando la mejor salida sea un diagrama.

## Traceability Rules

- Agregar comentarios categoricos solo si aclaran una construccion no trivial.
- En SQL o Prisma, anotar pullbacks, pushouts o equalizers cerca de la definicion relevante.
- En JSON Schema y OpenAPI, usar una nota breve fuera del bloque cuando el formato no soporte comentarios claros.
- En auditorias, no mezclar trazabilidad inline con el codigo; separar hallazgos y correcciones.

## Required Note

Declarar `Functor Information Loss` cuando el formato target no pueda expresar:

- path equations importantes;
- proveniencia;
- comportamiento observable;
- equivalencias semanticas entre fuentes.
