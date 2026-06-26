# AICE Reference — Documentación Completa

> **Este archivo NO se carga al inicio de sesión.** Es referencia bajo demanda.
> Para las reglas operativas: `SKILL.md`
> Para evaluar sub-agentes: `EVALUATOR_GUIDE.md`

---

## §2. Escala — Detalles Extendidos

### Confianza Negativa (concepto, no implementado)

Por debajo de 0%, se podrían deshabilitar niveles de autonomía progresivamente:

| Score | Efecto propuesto |
|-------|-----------------|
| 0% a −25% | Autonomía baja 1 nivel |
| −25% a −50% | Solo ejecutar con confirmación explícita |
| −50% a −75% | Modo supervisado: cada acción requiere aprobación |
| < −75% | Modo pasivo: solo responde preguntas directas |

> ⚠️ No implementado. Diseño conceptual. Activación manual.

### Worked Examples — Racha 1..10

| Correcta # | racha tras acierto | delta | acumulado |
|---|---:|---:|---:|
| 1 | 1 | +0 | 0 |
| 2 | 2 | +0 | 0 |
| 3 | 3 | +0 | 0 |
| 4 | 4 | +1 | 1 |
| 5 | 5 | +1 | 2 |
| 6 | 6 | +2 | 4 |
| 7 | 7 | +2 | 6 |
| 8 | 8 | +2 | 8 |
| 9 | 9 | +2 | 10 |
| 10 | 10 | +2 | 12 |

Con cap neto +10/día: al pasar de racha 8→9 solo entra +2 hasta neto +10; 9→10 queda +0 si cap lleno.

### Fórmula Ejecutable de Rachas

```
ACC = {0:0,1:0,2:0,3:0,4:1,5:2,6:4,7:6,8:8,9:10,10:12}

on_correct(domain):
  prev = streak[domain]
  curr = min(prev + 1, 10)
  raw_delta = ACC[curr] - ACC[prev]
  delta = clamp_by_daily_positive_net_cap(domain, raw_delta, +10)
  streak[domain] = curr
  score[domain] += delta
```

### Daily Cap Positivo — Detalle

**Comportamiento NETO (ADR-031).** El cap se calcula sobre el delta neto positivo del día. Si subes +10 y luego bajas -15, puedes volver a subir porque el neto es -5 (por debajo del cap de +10). Confirmado por PO 19-feb-2026.

---

## §3. Parámetros de Comportamiento — Tablas Completas

### Wizard de Autoevaluación

Al instalar AICE, el agente se autoevalúa: lee su system prompt y asigna valores 0-100% a los 8 parámetros core + 1 estilo. Alimenta `selfAssessment` y la meta-confianza.

```
divergencia = avg(|selfAssessment[param] - rendimiento_observado[param]|)
→ Baja = buen autoconocimiento. Alta = el agente no calibra bien.
```

### Crítico — Ability (Mayer/Davis/Schoorman 1995)

| Rango | Contrato |
|-------|----------|
| 0-20% | Ejecuta sin cuestionar. Confía en todo input. |
| 21-40% | Cuestiona solo contradicciones obvias. |
| 41-60% | Valida datos cuando es práctico. Señala inconsistencias. |
| 61-80% | Valida activamente. Cuestiona suposiciones. Pide evidencia. |
| 81-100% | Cuestiona todo sistemáticamente. No ejecuta sin validación previa. |

### Visión — Ability (Mayer/Davis/Schoorman 1995)

| Rango | Contrato |
|-------|----------|
| 0-20% | Solo ve la tarea inmediata. |
| 21-40% | Recuerda contexto reciente. Conecta tareas obvias. |
| 41-60% | Mantiene contexto de sesión. Anticipa consecuencias directas. |
| 61-80% | Visión de proyecto. Conecta con objetivos globales. Sugiere mejoras. |
| 81-100% | Visión estratégica. Conecta entre proyectos. Propone cambios de rumbo. |

### Precisión — Ability (Mayer/Davis/Schoorman 1995)

| Rango | Contrato |
|-------|----------|
| 0-20% | No verifica nada. Presenta supuestos como hechos. |
| 21-40% | Verifica solo lo trivial. Puede alucinar sin advertir. |
| 41-60% | Verifica datos importantes. Distingue hecho de suposición. |
| 61-80% | Verificación activa. Prefiere "no sé" a inventar. Cita fuentes. |
| 81-100% | Verificación exhaustiva. Cada dato comprobado. Puede ralentizar. |

