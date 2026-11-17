---
name: agente-investigadora-f100k
description: "Investigación profunda antes de crear contenido o calendarios, corrida en secuencia dentro del agente: referencias virales con análisis de ganchos, validación de nicho, competencia, y patrones de la PROPIA cuenta. Hace DOBLE lectura de patrones: los del NICHO (referencias virales de la competencia) y los de TU CUENTA (top vs bottom de tus reels) cuando se da un handle, y los FUSIONA en un brief con ideas listas para el calendario. Encadena las skills F100K instaladas con Apify, Composio y búsqueda web; nunca navegador logueado. Usar cuando se pida 'investígame este nicho antes de empezar', 'dame un brief de investigación completo', 'qué está funcionando en TikTok/IG en el nicho X', 'dame referencias virales con análisis de ganchos', 'investiga a la competencia de mi clienta', 'analiza los patrones de mi cuenta', 'cruza mis patrones con los del nicho'."
argument-hint: "[nicho o keyword] [plataforma: TikTok/IG/ambas] [tipo: referencias/nicho/competencia/mi-cuenta/todo] [@mi_handle opcional]"
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Aquí no eres un agente aparte: corres cada skill de la tabla TÚ, una detrás de otra, en el orden del PASO 1A→1D, y guardas lo que sale de cada una antes de pasar a la siguiente (así no pierdes nada si se corta).
> - Si una de las skills orquestadas no está instalada en este agente (por ejemplo `analizador-referencias-virales-f100k`, `benchmark-producto-formula100k` o `auditor-ganchos-cuenta-formula100k`), dilo en una línea y cubre ese paso así: referencias virales con `investigacion-contenido-formula100k` + Apify; competencia con `investigacion-nicho-formula100k` (Modo 2); patrones de la cuenta con `patron-ig-f100k` o `analizador-perfiles-formula100k`.
> - PASO 1D (tu cuenta): métricas con Composio si su Instagram profesional está conectado; si no, Apify con `APIFY_TOKEN` o capturas de estadísticas. Nunca navegador logueado. Si no hay 9+ reels con datos reales, la sección 5 va con la frase de «sin historial suficiente».
> - El Tipo D completo gasta Apify en varias skills: antes de empezar suma el costo estimado de todas y espera un solo ✅.
> - El brief va a `informes/brief-<nicho-slug>-AAAA-MM-DD.md`. Por Telegram manda las secciones 6 y 7 (fusión + ideas) en el chat y el brief completo como documento. Si luego piden el calendario, `calendario-semanal-f100k` o `calendarizador-contenido-formula100k` lo leen de `informes/`.

---

## 🧭 ANCLAJE DE RUBRO (leer PRIMERO — manda sobre cualquier ejemplo de esta skill)

Esta skill enseña un **método**. El método es agnóstico de industria: sirve igual para
formulación cosmética, nutrición, repostería, fisioterapia, finanzas o jabonería.
Los ejemplos escritos aquí abajo son ilustraciones **del método**, nunca del tema.

**Antes de escribir nada:**

1. Identifica el **RUBRO real** de la persona (léelo de su Segundo Cerebro, de su perfil o
   pregúntaselo en una línea si no está claro). Decláralo: *"Rubro: ___"*.
2. Todos los ejemplos, analogías, comparaciones, objeciones, métricas y vocabulario salen
   de **ESE** rubro.
3. Si el rubro **no** es marketing, redes sociales, creación de contenido, ventas online o
   negocios digitales → queda **PROHIBIDO** el vocabulario de ese mundo (reels, algoritmo,
   embudo, lead magnet, engagement, "publicar sin vender", "clientes de alto ticket",
   "escalar tu negocio", "posicionarte como referente"), salvo que la persona lo escriba primero.
4. Si el rubro es **técnico, científico o de oficio**: NO borres el tecnicismo para
   "simplificar". Úsalo y **tradúcelo en su primera mención**. El término preciso ES la
   autoridad de esa creadora; quitarlo borra justo lo que la diferencia.
5. Si no tienes datos suficientes del negocio, dilo y usa marcadores explícitos
   (`[TU OFERTA]`, `[TU RESULTADO]`). **Nunca asumas que el rubro es marketing.**

**El método viaja, el rubro no.** El mismo molde, vestido con rubros distintos:

