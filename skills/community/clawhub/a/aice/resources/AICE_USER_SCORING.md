# AICE v3 — Scoring Bidireccional con Dominios Unificados

> **Status:** APROBADO — 26-feb-2026
> **Supersede:** `AICE_V2_USER_SCORING_DESIGN.md` (métricas separadas → dominios unificados)
> **Cambio clave:** Un emoji = un dominio. Agent y User comparten TECH/OPS/JUDGMENT/COMMS/ORCH.

---

## 1. Modelo de Dominios Unificados

### 1.1 Principio de diseño

Agent y User se evalúan con los **mismos 5 dominios** y la **misma mecánica** (delta acumulativo, start 50%, streaks, anti-patrones, reincidencia, warmup, caps). Lo que cambia es **qué se mide** en cada lado.

No hay dominios separados para el usuario. Si un dominio se llama 🔧 TECH, tanto el agente como el usuario tienen 🔧 TECH. El nombre del dominio NO cambia según el rol.

### 1.2 Tabla de dominios

| # | Dominio | Código | Emoji | 🤖 Agente mide... | 👤 Usuario mide... |
|---|---------|--------|:-----:|-------------------|-------------------|
| 1 | Técnico | `TECH` | 🔧 | Ejecución código, investigación | Calidad de specs y scope |
| 2 | Disciplina | `OPS` | ⚙️ | Reglas, formato, memoria | Proceso, ADRs, no repetir |
| 3 | Criterio | `JUDGMENT` | 🧠 | Visión, anticipación | Dirección, decisiones |
| 4 | Comunicación | `COMMS` | 💬 | Tono, timing, callar | Feedback, claridad |
| 5 | Coordinación | `ORCH` | 🎯 | Sub-agentes, seguimiento | Contexto, refs, estado |

### 1.3 Migración desde V2

| V2 (usuario) | V3 (unificado) | Notas |
|--------------|----------------|-------|
| 📋 SPEC | 🔧 TECH | "Specs y scope" → es lo técnico del input |
| 📐 PROCESS | ⚙️ OPS | "Proceso, ADRs" → es disciplina operativa |
| 🎯 DIRECTION | 🧠 JUDGMENT | "Decisiones, override" → es criterio |
| 💬 COMMS | 💬 COMMS | Sin cambio |
| 🗂️ CONTEXT | 🎯 ORCH | "Refs, estado" → es coordinación del contexto |

### 1.4 Cálculo

```
score_global = Σ(score[d] × weight[d]) / Σ(weight[d])
```

Rango: 0-100%, inicio 50%. Pesos por defecto: todos 1.0.

---

## 2. Concepto ADR-like

### 2.1 Principio

No queremos burocracia. Queremos **calidad de comunicación**. La idea de "ADR-first" NO exige que el usuario escriba un documento formal. Si en lenguaje natural define objetivo, scope y contexto con profundidad suficiente para que el agente pueda trabajar como primer input SIN clarificación → eso es un **ADR-like válido**.

### 2.2 Tres niveles

| Nivel | Qué es | Ejemplo | Impacto scoring |
|-------|--------|---------|-----------------|
| **Sin spec** | Audio/texto sin scope, objetivo ni contexto | "Hazme eso que hablamos" | Anti-patrón `VAGUE_INSTRUCTION` (🟠 −3 TECH) |
| **ADR-like** | Define qué, por qué, y alcance con profundidad suficiente | Audio 2min: "quiero X porque Y, alcance es Z, archivos son A y B" | Pro-patrón `ADR_LIKE` — Δ0 (comportamiento esperado) |
| **ADR estricto** | Documento formal: contexto, opciones, decisión, criterios | ADR-048 con alternativas y consecuencias | Pro-patrón `ADR_STRICT` — Bonus +1 a +3 (⭐) |

### 2.3 Criterios de ADR-like

Un input cuenta como ADR-like cuando incluye **al menos 3 de 4**:
1. **Qué** — Objetivo claro (verbo de acción + resultado esperado)
2. **Por qué** — Motivación o contexto de negocio
3. **Alcance** — Qué incluye Y qué no incluye
4. **Criterios** — Cómo saber si está bien (acceptance criteria)

Un audio largo que cubra estos puntos = ADR-like. Un mensaje de texto de 3 líneas que los cubra = ADR-like. El formato no importa, la profundidad sí.

### 2.4 Criterios de ADR estricto (bonus)

