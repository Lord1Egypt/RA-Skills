---
name: caso-estudio-contenido-f100k
description: "Reto final del módulo de Creación de Contenido de FÓRMULA 100K: corre el pipeline completo sobre el nicho de una alumna y entrega una PÁGINA DE CASO DE ESTUDIO (HTML de una sola página) lista para subir a Netlify/Vercel como portafolio, más el calendario en CSV. Activar SIEMPRE que se pida 'quiero hacer el reto final', 'crea mi caso de estudio de contenido', 'arma mi calendario + investigación del reto', 'el reto del módulo de contenido', 'haz mi caso de estudio', o cuando se invoque /caso-estudio. Investiga referencias virales reales, arma guiones, ganchos y calendario de 30 días con un checkpoint humano en medio, suma el plan de mes 2 y maqueta el HTML final. NO confundir con calendarizador-contenido (solo el calendario) ni con MAESTRO (semana completa con colocación en Yapper/Bento)."
argument-hint: "[nicho o keyword]"
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - LUNA y CALI no existen aquí: haz tú la investigación y luego guiones, ganchos y calendario, en secuencia, con `investigacion-contenido-formula100k`, `analizador-referencias-virales-f100k`, `guionizacion-formula100k`, `generador-ganchos-formula100k` y `calendarizador-contenido-formula100k` si están instaladas. El checkpoint entre investigación y producción va por Telegram y se espera su ✅.
> - Las 12 referencias virales salen de Apify con `APIFY_TOKEN` (datos públicos, costo estimado y ✅ antes) o de los links que mande la alumna. Nunca navegador logueado. Si no hay Apify, dilo y deja las vistas como «pendiente», nunca «Original» ni inventadas.
> - Los patrones de SU cuenta: Composio si tiene Instagram profesional conectado; si no, pídele capturas de sus estadísticas por Telegram. Sin datos, sáltalo y anótalo.
> - Todo va a `entregables/casos-de-estudio/<nicho-slug>-<AAAA-MM-DD>/`. El render usa solo la librería estándar: `python3 skills/caso-estudio-contenido-f100k/render_caso_estudio.py <carpeta>/data.json <carpeta>/index.html`.
> - `calendario.xlsx` necesita `openpyxl`; si no está, entrega solo el CSV y dilo. Revisa el `index.html` con el navegador del agente (captura a 390 px) antes de entregarlo.
> - Despliega la página directo en Vercel con `VERCEL_TOKEN` de la usuaria (`vercel --prod --yes --token "$VERCEL_TOKEN"`) y mándale la URL, más el CSV por Telegram. Sin token, pídele que lo conecte; el `.zip` es el último recurso.

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

# Reto Final · Caso de Estudio de Contenido · FÓRMULA 100K

Esta skill es el **examen final del módulo de Creación de Contenido**. La alumna corre
una sola skill sobre SU nicho y termina con la misma página de caso de estudio que
produjo una alumna real del reto (su página no viaja en este paquete): investigación de
virales → guiones → ingeniería de ganchos → calendario de 30 días → plan mes 2,
maquetada como una página web lista para su portafolio.

**Es una skill ORQUESTADORA (thin):** no reimplementa nada. Despacha a los agentes que
ya existen y al final maqueta el HTML.

## Contexto crítico

- **Usuario:** creador/a de contenido hispano (audiencia hispana, español neutro — NO voseo).
- **Reglas de la casa (innegociables):**
  - Referencias virales SIEMPRE reales: URL + reproducciones reales, NUNCA "Original".
  - NUNCA inventar métricas, fechas ni conteos. Si falta un dato real, preguntar.
  - **Checkpoint humano obligatorio** entre la investigación y la producción.
- **Salida:** `entregables/casos-de-estudio/<nicho-slug>-<AAAA-MM-DD>/`
  - `index.html` — la página de caso de estudio (deploy a Netlify/Vercel).
  - `data.json` — los datos estructurados que alimentan el HTML.
  - `calendario.csv` + `calendario.xlsx` — los que devuelve CALI.
- **Render:** `python3` (ver `render_caso_estudio.py` en esta carpeta). El HTML es
  estático (CSS inline, sin React/Babel) — evita el gotcha del artifact en blanco.

## Flujo paso a paso (6 fases, 1 checkpoint)

### Fase 0 — Brief
Si la alumna no dio los datos en el mensaje, pregunta SOLO lo esencial (una tanda):
1. ¿Cuál es tu **nicho** y para quién? (avatar aproximado)
2. ¿Es una **cuenta nueva** o ya existente? (handle si existe)
3. ¿Qué **vendes o vas a vender**? (oferta/producto, aunque sea idea)
4. ¿Cuál es el **propósito del mes**?
   - Experimentación (70% experimentación / 30% crecimiento / 0% venta)
   - Crecimiento (40 / 50 / 10)
   - Nutrición (20 / 70 / 10)
   - Venta (20 / 50 / 30)

Si la alumna ya dio nicho + propósito, no preguntes de más: asume defaults razonables
y anótalos.