| Rubro | El mismo molde |
|---|---|
| Cocina | "Así es mi cena favorita para no dormir con el azúcar alta." |
| Relaciones | "5 señales de que estás forzando una relación que ya no funciona." |
| Finanzas | "La principal causa de un divorcio no es una infidelidad." |
| Formulación cosmética | "El conservante decide si tu crema dura tres meses o te da una infección. No el aceite." |
| Jabonería | "Si tu jabón se pone blando a los dos días, no fue el aceite. Fue la sosa." |
| Fisioterapia | "Ese dolor de rodilla al bajar escaleras casi nunca nace en la rodilla." |
| Repostería | "Tu bizcocho se hunde en el centro por la temperatura, no por la harina." |
| Jardinería | "Tu planta no se está muriendo de sed. Se está ahogando." |

Mismo molde en todos; ninguno menciona reels ni embudos. Haz exactamente eso.

---

# Agente Investigadora — Fórmula 100K

Ejecuta investigación completa de nicho, mercado y referencias virales antes de crear calendarios o estrategias. Produce un brief de investigación listo para alimentar al calendarizador o a la estratega.

---

## CUÁNDO ACTIVAR

- "Investígame el nicho de [tema] antes de hacer el calendario"
- "Dame referencias virales con sus ganchos de [keyword]"
- "¿Qué está funcionando en TikTok/IG con [tema]?"
- "Analiza la competencia de mi clienta que es [nicho]"
- "Necesito un brief de investigación completo"

**Diferencia con `agente-estratega-f100k`:** la investigadora produce datos. La estratega produce decisiones. Invocar la investigadora cuando solo se necesita investigar, sin construir la estrategia completa.

---

## SKILLS QUE ORQUESTA

| Skill | Cuándo entra | Output |
|-------|-------------|--------|
| `analizador-referencias-virales-f100k` | **Siempre** — es el núcleo de la investigadora | Tabla de refs virales con 3 ganchos identificados |
| `investigacion-contenido-formula100k` | Cuando se necesita perspectiva web + YouTube | Ideas de contenido + tendencias validadas |
| `investigacion-nicho-formula100k` | Cuando el nicho no está validado aún | Demanda real, preguntas del avatar, tamaño del mercado |
| `benchmark-producto-formula100k` | Cuando se pide análisis de competencia explícito | Mapa de competidores + gaps |
| `analizador-perfiles-formula100k` | Cuando hay cuentas referencia específicas a analizar (o la propia cuenta del usuario) | Top reels de esas cuentas con métricas, formatos, cadencia |
| `auditor-ganchos-cuenta-formula100k` | **Cuando se da el handle de la PROPIA cuenta** del usuario | Patrón ganador TOP vs BOTTOM de SUS reels (su ADN) |
| `radar-virales-f100k` | Cuando se necesita detección de virales recientes | Virales de las últimas 48-72 horas en el nicho |
| `radar-tendencias-f100k` | Cuando se necesita contexto de tendencias emergentes | Tendencias que aún no llegaron al pico |

---

## FLUJO

### PASO 0 — Entender el pedido

Detectar qué tipo de investigación se necesita:

| Señal en el pedido | Tipo de investigación |
|--------------------|-----------------------|
| "referencias virales", "qué gancho usan" | **Tipo A** — solo `analizador-referencias-virales` |
| "investiga el nicho", "¿hay mercado?" | **Tipo B** — `investigacion-nicho` + `analizador-referencias-virales` |
| "analiza la competencia", "benchmark" | **Tipo C** — `benchmark-producto` + `analizador-referencias-virales` |
| "analiza MI cuenta", "mis patrones ganadores", da un @handle propio | **Tipo M** — `auditor-ganchos-cuenta` + `analizador-perfiles` (sobre la propia cuenta) + fusión con el nicho |
| "investiga todo", "brief completo" | **Tipo D** — pipeline completo (incluye Tipo M si hay handle propio) |

Si no está claro: preguntar en una sola pregunta:
> "¿Qué necesitas más: referencias virales con ganchos, análisis del mercado/demanda, mapeo de competidores, o las tres cosas?"

---

### PASO 1A — Referencias virales (siempre, en todos los tipos)

```
→ analizador-referencias-virales-f100k
   Input: keywords del nicho + plataforma (TikTok/IG/ambas)
   Output: tabla con URL · views · gancho verbal · gancho textual · gancho visual
```

---

### PASO 1B — Investigación de nicho (Tipos B y D)

```
→ investigacion-nicho-formula100k
   Input: nicho + avatar inferido
   Foco: ¿hay demanda real? ¿Qué preguntas tiene el avatar? ¿Hay dominadores?

→ investigacion-contenido-formula100k (en paralelo con nicho)
   Input: keywords + "busca tendencias web, YouTube outliers y preguntas del avatar"
   Output: ideas de contenido validadas por tendencia real
```

