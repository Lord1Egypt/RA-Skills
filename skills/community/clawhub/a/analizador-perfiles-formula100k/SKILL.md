---
name: analizador-perfiles-formula100k
description: "Analiza perfiles de Instagram y TikTok a profundidad. Usar SIEMPRE que se pida analizar un perfil, revisar métricas, identificar qué videos funcionan/repetir/dejar de hacer, qué genera seguidores o ventas, auditar una cuenta, diagnosticar por qué no crece, o cualquier análisis de contenido en redes. En un agente OpenClaw la captura es: Composio con Instagram profesional para la cuenta propia (métricas reales), Apify para cuentas ajenas (datos públicos, reels con transcripción) o capturas que manda la usuaria; nunca un navegador logueado. Basada en la metodología F100K para leer métricas como experta: top videos, ángulos de venta, qué dejar de hacer, vacíos en comentarios y plan de 2 semanas."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - **En este servidor NO se usa agent-browser ni sesión logueada** aunque la skill lo pida primero: el PASO 2 y el 2.5 se hacen con otras fuentes.
> - Cuenta propia: Composio con Instagram profesional (alcance, guardados, compartidos reales). Cuentas ajenas: Apify con `APIFY_TOKEN` (datos públicos; `references/auditoria-profunda-apify.md`). Sin ninguno: pide capturas de estadísticas y de los posts.
> - Transcripts con Supadata solo si hay `SUPADATA_API_KEY`. Comentarios: Apify o capturas.
> - Lo que solo se ve con login (retención, insights de cuentas ajenas) va marcado como no disponible: no lo estimes. Informe en `informes/` y por Telegram.

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

# Skill: Analizador de Perfiles FORMULA 100K

Skill especializada en auditar perfiles de Instagram y TikTok con la metodología de FORMULA 100K. Usa Supadata MCP para obtener datos reales de videos, métricas y tendencias.

---

## PROCESO OBLIGATORIO DE ANÁLISIS

### PASO 1 — Recolectar información del perfil
Preguntar si no se proporcionó:
1. ¿Cuál es el usuario o URL del perfil a analizar? (Instagram o TikTok)
2. ¿Cuál es el objetivo del creador? (vender, crecer audiencia, monetizar, autoridad)
3. ¿Cuánto tiempo lleva activo el perfil?
4. ¿Hay algún video o período específico que preocupa?
5. **¿Quieres una evaluación profunda con descarga de reels y transcripciones de audio?** (usa Apify, costo ~$0.40-$3 según volumen, tarda 1-2 minutos extra). Si sí → activar PASO 2.C además de los demás.

> **Importante:** la pregunta 5 NO se hace automáticamente para auditorías express. Solo cuando el usuario:
> - Pidió explícitamente analizar CTAs, ganchos o patrones reproducibles
> - Pidió un análisis "completo", "profundo" o "exhaustivo"
> - agent-browser falló por detección CDP (página de error de IG)
> - Quiere transcripciones del audio de varios reels

### PASO 2 — Extraer datos · agent-browser primero, Supadata como complemento

**Stack obligatorio (en este orden):**

**A. agent-browser (motor principal)**

Lanzar agent-browser con sesión real logueada para extraer lo que ningún API puede ver:

```
[agent-browser]

Abre Chrome con sesión existente (IG/TikTok logueados con la cuenta del usuario).

Para el perfil @[usuario]:
1. Visita instagram.com/[usuario]/reels/ (o tiktok.com/@[usuario])
2. Extrae los 30 reels/videos más recientes con:
   - URL del reel
   - Caption completo
   - Views (número exacto si IG lo muestra)
   - Likes + comentarios + compartidos (si visibles)
   - Formato del primer frame (rostro/texto grande/split/B-roll/etc.)
   - Tipo (reel, carrusel, post estático)
3. Si el usuario es dueña del perfil → entrar a Reels Insights y sacar:
   - Retención promedio
   - Alcance no-seguidores
   - Guardados, compartidos
4. Para los TOP 5 por engagement: visita cada reel y extrae los 50 comentarios principales.

OUTPUT: markdown crudo con secciones por video. Sin análisis.
```