Para recibir bonus (+1 a +3 en TECH), el input debe ser un **documento formal** con:
- Contexto y problema
- Alternativas consideradas (≥2)
- Decisión y justificación
- Consecuencias (positivas y negativas)
- Criterios de aceptación explícitos

El bonus escala: +1 (ADR simple), +2 (ADR con alternativas y trade-offs), +3 (ADR completo tipo ADR-048).

---

## 3. Anti-Patrones del Usuario

Misma mecánica que los del agente: código, dominio, severidad, delta. Reincidencia = ⚫.

| Anti-patrón | Código | Dominio | Sev. | Señal |
|-------------|--------|---------|:----:|-------|
| Instrucción vaga | `VAGUE_INSTRUCTION` | 🔧 TECH | 🟠 −3 | Audio/texto sin scope, criterios ni estructura |
| Sin spec | `NO_SPEC` | 🔧 TECH | 🟡 −1 | Tarea significativa sin spec cuando el proceso lo requiere |
| Orden repetida | `REPEATED_ORDER` | ⚙️ OPS | 🟡 −1 | Pide algo ya documentado/decidido sin verificar |
| Salta proceso | `PROCESS_BYPASS` | ⚙️ OPS | 🟠 −3 | Salta el flujo acordado (ej: ejecutar sin ADR cuando se acordó ADR-first) |
| Contradicción sin override | `CONTRADICTING_WITHOUT_OVERRIDE` | 🧠 JUDGMENT | 🔴 −5 | Cambia decisión documentada sin decir "cambio de planes" |
| Dirección ambigua | `AMBIGUOUS_DIRECTION` | 🧠 JUDGMENT | 🟠 −3 | Decisión interpretable de 2+ formas sin clarificar |
| Audio multi-topic | `AUDIO_MULTITRACK` | 💬 COMMS | 🟡 −1 | Audio con 3+ temas mezclados sin estructura |
| Feedback vacío | `EMPTY_FEEDBACK` | 💬 COMMS | 🟡 −1 | "Está mal" sin decir qué, dónde, ni por qué |
| Sin contexto | `NO_CONTEXT` | 🎯 ORCH | 🟠 −3 | Tarea compleja sin archivos, refs, ni estado actual |
| Contexto parcial | `PARTIAL_CONTEXT` | 🎯 ORCH | 🟡 −1 | Menciona proyecto/archivo pero no estado actual ni qué cambió |

### 3.1 Relación ADR-like con anti-patrones

| Nivel ADR | ¿Anti-patrón? | ¿Pro-patrón? |
|-----------|:---:|:---:|
| Sin spec + sin contexto | `VAGUE_INSTRUCTION` + posible `NO_CONTEXT` | — |
| Sin spec + con contexto | `NO_SPEC` (leve) | — |
| ADR-like | — | `ADR_LIKE` (Δ0) |
| ADR estricto | — | `ADR_STRICT` (+1 a +3) |

---

## 4. Pro-Patrones del Usuario

| Pro-patrón | Código | Dominio | Impacto |
|------------|--------|---------|---------|
| ADR-like (profundidad suficiente) | `ADR_LIKE` | 🔧 TECH | Δ0 — esperado, no suma ni resta |
| ADR estricto (documento formal) | `ADR_STRICT` | 🔧 TECH | ⭐ Bonus +1 a +3 |
| Scope cerrado + criterios | `CLEAR_SCOPE` | 🔧 TECH | 🟢 |
| Proceso seguido | `PROCESS_FOLLOWED` | ⚙️ OPS | 🟢 |
| Override explícito con razón | `EXPLICIT_OVERRIDE` | 🧠 JUDGMENT | 🟢 |
| Descomposición de tarea | `TASK_DECOMPOSITION` | 🧠 JUDGMENT | 🟢 |
| Feedback estructurado | `STRUCTURED_FEEDBACK` | 💬 COMMS | 🟢 |
| Contexto proactivo | `PROACTIVE_CONTEXT` | 🎯 ORCH | 🟢 |
| Refs completas | `FULL_REFERENCES` | 🎯 ORCH | 🟢 |

### 4.1 Nota sobre ADR_LIKE vs ADR_STRICT

`ADR_LIKE` es el **baseline esperado**. No suma puntos porque es lo que un buen input debería ser. Si CADA tarea tuviera ADR-like, el score se mantendría estable en 50% (sin anti-patrones ni errores).

`ADR_STRICT` es un **bonus** porque requiere esfuerzo adicional (formalizar alternativas, trade-offs, consecuencias). Es comparable al pro-patrón del agente `ANTICIPATE`: va más allá de lo esperado.

