---
name: broll-vsl-formula100k
description: "Genera entre 15-25 clips de B-roll cinematográficos para VSL o videos largos usando Higgsfield Seedance 2.0 y Cinema Studio 3.0. Regla 80/20: 80% de los clips incluyen el avatar/presentadora con foto de referencia (Seedance 2.0 + medias identity), 20% son tomas cinemáticas abstractas sin persona (Seedance 2.0 o Cinema Studio 3.0 puro). Estética configurable (default: cyberpunk azul eléctrico). Input: guion VSL (texto). Output: catálogo completo con URLs de video + frase exacta del guion donde insertar cada clip. Activar cuando se diga 'genera b-roll para mi VSL', 'clips para video largo', 'recursos cinematográficos para mi guion', 'haz los b-rolls de mi VSL', o cualquier variación que combine un guion largo (VSL, webinar, masterclass) con producir clips de b-roll con Higgsfield."
argument-hint: "<ruta-al-guion.md | texto-del-guion> [--escenas=N] [--estetica=cyberpunk|corporativo|minimalista] [--duracion=5]"
allowed-tools: "Bash, Read, Write, AskUserQuestion, mcp__higgsfield__generate_video, mcp__higgsfield__job_status, mcp__higgsfield__media_upload, mcp__higgsfield__media_confirm"
metadata: {"version": "1.0.0", "models": ["seedance_2_0", "cinematic_studio_3_0"], "aspect_ratio": "16:9", "default_duration": 5, "max_concurrent_jobs": 8, "openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Genera video con el plugin de Higgsfield: solo si está conectado. Es de lo más caro por pieza: antes calcula créditos totales (clips × duración), muéstralos y espera ✅.
> - Las preguntas con opciones van por Telegram, numeradas. La foto de referencia sale de `cerebro/fotos/`; si está vacía, pide 1 a 3 fotos enviadas como archivo.
> - Sin Higgsfield: entrega la lista de escenas con su prompt en inglés, lista para pegar en Higgsfield a mano.
> - Los clips se descargan a `entregables/broll/` y se mandan por link o como archivo si pesan menos de 50 MB (límite de Telegram).

---

# B-Roll VSL — FÓRMULA 100K

Genera clips de B-roll cinematográficos con Higgsfield para enriquecer VSLs y videos largos, priorizando siempre la presencia de la presentadora (80% con avatar, 20% cinemático puro).

---

## Cuándo activar

- El usuario pasa un guion de VSL, masterclass, webinar o cualquier video largo (>5 min de script)
- Pide "b-roll", "clips cinematográficos", "recursos visuales para mi guion", "haz los videos de mi VSL"
- Quiere un catálogo final con URLs y frases de inserción

## NO activar para

- Videos cortos (reels <3 min) → `recursos-de-video-formula100k`
- Solo imágenes fijas → `graficos-de-video-formula100k`
- Videos con avatar hablando (lip-sync) → `videos-avatar-formula100k`
- Stories de IG → `historias-a-imagenes-nanobanana`

---

## Regla 80/20 — OBLIGATORIA

| Tipo | % | Modelo | Cuándo usar |
|------|---|--------|-------------|
| **Avatar** (con foto de referencia) | **80%** | Seedance 2.0 | Momentos emocionales, CTAs, credibilidad, transformación, autoridad, revelaciones personales |
| **Cinemático abstracto** (sin persona) | **20%** | Seedance 2.0 o Cinema Studio 3.0 | Conceptos abstractos, sistemas/tecnología, tiempo/urgencia, datos/métricas, redes/comunidades |

Si el guion tiene 20 escenas → 16 con avatar + 4 sin avatar.
Si tiene 15 → 12 con avatar + 3 sin avatar.
Si tiene 25 → 20 con avatar + 5 sin avatar.

Redondear **hacia arriba** en la categoría con avatar. El presentador es la marca.

---

## Estilos disponibles

| Clave | Paleta | Géneros preferidos | Ideal para |
|-------|--------|-------------------|------------|
| `cyberpunk` (default) | Azul eléctrico #00BFFF, neón, fondo oscuro | `action`, `epic`, `drama` | VSLs de cursos digitales, IA, marketing |
| `corporativo` | Azul navy, blanco, plateado | `drama`, `epic` | Coaching de negocios, finanzas, liderazgo |
| `minimalista` | Blanco-gris-negro, una acción de color | `drama` | Bienestar, lifestyle, marca personal premium |
| `espiritual` | Dorado, violeta, negro | `drama`, `epic` | Coaching espiritual, desarrollo personal |
| `calido` | Ámbar, tierra, luz solar | `drama`, `comedy` | Salud, familia, nicho femenino |

---

## Pipeline (8 pasos)

### Paso 1 — Recibir el guion

Aceptar el guion como:
- Texto pegado directamente en el chat
- Ruta a un archivo `.md`, `.txt`, `.docx` → leer con `Read`
- Si es `.docx`, extraer texto con: `python3 -c "import docx; print('\n'.join([p.text for p in docx.Document('archivo.docx').paragraphs]))"` (requiere `python-docx`)

Si el guion es muy largo (>10,000 palabras), confirmar que es correcto antes de continuar.

### Paso 2 — Preguntar configuración básica

Si el usuario no especificó los parámetros en el mensaje, preguntar con `AskUserQuestion`:

```
AskUserQuestion:
  questions:
    - question: "¿Cuántos clips de B-roll necesitas para esta VSL?"
      header: "Cantidad de clips"
      multiSelect: false
      options:
        - label: "15 clips"
          description: "Ideal para VSLs de 15-20 minutos. Densidad media."
        - label: "20 clips (Recomendado)"
          description: "El sweet spot para la mayoría de VSLs de 25-35 minutos."
        - label: "25 clips"
          description: "Alta densidad visual. VSLs largas con mucha narrativa."

    - question: "¿Qué estética quieres para los clips?"
      header: "Estética visual"
      multiSelect: false
      options:
        - label: "Cyberpunk / Futurista (Recomendado)"
          description: "Azul eléctrico, neón, fondo oscuro. Ideal para contenido de marketing digital e IA."
        - label: "Corporativo"
          description: "Navy, plateado, limpio. Para negocios, finanzas, coaching ejecutivo."
        - label: "Cálido / Lifestyle"
          description: "Ámbar, tierra. Para bienestar, lifestyle, marca personal femenina."
        - label: "Espiritual"
          description: "Dorado y violeta. Para desarrollo personal, mindset, espiritualidad."
```

Atajos textuales que saltan la pregunta:
- "20 clips", "15 clips", "25 clips" → número de escenas directo
- "cyberpunk", "corporativo", "cálido", "espiritual" → estética directa
- Si el usuario ya lo dijo en el mensaje inicial, NO preguntar

### Paso 3 — Obtener foto de referencia de la presentadora

**Si el usuario ya tiene su carpeta de selfies configurada** (por ejemplo `cerebro/fotos`, o la que haya indicado en sesiones anteriores) y esa carpeta existe: saltar la pregunta y usarla. Leer 3-4 archivos con `Read` y elegir el que tenga: cara frontal/3-cuartos clara, buena iluminación, sin objetos tapando el rostro, expresión neutra o natural. Priorizar fotos con fondo limpio.

**Si no hay carpeta conocida:** preguntar:

```
AskUserQuestion:
  questions:
    - question: "¿Dónde están tus selfies/fotos de referencia para los clips con tu avatar?"
      header: "Fotos de referencia"
      multiSelect: false
      options:
        - label: "Tengo una carpeta, te paso la ruta"
          description: "Ejemplo: cerebro/fotos. El sistema elige la mejor automáticamente."
        - label: "No tengo fotos — usar solo tomas cinemáticas"
          description: "Se genera el 100% como tomas abstractas/cinemáticas, sin avatar personal."
```

**Si hay foto de referencia → subirla a Higgsfield:**

```
1. mcp__higgsfield__media_upload(filename: "reference.jpg")
   → recibir {upload_url, media_id}

2. Bash: curl -X PUT -T "<ruta_foto>" "<upload_url>"
   → respuesta vacía = éxito

3. mcp__higgsfield__media_confirm(media_id: "<media_id>")
   → confirmar registro

4. Guardar media_id en memoria conversacional → se reutiliza en TODAS las escenas con avatar
```

**Si NO hay foto** → pasar a modo 100% cinemático (ignorar la regla 80/20, generar todo con Seedance abstracto o Cinema Studio).

### Paso 4 — Identificar escenas estratégicas del guion

Leer el guion completo e identificar los N momentos más cinematográficos/impactantes.

**Criterios de selección (priorizar en este orden):**

1. **Dicotomías y contrastes** ("hay dos tipos de personas", "antes vs después")
2. **Revelaciones numéricas** ("analicé 1,000 videos", "en 8 semanas", "más de 500 alumnas")
3. **Momentos de autoridad/credibilidad** (logros, prueba social, historia de origen)
4. **CTAs y puntos de decisión** ("si quieres saber más", "haz clic ahora", "la puerta se cierra")
5. **Presentación de la solución** (nombre del producto/método, beneficios clave)
6. **Agitación de dolor** (el problema que tiene el espectador)
7. **Transformaciones y resultados** (casos de éxito, promesas concretas)
8. **Conceptos clave del método** (pasos, sistemas, frameworks)

**Para cada escena extraer:**
- `numero`: 1-N
- `bloque_vsl`: nombre del bloque narrativo (Gancho / Problema / Credibilidad / Solución / Oferta / CTA)
- `frase_trigger`: la frase EXACTA del guion donde se inserta el clip (copiar verbatim, 8-15 palabras)
- `concepto_visual`: qué debe mostrarse visualmente (1 línea descriptiva)
- `tipo`: `avatar` (con presentadora) o `cinematico` (abstracto)
- `genero_seedance`: `action` / `epic` / `drama` / `noir` / `comedy` / `horror`
- `prompt_completo`: el prompt en inglés para Higgsfield (ver sección de prompts)

**Regla para asignar `tipo`:**
- Si la escena es sobre: la presentadora, sus logros, su método, su historia, CTAs, promesas personales, "yo hice X" → `avatar`
- Si la escena es sobre: conceptos abstractos (sistemas, IA, redes, tiempo, datos, antes/después sin persona) → `cinematico`
- Aplicar la regla 80/20 al final: si hay demasiados `avatar`, convertir los conceptos más abstractos a `cinematico`

### Paso 5 — Redactar prompts de Higgsfield

**Estructura base por estética:**

#### Cyberpunk (default)
```
[DESCRIPCIÓN DE LA ACCIÓN EN 1 LÍNEA],
electric blue neon lighting with dark backgrounds, cyberpunk futuristic aesthetic,
holographic particles and glowing elements, deep blacks contrasted with vivid electric blue (#00BFFF),
cinematic depth of field, dramatic atmospheric lighting, 
ultra-HD 16:9 cinematic composition, 5-second continuous motion.
```

#### Corporativo
```
[DESCRIPCIÓN DE LA ACCIÓN EN 1 LÍNEA],
clean corporate aesthetic, navy blue and silver tones, professional studio lighting,
crisp white surfaces, minimal environment, premium executive feeling,
cinematic depth of field, 16:9 composition, 5-second motion.
```

#### Cálido / Lifestyle
```
[DESCRIPCIÓN DE LA ACCIÓN EN 1 LÍNEA],
warm amber and golden hour tones, soft natural light, lifestyle aesthetic,
earth tones and organic textures, intimate human-scale framing,
cinematic depth of field, 16:9 composition, 5-second motion.
```

#### Espiritual
```
[DESCRIPCIÓN DE LA ACCIÓN EN 1 LÍNEA],
golden and violet ethereal tones, mystical atmosphere, sacred geometry elements,
soft glowing particles, transcendent mood, dramatic backlighting,
cinematic depth of field, 16:9 composition, 5-second motion.
```

**Para clips CON AVATAR (tipo: avatar):**

La descripción de la persona debe ser: `a Latin woman with long straight dark hair and light-tan skin`
Agregar **SIEMPRE** al final del prompt: `, character inspired by the reference image provided, maintain facial features from reference`
Pasar `medias: [{value: "<media_id>", role: "image"}]` en la llamada.

Ejemplo prompt avatar (cyberpunk):
```
A Latin woman with long straight dark hair and light-tan skin stands confidently at the center of a holographic command center, her hands touching floating electric-blue data panels that expand outward, glowing graphs and metrics orbiting around her in a futuristic dark space,
electric blue neon lighting with dark backgrounds, cyberpunk futuristic aesthetic,
holographic particles and glowing elements, deep blacks contrasted with vivid electric blue,
cinematic depth of field, dramatic atmospheric lighting,
ultra-HD 16:9 cinematic composition, 5-second continuous motion,
character inspired by the reference image provided, maintain facial features from reference.
```

**Para clips SIN AVATAR (tipo: cinematico):**

Sin mención de persona. Solo el objeto/concepto/ambiente:

Ejemplo (cyberpunk):
```
An intricate glowing holographic clock made of pure light slowly dissolves into electric-blue sand particles that drift upward and disappear, each grain of sand leaving a neon trace, the background pure black,
electric blue neon lighting with dark backgrounds, cyberpunk futuristic aesthetic,
deep blacks contrasted with vivid electric blue (#00BFFF),
cinematic depth of field, dramatic atmospheric lighting,
ultra-HD 16:9 cinematic composition, 5-second continuous motion.
```

### Reglas ANTI-NSFW (aprendidas en producción)

Evitar estos elementos que disparan el filtro de contenido de Higgsfield:
- ❌ Género `noir` + `macro closeup` + oscuridad → usar `drama` en su lugar
- ❌ "emerges from complete darkness" → sustituir por "appears in a dimly lit environment"
- ❌ "extreme closeup" de objetos cotidianos con género `drama` → usar plano medio o general
- ❌ Cualquier mención de violencia, sangre, armas, piel expuesta
- ✅ Géneros seguros: `action`, `epic`, `drama` (con cuidado), `comedy`
- ✅ Si un prompt es rechazado por NSFW: simplificar descripción, eliminar palabras relacionadas con oscuridad/intimidad, ampliar a toma general

### Paso 6 — Confirmar el plan antes de generar

Mostrar a la usuaria la tabla completa de escenas antes de ejecutar:

```
| # | Bloque | Frase trigger | Concepto visual | Tipo | Género |
|---|--------|--------------|-----------------|------|--------|
| 1 | Gancho | "Hay dos tipos..." | la creadora se divide en dos | avatar | action |
...
```

Preguntar: "¿Modificas algo antes de lanzar los [N] clips?"

Si dice "sí" → editar los prompts específicos.
Si dice "no" / "listo" / "lanza" → continuar.

### Paso 7 — Generar clips en lotes de 8 (máximo concurrent)

**Regla de concurrencia:** Higgsfield permite máximo 8 jobs simultáneos en el plan Creator. Nunca lanzar más de 8 a la vez.

**Para cada clip con avatar:**
```python
mcp__higgsfield__generate_video(
    model="seedance_2_0",
    prompt="<prompt_completo>",
    aspect_ratio="16:9",
    duration=5,
    resolution="1080p",
    genre="<genre>",
    medias=[{"value": "<media_id>", "role": "image"}]
)
```

**Para cada clip cinemático abstracto:**

Decidir modelo:
- Seedance 2.0: si el concepto tiene movimiento claro y dinámico (partículas, transformaciones, explosiones de datos)
- Cinema Studio 3.0: si el concepto requiere composición cinematográfica compleja (profundidad, planos elaborados, luz dramática de película)

```python
# Seedance abstracto:
mcp__higgsfield__generate_video(
    model="seedance_2_0",
    prompt="<prompt_completo>",
    aspect_ratio="16:9",
    duration=5,
    resolution="1080p",
    genre="<genre>"
    # NO incluir medias
)

# Cinema Studio:
mcp__higgsfield__generate_video(
    model="cinematic_studio_3_0",
    prompt="<prompt_completo>",
    aspect_ratio="16:9",
    duration=5
    # Cinema Studio no acepta genre ni resolution — omitir esos params
)
```

**Flujo de lotes:**

```
Lote 1: lanzar escenas 1-8 → guardar job_ids[]
  → Poll en loop con sync:true (25s por llamada):
      mcp__higgsfield__job_status(job_id: "<id>", sync: true)
  → Cuando un job termina (status: "completed"), anotar su output_url
  → Si falla (status: "failed"): revisar si fue NSFW o error de API
      - NSFW: reformular el prompt (simplificar + eliminar darkness) y regenerar
      - Error API: esperar 30s y reintentar una vez
  → Cuando todos los del lote terminan, pasar al siguiente lote

Lote 2: lanzar escenas 9-16 → igual
Lote 3: lanzar escenas 17-N → igual
```

**Si Higgsfield sugiere un preset (IN THE DARK, GOLDEN HOUR, etc.):**
Siempre declinar con `declined_preset_id` para que genere con el prompt exacto:
```python
mcp__higgsfield__generate_video(
    ...,
    declined_preset_id="<preset_id_sugerido>"
)
```

### Paso 8 — Entregar el catálogo final

Una vez todos los clips estén completados, presentar el catálogo con este formato:

```markdown
# CATÁLOGO B-ROLL VSL — [NOMBRE DEL PROYECTO]
Estética: [ESTÉTICA] · 16:9 · 5s · Seedance 2.0 + Cinema Studio 3.0
Con avatar (foto referencia): [N] clips · Cinemático abstracto: [M] clips

---

## BLOQUE: [NOMBRE DEL BLOQUE]

**E[N] · [NOMBRE DESCRIPTIVO]** [· CON TU FOTO si aplica]
> Inserta cuando dices: **`"[FRASE TRIGGER EXACTA DEL GUION]"`**
> [▶ VER VIDEO](<URL>)

---
```

Agrupar por bloque narrativo (Gancho → Problema → Credibilidad → Solución → Oferta → CTA).

Al final del catálogo, incluir:

```markdown
---
## RESUMEN TÉCNICO
- Total clips generados: N
- Con avatar (80%): X
- Cinemático abstracto (20%): Y
- Modelo: Seedance 2.0 / Cinema Studio 3.0
- Media ID foto referencia: <media_id> (reutilizar en futuras sesiones)
- Estética: [ESTÉTICA]
```

---

## Manejo de errores comunes

| Error | Causa | Solución |
|-------|-------|---------|
| `NSFW content detected` | Prompt disparó filtro | Simplificar prompt, reemplazar palabras de oscuridad/intimidad, usar `drama` en vez de `noir` |
| `Something went wrong` en media_upload | API temporalmente caída | Esperar 30s y reintentar |
| Job en `failed` sin razón clara | Timeout interno de Higgsfield | Reintentar el mismo prompt una vez |
| Higgsfield sugiere preset | Preset cambiaría la estética | Siempre declinar con `declined_preset_id` |
| Video sale en 720p (Cinema Studio) | Cinema Studio 3.0 no acepta `resolution` | Normal — Cinema Studio ignora ese param; el resultado es cinemático de todas formas |
| `concurrent job limit` | Demasiados jobs a la vez | Nunca lanzar más de 8. Esperar que terminen antes del siguiente lote |

---

## Notas para reutilización

- El `media_id` de la foto de referencia es **permanente** en la cuenta de Higgsfield. Si la usuaria tiene un media_id previo guardado en memoria, no hace falta re-subirla.
- Paral usuario: media_id conocido de sesiones anteriores → verificar con `mcp__higgsfield__show_medias` antes de re-subir.
- Los clips generados duran ~30 días en los servidores de Higgsfield. Para uso a largo plazo, descargar con: `curl -L "<url>" -o "escena_01.mp4"`
- Si se necesita descargar todos los clips en lote: `for url in <url1> <url2>...; do curl -L "$url" -o "$(echo $url | grep -o 'hf_[^.]*').mp4"; done`
