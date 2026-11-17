---
name: calendarizador-urgencias-formula100k
description: "Construye el CALENDARIO DE RAZONES DE URGENCIA (mensual + pool semanal) de cualquier producto/programa/servicio con la metodología de urgencia honesta de FÓRMULA 100K (motor biológico, 5 gatillos de decisión, aversión a la pérdida) + investigación web real con Tavily MCP para cazar fechas estacionales y comerciales del nicho. Activar SIEMPRE que el usuario, una clienta o alumna pida 'arma mi calendario de urgencias', 'razones de urgencia para mi producto', 'fechas de venta de [nicho]', 'cuándo activar urgencia este año', 'calendario de gatillos', 'dame razones de urgencia honestas', 'qué urgencia uso este mes', o cualquier variación que combine urgencia/escasez con planear cuándo activarla. NO confundir con calendarizador-contenido-formula100k (reels/carruseles) ni calendarizador-historias-formula100k (stories). Entrega calendario mensual + pool de razones reutilizables alineadas a fechas reales."
argument-hint: "[nombre del producto opcional]"
disable-model-invocation: false
metadata: {"version": "1.0.0", "depends-on": ["mcp__claude_ai_Tavily__*"], "openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Tu búsqueda web es Tavily por Composio: `composio execute TAVILY_SEARCH -d '{"query":"…","max_results":5}'` (sección 2 del puente). Las fechas reales del nicho salen de ahí, con su link. Si una fecha no se puede verificar, márcala `⚠️ verificar`.
> - Los 5 bloques de preguntas van por Telegram, uno a la vez, con opciones numeradas. Lo que ya esté en `cerebro/` (producto, precios, fechas propias) confírmalo en vez de preguntarlo.
> - `scripts/build_xlsx.py` necesita `openpyxl`: si no está, entrega el calendario en `.md` y el JSON, y dilo. Guarda en `entregables/urgencias/`.

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

# Skill: Calendarizador de Urgencias FÓRMULA 100K

Genera un calendario de **razones de urgencia** para vender un producto/programa/servicio,
basado en (1) la anatomía F100K de urgencia honesta y (2) fechas REALES del año cazadas
con Tavily para el nicho específico del usuario.

---

## ⚠️ ANTES DE EMPEZAR — LEE ESTOS REFERENCIALES

1. `references/anatomia-urgencia.md` — Motor biológico, 5 gatillos de decisión, anatomía F100K, reglas de oro
2. `references/pool-semanal-templates.md` — Templates de razones semanales por TIPO de activo del producto
3. `references/ejemplos-briefs-rellenos.md` — Briefs ya rellenados (F100K, Lab Sol, L'Atelier Adriana) como referencia

---

## QUÉ HACE (alto nivel)

1. **Conversa el BRIEF en 5 bloques** (Producto / Nicho / Activos / Calendario propio / Tono)
2. **Investiga con Tavily** 30-50 fechas REALES del año relevantes al nicho
3. **Cruza** fechas reales × 5 gatillos × activos del producto → mapa de urgencias mensuales
4. **Construye pool semanal** de 15-25 razones rotativas ancladas a activos
5. **Entrega .md + .xlsx** con 6 hojas en la carpeta correcta según el contexto

---

## INPUT — BRIEF EN CASCADA (no preguntar todo de golpe)

Usa `AskUserQuestion` en 5 bloques separados. Espera la respuesta del bloque antes
de pasar al siguiente. Si el usuario pasó `<nombre del producto>` como argumento, salta
esa parte del bloque A.

### Bloque A — PRODUCTO
Una sola pregunta de texto libre con este formato. Si falta info, repreguntar:

```
Cuéntame de tu producto (3 líneas máximo):
1. NOMBRE y QUÉ es (curso/comunidad/SaaS/servicio 1:1/producto físico/membresía)
2. PRECIO (mensual / anual / único) — todos los puntos de entrada
3. ¿Tiene OFERTA DE LANZAMIENTO o precio especial que NO se repite? (ej: "$280 anual de lanzamiento")
```

### Bloque B — NICHO / AUDIENCIA
`AskUserQuestion` con 4 preguntas en una tanda:

1. **Rubro principal** (multiSelect=false, options ejemplo):
   - Marketing/Contenido/Marca personal
   - Educación/Coaching/Mentoría
   - Salud/Fitness/Nutrición
   - Finanzas/Inversión/Negocios
   - Tecnología/SaaS/IA
   - Bienestar/Espiritualidad/Desarrollo personal
   - E-commerce/Producto físico
   - Servicios B2B/Consultoría
   - Inmobiliario
   - Otro (escribir)

2. **Geo principal** (multiSelect=true):
   - LATAM (MX/AR/CO/CL/PE)
   - España
   - USA hispano
   - USA inglés
   - Brasil
   - Global

3. **Avatar resumido (texto libre):**
   - "Mujer 25-40, freelance, ingresos irregulares, ya intentó vender online"

4. **Idioma del copy** (multiSelect=false):
   - Español neutro
   - Español de México
   - Español de Argentina
   - Español de España
   - Inglés
   - Portugués

### Bloque C — ACTIVOS DEL PRODUCTO (clave para pool semanal)
`AskUserQuestion` con multiSelect=true, 1 pregunta:

```
¿Qué ACTIVOS tiene tu producto? (selecciona TODOS los que apliquen — alimentan el pool semanal)

- Sesiones en vivo recurrentes (semanales/quincenales)
- Cohortes con onboarding sincronizado
- Comunidad activa (Skool/Discord/Telegram/FB Group/Slack)
- Drops de módulos/contenido nuevo
- Apps o herramientas exclusivas (solo dentro del producto)
- Bonos / sesiones 1-on-1
- Workshops o lives temáticos puntuales (1 al mes o trimestrales)
- Garantía (X días / resultado garantizado)
- Acceso a equipo / consultores / mentores adicionales
- Casos de éxito públicos / testimonios reales
- Hot seat / auditorías personalizadas
- Comunidad presencial / retiros / eventos físicos
- Certificación / título emitido
- Precio escalonado real (sube con cada cohorte)
```

Luego, pregunta texto libre:
```
Describe en 2-3 líneas el CADENCIA de cada activo elegido (ej: "sesiones en vivo
los miércoles 8pm CDMX", "cohorte abre el día 1 de cada mes", "drop de módulo
cada 6 semanas"). Esta cadencia es la que se usa para urgencia semanal honesta.
```

### Bloque D — CALENDARIO PROPIO
Pregunta de texto libre (puede saltarse):

```
¿Tienes fechas internas relevantes este año? (opcional)
- Aniversario del producto / comunidad
- Lanzamientos planeados
- Cierres de cohorte específicos
- Eventos en vivo agendados
- Subida de precio programada
Formato: "DD/MM/YYYY — evento". Si no tienes nada planeado, di "ninguna".
```

### Bloque E — REGLAS Y TONO
`AskUserQuestion` con 2 preguntas:

1. **Idioma neutro vs regional** (multiSelect=false):
   - Español neutro (NO vos / tenés / acá)
   - Permitir voseo / regionalismos
   - Otro

2. **¿Hay urgencias que NO quieres usar?** (multiSelect=true):
   - "Solo quedan X plazas" (si no es verdad verificable)
   - Cuenta regresiva agresiva
   - Aversión a la pérdida fuerte ("vas a seguir igual")
   - Comparación con competencia
   - Mención de garantías
   - Ninguna restricción — usa todas

---

## PROCESO

### Paso 1 — Validar brief
Antes de seguir: confirma con el usuario que el brief está completo. Muéstrale un
resumen tipo:

```
✅ Producto: [nombre] / [tipo] / [precio]
✅ Nicho: [rubro] / [geo] / [idioma]
✅ Avatar: [resumen 1 línea]
✅ Activos: [N activos seleccionados]
✅ Calendario propio: [N fechas]
✅ Reglas: [neutro/regional] + [exclusiones]

¿Empiezo la investigación con Tavily?
```

Solo arrancas la investigación cuando el usuario confirma.

### Paso 2 — Investigación con Tavily MCP
Lanza **8-12 búsquedas paralelas** con `mcp__claude_ai_Tavily__*`. Las queries
dependen del rubro + geo. Plantilla:

```
1. "fechas comerciales [rubro] [año actual]"
2. "calendario de marketing [rubro] [geo]"
3. "días internacionales [rubro]"
4. "Black Friday Cyber Monday [geo] [año]"
5. "Hot Sale / Buen Fin / Tianguis [geo]"
6. "regreso a clases [geo] fecha"
7. "cierre fiscal [geo] [año]"
8. "eventos del rubro [rubro] [año]"
9. "temporada alta [rubro]"
10. "pico de demanda [rubro] estacional"
11. "[fechas culturales relevantes geo año]"
12. "trends [rubro] [año]"
```

**Importante:** Si Tavily NO está autenticado, devuelve este mensaje:

```
⚠️ Tavily MCP no está autenticado. Para que la skill use fechas verificables del
nicho, conecta Tavily desde tu Claude Code. Mientras tanto, ¿quieres que use
conocimiento general del modelo? (menos preciso, puede errar fechas)
```

### Paso 3 — Síntesis del calendario mensual (12 meses)
Para cada mes, decide:

| Campo | Cómo se decide |
|---|---|
| **Eventos reales del mes** | Top 2-3 fechas más fuertes del nicho (Tavily) + fechas internas del usuario |
| **Gatillo dominante** | Uno de los 5: Urgencia táctica, Escasez cruda, Prueba social, Exclusividad, Aversión a la pérdida (ver `anatomia-urgencia.md`) |
| **Razones de urgencia** (3-5) | Cada una debe anclarse a un evento real Y/O a un activo del producto. Si no se ancla, NO se incluye. |
| **Mensaje tipo** | Un copy de 2-3 líneas listo para usar — en el IDIOMA del brief. Aplica regla de español neutro si corresponde. |

**Regla dura:** si el rubro NO tiene fechas estacionales fuertes (ej: SaaS B2B),
compensa con activos del producto (drops, cohortes, aniversarios).

### Paso 4 — Pool semanal (15-25 razones rotativas)
Para cada **activo del producto** seleccionado en Bloque C, genera 2-4 razones
semanales usando las plantillas en `references/pool-semanal-templates.md`. Ejemplo:

| Activo del usuario | Razón generada |
|---|---|
| Sesión en vivo semanal | "Si entras antes del martes, llegas a la sesión del miércoles" |
| Cohorte mensual | "Si no entras antes del 5, esperas un mes" |
| App exclusiva | "[nombre app] no se vende suelta — esta es la única puerta" |

Cada razón debe tener: cuándo activarla, copy modelo, qué gatillo activa.

### Paso 5 — Build de outputs

**5a.** Genera el archivo `.md` con secciones:
1. Resumen + motor biológico
2. Precios de referencia
3. Calendario mensual (12 meses) — formato H3 por mes con todo el detalle
4. Pool de razones semanales (tabla)
5. Activos REALES del producto que generan urgencia honesta
6. 7 reglas operativas
7. Pendientes para verificar antes de ejecutar
8. Anexo: fuentes Tavily consultadas (urls + título)

**5b.** Ejecuta `scripts/build_xlsx.py` con el JSON intermedio que armaste:

```bash
python3 skills/calendarizador-urgencias-formula100k/scripts/build_xlsx.py \
  --json /tmp/urgencias-<slug>.json \
  --out "<OUTPUT_DIR>/calendario-urgencias-<slug>.xlsx"
```

El script lee un JSON con la estructura definida en `scripts/build_xlsx.py` y
produce el Excel con 6 hojas (mismo formato que la primera prueba que se hizo
para F100K, pero parametrizado).

### Paso 6 — Output PATH (smart routing)
```
Si existe la carpeta entregables/ (el usuario ya trabaja con esa estructura):
  → entregables/urgencias/<slug>/

Si no existe:
  → ./calendarios-urgencia/<slug>/
  (relativo a cwd)
```

`<slug>` = `kebab-case` del nombre del producto (ej: "Fórmula 100K" → `formula-100k`).

---

## OUTPUT FORMAT

### Archivo .md
Ver plantilla completa en `references/anatomia-urgencia.md` sección "Template de output .md".

### Archivo .xlsx
6 hojas (color codificadas por gatillo):

1. **Resumen** — motor biológico + 5 gatillos + precios
2. **Calendario mensual** — 12 filas (Ene-Dic), columnas: Mes, Eventos reales, Gatillo dominante, Razones, Mensaje tipo
3. **Pool semanal** — N filas, columnas: Razón, Activo del que viene, Gatillo, Cuándo activarla, Copy modelo
4. **Activos reales** — los activos del producto que sustentan urgencia honesta
5. **Reglas operativas** — checklist de 7 reglas
6. **Pendientes equipo** — verificaciones antes de ejecutar

---

## NOTAS Y GUARDRAILS

### Reglas duras (no negociables)
1. **TODA razón de urgencia debe anclarse a (a) un evento real verificable O (b) un activo real del producto.** Nunca inventar plazas, deadlines o escasez.
2. **Si el usuario marcó "español neutro":** revisar TODO el output por vos/tenés/acá/copiá y reemplazar.
3. **Si una fecha de Tavily no es verificable** (resultados débiles, fuente dudosa), márcala con `⚠️ verificar` en el output.
4. **Aniversarios u otras fechas internas** que el usuario NO confirmó: márcalas como pendiente en hoja 6.
5. **Si el rubro es regulado** (salud/finanzas/inversión): aplicar disclaimer obligatorio en mensaje tipo.

### Qué NO hace esta skill
- NO escribe el VSL ni el copy largo de venta (→ `vsl-expert-f100k`)
- NO arma el calendario de contenido diario (→ `calendarizador-contenido-formula100k`)
- NO construye la oferta (→ `constructor-ofertas-f100k`)
- NO publica nada — solo entrega los archivos

### Si el usuario dice "ya tengo brief" / "usa el brief de X"
- Buscar primero en `references/ejemplos-briefs-rellenos.md`
- Si no está, pedir el path al archivo del brief
- Saltarse Bloque A-E si el brief está completo

### Costo aproximado
- Tavily: 8-12 búsquedas (~$0.03-0.05)
- Tokens LLM: ~15-25k input / ~8-12k output
- Tiempo total: 60-90 segundos desde "confirmo" hasta archivos generados

---

## ARGUMENTOS

- `$1` (opcional) — nombre del producto. Si está, salta la pregunta "¿cómo se llama tu producto?"

Ejemplos de invocación:
- `/calendarizador-urgencias-formula100k`
- `/calendarizador-urgencias-formula100k FÓRMULA 100K`
- `/calendarizador-urgencias-formula100k Lab de Sol Traverso`
