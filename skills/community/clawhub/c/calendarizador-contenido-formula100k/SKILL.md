---
name: calendarizador-contenido-formula100k
description: "Arma calendarios de contenido semanales (Lunes-Domingo) en CSV y XLSX con la metodología FÓRMULA 100K. Usar SIEMPRE que el usuario pida 'arma mi calendario', 'calendariza estos guiones', 'ordena estas ideas en un calendario', 'convierte esto en calendario semanal', 'haz mi calendario en Excel', 'organiza mis guiones por día', 'calendariza este lote/enlaces/TikToks/reels/carruseles'. 3 modos de entrada: (1) guiones listos; (2) ideas sueltas que desarrolla llamando a guionizacion-formula100k o carrusel-viral-formula100k; (3) enlaces de video que transcribe con transcripcion-youtube-formula100k y reescribe como referencia. 2 tipos de pieza: REELS y CARRUSELES (columnas propias, altura de fila dinámica). Distribución según propósito: Experimentación 70/30/0, Crecimiento 40/50/10, Nutrición 20/70/10, Venta 20/50/30. NO confundir con calendarizador-historias (stories) ni calendarizador-urgencias."
argument-hint: "[pega guiones, ideas o enlaces — o describe lo que quieres calendarizar]"
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Las referencias virales: con `APIFY_TOKEN` usa Apify (TikTok/IG públicos); sin token, tu búsqueda web. Transcripciones de YouTube: `transcripcion-youtube-formula100k` o la que te pegue la usuaria. Nunca navegador logueado.
> - El script `references/generate_calendar.py` corre con python3 sin librerías extra: úsalo con `--output-dir guiones/calendarios/`. El XLSX solo si `openpyxl` está instalado; si no, entrega el CSV.
> - Entrega por Telegram: la tabla resumida en el chat y los archivos como documentos.

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

# Skill: Calendarizador de Contenido FÓRMULA 100K

Convierte guiones, ideas sueltas o enlaces de referencia en un **calendario semanal Lunes-Domingo** listo para producir, exportado a CSV y XLSX.

Soporta **dos tipos de pieza** con esquemas de columnas distintos:

### Tipo REELS (default)

| Columna | Qué contiene |
|---|---|
| **DÍA** | Lunes a Domingo |
| **IDEA** | Concepto/título corto del video |
| **GUION** | Hook + Cuerpo + Outro completo |
| **LLAMADO A LA ACCIÓN** | CTA específico al propósito del slot |
| **FORMATO** | 1 de los 40 formatos del catálogo F100K |
| **REFERENCIA** | URL del video referencia o "Original" |

### Tipo CARRUSELES

| Columna | Qué contiene |
|---|---|
| **DÍA** | Día semana (LUN/MAR/MIE/…) coloreado por semana (S1 amarillo `#FCE96B`, S2 lila `#D9CCEC`) |
| **FECHA** | Fecha absoluta (ej. "18 MAY 2026") |
| **#** | Número del carrusel (01-99) |
| **IDEA** | Título del carrusel |
| **GUION (SLIDE x SLIDE)** | Texto de cada slide concatenado con saltos de línea reales. Altura de fila se ajusta automáticamente al largo del guion (wrap text activado, vertical-align top) |
| **CTA** | Palabra clave del CTA (ej. "MÁQUINA", "ROAST") |
| **FORMATO** | "Carrusel · N slides" |

El tipo CARRUSELES soporta **calendarios de hasta 2 semanas** (11-14 carruseles) en una sola hoja, con coloreo de la columna DÍA por semana para que visualmente se identifique el bloque S1 vs S2.

Distribución de los 7 días según el **propósito del calendario** (los 4 modos de la Estrategia V3.0).

---

## OUTPUTS

Carpeta de salida según tipo de pieza:
- **REELS:** `guiones/calendarios/`
- **CARRUSELES:** `guiones/calendarios/carruseles/`

Genera **3 archivos** por sesión:
1. `calendario_[modo]_[YYYY-MM-DD].csv` — CSV separado por comas, encoding UTF-8 (solo modo reels)
2. `calendario_[modo]_[YYYY-MM-DD].xlsx` — Excel con header en negrita, columnas anchas
3. Tabla markdown en el chat (preview)

Para tipo CARRUSELES el nombre por defecto es `00_CALENDARIO_CARRUSELES.xlsx` (en la carpeta destino del proyecto), pero el usuario puede pedir un nombre con fecha.

