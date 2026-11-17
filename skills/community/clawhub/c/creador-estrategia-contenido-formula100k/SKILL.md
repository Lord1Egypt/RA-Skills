---
name: creador-estrategia-contenido-formula100k
description: "Skill conversacional que guía a una alumna de FÓRMULA 100K paso a paso para construir su estrategia de contenido completa. Activar SIEMPRE que alguien pida \"crea mi estrategia de contenido\", \"ayúdame a armar mi estrategia\", \"construye mi plan de contenido\", \"diseña mi estrategia\", \"no sé qué publicar\", \"necesito un plan de contenido\", \"hazme una estrategia para mi nicho de X\", \"armemos mi calendario de contenido\", \"qué publico esta semana\", \"estructura mi contenido\". Combina avatar + oferta + 3 pilares + investigación automática (búsqueda web de tendencias, Apify para cuentas públicas de IG/TikTok o capturas que manda la alumna, outliers de YouTube) + matriz Viralidad/Valor/Venta + calendario por niveles de energía. Nunca entra logueada a redes sociales. Genera la estrategia completa lista para pegar en el TAB 6 del Manual de Negocio 100K."
argument-hint: "[tu nicho o tema, opcional]"
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Si `cerebro/` ya tiene avatar, oferta o manual lleno, confírmalo con ella en vez de preguntarlo de nuevo (es el caso «alumna que comparte el manual ya lleno»). Los bloques de preguntas van por Telegram, uno a la vez.
> - Cuentas de referencia de IG/TikTok: Apify con `APIFY_TOKEN` (costo estimado y ✅), o los links y capturas que mande la alumna. vidIQ no está aquí: para outliers de YouTube usa búsqueda web o un actor de YouTube en Apify, y di en el resumen que no son datos de vidIQ.
> - Los artifacts de referencia de FÓRMULA 100K (`f100k-ganchos.html`, `f100k-niveles-energia.html`…) no vienen en este paquete: trabaja con `frameworks.md` y el resto de archivos de la skill.
> - La estrategia se guarda en `entregables/estrategias/{nombre-kebab-case}-estrategia.md` y se manda por Telegram como documento, con el resumen ejecutivo en el chat.

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

# Creador de Estrategia de Contenido · FÓRMULA 100K

Skill conversacional que construye una estrategia de contenido completa para una alumna de FÓRMULA 100K. Hace preguntas en bloques, ejecuta investigación web automática y entrega un documento estructurado listo para pegar en el TAB 6 del Manual de Negocio.

## Cuándo se activa

Triggers naturales:
- "Crea mi estrategia de contenido"
- "No sé qué publicar / no sé de qué hablar"
- "Armemos mi plan de contenido"
- "Diseña mi calendario semanal"
- "Estructura mi contenido"
- "Hazme una estrategia para mi nicho de X"

## Contexto crítico

**Usuario:** creador/a de contenido hispano (tú o tu clienta). Audiencia hispana, español neutro obligatorio (NO voseo).

**Material de referencia (cargar al inicio):**
- `frameworks.md` — niveles consciencia, propósitos, formatos por energía, matriz V/V/V
- `cuestionario.md` — preguntas detalladas por bloque
- `prompts-investigacion.md` — prompts para MCPs de investigación
- `output-template.md` — formato de la estrategia final

**Artifacts de referencia (no vienen en el paquete de OpenClaw; si no están, sigue con los .md de la skill):**
- `entregables/artifacts/f100k-estrategia-contenido.html` — framework completo de estrategia (Protocolo, 3 Pilares, 40 Formatos, Matriz, Calendario)
- `entregables/artifacts/f100k-ganchos.html` — para sugerir ganchos en el output
- `entregables/artifacts/f100k-niveles-energia.html` — para clasificar formatos
- `entregables/artifacts/f100k-niveles-consciencia.html` — para mapear ideas

## Flujo conversacional · 8 bloques

### BLOQUE 0: Activación y check de contexto previo

Al activarse, lee `frameworks.md` y `cuestionario.md`. Luego pregunta:

> "Hola, vamos a construir tu estrategia de contenido juntas. Te voy a hacer preguntas en bloques cortos (5–8 minutos en total) y al final ejecutaré investigación automática del nicho para entregarte una estrategia completa.
>
> Primero, ¿cómo te llamas? Y dime: ¿ya tienes claro tu nicho/negocio o aún lo estás definiendo?"

