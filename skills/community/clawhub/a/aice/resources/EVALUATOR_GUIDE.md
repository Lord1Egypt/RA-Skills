# AICE Evaluator Guide — Para Agentes que Evalúan Sub-Agentes

> **Audiencia:** Arquitectos y otros agentes que evalúan el trabajo de su equipo.
> **NO es para:** Agentes ejecutores (backend, frontend, etc.) — ellos no evalúan a nadie.

---

## Tu Rol como Evaluador

Eres parte de la **cadena de evaluación** de AICE:

```
Sergio (humano) → evalúa → ComPi
ComPi            → evalúa → Arquitectos (tú, si eres arquitecto)
Arquitectos      → evalúan → Backend, Frontend, DataEng, Tester
```

Cuando revisas el output de un sub-agente, **debes evaluar** su trabajo y registrar el resultado.

---

## Qué Evaluar

### Dominios

| # | Dominio | Código | Qué mide en el sub-agente |
|---|---------|--------|---------------------------|
| 1 | 🔧 Ejecución técnica | `TECH` | ¿El código/output es correcto? ¿Funciona? |
| 2 | ⚙️ Disciplina operativa | `OPS` | ¿Siguió las instrucciones? ¿Respetó formatos/convenciones? |
| 3 | 🧠 Criterio y visión | `JUDGMENT` | ¿Tomó buenas decisiones? ¿Anticipó problemas? |
| 4 | 💬 Comunicación | `COMMS` | ¿Reportó claramente? ¿Preguntó cuando debía? |
| 5 | 🎯 Orquestación | `ORCH` | Solo si el sub-agente coordina a otros (raro en equipo base) |

### Resultados

| Resultado | Cuándo | Efecto |
|-----------|--------|--------|
| `correct` | Output cumple criterios de aceptación | +streak en el dominio |
| `error` | Output incorrecto o incompleto | −delta según severidad, streak reset |

### Severidades de Error

| Severidad | Delta | Cuándo |
|-----------|:-----:|--------|
| 🟡 Leve | −1 | Detalle menor, no afecta funcionalidad |
| 🟠 Medio | −3 | Error funcional corregible, omisión parcial |
| 🔴 Grave | −5 | Error importante, no funciona, spec ignorada |
| ⚫ Crítico | −10 | Fallo total o reincidencia del mismo error |

---

## Cómo Evaluar (Paso a Paso)

### 1. Revisa el output del sub-agente

Aplica tus criterios de aceptación. ¿Cumple? ¿Tiene errores?

### 2. Determina resultado, dominio y severidad

```
output_correcto  → result: "correct", domain: TECH (o el que aplique)
output_con_error → result: "error", domain: TECH, severity: "medio"
```

### 3. Actualiza el confidence.json del sub-agente

Archivo: `skills/aice/agents/<agent-id>/confidence.json`

```
Lectura: Lee el archivo
Actualización:
  Si correct:
    domain.streak += 1 (max 10)
    domain.evaluations += 1
    domain.score += delta_por_racha (ver tabla abajo)
  Si error:
    domain.streak = 0
    domain.evaluations += 1
    domain.corrections += 1
    domain.score += delta_severidad (negativo)
    Respetar dailyCap por dominio
  
  Recalcular globalScore = avg(domain.score * weight) / sum(weights)
  Actualizar maturity.individualEvaluations = sum(all domain.evaluations)
  Actualizar updatedAt
```

**Tabla de racha (acumulado):**

| Streak | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|--------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:--:|
| Delta  | 0 | 0 | 0 |+1 |+1 |+2 |+2 |+2 |+2 | +2 |

**Daily caps (durante warmup):** +15 positivo / −30 negativo por dominio.
**Daily caps (normal, tras 40 evals):** +10 positivo / −20 negativo por dominio.

### 4. Escribe en confidence-log.jsonl del sub-agente

Archivo: `skills/aice/agents/<agent-id>/confidence-log.jsonl`

Append una línea:
```json
{"id":"eval_YYYYMMDD_NNN","timestamp":"2026-02-24T14:00:00Z","domain":"TECH","result":"correct","severity":null,"delta":0,"scoreBefore":50,"scoreAfter":50,"streakBefore":0,"streakAfter":1,"evaluatedBy":"architect-aice","task":"Implementar endpoint /api/users","note":"Código correcto, tests pasan"}
```

### 5. Recalcula pool-index.json

Archivo: `skills/aice/pool-index.json`

```
Para el pool del sub-agente (ej: sonnet-4-5|high):
  1. Leer todos los confidence.json de miembros activos del pool
  2. poolScore = Σ(agent.globalScore × agent.totalEvals) / Σ(agent.totalEvals)
  3. Por cada dominio: poolDomainScore[d] = Σ(agent.domains[d].score × agent.domains[d].evaluations) / Σ(agent.domains[d].evaluations)
  4. poolMaturity.totalEvaluations = Σ(member.individualEvaluations)
  5. Recalcular tier (GREEN ≤100, JUNIOR ≤500, ESTABLISHED ≤2000, MATURE >2000)
  6. Recalcular confidenceInterval = 25 / sqrt(totalEvaluations)
  7. Actualizar lastUpdated
```

---

## Cuándo Evaluar

- **Cada vez que revisas un entregable** de un sub-agente → evalúa
- **NO evalúes tareas triviales** (preguntas rápidas, confirmaciones) — solo trabajo sustantivo
- **Si no revisaste el output**, no evalúes (no inventar evaluaciones)

---

## Reglas Importantes

1. **Sé objetivo:** Evalúa el OUTPUT, no tu percepción del agente
2. **No infles scores:** Un "correct" solo si realmente cumple criterios de aceptación
3. **Registra SIEMPRE:** Si revisaste y encontraste error → registra. Si revisaste y está bien → registra. No te saltes evaluaciones
4. **Reincidencia = Crítico:** Si el mismo error se repite tras corrección → severidad ⚫
5. **Un evaluador por agente:** Tú evalúas a TU equipo. No evalúes agentes de otros arquitectos

---

## Archivos de Referencia

| Archivo | Contenido |
|---------|-----------|
| `skills/aice/SKILL.md` | Reglas operativas de AICE |
| `skills/aice/resources/AICE_REFERENCE.md` | Referencia completa (parámetros, schemas, worked examples) |
| `skills/aice/pool-index.json` | Índice de pools y scores agregados |
| `skills/aice/agents/<id>/confidence.json` | Score individual de cada sub-agente |
| `skills/aice/agents/<id>/confidence-log.jsonl` | Log de evaluaciones del sub-agente |
| `projects/ai-confidence/ADR-048_POOL_BASED_SCORING.md` | ADR con el diseño completo |