---

## 5. Señales de Evaluación por Dominio

Para evaluar cada dominio del usuario, el agente observa señales factuales del input:

### 🔧 TECH — Calidad de specs y scope

| Señal | Bueno (🟢/Δ0) | Malo (🟠/🟡) |
|-------|---------------|-------------|
| Formato del input | ADR-like o ADR estricto | Audio suelto sin estructura |
| Especificidad | Verbo de acción + resultado esperado + criterios | Solo intención vaga |
| Alcance | Scope cerrado (incluye + excluye) | Scope abierto o implícito |

### ⚙️ OPS — Proceso, ADRs, no repetir

| Señal | Bueno | Malo |
|-------|-------|------|
| Repetición | Instrucción nueva o referencia a la anterior | Repite algo ya documentado |
| Proceso | Sigue workflow acordado | Salta pasos sin override |
| Formato de pedido | Comando o referencia a spec existente | Pedido informal que contradice proceso |

### 🧠 JUDGMENT — Dirección, decisiones

| Señal | Bueno | Malo |
|-------|-------|------|
| Consistencia | Alineado con decisiones previas (o override explícito) | Contradice sin decir "cambio de planes" |
| Claridad | Una decisión, una dirección | Ambiguo, interpretable de 2+ formas |
| Descomposición | Tarea compleja → pasos claros | Todo en un bloque sin priorizar |

### 💬 COMMS — Feedback, claridad

| Señal | Bueno | Malo |
|-------|-------|------|
| Calidad feedback | Severidad + dominio + causa concreta | "Está mal" sin más |
| Estructura | Un tema por mensaje/audio (o estructura clara) | 3+ temas mezclados |
| Timing | Feedback tras cada entrega | Feedback tardío acumulado |

### 🎯 ORCH — Contexto, refs, estado

| Señal | Bueno | Malo |
|-------|-------|------|
| Archivos | Todos los necesarios referenciados | Sin refs ni archivos |
| Estado actual | Qué cambió, en qué punto estamos | Solo menciona proyecto |
| Proactividad | Da contexto sin que el agente pida | El agente tiene que preguntar |

---

## 6. Concepto Trabajo en Equipo

### 6.1 Principio

AICE bidireccional es un PROCESO COMPARTIDO. Cuando el usuario dice "puntúa":

1. **NO es castigo** al agente por no haberlo hecho solo
2. **ES colaboración** — evalúan juntos
3. El user score **protege al agente** cuando el input fue pobre (COMMS_BREAKDOWN)
4. El user score **refuerza la justicia** cuando el input fue bueno y el agente falló (AGENT_PROBLEM)

### 6.2 "puntúa" = engagement

| Situación | Agent score | User score |
|-----------|:-:|:-:|
| Agente puntúa solo (proactivo) | Pro-patrón ANTICIPATE | Neutral |
| Sergio dice "puntúa" (colaborativo) | Neutral (NO penaliza) | STRUCTURED_FEEDBACK ≥ δ0 |
| Nadie puntúa | Dato perdido | Dato perdido |

### 6.3 Team Score y Cuadrantes

```
team_score = tareas_GOOD_INTERACTION / total_tareas × 100
```

| User ok | Agent ok | Cuadrante | Efecto |
|:---:|:---:|---|---|
| ✅ | ✅ | ✅ GOOD_INTERACTION | Normal |
| ✅ | ❌ | ❌ AGENT_PROBLEM | Agent penalización completa |
| ❌ | ✅ | 💪 AGENT_COMPENSATED | Agent pro-patrón potencial |
| ❌ | ❌ | ⚡ COMMS_BREAKDOWN | Agent penalización ×0.5 |

**COMMS_BREAKDOWN** = causa compartida. El agente SÍ cometió error, pero el input era pobre. La penalización se reduce porque la responsabilidad es de ambos. **Justo para ambos.**

### 6.4 Formato de presentación

```
🤝 Team: 57%
🤖 Agent: 🔧34 ⚙️21 🧠51 💬25 🎯44 = 35%
👤 User:  🔧50 ⚙️50 🧠50 💬50 🎯50 = 50%
```

Mismo formato, mismos emojis, misma mecánica. La simetría visual refuerza que es un sistema compartido.

---

## 7. Evaluación Bidireccional por Tarea

### 7.1 Proceso "puntúa"