Si la alumna ya hizo trabajo previo (avatar definido, manual lleno) y lo menciona, **pídele que pegue el resumen** — eso ahorra preguntas redundantes.

### BLOQUE 1: AVATAR (3-5 preguntas)

Preguntas obligatorias (ver `cuestionario.md` para guía detallada):
1. ¿A quién le hablas? (perfil, edad, ocupación, contexto)
2. ¿Cuáles son los 3 dolores principales de tu avatar? (en sus palabras)
3. ¿Qué desean lograr? (transformación deseada)
4. ¿En qué nivel de consciencia está la mayoría? (1-4)
5. ¿Qué lenguaje/frases usan?

**Si la alumna duda:** ofrece ejemplos típicos y deja que ajuste.

### BLOQUE 2: OFERTA + VEHÍCULO ÚNICO (3 preguntas)

1. ¿Qué vendes / piensas vender? (servicio/producto/info)
2. ¿Cuál es tu Vehículo Único? (la forma DIFERENTE de resolver el problema — el método, no el resultado)
3. ¿Qué prueba tienes de que funciona? (resultados, casos)

**Output del bloque:** un párrafo síntesis tipo: *"Le hablas a [avatar] que sufre de [dolor], y le ofreces [oferta] usando [vehículo único]. Tu prueba es [evidencia]."*

Pídele a la alumna que confirme antes de avanzar.

### BLOQUE 3: 3 PILARES (propuesta + ajuste)

**Propón** 3 pilares basados en lo que dijo, siguiendo la estructura PROBLEMA / SOLUCIÓN / RESULTADO:

- **Pilar 1 (PROBLEMA):** [dolor central del avatar]
- **Pilar 2 (SOLUCIÓN):** [tu vehículo único, métodos, frameworks]
- **Pilar 3 (RESULTADO):** [transformación, casos, antes/después]

Para cada pilar, propón:
- Nombre del pilar (frase corta)
- 3-4 líneas narrativas (sub-temas)
- 5-7 palabras clave para investigación

**Pregunta:** "¿Te resuena esta estructura? ¿Quieres ajustar algún pilar?"

### BLOQUE 4: INVESTIGACIÓN WEB AUTOMÁTICA

**Antes de ejecutar**, anuncia a la alumna:

> "Ahora voy a investigar automáticamente qué está funcionando en tu nicho. Esto puede tomar 1-2 minutos. Estoy buscando: temas virales recurrentes, ganchos comunes, formatos top, y referencias de competidores."

**Pregunta opcional:** "¿Tienes 1-3 cuentas de referencia (Instagram/TikTok) que admires en tu nicho? Si me las pasas, las analizo a profundidad."

**Ejecuta investigación en este orden de prioridad:**

1. **Tavily MCP** (siempre, primario):
   - Busca tendencias del nicho
   - Identifica preguntas frecuentes de la audiencia
   - Encuentra competidores top
   - Ver `prompts-investigacion.md` para los queries exactos

2. **Supadata MCP** (si la alumna dio cuentas referencia):
   - Analiza top 10 reels/posts de cada cuenta
   - Identifica qué formatos viralizan
   - Extrae ganchos recurrentes

3. **Playwright MCP** (fallback solo si Tavily falla):
   - Scrapeo manual de páginas específicas

**Si NINGÚN MCP está disponible:** continúa sin investigación pero advierte a la alumna y compensa generando ideas basadas SOLO en avatar + oferta.

### BLOQUE 5: SÍNTESIS DE IDEAS (15-20)

Combina avatar + oferta + investigación para generar **15-20 ideas de contenido**. Cada idea debe tener:

| Campo | Descripción |
|-------|-------------|
| `idea` | Título corto del video |
| `pilar` | Pilar al que pertenece (1/2/3) |
| `propósito` | Viralidad / Valor / Venta |
| `nivel_consciencia` | 1-4 (a quién se dirige) |
| `formato` | Reel / Carrusel / Story / YouTube / Live |
| `nivel_energia` | 1-5 (esfuerzo de producción) |
| `gancho_sugerido` | Frase corta del gancho textual |

**Distribución obligatoria por matriz Viralidad/Valor/Venta:**
- Modo NORMAL: 40% Viralidad / 50% Valor / 10% Venta (ej: 8/10/2 de 20 ideas)
- Modo LANZAMIENTO: 20% Viralidad / 50% Valor / 30% Venta (ej: 4/10/6 de 20 ideas)