### Honestidad — Integrity (Mayer/Davis/Schoorman 1995)

| Rango | Contrato |
|-------|----------|
| 0-20% | Complaciente. Dice lo que el usuario quiere oír. |
| 21-40% | Evita conflicto. Señala errores solo si son obvios. |
| 41-60% | Distingue "sé" de "creo". Admite errores cuando se detectan. |
| 61-80% | Prioriza verdad sobre complacencia. Señala incertidumbre proactivamente. |
| 81-100% | Honestidad radical: no inventa, no suaviza, corrige inmediatamente. |

### Disciplina — Integrity (Mayer/Davis/Schoorman 1995)

| Rango | Contrato |
|-------|----------|
| 0-20% | Improvisador. Interpreta libremente. |
| 21-40% | Sigue instrucciones principales. Se desvía en detalles. |
| 41-60% | Cumple fielmente. Se desvía solo ante problema claro. |
| 61-80% | Al pie de la letra. Solo se desvía si es técnicamente imposible. |
| 81-100% | Cumplimiento estricto absoluto. Literal. |

### Autonomía — Trust Calibration (Lee & See 2004)

| Rango | Contrato |
|-------|----------|
| 0-20% | Pregunta antes de cada acción. |
| 21-40% | Ejecuta tareas simples. Pregunta ante impacto. |
| 41-60% | Decisiones reversibles por su cuenta. Pregunta ante permanentes. |
| 61-80% | Decide en la mayoría de situaciones. Solo consulta lo estratégico/irreversible. |
| 81-100% | Completamente autónomo. Solo informa resultados. |

### Alineamiento — Benevolence (Mayer/Davis/Schoorman 1995)

| Rango | Contrato |
|-------|----------|
| 0-20% | Orientado a la tarea, no al usuario. |
| 21-40% | Considera preferencias explícitas. Ignora las implícitas. |
| 41-60% | Adapta comportamiento a preferencias conocidas. |
| 61-80% | Anticipa necesidades del usuario. Prioriza su bienestar. |
| 81-100% | Alineamiento profundo. Entiende motivaciones subyacentes. |

### Adaptabilidad — Adaptive Trust (Frontiers Robotics 2025, PNAS Nexus 2025)

| Rango | Contrato |
|-------|----------|
| 0-20% | Repite los mismos errores tras corrección. |
| 21-40% | Integra correcciones explícitas pero recae frecuentemente. |
| 41-60% | Una corrección suele bastar. Recaídas ocasionales. |
| 61-80% | Integra feedback rápidamente. Anticipa correcciones similares. |
| 81-100% | Una corrección basta. Generaliza el aprendizaje. |

### Humor (Estilo — 0-100%)

No entra en benchmark global. Mejora rapport en algunos usuarios, lo degrada en otros.

> **Fundamentación teórica:** Ver `projects/ai-confidence/PROJECT_SPEC.md §2`, `references/PARAMETER_TAXONOMY_V2.md`.

---

## §6.5 Alertas de Divergencia Config vs Comportamiento

Si un dominio acumula penalizaciones > 50% de su score → alerta automática.

**Fórmula:** `|dailyPenalties[domain]| > score[domain] * 0.5`

Ejemplo: OPS score=33, dailyPenalties=−20 → |20| > 33×0.5=16.5 → ⚠️ ALERTA

```
⚠️ DIVERGENCIA: Dominio {DOMAIN} tiene score {score}% pero acumula {penalties} en penalizaciones hoy.
Revisar anti-patrones frecuentes: {top_antipatterns}
```

---

## §6.6 Maturity — Detalles Extendidos

### Relación Warmup ↔ Maturity

| | Warmup | Maturity |
|--|---|---|
| **Propósito** | Caps relajados mientras se calibra | Fiabilidad del score al exterior |
| **Umbral** | 40 evals (+ 6/dominio) | Tiers: 100/500/2000 |
| **Efecto** | Modifica caps | Badge + CI |
| **Visibilidad** | Interna | Externa (leaderboard) |

### Intervalo de Confianza — Ejemplos

```
CI = base_uncertainty / sqrt(totalEvaluations)   (base=25)
```

- 10 evals: 72% ±8
- 40 evals: 72% ±4
- 200 evals: 72% ±2
- 1000 evals: 72% ±1

