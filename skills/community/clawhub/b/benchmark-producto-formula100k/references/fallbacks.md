# Fallbacks · Qué hacer cuando una herramienta falla

Esta skill orquesta varias herramientas externas. Cuando alguna falla, NO abortar — degradar con gracia y marcarlo en el reporte.

---

## 🚨 ESCENARIOS Y RESPUESTAS

### Escenario 1: Apify MCP no está autenticado

**Síntoma:** no aparecen tools `mcp__apify__*` en la lista.

**Respuesta:**
1. Mostrar el bloque del Paso 0 con las 2 opciones (activar / continuar parcial)
2. Si el usuario elige activar, dar instrucciones:
   ```
   1. Abre el chat de Claude (claude.ai o Claude Desktop)
   2. Settings → Connectors → Add MCP Server
   3. URL: https://mcp.apify.com
   4. Sign in con tu cuenta de Apify (o crea una gratis, incluye $5/mes)
   5. Reinicia esta conversación
   ```
3. Si el usuario elige continuar parcial:
   - Marcar en el reporte final: "Sección de reviews externas no disponible — requiere Apify"
   - Marcar en el reporte final: "Sección de ads activos no disponible — requiere Apify"
   - Aún hacer el benchmark de pricing/posicionamiento/producto con Tavily + Supadata

### Escenario 2: Tavily MCP no está autenticado

**Síntoma:** las búsquedas con Tavily devuelven error de auth.

**Respuesta:**
1. Caer a `WebSearch` nativo (siempre disponible)
2. Misma estrategia de queries, solo cambia el motor
3. Marcar en el apéndice: "Discovery realizado con WebSearch en lugar de Tavily — menos profundidad"

### Escenario 3: Un competidor bloquea el scrape de Supadata

**Síntoma:** Supadata devuelve error 403, captcha, o página vacía.

**Respuesta:**
1. Reintentar 1 vez con `format: "html"` en lugar de `markdown`
2. Si sigue fallando, intentar con `WebFetch` simple (modelo + URL)
3. Si sigue fallando, usar `agent-browser` para abrir el sitio con navegador real
4. Si TODO falla, marcar al competidor como "Sitio con anti-bot — análisis basado en lo público (RRSS, Google cache)"

### Escenario 4: La landing del competidor está detrás de login / call-only

**Síntoma:** la URL pública no muestra el producto, solo un form de "agenda llamada".

**Respuesta:**
1. NO inventar. Marcar pricing como "Oculto — requiere call de venta" (esto en sí es un dato).
2. Investigar testimonios/menciones en otras fuentes (LinkedIn del fundador, podcasts, entrevistas) para inferir el rango.
3. Si Apify tiene un scraper de LinkedIn, usarlo para extraer la bio del fundador.
4. Nota en el reporte: "[Marca] usa el modelo 'aplica para hablar con un asesor', típico de high-ticket. Rango estimado por mercado: $X-Y."

### Escenario 5: La comunidad Skool es privada y no tenemos acceso

**Síntoma:** la URL de Skool muestra About Page pero no permite ver el classroom/foro.

**Respuesta:**
1. Analizar TODO lo que SÍ es público en la About Page:
   - Promesa
   - Pricing
   - Bonos
   - Garantía
   - Testimonios visibles
   - Cancellation video (si está)
   - Sample classroom (si lo tienen)
2. Marcar el interior como "no visible — análisis basado en About Page".
3. Sugerir al cliente: "Si quieres ver el interior de [Marca], podrías comprar 1 mes ($X) — pago por research más que vale para un benchmark de [profundidad]."

### Escenario 6: BuiltWith no muestra el stack tech

**Síntoma:** WebFetch a builtwith.com devuelve "no data".

**Respuesta:**
1. Intentar `wappalyzer.com/lookup/[domain]` como alternativa
2. Detectar manualmente desde el HTML del scrape:
   - `skool.com/[community]` en URLs → comunidad en Skool
   - `kajabi.com` o `mykajabi.com` en assets → Kajabi
   - `<meta name="generator" content="...">` → CMS
   - Forms apuntando a `formsubmit.co` / `convertkit.com` / `mailerlite.com`
3. Marcar como "Stack estimado por inspección manual" si no fue automático.

### Escenario 7: El nicho está vacío en Tavily

**Síntoma:** Tavily devuelve <5 candidatos.

**Respuesta:**
1. Reformular queries con sinónimos del nicho
2. Buscar en idioma alterno (si el cliente es español, buscar también en inglés para encontrar referentes globales)
3. Si después de 3 reformulaciones siguen siendo <5: avisar al usuario
   ```
   El nicho "[X]" tiene poca competencia visible online. Posibles razones:
   1. Nicho muy nuevo (oportunidad?)
   2. Nombre del nicho mal definido (¿cómo lo llaman ellos mismos?)
   3. Competencia opera offline / boca en boca
   
   ¿Refinamos el nombre del nicho, o seguimos con los pocos competidores encontrados?
   ```

### Escenario 8: Demasiados competidores (>30)

**Síntoma:** Tavily devuelve 50+ candidatos en un nicho saturado.

**Respuesta:**
1. NO intentar analizarlos todos
2. Filtrar por criterios:
   - Tener landing pública en buen estado
   - Tener al menos 10K seguidores combinados en RRSS
   - Estar activo en últimos 90 días (último post / último ad)
3. Quedarse con los top N según la profundidad elegida
4. Mencionar los descartados en el apéndice: "Otros [N] competidores existen pero fueron descartados por [criterio]. Lista completa en `raw/descartados.md`."

---

## 🛡 REGLA DE ORO

**No inventar datos cuando una herramienta falla.** Es mejor un reporte con menos data y nota honesta que un reporte completo con datos fabricados.

Cada limitación se documenta en la sección "Limitaciones de este reporte" del apéndice, así el usuario/el cliente sabe qué tan robusto es el análisis y dónde habría que profundizar manualmente.

---

## 🔄 ESTRATEGIA DE REINTENTOS

| Herramienta | Reintentos | Backoff | Acción si falla todo |
|-------------|-----------|---------|----------------------|
| Tavily search | 2 | inmediato | Caer a WebSearch |
| Supadata scrape | 1 | inmediato | Caer a WebFetch → agent-browser |
| Apify actor | 1 | inmediato | Marcar dimensión como "no disponible" |
| WebFetch | 1 | inmediato | Marcar URL como "inaccesible" |
| agent-browser | 1 | inmediato | Pedir intervención manual al usuario |

Nunca hacer más de 2 reintentos del mismo error — gasta tiempo y créditos sin valor.