### Fase 1 — Investigación (despacha a LUNA)
Despacha el agente **agente-investigadora-f100k** (LUNA) en contexto aislado con este
brief:

> Investiga el nicho **<nicho>** para una cuenta de Instagram/TikTok (<nueva|existente>)
> que vende **<oferta>**. Necesito un brief que incluya: (1) **12 referencias virales
> reales** del nicho con URL + reproducciones + comentarios + engagement + el gancho
> verbal/textual de los primeros 3 segundos; (2) **5 patrones virales recurrentes** que
> se repiten entre esas referencias; (3) un **avatar nombrado** (nombre, rango de edad,
> creencia restrictiva principal, deseo profundo); (4) **si te paso el handle de la
> cuenta del usuario (<@handle>) y tiene historial (~9+ reels), tu PASO 1D: analiza los
> patrones de ESA cuenta (TOP vs BOTTOM con auditor-ganchos-cuenta + analizador-perfiles)
> y sintetiza su ADN — patrones ganadores propios, patrones negativos propios y
> voz/formato/cadencia — y FUSIÓNALO con los del nicho** (qué duplicar, qué oportunidad
> sin explotar, qué evitar). Si la cuenta es nueva/sin data, sáltalo y anótalo, no
> inventes patrones propios. Respeta las reglas: métricas reales, nunca "Original",
> Apify con `APIFY_TOKEN` o links que mande la alumna; nunca navegador logueado. Devuelve todo estructurado.

Cuando LUNA devuelva, **NO sigas todavía**.

### CHECKPOINT humano
Muéstrale a la alumna el resumen de la investigación: las 12 referencias (con métricas),
los 5 patrones del nicho, el avatar, y —si la cuenta tenía data— el **ADN de su cuenta**
(patrones ganadores y negativos propios) y la **fusión** (tu ADN × el nicho: qué duplicar,
qué oportunidad, qué evitar). Pregunta:
> "Esta es la investigación de tu nicho + los patrones de tu propia cuenta. ¿El avatar,
> tus patrones ganadores y la fusión te cuadran, o ajusto algo antes de generar guiones,
> ganchos y el calendario de 30 días?"

Solo continúa cuando la alumna lo apruebe (o corrige y vuelve a Fase 1 acotada).

### Fase 2 + 3 + 4 — Guiones, ganchos y calendario (despacha a CALI)
Despacha el agente **agente-calendarizadora-f100k** (CALI) en contexto aislado,
pasándole la investigación de LUNA y este brief:

> Con esta investigación ya hecha (te paso referencias, patrones y avatar), arma para el
> nicho **<nicho>**, propósito **<propósito>**, un mes completo (**30 reels**):
> (1) **5 guiones** desarrollados, cada uno con pilar temático, gancho verbal, texto en
> pantalla y propósito estratégico; (2) para cada guion, **3 variantes de gancho** con
> la técnica usada (enemigo común / datos concretos / morbo controlado / etc.) y cuál es
> el **ganador y por qué**; (3) un **calendario de 30 días** (día · semana · pilar ·
> título · CTA · formato) respetando la distribución del propósito, exportado en CSV +
> XLSX. Reglas: español neutro, referencias con URL + views reales, nunca inventes
> métricas. Devuélveme las rutas de calendario.csv y calendario.xlsx y el detalle por día.

### Fase 5 — Plan mes 2
Redacta tú (no requiere agente) un plan de mes 2 corto basado en `multiplicador-de-contenido`:
un **formato ancla** (por defecto un podcast de entrevistas del nicho) y el sistema de
reutilización **1 pieza ancla = 8–10 reels**, conectado a la cuenta madre. Ajusta el
ejemplo al nicho de la alumna.

### Fase 6 — Render del caso de estudio
1. Arma el `data.json` con TODO lo recolectado (esquema en `render_caso_estudio.py`).
2. Crea la carpeta de salida y guarda ahí el `data.json`, `calendario.csv` y `.xlsx`.
3. Renderiza:
   ```bash
   python3 skills/caso-estudio-contenido-f100k/render_caso_estudio.py \
     "<carpeta_salida>/data.json" "<carpeta_salida>/index.html"
   ```
4. Abre/verifica el `index.html` y entrega a la alumna:
   - la ruta del `index.html` + cómo subirlo a Netlify (arrastrar carpeta a netlify.com/drop) o `vercel`,
   - la ruta del CSV/XLSX,
   - el recordatorio del checklist de entrega (página publicada + Sheets) para dar el reto por completado.

## Degradación elegante
- Si un agente no está disponible o falla, corre las sub-skills equivalentes
  directamente (`analizador-referencias-virales-f100k`, `guionizacion-formula100k`,
  `generador-ganchos-formula100k`, `calendarizador-contenido-formula100k`) y sigue.
- Si no hay datos reales para una métrica, déjala marcada como pendiente y avisa — NUNCA
  la inventes.

## Lo que esta skill NO hace
- No automatiza el deploy a Netlify (la alumna lo sube; tú le explicas cómo).
- No genera B-roll ni recursos visuales (eso es NOVA / recursos-de-video).
- No coloca nada en Yapper/Bento (esto es un entregable-portafolio).