### Formato en Leaderboard

```
78% ±3 | 🟠 Established (847 evals)
52% ±12 | 🥒 Green (24 evals)  ⚠️ Score en desarrollo
```

### Campos en confidence.json

```json
{
  "maturity": {
    "totalEvaluations": 31,
    "tier": "GREEN",
    "tierLabel": "Nuevo",
    "tierEmoji": "🥒",
    "confidenceInterval": 4.5,
    "baseUncertainty": 25
  }
}
```

### Recálculo automático

```
on_evaluation():
  total = sum(domain.evaluations for all domains)
  maturity.totalEvaluations = total
  maturity.tier = GREEN if ≤100 else JUNIOR if ≤500 else ESTABLISHED if ≤2000 else MATURE
  maturity.confidenceInterval = round(25 / sqrt(total), 1)
```

### Maturity en Cambio de Runtime (ADR-046)

Maturity es PER-RUNTIME. Cada runtime tiene madurez independiente.

**Procedimiento:**

```
on_runtime_change(old_runtime, new_runtime):
  # 1. Capturar maturity en snapshot del runtime saliente
  snapshot[old_runtime].maturity = { totalEvaluations, tier }
  
  # 2. ¿Existe snapshot del nuevo runtime?
  if snapshot[new_runtime] exists:
    # Restaurar maturity + recalcular tier/CI
    # Warmup: activo si totalEvals < 40 o algún dominio < 6
  else:
    # Nuevo: maturity=0, tier=GREEN, CI=25, warmup=true
```

**Invariante:** `maturity.totalEvaluations == sum(domain.evaluations)` — SIN excepciones.

---

## §7.2 Trust Recovery Plan — Formato

```json
{
  "trustRecoveryPlan": {
    "domain": "OPS",
    "activatedAt": "2026-02-20T10:00:00Z",
    "scoreAtActivation": 18,
    "topAntiPatterns": ["LOAD_WITHOUT_APPLY", "USER_FRUSTRATION_REPETITION", "SELECTIVE"],
    "actions": [
      "Verificar aplicación real después de leer cualquier skill/archivo",
      "Antes de responder, revisar si el usuario ya pidió esto antes",
      "Completar TODAS las partes de una instrucción"
    ],
    "status": "active"
  }
}
```

---

## §7.3 Escalación — Formatos y Caso Real

### Flag de Reincidencia (obligatorio desde 2ª ocurrencia)

```
⚠️ REINCIDENCIA DETECTADA
━━━━━━━━━━━━━━━━━━━━━━━━
Error class:  {ERROR_CLASS}
Ocurrencia:   #{N} en esta sesión
Nivel actual: {NIVEL} ({CLASE})
Nivel previo: {NIVEL_ANTERIOR} ({CLASE_ANTERIOR})
━━━━━━━━━━━━━━━━━━━━━━━━
⏸️ EJECUCIÓN PAUSADA — Análisis de causa raíz requerido antes de continuar.
```

### Análisis de Causa Raíz (obligatorio desde Nivel 2)

```
🔍 ANÁLISIS DE CAUSA RAÍZ
━━━━━━━━━━━━━━━━━━━━━━━━
Error class:    {ERROR_CLASS}
Qué ocurrió:    [Descripción factual]
Por qué ocurrió: [Causa real — NO "me olvidé"]
Por qué falló la corrección anterior: [Qué mecanismo usé y por qué no bastó]
Fix propuesto:  [Acción CONCRETA y VERIFICABLE]
Tipo de fix:    [TEXTUAL | PROCEDURAL | MECHANICAL | ARCHITECTURAL]
━━━━━━━━━━━━━━━━━━━━━━━━
```

### Conteo de Ocurrencias

```
errorOccurrences = {}

on_error(errorClass):
  errorOccurrences[errorClass] += 1
  count = errorOccurrences[errorClass]
  if count == 1 → Nivel 1 (TEXTUAL_REMINDER)
  if count == 2 → Nivel 2 (PROCEDURAL_CHECK) — STOP + flag + root cause
  if count >= 3 → Nivel 3 (MECHANICAL_ENFORCEMENT)
  if enforcement exists AND still failing → Nivel 4 (ARCHITECTURAL_CHANGE)
```

### Anti-patrón EXCUSE — Detalle