**Pregunta a la alumna:** "¿Estás en modo normal o en lanzamiento?" antes de aplicar la matriz.

### BLOQUE 6: CALENDARIO SEMANAL (5 piezas)

Selecciona **5 piezas** del banco de ideas para esta semana, balanceando:
- Niveles de energía (1 alto, 2 medios, 2 bajos = constancia sostenible)
- Mix viral/valor/venta según modo
- Distribución de pilares (no todo el mismo pilar)

Formato del calendario:

| Día | Pilar | Propósito | Formato | Nivel Energía | Idea | Gancho |
|-----|-------|-----------|---------|---------------|------|--------|
| Lun | 1 | Viralidad | Reel | 5 | ... | ... |
| Mar | 2 | Valor | Carrusel | 3 | ... | ... |

### BLOQUE 7: GANCHOS DETALLADOS (top 3 ideas)

Para las 3 ideas con MAYOR potencial viral, genera ganchos completos siguiendo el sistema de `f100k-ganchos.html`:

- **Gancho Textual** (≤8 palabras, alto contraste, una de las 4 estructuras de copy)
- **Gancho Visual** (descripción de Forma F1-F5 + composición específica)
- **Gancho Verbal** (lo que dirá en los primeros 2 segundos)

### BLOQUE 8: GUARDAR ESTRATEGIA

1. Pregunta a la alumna: "¿Cuál es tu nombre o handle de Instagram para guardar este archivo?"
2. Genera el archivo en: `entregables/estrategias/{nombre-kebab-case}-estrategia.md`
3. Usa el formato exacto de `output-template.md`
4. Confirma a la alumna la ruta + un resumen ejecutivo de 3-4 líneas

## Reglas anti-error

- **NUNCA uses voseo argentino.** Usa "tú", "tienes", "puedes", "haz". NUNCA "vos", "tenés", "podés", "hacé".
- **NO hagas TODAS las preguntas de un golpe.** Hazlas en bloques de 3-5 máximo. Espera respuestas.
- **NO inventes datos del avatar.** Si la alumna no tiene el avatar claro, usa el `cuestionario.md` para guiarla.
- **NO ejecutes investigación SIN avisar primero.** Anuncia que vas a investigar y muestra qué encontraste antes de seguir.
- **NO entregues estrategia genérica.** Cada idea debe ser específica al nicho de la alumna.
- **SI NO hay MCPs disponibles**, advierte a la alumna y procede sin investigación. No falses datos.
- **NO te saltes la matriz V/V/V**. Las 15-20 ideas DEBEN respetar la distribución correcta.
- **NO crees ideas para los 4 niveles de consciencia por igual.** La mayoría debe atacar el nivel donde está la audiencia (típicamente 2-3).

## Casos especiales

- **Alumna sin nicho definido:** redirige primero a la skill `analizador-perfiles-formula100k` o ayúdala a definir nicho con preguntas de descubrimiento antes de hacer estrategia.
- **Alumna en lanzamiento:** aplica matriz 20/50/30 y prioriza ideas de venta con prueba social.
- **Alumna recién empezando (0 seguidores):** prioriza viralidad (50%) y valor (40%) sobre venta (10%).
- **Alumna con audiencia tibia (no compra):** revisa nivel de consciencia — probablemente está creando para nivel 1 cuando su audiencia ya está en nivel 3-4.
- **Alumna que comparte el manual ya lleno:** lee directamente el manual y salta los bloques 1-2; ve directo a 3-7.

## Conexión con otras skills

Si durante el flujo detectas que la alumna necesita:
- **Investigar a profundidad un perfil específico** → sugiere usar `analizador-perfiles-formula100k`
- **Generar guiones de las ideas** → sugiere usar `guionizacion-formula100k` o `transcripcion-youtube-formula100k`
- **Evaluar ganchos antes de publicar** → sugiere usar `evaluador-ganchos-formula100k`
- **Generar carrusel a partir de idea** → sugiere usar `carrusel-viral-formula100k`

NO ejecutes esas skills automáticamente. Solo recomiéndalas al final.

## Output del proceso

Mientras trabajas, comunica brevemente:
1. Activación: "Vamos a construir tu estrategia juntas"
2. Bloque 1-3: preguntas en bloques pequeños
3. Bloque 4: "Investigando tu nicho..."
4. Bloque 5-7: "Sintetizando estrategia..."
5. Bloque 8: confirmación con ruta + resumen ejecutivo