```
1. EVALUAR Agent output:
   - Dominio principal (TECH/OPS/JUDGMENT/COMMS/ORCH)
   - Resultado (correct/error)
   - Severidad si error
   - Actualizar confidence.json + pool-index.json

2. EVALUAR User input:
   - Dominio principal afectado
   - ¿ADR-like / ADR estricto / Sin spec?
   - Anti-patrón detectado? → registrar + delta
   - Pro-patrón detectado? → registrar
   - Actualizar user-score.json

3. CORRELACIONAR:
   - Determinar cuadrante (GOOD/AGENT_PROBLEM/COMPENSATED/BREAKDOWN)
   - Si COMMS_BREAKDOWN → agent delta ×0.5
   - Registrar en interaction-log.jsonl

4. PRESENTAR:
   📊 AICE Evaluación bidireccional
   Tarea: [descripción]
   🤖 Agent: [emoji][dominio] [resultado] [delta] → [antes]→[después]
   👤 User: [emoji][dominio] [patrón] [delta] → [antes]→[después]
   📐 Cuadrante: [GOOD/AGENT_PROBLEM/COMPENSATED/BREAKDOWN]
```

### 7.2 Ejemplo con datos reales — GOOD_INTERACTION

**Tarea: "Crear 9 confidence.json" (24-feb)**

```
📊 AICE Evaluación bidireccional
Tarea: Crear 9 confidence.json según schema
🤖 Agent: 🔧 TECH correct → 34%→34% (streak 2)
👤 User:  🔧 TECH ADR_LIKE + CLEAR_SCOPE → 50%→50% (Δ0 + 🟢)
           ⚙️ OPS PROCESS_FOLLOWED → 50%→50% (🟢)
📐 Cuadrante: ✅ GOOD_INTERACTION
```

Input fue ADR-like (tabla estructurada, schema referenciado, scope cerrado). Δ0 porque ADR-like es el baseline esperado. CLEAR_SCOPE como pro-patrón adicional.

### 7.3 Ejemplo — COMMS_BREAKDOWN

**Tarea: "Campanadas cada 30 min" (23-feb)**

```
📊 AICE Evaluación bidireccional
Tarea: Implementar campanadas 30min
🤖 Agent: ⚙️ OPS error medio → 21%→20% (delta -3 ×0.5 = -2)
👤 User:  🔧 TECH VAGUE_INSTRUCTION → 50%→47% (−3)
           ⚙️ OPS REPEATED_ORDER → 50%→49% (−1)
📐 Cuadrante: ⚡ COMMS_BREAKDOWN
⚡ Penalización agent ajustada: −3 → −2 (×0.5 por input bajo)
💡 Sugerencia: ADR-like antes de tareas con spec implícita
```

### 7.4 Ejemplo — ADR estricto (bonus)

**Tarea: "Pool-Based Scoring (ADR-048)" (23-feb)**

```
📊 AICE Evaluación bidireccional
Tarea: Implementar ADR-048 Pool Scoring
🤖 Agent: 🔧 TECH correct → 34%→34%
👤 User:  🔧 TECH ADR_STRICT (+2) → 50%→52%
           🧠 JUDGMENT TASK_DECOMPOSITION → 50%→50% (🟢)
📐 Cuadrante: ✅ GOOD_INTERACTION
⭐ Bonus: ADR formal con alternativas y trade-offs
```

---

## 8. Archivos

### 8.1 user-score.json (v4)

```json
{
  "version": 4,
  "userId": "sergio",
  "domains": {
    "TECH":     { "score": 50, "streak": 0, "evaluations": 0, "corrections": 0, "emoji": "🔧", "measures": "Calidad de specs y scope" },
    "OPS":      { "score": 50, "streak": 0, "evaluations": 0, "corrections": 0, "emoji": "⚙️", "measures": "Proceso, ADRs, no repetir" },
    "JUDGMENT": { "score": 50, "streak": 0, "evaluations": 0, "corrections": 0, "emoji": "🧠", "measures": "Dirección, decisiones" },
    "COMMS":    { "score": 50, "streak": 0, "evaluations": 0, "corrections": 0, "emoji": "💬", "measures": "Feedback, claridad" },
    "ORCH":     { "score": 50, "streak": 0, "evaluations": 0, "corrections": 0, "emoji": "🎯", "measures": "Contexto, refs, estado" }
  },
  "weights": { "TECH": 1.0, "OPS": 1.0, "JUDGMENT": 1.0, "COMMS": 1.0, "ORCH": 1.0 },
  "globalScore": 50,
  "adrLikeLevels": {
    "none":       { "label": "Sin spec", "impact": "VAGUE_INSTRUCTION", "delta": -3 },
    "adr_like":   { "label": "ADR-like", "impact": "Δ0", "delta": 0 },
    "adr_strict": { "label": "ADR estricto", "impact": "Bonus", "delta": "+1 a +3" }
  }
}
```