**B. Supadata MCP (complemento)**

Solo cuando agent-browser ya extrajo el listado y necesitas:
- `supadata_transcript` → texto completo de un video específico (útil para analizar el guion)
- `supadata_metadata` → datos generales del perfil si el público es accesible

Para TikTok: `https://www.tiktok.com/@usuario`
Para Instagram: `https://www.instagram.com/usuario/`

**Si Supadata responde con "limit-exceeded" o login wall:** agent-browser ya tiene los datos, no hay bloqueo. Sigue adelante.

Extraer mínimo los últimos 20-30 videos.

**C. Apify · `apify~instagram-reel-scraper` (OPCIONAL, solo si el usuario lo pidió en PASO 1.5)**

Activar este módulo cuando:
- El usuario respondió SÍ a la pregunta de auditoría profunda en el PASO 1
- O agent-browser fue bloqueado por la página de error de IG (detección CDP)
- O se necesitan 60+ reels con transcripciones de audio palabra-por-palabra

Proceso de 2 pasadas (instrucciones completas en `references/auditoria-profunda-apify.md`):

1. **Pasada 1** — `mcp__apify__call-actor` con `apify~instagram-reel-scraper` + `{username:[usuario], resultsLimit:60}` para obtener metadata de 60 reels SIN transcript. Costo ~$0.16.
2. **Ordenar por `commentsCount` descendente** y elegir top 5-10.
3. **Pasada 2** — re-llamar al actor pasando las URLs específicas + `includeTranscript: true`. Costo ~$0.24.
4. Output cruza con el análisis de patrones de CTA (ver `references/auditoria-profunda-apify.md` → sección "Análisis de patrones de CTA" y la memoria [[feedback-ctas-guiones]]).

**Gotcha:** el transcriber confunde "Claude" con "Cloud". Corregir en el reporte final.

### PASO 2.5 — Comentarios de los videos más virales (agent-browser)

agent-browser ya los trajo en el PASO 2.A.4. Si quedaron pendientes, ejecuta:

```
[agent-browser]

Para cada URL de video en [lista_top5]:
1. Visita la URL
2. Despliega TODOS los comentarios visibles (scroll + clic en "ver más respuestas")
3. Extrae cada comentario con: autor · texto · likes · respuestas
4. Output markdown ordenado por likes descendente.
```

**Qué buscar en los comentarios (clasificar cada comentario en una categoría):**

| Categoría | Ejemplos | Qué revela |
|-----------|----------|------------|
| 🔍 **Preguntas sin responder** | "¿cómo hago para...?", "¿dónde consigo...?" | Vacío de contenido = oportunidad de video |
| 😤 **Frustraciones explícitas** | "nadie me explica...", "siempre me pasa que..." | Dolor de mercado no resuelto |
| 💡 **Deseos declarados** | "quisiera que hicieras un video de...", "me encantaría saber..." | Demanda validada de contenido |
| ⚠️ **Objeciones y miedos** | "sí pero...", "eso no funciona porque...", "qué pasa si..." | Ideas para refutar objeciones en contenido de venta |
| ✅ **Validaciones sociales** | "esto me pasó exactamente", "yo lo hice y funciona" | Prueba social → usar como ángulo de testimonial |

**Aplicar también a perfiles de competidores** si el usuario quiere analizar vacíos en su nicho:
- Scrapear los top 3-5 videos virales del competidor
- Buscar preguntas que el competidor NO respondió en su contenido
- Esas preguntas no respondidas = **vacíos de contenido** que tú puedes cubrir

Ver guía completa en: `references/analisis-comentarios.md`

### PASO 3 — Clasificar cada video en 4 categorías
Basado en métricas de comentarios, likes, compartidos y vistas:

| Categoría | Criterio | Acción |
|-----------|----------|--------|
| 🟢 **REPETIR** | Alto engagement + comentarios elevados | Hacer más videos con este ángulo |
| 🔵 **ESCALAR** | Vistas altas + bajo engagement | Mejorar CTA y gancho |
| 🔴 **ELIMINAR** | Bajo rendimiento en todo + 3+ meses sin tracción | Dejar de hacer este formato |
| 🟡 **OPTIMIZAR** | Potencial pero métricas mediocres | Cambiar gancho o estructura |

### PASO 4 — Análisis de Métricas con Metodología FORMULA 100K
Ver instrucciones detalladas en: `references/lectura-metricas.md`

Aplicar el marco completo de interpretación de métricas para dar diagnóstico preciso.

### PASO 5 — Identificar Ángulos Ganadores de Venta
Listar los videos con MÁS comentarios → estos son los **ángulos de venta ganadores**.
- Los comentarios = personas interesadas que puedes contactar
- Las vistas NO igualan ventas
- El video con más comentarios = el tema que más conecta con intención de compra
- Cruzar con el análisis de comentarios del PASO 2.5 para validar qué ángulos tienen demanda real
- **Si se ejecutó PASO 2.C (modo profundo con Apify)**: agregar al reporte una sección dedicada "Top N CTAs ganadores" con caption verbatim, transcripción corregida (Claude/Cloud), gancho del primer segundo, CTA exacto y los 6 patrones que se cumplen. Estructura completa en `references/auditoria-profunda-apify.md` → sección "Output del modo profundo".

### PASO 5.5 — Detectar Vacíos de Contenido en Competidores
Si se analizaron comentarios de competidores en el PASO 2.5:
- Listar las preguntas recurrentes que el competidor NO respondió en su contenido
- Identificar frustraciones que siguen sin solución en el nicho
- Convertir cada vacío en una **idea de contenido accionable** para el creador analizado
- Priorizar por frecuencia: las preguntas que más se repiten = mayor demanda

Ver framework completo en: `references/analisis-comentarios.md`

### PASO 6 — Entregar Reporte Final
Estructura del reporte obligatorio (ver `references/reporte-estructura.md`).

---

## FRAMEWORK DE INTERPRETACIÓN RÁPIDA

### Señales de crecimiento de seguidores
- Videos con alta tasa de guardados → contenido de alto valor → genera follows orgánicos
- Videos con alto % de reproducción completa → formato correcto → el algoritmo lo amplifica
- Videos con muchos compartidos → contenido identificable → atrae audiencia nueva

### Señales de potencial de venta
- Videos con comentarios tipo pregunta ("¿cómo hago eso?", "¿cuánto cuesta?")
- Videos donde la gente menciona problemas específicos
- Videos con palabras clave del nicho en comentarios
- Estos son los **ángulos de venta**: repetirlos en variantes

### Señales de contenido a detener
- Videos con menos del 15% de engagement vs promedio del perfil
- Formato que no genera ni comentarios ni guardados ni shares
- Temas ajenos al nicho central que no conectan
- Videos donde las vistas son altas pero sin ninguna otra acción

---

## REGLAS DEL ANÁLISIS

1. **Vistas ≠ ventas.** Siempre priorizar comentarios y engagement cualitativo
2. **No recomendar borrar videos** a menos que tengan 3+ meses sin tracción y dañen la imagen del perfil
3. **Cada recomendación debe tener evidencia** del análisis (citar el video específico)
4. **Siempre dar ejemplos accionables** de qué cambiar (no solo decir "mejora el gancho", sino cómo)
5. **Comparar contra el promedio del propio perfil**, no contra benchmarks externos genéricos
6. Si no hay datos suficientes (perfil muy nuevo, menos de 10 videos), indicarlo claramente

---

## REFERENCIA DETALLADA

Para lectura de curvas de retención y patrones de métricas:
→ `references/lectura-metricas.md`

Para estructura del reporte final:
→ `references/reporte-estructura.md`

Para scrapeo y clasificación de comentarios + detección de vacíos de contenido:
→ `references/analisis-comentarios.md`

Para auditoría profunda OPCIONAL con Apify (descarga masiva de reels + transcripciones + análisis de patrones de CTA):
→ `references/auditoria-profunda-apify.md`