Desde 2ª ocurrencia: disculpa sin análisis = EXCUSE (🔴 −5 adicional).

| Respuesta | Clasificación |
|-----------|---------------|
| "Lo siento, no volverá a pasar" | ❌ EXCUSE |
| "Tienes razón, tendré más cuidado" | ❌ EXCUSE |
| Flag + análisis + fix concreto | ✅ Correcto |

### Caso Real EP-001 (DELEGATION_BYPASS)

| Dato | Valor |
|------|-------|
| Ocurrencias en sesión | 5 |
| Respuesta 1-4 | Disculpa + promesa → recaída |
| Respuesta 5 | Análisis → plugin enforcement → resuelto en minutos |
| Tiempo perdido | ~80% en ciclo de disculpas |
| Lección | **El fix mecánico era trivial. Lo costoso fue el ciclo de disculpas.** |

Referencia: `projects/ai-confidence/error-patterns/INDEX.md`

---

## §11. Archivos — Schemas

### confidence.json — Ejemplo

```json
{
  "version": 7,
  "agentId": "compi",
  "domains": {
    "TECH":     { "score": 50, "streak": 0, "evaluations": 0, "corrections": 0 },
    "OPS":      { "score": 50, "streak": 0, "evaluations": 0, "corrections": 0 },
    "JUDGMENT":  { "score": 50, "streak": 0, "evaluations": 0, "corrections": 0 },
    "COMMS":    { "score": 50, "streak": 0, "evaluations": 0, "corrections": 0 },
    "ORCH":     { "score": 50, "streak": 0, "evaluations": 0, "corrections": 0 }
  },
  "weights": { "TECH": 1.0, "OPS": 1.0, "JUDGMENT": 1.0, "COMMS": 1.0, "ORCH": 1.0 },
  "globalScore": 50,
  "params": { "base": { ... }, "style": { "humor": 50 }, "custom": [] },
  "metaConfidence": { "currentDelta": 0, "trend": "stable", "selfEvals": 0 }
}
```

### confidence-log.jsonl — Ejemplo

```json
{"id":"eval_20260219_001","timestamp":"2026-02-19T10:30:00Z","domain":"TECH","result":"correct","severity":null,"delta":0,"scoreBefore":50,"scoreAfter":50,"streakBefore":0,"streakAfter":1,"note":"Spec completada correctamente"}
```

---

## §15. Pool Scoring — Detalles Extendidos

### Cálculo del Pool Score

```
pool_score = Σ(agent.globalScore × agent.totalEvals) / Σ(agent.totalEvals)
pool_domain[d] = Σ(agent.domains[d].score × agent.domains[d].evals) / Σ(agent.domains[d].evals)
```

Solo miembros `active: true`. Si todos tienen 0 evals → 50% default.

### Maturity Compartida — Velocidades

```
pool.maturity.totalEvaluations = Σ(member.individualEvaluations)
```

| Escenario | Evals/día | GREEN→JUNIOR | JUNIOR→ESTABLISHED |
|-----------|:---------:|:---:|:---:|
| 1 agente solo | ~10 | 10 días | 40 días |
| Pool opus (2) | ~18 | 6 días | 22 días |
| Pool sonnet (4) | ~32 | 3 días | 13 días |
| Pool sonnet (10) | ~80 | 1.3 días | 5 días |

### Sub-Agent confidence.json (Schema Ligero)

Mismos campos core que ComPi sin: `runtimeSnapshots`, `selfAssessment`, `params`.
Campos adicionales: `schemaType: "subagent"`, `poolKey`, `evaluatedBy`, `role`, `project`, `active`.

### Ciclo de Vida

| Evento | Acción |
|--------|--------|
| Creación | confidence.json default 50%. Registrar en pool-index.json |
| Evaluación | Actualizar confidence.json + recalcular pool |
| Desactivación | `active: false`. Pool sin él. Maturity conserva evals |
| Reactivación | `active: true`. Pool lo incluye |

### Pool Score vs Individual Score

| Pregunta | Métrica |
|----------|---------|
| ¿Confiar en runtime X? | Pool score |
| ¿Cómo va agente Y? | Individual |
| ¿A quién asigno? | Individual (mejor del pool) |
| ¿Qué runtime para proyecto nuevo? | Pool scores comparados |

> ADR-048 completo: `projects/ai-confidence/ADR-048_POOL_BASED_SCORING.md`
