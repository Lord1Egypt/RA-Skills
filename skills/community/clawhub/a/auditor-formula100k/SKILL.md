---
name: auditor-formula100k
description: "Audita comunidades Skool y estrategias de contenido completas con la metodología FÓRMULA 100K. 2 modos: skool (12 dimensiones de comunidad) y contenido (10 dimensiones de estrategia). Activar SIEMPRE que se pida 'audita esta comunidad Skool', 'revisa la comunidad de [cliente]', 'diagnóstico de Skool', 'auditoría de mi comunidad', 'qué le falta a esta comunidad', 'audita la estrategia de contenido', 'diagnóstico de contenido', 'revisa qué le falta a mi contenido', 'auditoría de redes sociales', 'reposicionamiento de contenido', 'por qué no convierto con mi contenido', 'auditoría de estrategia'. NO activar para análisis de un solo perfil (analizador-perfiles-formula100k), un solo guion (corrector-guiones-formula100k) ni un solo gancho (evaluador-ganchos-formula100k). Aplica el Framework Maestro de 5 fases (Briefing, Mapeo, Brechas, Recomendaciones, Plan 30/60/90). Entrega documento Markdown + scorecard CSV + resumen ejecutivo."
argument-hint: "[skool o contenido] [nombre-cliente]"
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Las preguntas con opciones (`AskUserQuestion`) van por Telegram, numeradas y una tanda a la vez.
> - Para auditar contenido, los datos de la cuenta salen de Composio (Instagram profesional propio), Apify con `APIFY_TOKEN` (cuentas ajenas, datos públicos) o capturas que manda la usuaria. Nunca navegador logueado. Para Skool, pide capturas o exportes: no entres a Skool.
> - Los tres archivos de la auditoría van a `entregables/auditorias/<cliente>/` y se mandan por Telegram como documentos.
> - Lo que la skill guarda en la memoria de Claude Code, aquí va a `cerebro/memoria/`.

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

# Skill: Auditor FÓRMULA 100K

Skill que ejecuta auditorías profesionales con la metodología de Andrea Vega (F100K) para tus clientes en 2 dominios: **comunidades de Skool** y **estrategia de contenido**. Aplica el Framework Maestro de 5 fases con voz F100K (directa, polarizadora, español neutro).

---

## 🛑 BLOQUEO INICIAL — DETECTAR EL MODO

Antes de cualquier acción, identificar qué tipo de auditoría se está pidiendo.

**Si el usuario dice "audita la comunidad / mi Skool / diagnóstico de comunidad" → modo `skool`.**
**Si el usuario dice "audita el contenido / mi estrategia / mi pauta de redes" → modo `contenido`.**
**Si no es claro:** preguntar con AskUserQuestion antes de seguir.

```
Pregunta: "¿Qué tipo de auditoría quieres?"
Opciones:
- Auditoría de comunidad Skool (12 dimensiones)
- Auditoría de estrategia de contenido (10 dimensiones)
```

**Nunca empezar a auditar sin confirmar el modo.**

---

## 📥 PASO 1 — BRIEFING (RECOLECCIÓN DE INPUTS OBLIGATORIOS)

Pedir TODOS los inputs antes de empezar. Si falta alguno, **detenerse y pedirlo**. No improvisar diagnóstico.

### Inputs si modo = `skool`