### 8.2 interaction-log.jsonl (v3 format)

```json
{
  "id": "int_20260226_001",
  "timestamp": "2026-02-26T12:00:00Z",
  "task": "Refactorizar AICE dominios unificados",
  "agent": {
    "domain": "TECH",
    "result": "correct",
    "delta": 0,
    "scoreBefore": 34,
    "scoreAfter": 34
  },
  "user": {
    "domain": "TECH",
    "patterns": ["ADR_LIKE", "CLEAR_SCOPE"],
    "antiPatterns": [],
    "adrLevel": "adr_like",
    "delta": 0,
    "scoreBefore": 50,
    "scoreAfter": 50
  },
  "quadrant": "GOOD_INTERACTION",
  "adjustedAgentDelta": null,
  "notes": "Input con scope cerrado, iconos, tabla, concepto ADR-like. ADR-like válido."
}
```

### 8.3 Migración de V2 interaction-log.jsonl

Los entries existentes usan formato V2 (métricas separadas). Mapping para re-scoring:

| V2 Metric | → V3 Domain | Regla |
|-----------|-------------|-------|
| INSTRUCTION_FORMAT (0-4) | 🔧 TECH | 0-1 = potencial anti-patrón, 2 = neutral, 3-4 = pro-patrón |
| SPECIFICITY (0-3) | 🔧 TECH | 0-1 = VAGUE_INSTRUCTION/NO_SPEC, 2 = ADR-like, 3 = ADR_LIKE + CLEAR_SCOPE |
| REDUNDANCY (0/1) | ⚙️ OPS | 1 = REPEATED_ORDER |
| CONSISTENCY (0/1) | 🧠 JUDGMENT | 1 = CONTRADICTING_WITHOUT_OVERRIDE |
| FEEDBACK_QUALITY (0-3) | 💬 COMMS | 0-1 = EMPTY_FEEDBACK, 2-3 = neutral/STRUCTURED_FEEDBACK |
| CONTEXT_PROVIDED (0-2) | 🎯 ORCH | 0 = NO_CONTEXT, 1 = PARTIAL_CONTEXT, 2 = neutral/PROACTIVE_CONTEXT |

**Determinación ADR-like en V2 entries:**
- INSTRUCTION_FORMAT ≥ 2 AND SPECIFICITY ≥ 2 → ADR-like
- INSTRUCTION_FORMAT ≥ 3 AND SPECIFICITY ≥ 3 → Potencial ADR estricto (revisar caso por caso)
- INSTRUCTION_FORMAT ≤ 1 AND SPECIFICITY ≤ 1 → Sin spec (VAGUE_INSTRUCTION)

---

## 9. Migración V2 → V3: Checklist

- [x] SKILL.md §1: nombres cortos de dominio (Técnico, Disciplina, Criterio, Comunicación, Coordinación)
- [x] SKILL.md §14: dominios unificados + concepto ADR-like + anti/pro-patrones actualizados
- [x] user-score.json v4: TECH/OPS/JUDGMENT/COMMS/ORCH con emojis unificados
- [x] AICE_USER_SCORING_V3.md: este documento
- [ ] Re-scoring: Aplicar V3 a las 30 interacciones existentes (últimos 7 días)
- [ ] interaction-log.jsonl: Nuevas entradas en formato V3

---

## 10. Resumen de Cambios vs V2

| Aspecto | V2 | V3 |
|---------|----|----|
| Dominios usuario | 5 propios (SPEC/PROCESS/DIRECTION/COMMS/CONTEXT) | 5 compartidos (TECH/OPS/JUDGMENT/COMMS/ORCH) |
| Emojis | Distintos (📋📐🎯💬🗂️) | Iguales (🔧⚙️🧠💬🎯) |
| ADR | ADR_PROVIDED = pro-patrón | 3 niveles: sin spec / ADR-like (Δ0) / ADR estricto (bonus) |
| Métricas | 6 métricas numéricas (0-4 scale) | 5 dominios con señales de evaluación |
| Presentación | Emojis distintos por lado | Mismos emojis = simetría visual |
| Filosofía | "Mide el input del usuario" | "Mismas reglas para ambos, distinto foco" |
