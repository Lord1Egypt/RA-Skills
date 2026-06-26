# Clarification Taxonomy

Usar este archivo cuando una sola decision estructural pueda cambiar el artefacto final.

## Rule

- Detectar la tension dominante.
- Formular una sola pregunta socratica.
- No emitir el artefacto final hasta recibir el colapso.

## A1 Ser

- entidad vs evento
  Pregunta: `Lo modelamos como cosa persistente o como algo que ocurre?`
- token vs type
  Pregunta: `Necesitas individuos concretos o una clase reusable?`
- todo vs partes
  Pregunta: `Priorizamos el agregado global o los componentes con autonomia?`

## A2 Devenir

- estatico vs dinamico
  Pregunta: `El foco es la estructura declarativa o el comportamiento en el tiempo?`
- secuencial vs paralelo
  Pregunta: `El flujo se compone paso a paso o por ramas concurrentes?`
- determinista vs probabilistico
  Pregunta: `La transicion debe ser unica o admite distribucion de resultados?`

## A3 Conocer

- conocido vs desconocido
  Pregunta: `La ausencia es un dato valido o debe prohibirse?`
- explicito vs tacito
  Pregunta: `La regla debe quedar declarada en el schema o solo observarse en el comportamiento?`

## A4 Expresar

- SQL vs documento
  Pregunta: `Priorizamos integridad por joins o flexibilidad por agregados?`
- formal vs informal
  Pregunta: `Necesitas especificacion ejecutable o una explicacion conceptual?`
- compacto vs verboso
  Pregunta: `Conviene un artefacto minimo o una salida con trazabilidad expandida?`

## Escalation

Si hay varias tensiones, preguntar primero por la que cambie:

- identidad;
- cardinalidad;
- limite vs colimite;
- operador de migracion;
- formato de salida.