Donde `[modo]` es uno de: `experimentacion`, `crecimiento`, `nutricion`, `venta`.

---

## FLUJO COMPLETO (seguir en orden)

### PASO 0 · Detectar tipo de pieza (REELS vs CARRUSELES)

**Antes que nada**, determinar si lo que se va a calendarizar son **reels** (default) o **carruseles**.

Señales para detectar tipo CARRUSELES:
- Usuario menciona explícitamente "carrusel", "carruseles", "slides", "diapositivas"
- Input incluye estructura "SLIDE 1 / SLIDE 2 / …" o "Slide 1: … Slide 2: …"
- Usuario pasa archivos `.md` generados por la skill `carrusel-viral-formula100k`
- Carpeta de origen es `entregables/carruseles/`

Si no hay señales explícitas → asumir **REELS**.

Si hay ambigüedad → preguntar:
> ¿Estos son reels o carruseles? Cambia las columnas del calendario y el formato del guion.

El tipo de pieza determina:
- Esquema de columnas del CSV/XLSX (ver tabla de `QUÉ HACE` arriba)
- Si el guion va resumido en una línea (reels) o slide-by-slide completo (carruseles)
- Carpeta de output: `CALENDARIOS/` para reels · `CARRUSELES/CALENDARIO DE CARRUSELES/` para carruseles

### PASO 1 · Detectar modo de entrada

Inspecciona lo que pegó el usuario y clasifica:

| Señal en el input | Modo |
|---|---|
| Bloques largos con "Hook:", "Gancho:", "Cuerpo:", "CTA:", o párrafos completos de 80+ palabras por idea | **Modo A · Guiones listos** |
| Líneas cortas (5-30 palabras) que describen un tema o concepto, sin estructura de guion | **Modo B · Ideas sueltas** |
| URLs de TikTok, Instagram Reels, YouTube Shorts/Long | **Modo C · Enlaces de referencia** |
| **SOLO nicho/avatar/brief de cliente** (sin guiones, sin ideas, sin URLs) — ej. "calendariza para mi clienta que es nutricionista de SII" | **Modo D · Investigación viral por keyword** ⭐ |
| Mezcla de varios | **Modo Híbrido** — procesa cada bloque según su tipo |

> ⚠️ **Modo D es el default cuando solo tienes el brief del cliente.** NO inventes ideas genéricas del nicho. Primero caza referencias virales reales en TikTok/IG por keyword. El calendario debe basarse en lo que ya está funcionando, no en lo que tú asumes que funciona.

### PASO 2 · Preguntar propósito del calendario

Antes de calendarizar, **siempre** preguntar (a menos que el usuario lo haya dicho explícitamente):

> ¿Cuál es el propósito de este calendario? Elige uno:
> - 🧪 **Experimentación** (70% viral / 30% valor / 0% venta) — recién empiezas o no tienes formato estrella
> - 📈 **Crecimiento** (40% viral / 50% valor / 10% venta) — atraer audiencia fría nueva
> - 🌱 **Nutrición** (20% viral / 70% valor / 10% venta) — pre-lanzamiento, calentar audiencia
> - 💰 **Venta** (20% viral / 50% valor / 30% venta) — lanzamiento o promo activa en 14 días

Si el usuario duda, ofrécele hacer el mini test (5 preguntas) que está en el artifact `f100k-estrategia-contenido.html`.

### PASO 3 · Asignar slots Lunes-Domingo según propósito

Cada modo tiene un patrón fijo de 7 días con tipo (Viral/Valor/Venta) y formato sugerido:

Cargar la tabla de slots desde [references/slots-por-modo.md](references/slots-por-modo.md). Resumen:

**🧪 Experimentación** (cada día un formato distinto, prioridad viralidad):
- Lun: Viral · POV (#3) · Mar: Viral · Sketch (#7) · Mié: Valor · Pizarra (#19) · Jue: Viral · Cinemático (#2) · Vie: Viral · Historia Curiosa (#1) · Sáb: Valor · Mitos (#23) · Dom: Viral · Reacción Viral (#4)

**📈 Crecimiento** (40/50/10):
- Lun: Valor · Pizarra (#19) · Mar: Viral · POV (#3) · Mié: Valor · Versus (#12) · Jue: Viral · Sketch (#7) · Vie: Valor · Mitos (#23) · Sáb: Viral · Cinemático (#2) · Dom: Venta · Testimonio (#32)

**🌱 Nutrición** (20/70/10):
- Lun: Valor · Tutorial (#25) · Mar: Valor · Pizarra (#19) · Mié: Viral · POV (#3) · Jue: Valor · Versus (#12) · Vie: Valor · Mitos (#23) · Sáb: Valor · Errores (#30) · Dom: Venta · Testimonio (#32)

**💰 Venta** (20/50/30):
- Lun: Valor · Tutorial (#25) · Mar: Venta · Testimonio (#32) · Mié: Valor · Errores (#30) · Jue: Viral · POV (#3) · Vie: Venta · Demo (#33) · Sáb: Valor · Pizarra (#19) · Dom: Venta · Caso de Éxito (#34)

> Los formatos por día son **sugerencias base**. Si una idea/guion del usuario calza mejor con otro formato del catálogo (ver [references/catalogo-40-formatos.md](references/catalogo-40-formatos.md)) que respeta el tipo del slot, úsalo.

### PASO 4 · Procesar cada modo de entrada

#### MODO A · Guiones listos

1. Para cada guion del usuario:
   - Detectar el formato implícito (Tutorial, POV, Versus, etc.) leyendo la estructura del cuerpo
   - Detectar el tipo (Viral/Valor/Venta) por el CTA y nivel de conciencia que ataca
2. Hacer match de cada guion al slot del día que más se ajuste
3. Si hay más guiones que slots (>7), avisar al usuario y preguntar qué semana usar (esta o la siguiente)
4. Si hay menos de 7 guiones, completar slots vacíos sugiriendo desarrollar nuevas ideas (no inventar guiones a la fuerza)

#### MODO B · Ideas sueltas

1. Para cada idea, decidir formato basándose en el slot del día asignado y el catálogo de 40 formatos
2. **Delegar el desarrollo del guion** a la skill apropiada:
   - Si el slot pide formato carrusel (poco común en calendario semanal de reels) → usar `carrusel-viral-formula100k`
   - En todos los demás casos → usar `guionizacion-formula100k`
3. Para invocar la skill: usa el formato de delegación de Claude Code, pasando: la idea, el formato sugerido, el tipo (viral/valor/venta), y la instrucción de devolver Hook + Cuerpo + CTA en formato compacto
4. Mientras se desarrollan los guiones, ir poblando la tabla

#### MODO C · Enlaces de referencia

1. Para cada URL:
   - Llamar a `transcripcion-youtube-formula100k` para YouTube, o usar Supadata/yt-transcript-mcp si es TikTok/Reels
   - Extraer la transcripción y los puntos clave
2. **Reescribir la idea con voz del usuario** aplicando frameworks F100K (no copiar)
3. Pasar el guion reescrito por `guionizacion-formula100k` para validar estructura y CTA
4. Guardar la URL original en la columna REFERENCIA

#### MODO D · Investigación viral por keyword ⭐

**Usar SIEMPRE que solo tengas el brief del cliente (nicho + avatar) y NO tengas guiones, ideas ni URLs.** Es el modo más común para clientes nuevos del usuario.

Pipeline:

1. **Extraer 4-6 keywords del nicho** desde el brief del cliente. Combinar:
   - Keyword del problema central (ej. "colon irritable", "ansiedad laboral", "primera casa")
   - Keyword del avatar (ej. "mujer profesional", "emprendedora")
   - Keyword de la solución/método (ej. "FODMAP", "IA productividad", "venta crypto")
   - Keyword de objeciones comunes (ej. "no funciona", "estafa", "mito")

2. **Invocar `analizador-referencias-virales-f100k`** con las keywords del paso 1:
   - Input: keywords extraídas + plataforma "Ambas" + contexto del nicho del cliente
   - La skill busca en TikTok + IG (Apify), transcribe con Supadata, identifica gancho verbal/textual/visual por video, y devuelve tabla enriquecida con `formato_inferido` por video
   - Costo aprox: **$0.80-$1.20 por calendario** (Apify TikTok + IG + transcripciones)
   - Si el nicho tiene mucho YouTube (negocios, finanzas, salud): complementar con vidIQ MCP para outliers

3. **Si la skill devuelve <7 refs** con +20K views → avisar al usuario que el nicho es chico y usar las mejores disponibles. NO inventar ideas genéricas.

4. **Mapear cada viral a un slot del calendario** usando el `formato_inferido` que la skill ya detectó:
   - `Pizarra / Valor` → slots de Valor
   - `POV / Viral` → slots de Viral
   - `Testimonio / Venta` → slots de Venta
   - Si más de un viral compite por el mismo slot, elegir el de más views

5. **Reescribir cada idea con voz del cliente** aplicando frameworks F100K:
   - NO copiar el guion del viral, solo el ÁNGULO y el HOOK
   - Adaptar al avatar específico del cliente (ej. el viral habla a público general → reescribir para "mujer profesional con SII")
   - Aplicar las 35 estructuras de `guionizacion-formula100k` para mantener calidad de hook + cuerpo + CTA
   - Si el cliente escribe en voseo (Ricardo Shiva, argentinos), adaptar. Default = español neutro tú.

6. **Llenar la columna REFERENCIA con la URL real del viral** + las métricas (ej. `https://www.tiktok.com/@dra/video/123 (458K views)`)

**Reglas clave del Modo D:**
- ❌ NUNCA inventar ideas del nicho desde tu conocimiento general. Si no hay refs reales, AVISAR al usuario que el nicho no tiene viralidad medible aún.
- ❌ NUNCA copiar guiones verbatim del viral. Inspirarse en ángulo + hook, reescribir.
- ✅ La columna REFERENCIA SIEMPRE lleva la URL real + views (nunca "Original" en Modo D).
- ✅ Mezclar refs de TikTok + IG + YouTube para evitar dependencia de un solo algoritmo.
- ✅ Si el cliente tiene cuenta de IG/TikTok pre-existente, primero analizar SUS top reels con `analizador-perfiles-formula100k` y solo después complementar con búsqueda de refs externas.

#### MODO Híbrido

Procesar cada bloque del input según su tipo. Mantener el orden del usuario solo si hay 7 piezas; si hay diferente cantidad, redistribuir según slots óptimos.

### PASO 5 · Asignar CTAs según tipo de slot

| Tipo de slot | CTA por defecto |
|---|---|
| Viral | "Sígueme para más" |
| Valor | "Guarda este post" o "Comenta [palabra clave] para enviarte el [recurso]" |
| Venta | "Haz clic en el enlace" / "Link en bio" / "Reserva tu lugar" |

Si el guion ya trae CTA, respétalo (solo verifica que coincida con el tipo del slot — si hay error de coherencia, corregir y avisar al usuario).

### PASO 6 · Generar archivos CSV y XLSX

Ejecutar el script Python `generate_calendar.py` (ubicado en `references/generate_calendar.py`) pasando los datos como JSON via stdin. El argumento `--tipo-pieza` cambia el esquema de columnas y el layout del Excel:

**Modo REELS:**
```bash
python3 skills/calendarizador-contenido-formula100k/references/generate_calendar.py \
  --tipo-pieza "reels" \
  --modo "[modo]" \
  --output-dir "guiones/calendarios/" \
  --data-json '<JSON_DATA>'
```

**Modo CARRUSELES:**
```bash
python3 skills/calendarizador-contenido-formula100k/references/generate_calendar.py \
  --tipo-pieza "carruseles" \
  --modo "[modo]" \
  --output-dir "guiones/calendarios/carruseles/" \
  --output-name "00_CALENDARIO_CARRUSELES" \
  --data-json '<JSON_DATA>'
```

JSON para REELS:

```json
{
  "modo": "crecimiento",
  "fecha_inicio": "2026-05-04",
  "filas": [
    {"dia":"Lunes","idea":"...","guion":"...","cta":"...","formato":"Pizarra (#19)","referencia":"Original"},
    {"dia":"Martes","idea":"...","guion":"...","cta":"...","formato":"POV (#3)","referencia":"https://..."}
  ]
}
```

JSON para CARRUSELES (más campos por fila):

```json
{
  "modo": "crecimiento",
  "fecha_inicio": "2026-05-18",
  "titulo": "CALENDARIO DE CARRUSELES — SEMANA 18 MAYO 2026",
  "subtitulo": "[TU NOMBRE] · [TU MARCA] · @tuhandle",
  "filas": [
    {
      "dia": "LUN",
      "fecha": "18 MAY 2026",
      "numero": "01",
      "idea": "Te están viendo la cara con Claude",
      "guion": "SLIDE 1 — GANCHO\n\"Te están viendo la cara con Claude\"\n\nSLIDE 2 — EL PROBLEMA\n...",
      "cta": "MÁQUINA",
      "formato": "Carrusel · 7 slides",
      "semana": "S1"
    }
  ]
}
```

Notas clave del modo carruseles:
- Campo `semana` con valor `"S1"` o `"S2"` colorea la celda DÍA (amarillo `#FCE96B` o lila `#D9CCEC`).
- Campo `guion` debe traer los slides separados con `\n\n` o títulos `SLIDE N — …`. El script calcula la altura de fila automáticamente.
- El script NO genera CSV para tipo carruseles (los saltos de línea internos del guion rompen Excel CSV); solo XLSX.

El script genera los archivos automáticamente. Si Python no tiene `openpyxl` instalado, intenta `pip install openpyxl --quiet` antes; si falla, generar solo CSV (reels) o avisar (carruseles).

### PASO 7 · Mostrar preview en chat

Imprimir tabla markdown con los 7 días. Truncar GUION a primeras 80 caracteres + "…" para que el preview sea legible. Después de la tabla, listar:
- 📁 Ruta del CSV
- 📊 Ruta del XLSX
- 📌 Resumen de distribución (X viral / Y valor / Z venta)
- ⚠️ Si algún slot quedó vacío o forzado

---

## FORMATO DE OUTPUT EN CHAT

```markdown
## 📅 Calendario [Modo] · Semana del [fecha]

| DÍA | IDEA | GUION (preview) | CTA | FORMATO | REFERENCIA |
|---|---|---|---|---|---|
| Lunes | ... | ... | ... | ... | ... |
| ... | | | | | |

📁 CSV: guiones/calendarios/calendario_[modo]_[fecha].csv
📊 XLSX: guiones/calendarios/calendario_[modo]_[fecha].xlsx

📌 Distribución real: X viral / Y valor / Z venta
✅ Listo para producir
```

---

## REGLAS Y GUARDARRAÍLES

- **NUNCA inventar referencias** (URLs falsas). Si la idea no tiene referencia, columna = "Original".
- **NUNCA mezclar tipos en un mismo slot.** Si una idea de venta cae en slot viral, mover de día o pedir reemplazo al usuario.
- **NUNCA inflar guiones a relleno.** Mejor 5 días con guiones sólidos + 2 slots vacíos que 7 días forzados.
- **Si el usuario tiene >7 ideas/guiones**, ofrecer guardar las extras para la semana siguiente (crear segundo archivo).
- **Si el usuario tiene <7**, completar el resto sugiriendo ángulos basados en los pilares (Problema/Solución/Resultado) de su nicho — no inventar contenido.
- **Respetar el formato estrella del usuario** si lo menciona ("siempre uso pizarra"). En ese caso, predominar ese formato sin romper la distribución viral/valor/venta del modo.
- **Si el usuario pasa enlaces sin contexto de su nicho**, preguntar el nicho antes de reescribir.
- **No llamar a las skills delegadas si el guion ya está completo** (Modo A) — ahorra tokens.
- **Encoding del CSV: UTF-8 con BOM** para que Excel en Mac/Windows abra acentos correctamente.

---

## REFERENCIAS Y ARCHIVOS DE APOYO

- `references/slots-por-modo.md` — Tabla completa de slots Lun-Dom para los 4 modos
- `references/catalogo-40-formatos.md` — Los 40 formatos F100K agrupados (A/B/C)
- `references/generate_calendar.py` — Script Python que produce CSV + XLSX
- `references/ejemplos-cta.md` — Bank de CTAs por tipo de slot

---

## EJEMPLO DE INVOCACIÓN

**Usuario:** "Calendariza estos 5 guiones para mi semana de venta del lanzamiento del 12 de mayo"

**Skill:**
1. Detecta Modo A (guiones listos)
2. Confirma propósito = Venta (20/50/30)
3. Mapea cada guion a un día según tipo (probablemente 1 viral / 2-3 valor / 2 venta)
4. Para los 2 días sin guion del usuario, sugiere completarlos con: 1 testimonio extra (slot venta domingo) y 1 valor (Tutorial paso a paso)
5. Genera CSV + XLSX
6. Muestra preview con distribución real y rutas de archivos
