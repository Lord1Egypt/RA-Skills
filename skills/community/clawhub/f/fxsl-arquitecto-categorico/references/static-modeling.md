# Static Modeling

Formalizar dominios como categorias y emitir artefactos declarativos sin contaminar el modelo con logica procedimental.

## Modelo Minimo

Definir siempre:

- objetos: entidades, tipos o agregados;
- morfismos: relaciones tipadas, atributos funcionales o referencias;
- identidades: `id_A` por objeto;
- composicion: cadenas `g o f`;
- path equations: restricciones que deben conmutar.

## Construcciones Universales

Usar limites cuando importe integridad y composicion fuerte:

- producto para combinacion estructural;
- pullback para joins por clave comun;
- equalizer para exigir igualdad de dos caminos.

Usar colimites cuando importe fusion o flexibilidad:

- coproducto para union tipada;
- pushout para merge por parte comun;
- coequalizer para identificar equivalencias.

## Decision Procedure

1. Identificar si el dominio es de entidades persistentes, eventos o ambos.
2. Elegir si el target favorece limites fuertes o colimites flexibles.
3. Expresar restricciones como path equations antes de pensar en columnas o campos.
4. Emitir el schema solo cuando la categoria ya este fijada.

## Tensiones Tipicas

- entidad vs evento;
- token vs type;
- SQL vs documento;
- todo vs partes;
- formal vs informal.

Si alguna tension cambia llaves, cardinalidades o fronteras del esquema, pedir una sola aclaracion.

## Deepen Only If Needed

Ir a `kb-map.md` y cargar estas fuentes de solo lectura cuando haga falta justificar el diseno:

- `categorical-data-structures.md` para schema como categoria e instancia como funtor;
- `constraint-logic.md` para restricciones, monomorfismos, epimorfismos y auditoria de theories;
- `action-primary-key.md` si la identidad real esta en la accion y no en el estado;
- `seven-sketches.md` para migraciones functoriales y uso clasico de limites/colimites.

## Signature

```text
Categoria: C_dom
Obj: {...}
Morph: {...}
Path Equations: [...]
Construcciones: [...]
Artefacto target: ...
```
