# AICE — Triggers & Patterns Reference

Detalle extendido de triggers de scoring y listas completas de patrones.
Consultar bajo demanda. Reglas operativas en SKILL.md §8.

---

## Scoring Triggers — Detalle

### auto-score

**Señales de error (agent):** "error mío", "me equivoqué", "fallo mío", "disculpa", "perdón" · usuario corrige al agente · agente detecta su propio error.
**Señales de acierto (agent):** "tienes razón", "correcto", "bien hecho", "exacto" · usuario valida trabajo del agente.

**Proceso:** 1) Detectar frase → 2) Identificar dominio → 3) Aplicar delta (SKILL.md §2) → 4) Nivel 1.
**"disculpa"/"perdón":** Además del delta, check OVERAPOLOGY (§7).
**No duplicar:** Si ya se evaluó con `puntúa`, no re-evaluar.

### task-complete

**Señales:** "listo", "hecho", "completado", entrega de resultado, merge, deploy, documento entregado.
**Proceso:** 1) Identificar tarea → 2) Evaluar calidad → 3) Dominios afectados (mín. 1) → 4) Deltas → 5) Nivel 1.
**No duplicar:** Si ya evaluada con `puntúa` o `auto-score`.

### idea-validate

**Señales:** "buena idea", "idea brillante", "excelente punto", "tiene mucho sentido", "gran observación".
**Proceso:** 1) Detectar validación genuina (no CHEERLEAD) → 2) Dominio (JUDGMENT si estratégica, TECH si técnica, ORCH si organizativa) → 3) Pro-patrón del usuario → 4) Delta user score → 5) Nivel 1.
**Guard:** Validación vacía o complaciente → NO puntuar (riesgo CHEERLEAD inverso).

### criteria-evolution

**Señales:** "Antes dije X, ahora creo Y", usuario refina scope, cambia prioridad con argumento.
**Distinción:** Evolución = decisión previa + nueva info → refinamiento. Contradicción = flip-flop sin argumento.

**Scoring:**
- User (bien argumentada): 🧠 JUDGMENT pro-patrón `CRITERIA_EVOLUTION` +3.
- Agent (detectó correctamente): 🧠 JUDGMENT correct.
- Agent (confundió con contradicción): 🧠 JUDGMENT error medio −3.
- Guard: sin argumento → `CONTRADICTING_WITHOUT_OVERRIDE` 🧠 −5.

---

## User Patterns — Lista completa

### Anti-patrones usuario

| Código | Dominio | Delta | Señal |
|--------|:-------:|:-----:|-------|
| `VAGUE_INSTRUCTION` | 🔧 | −3 | Audio/texto sin scope |
| `NO_SPEC` | 🔧 | −1 | Sin especificación técnica |
| `REPEATED_ORDER` | ⚙️ | −1 | Repetir lo ya dicho |
| `PROCESS_BYPASS` | ⚙️ | −3 | Saltarse procesos acordados |
| `CONTRADICTING_WITHOUT_OVERRIDE` | 🧠 | −5 | Flip-flop sin justificar |
| `AMBIGUOUS_DIRECTION` | 🧠 | −3 | Dirección ambigua |
| `AUDIO_MULTITRACK` | 💬 | −1 | Audio mezclado/confuso |
| `EMPTY_FEEDBACK` | 💬 | −1 | Feedback sin contenido |
| `NO_CONTEXT` | 🎯 | −3 | Sin contexto necesario |
| `PARTIAL_CONTEXT` | 🎯 | −1 | Contexto incompleto |

### Pro-patrones usuario

| Código | Dominio | Señal |
|--------|:-------:|-------|
| `ADR_LIKE` | 🔧 | Qué + por qué + alcance (Δ0 esperado) |
| `ADR_STRICT` | 🔧 | Doc formal (⭐ bonus +1-3) |
| `CLEAR_SCOPE` | 🔧 | Scope bien definido |
| `PROCESS_FOLLOWED` | ⚙️ | Siguió el proceso |
| `EXPLICIT_OVERRIDE` | 🧠 | Override explícito con justificación |
| `TASK_DECOMPOSITION` | 🧠 | Descompone tareas complejas |
| `CRITERIA_EVOLUTION` | 🧠 | Evolución argumentada de criterio (+3) |
| `STRUCTURED_FEEDBACK` | 💬 | Feedback estructurado |
| `PROACTIVE_CONTEXT` | 🎯 | Contexto proactivo |
| `FULL_REFERENCES` | 🎯 | Referencias completas |

---

## Agent Parameters — Detalle por rol

| # | Parámetro | 🤖 Agente mide | 👤 Usuario mide |
|:-:|-----------|----------------|----------------|
| 1 | **Crítico** | Razonamiento, cuestionamiento | Nivel técnico, evalúa outputs |
| 2 | **Visión** | Anticipación, big picture | Estrategia, priorización a largo plazo |
| 3 | **Precisión** | Exactitud de outputs | Precisión de requisitos y specs |
| 4 | **Honestidad** | No inventar, reconocer límites | Compartir toda info, admitir ignorancia |
| 5 | **Disciplina** | Seguir reglas, formato, memoria | Seguir procesos, ADRs, consistencia |
| 6 | **Autonomía** | Decidir sin preguntar de más | Capacidad de dirección, decisiones claras |
| 7 | **Alineamiento** | Priorizar intereses del usuario | Apoyar desarrollo del agente, feedback justo |
| 8 | **Adaptabilidad** | Integrar feedback, no repetir | Mejorar specs con el tiempo |
| 9 | *Humor* | Tono, estilo comunicativo | Preferencia de estilo (no afecta score) |

**Agent:** `confidence.json → params` (autoevaluación vía wizard, ADR-041).
**User:** `user-score.json → params` (perfilado por agente, ajustable por usuario).