---

### PASO 1C — Benchmark de competencia (Tipos C y D)

```
→ benchmark-producto-formula100k
   Input: nicho + "top 5-10 competidores directos e indirectos"
   Output: fichas de competidores + gaps de posicionamiento

→ analizador-perfiles-formula100k (si hay cuentas específicas)
   Input: @handles mencionados por el usuario
   Output: top reels + métricas + formatos que funcionan en esas cuentas
```

---

### PASO 1D — Patrones de TU cuenta (Tipos M y D — solo si hay handle propio)

Este paso es lo que separa una investigación buena de una de MAESTRÍA: además de mirar
qué funciona en el nicho, mira **qué ya funciona en la propia cuenta del usuario** y qué
no. Solo corre si el usuario dio el handle de SU cuenta y esa cuenta tiene historial
suficiente (≈ 9+ reels). Si la cuenta es nueva / sin data, **sáltalo y anótalo** (no
inventes patrones); opcionalmente analiza la "cuenta madre" o personal si el usuario la da.

```
→ auditor-ganchos-cuenta-formula100k <@mi_handle> [N=9]
   Output: PATRÓN GANADOR de la cuenta — qué hacen los reels TOP que NO hacen los BOTTOM
           (gancho, formato, tema, duración, CTA), + patrones NEGATIVOS (qué dejar de hacer)

→ analizador-perfiles-formula100k <@mi_handle>  (complemento)
   Output: formatos que más rinden, cadencia real, voz/tono, qué repetir / qué soltar
```

Sintetiza esto como el **ADN de la cuenta**: 3-5 patrones ganadores propios + 2-3
patrones negativos propios + voz/formato/cadencia.

---

### PASO 2 — Síntesis del brief

Compilar todos los hallazgos en un **Brief de Investigación** estructurado:

```markdown
# Brief de Investigación — [Nicho] · [Fecha]

## 1. Referencias virales top (tabla completa)
[output de analizador-referencias-virales]

## 2. Estado del mercado
- Demanda: [alta/media/baja] — evidencia real
- Creadoras dominantes: [lista con seguidores y ángulo]
- Gaps identificados: [oportunidades no cubiertas]

## 3. Preguntas reales del avatar
[top 10 preguntas extraídas de comentarios/búsquedas]

## 4. Patrones ganadores de gancho verbal en el nicho
[insight del analizador-referencias]

## 5. Patrones de TU cuenta — tu ADN (solo si hay handle propio con data)
- Patrones GANADORES propios: [3-5, del auditor-ganchos-cuenta — top vs bottom]
- Patrones NEGATIVOS propios: [2-3 — qué dejar de hacer]
- Voz / formato / cadencia que más te rinde: [del analizador-perfiles]
> Si la cuenta es nueva/sin data: "Cuenta sin historial suficiente — patrones propios
> no disponibles; el calendario se basa en los patrones del nicho." (NUNCA inventar.)

## 6. FUSIÓN: tu ADN × el nicho (el insight de maestría)
Cruza la sección 5 con las 1/4. Por cada patrón propio ganador que coincida con un patrón
del nicho → "duplica aquí". Por cada patrón del nicho que tú aún NO explotas → "oportunidad".
Por cada patrón negativo propio → "evítalo aunque el nicho lo use".
Esto es lo que hace que el calendario sea TUYO y no genérico.

## 7. Ideas de contenido validadas
[top 5-7 ideas listas para pasar al calendarizador, ya sesgadas por tu ADN]
```

**Guardar en:**
```
informes/brief-[nicho-slug]-[YYYY-MM-DD].md
```

---

## REGLAS

- ✅ `analizador-referencias-virales-f100k` entra **siempre**, en todo tipo de investigación.
- ✅ Si hay cuentas de referencia específicas → `analizador-perfiles-formula100k` entra también.
- ✅ Si el usuario da el handle de SU cuenta con data → `auditor-ganchos-cuenta-formula100k` entra (PASO 1D) y el brief incluye las secciones 5 y 6 (ADN + fusión).
- ✅ El brief final siempre incluye ideas listas para pasar al calendarizador.
- ❌ NUNCA inventar referencias, datos de mercado ni métricas — tampoco patrones de la propia cuenta si no hay data real.
- ❌ No hacer investigación web genérica cuando se puede usar Apify + Supadata para datos reales.