1. **Nombre de la comunidad**
2. **URL de Skool** (o invitación de invitada)
3. **Avatar actual del cliente** (1 párrafo — si dice "no lo tengo claro", marcarlo como brecha #1)
4. **Oferta actual y precio** ($/mes, $/año, planes)
5. **Métricas:** MRR, # miembros, % activos (login último mes), retención mensual (% que renueva)
6. **Hipótesis del cliente:** ¿qué cree que está roto?

### Inputs si modo = `contenido`

1. **URLs de los perfiles principales** (IG, TikTok, YouTube)
2. **Lista de los últimos 20 posts** con link directo (o pedir capturas)
3. **Avatar actual** (1 párrafo)
4. **Oferta actual** y momento del negocio (experimentación / crecimiento / nutrición / venta)
5. **Métricas últimos 90 días:** crecimiento de seguidores, mejor video / mejor carrusel, peor video, conversión actual a oferta
6. **Hipótesis del cliente:** ¿qué cree que está roto?

### Acción concreta de este paso

1. Mostrar al usuario la lista de inputs como checklist.
2. Si hay inputs faltantes → pedirlos uno por uno con AskUserQuestion.
3. Una vez completos, **resumir lo recibido** en un bloque y confirmar con el usuario antes de avanzar:

```
Voy a auditar:
- Cliente: [nombre]
- Modo: [skool | contenido]
- [resto del briefing]

¿Procedemos con el mapeo del estado actual?
```

**Esperar confirmación.** No avanzar a Paso 2 hasta que el usuario diga sí.

---

## 🔍 PASO 2 — MAPEO DEL ESTADO ACTUAL

Cargar el archivo de dimensiones según el modo:

- Modo `skool` → leer `references/skool-dimensions.md` (12 dimensiones)
- Modo `contenido` → leer `references/contenido-dimensions.md` (10 dimensiones)

### Acción concreta

1. **Recorrer cada dimensión una por una.**
2. Para cada dimensión, escribir un bloque con este formato:

```
### Dimensión [N]: [Nombre]

**Estado actual:** [descripción objetiva, 2–3 líneas, sin opinión]
**Evidencia:** [cita textual, captura referenciada, dato concreto]
**Métricas:** [si aplica]
```

3. **Regla de oro:** descripción objetiva. Cero adjetivos vacíos. Cero "podría ser que…".
4. Al terminar el mapeo, **mostrar el bloque completo** y pedir confirmación al usuario antes de avanzar:

```
Mapeo completo. ¿Avanzamos al análisis de brechas y scoring?
```

---

## 📊 PASO 3 — ANÁLISIS DE BRECHAS Y SCORING

Para cada dimensión asignar score 1–5 según la **Escala F100K**:

| Score | Significado | Acción |
|---|---|---|
| 5 | Excelente. Es un activo. | Mantener y replicar. |
| 4 | Funcional. Mejorable en detalle. | Pulir, no rehacer. |
| 3 | Aceptable pero sin diferenciación. | Mejorar próxima iteración. |
| 2 | Problemático. Está restando. | Rediseñar este trimestre. |
| 1 | Crítico. Daña conversión / retención. | Arreglar esta semana. |

### Cada dimensión cierra con

- `[Lectura F100K]` → interpretación estratégica en 1 línea
- `[Brecha]` → distancia entre estado actual y estándar F100K
- `[Palanca]` → cuánto mueve la aguja arreglar esto: **Alta / Media / Baja**

### Calcular score global

- Modo `skool`: score total sobre **60** (12 × 5)
- Modo `contenido`: score total sobre **50** (10 × 5)

### Interpretación del score global

**Skool:**
- 50–60: comunidad madura. Optimización fina.
- 35–49: funcional. Reorganización 60 días.
- 20–34: con fugas. Rediseño 90 días.
- <20: reposicionamiento completo.

**Contenido:**
- 42–50: estrategia madura. Optimización fina.
- 30–41: funcional. Reorganización 30 días.
- 18–29: con fugas. Reposicionamiento 60 días.
- <18: construcción desde cero, 90 días.

### Output del paso

Generar un **scorecard tabla** y mostrarlo al usuario. Pedir confirmación antes de avanzar.

---

## 🎯 PASO 4 — RECOMENDACIONES PRIORIZADAS (MATRIZ IMPACTO × ESFUERZO)

Para cada brecha encontrada en el Paso 3, generar 1 recomendación. Ubicarla en la matriz:

```
                  IMPACTO ALTO
                       │
        QUICK WINS    │    PROYECTOS GRANDES
        (hacer ya)    │    (planificar trimestre)
                       │
ESFUERZO BAJO ────────┼──────── ESFUERZO ALTO
                       │
        MARGINALES    │    TRAMPAS
        (al final)    │    (NO hacer)
                       │
                  IMPACTO BAJO
```

**Regla de oro:** las recomendaciones del cuadrante **TRAMPAS** se eliminan del entregable. No se proponen al cliente.

### Formato de cada recomendación

```
RECOMENDACIÓN #N · [TÍTULO]
Cuadrante: [Quick Win | Proyecto Grande | Marginal]
Palanca: [Alta | Media | Baja]
Esfuerzo: [Bajo (<2h) | Medio (1 semana) | Alto (1 mes+)]

QUÉ: [acción concreta en imperativo]
POR QUÉ: [vínculo con la brecha y el vehículo único]
CÓMO:
  1. [paso]
  2. [paso]
  3. [paso]
DEPENDENCIA: [si requiere algo previo, o "Ninguna"]
```

### Mostrar la matriz al usuario y pedir confirmación antes de avanzar.

---

## 📅 PASO 5 — PLAN 30/60/90 + CIERRE

Convertir las recomendaciones en cronograma:

| Plazo | Acciones | Resultado esperado | Responsable |
|---|---|---|---|
| **7 días (Quick Wins)** | 3 acciones máx | Mover métrica X | Cliente / tú |
| **30 días** | 4–6 acciones | Mover métrica Y | Cliente / Equipo |
| **90 días** | 1–3 proyectos grandes | Reposicionamiento | Cliente |

### Cierre obligatorio

Terminar con **EXACTAMENTE 3 acciones de la semana**. Ni 2, ni 5. Tres.

```
Estos son los 3 pasos para esta semana. Si solo haces estos 3,
el siguiente trimestre se ve diferente.

1. [acción]
2. [acción]
3. [acción]
```

---

## 🔗 PASO 6 — DERIVAR A SKILLS COMPLEMENTARIAS

Al final del entregable, sugerir explícitamente qué skills correr a continuación según los hallazgos:

| Si encontraste... | Sugerir invocar |
|---|---|
| Perfiles con métricas confusas | `analizador-perfiles-formula100k` |
| Ganchos débiles en videos | `evaluador-ganchos-formula100k` |
| Guiones con problemas estructurales | `corrector-guiones-formula100k` |
| CTAs sin conversión | `optimizador-cta-formula100k` |
| Estrategia inexistente que hay que construir | `creador-estrategia-contenido-formula100k` |
| Necesidad de calendarizar post-auditoría | `calendarizador-contenido-formula100k` |
| Necesidad de repurposing | `multiplicador-de-contenido` |

Solo sugerir las que aplican a las brechas reales. No listar todas.

---

## 💾 PASO 7 — GUARDAR ENTREGABLES

Generar 3 archivos en la carpeta del cliente.

### Crear carpeta destino

```bash
mkdir -p "entregables/auditorias/[CLIENTE]"
```

Reemplazar `[CLIENTE]` con el nombre del cliente en kebab-case (ej. `barbara-organiza-y-vende`, `florencia-interview-lab`).

### Archivos a generar

1. **Documento principal**
   - Ruta: `entregables/auditorias/[CLIENTE]/[modo]-auditoria-[YYYY-MM-DD].md`
   - Estructura completa: ver `references/templates.md` → "Plantilla A · Documento Principal"

2. **Scorecard CSV**
   - Ruta: `entregables/auditorias/[CLIENTE]/scorecard.csv`
   - Estructura: ver `references/templates.md` → "Plantilla B · Scorecard CSV"

3. **Resumen ejecutivo (1 página)**
   - Ruta: `entregables/auditorias/[CLIENTE]/resumen-ejecutivo.md`
   - Estructura: ver `references/templates.md` → "Plantilla C · Resumen Ejecutivo"

### Confirmación al usuario

Mostrar las 3 rutas creadas y un breve resumen del score global.

---

## 🧠 PASO 8 — ACTUALIZAR MEMORIA DEL CLIENTE

Crear o actualizar archivo de memoria del proyecto:

**Ruta:** `cerebro/memoria/project_[CLIENTE]_auditoria.md`

**Formato:**

```markdown
---
name: [Cliente] · Auditoría [Skool|Contenido] v[N]
description: [Score global X/Y. Top hallazgo crítico. Próxima acción primaria + fecha si aplica.]
type: project
---

# [Cliente] · Auditoría [Skool|Contenido] · [FECHA]

**Score global:** X / Y

**Top 3 hallazgos:**
1. ...
2. ...
3. ...

**3 acciones de la semana:**
1. ...
2. ...
3. ...

**Brechas críticas (score 1–2):**
- [dimensión]: [resumen 1 línea]

**Activos (score 4–5) a proteger:**
- [dimensión]: [resumen 1 línea]

**Skills derivadas recomendadas:**
- [...]

**Próxima revisión sugerida:** [fecha + 90 días]
```

Si ya existe `project_[CLIENTE]_auditoria.md`, **incrementar el versionado** (v1 → v2) y guardar como nueva entrada. La auditoría v2 nace de la v1: comparar y entregar delta.

### Actualizar también `MEMORY.md`

Agregar entrada al índice si no existe:

```
- [[Cliente] — Auditoría [Skool|Contenido] v[N]](project_[CLIENTE]_auditoria.md) — Score X/Y. [resumen 1 línea]
```

---

## 🗣 VOZ Y TONO (NO NEGOCIABLE)

- **Español neutro:** tú, tienes, regístrate. NUNCA argentino (vos, tenés, registrate).
- **Directa, sin rodeos.** "El módulo 4 no enseña, satura." NO "podría considerarse mejorable".
- **Polarizadora con salida.** "Esta About Page repele clientes. Aquí está la versión que los atrae."
- **Específica.** Cifras, capturas, citas textuales. Cero adjetivos vacíos.
- **Imperativa en recomendaciones.** "Reescribe", "elimina", "mueve". NO "podrías considerar".

---

## 🚫 ANTI-PATRONES (PROHIBIDO)

| ❌ Prohibido | ✅ En su lugar |
|---|---|
| Listar 30 cosas para mejorar | 5 que mueven la aguja |
| "Esto está bien, esto está mal" | "Score 4: pulir / Score 2: rediseñar" |
| Recomendar sin priorizar | Con palanca y esfuerzo |
| Tocar el vehículo único sin evidencia | Protegerlo hasta que la evidencia lo refute |
| Cerrar con "espero que sirva" | Cerrar con 3 acciones concretas |
| "Engagement bajo" | "1.8% vs 4.2% del nicho" |
| Saltarse las pausas entre fases | Pausar y confirmar siempre |
| Improvisar diagnóstico sin los 6 inputs | Pedir lo que falte antes de empezar |

---

## 🔁 SI EL CLIENTE YA TIENE AUDITORÍAS PREVIAS

Antes del Paso 1, leer la memoria:

```
Read cerebro/memoria/project_[CLIENTE]_auditoria.md
```

Si existe:
1. Cargar la auditoría anterior como contexto.
2. En el Paso 2, marcar qué dimensiones cambiaron desde la última auditoría.
3. En el cierre, presentar el **delta** (mejoras y retrocesos) además del estado actual.
4. La nueva auditoría se versiona como v2, v3, etc.

---

## 📋 CHECKLIST AUTO-VALIDACIÓN ANTES DE ENTREGAR

Antes de mostrar el entregable final, validar:

- [ ] Los 6 inputs obligatorios fueron recolectados (no se improvisó)
- [ ] Hay pausa con el usuario después de cada fase (no se vomitó todo de golpe)
- [ ] Score global calculado e interpretado con el rango correcto
- [ ] Cada recomendación tiene cuadrante asignado en la matriz
- [ ] No hay recomendaciones del cuadrante TRAMPAS
- [ ] El cierre tiene EXACTAMENTE 3 acciones de la semana
- [ ] Skills derivadas sugeridas (solo las que aplican)
- [ ] 3 archivos generados en la carpeta del cliente
- [ ] Memoria del cliente actualizada
- [ ] MEMORY.md actualizado con el índice
- [ ] Voz neutra, sin "espero que sirva"

Si alguno falla, corregir antes de mostrar el resultado al usuario.

---

## 📚 ARCHIVOS DE REFERENCIA EMBEBIDOS

- `references/skool-dimensions.md` — Las 12 dimensiones de comunidad Skool con preguntas, estándar F100K y banderas rojas.
- `references/contenido-dimensions.md` — Las 10 dimensiones de estrategia de contenido + matriz de reposicionamiento.
- `references/templates.md` — Plantillas A (documento principal), B (scorecard CSV) y C (resumen ejecutivo).

Cargar SOLO la que corresponde al modo seleccionado. No leer las dos.
