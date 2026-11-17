# Análisis de Comentarios — Metodología FORMULA 100K

## POR QUÉ LOS COMENTARIOS SON DATOS DE INVESTIGACIÓN DE MERCADO

Los comentarios de un video viral son la forma más honesta de focus group gratuito.
La gente escribe lo que piensa EN EL MOMENTO en que el contenido les tocó un punto de dolor.
Eso es oro de investigación que los competidores ya recolectaron por ti.

**Regla de oro:** Un comentario que se repite 5+ veces = un video validado antes de crearlo.

---

## CÓMO EXTRAER COMENTARIOS CON SUPADATA MCP

### Para videos de TikTok:
```
supadata_scrape(url="https://www.tiktok.com/@usuario/video/VIDEO_ID")
```

### Para videos de Instagram (Reels):
```
supadata_scrape(url="https://www.instagram.com/reel/SHORTCODE/")
```

**Proceso:**
1. Identificar los top 5 videos con mayor número de comentarios del perfil analizado
2. Si se analizan competidores, tomar los top 3-5 videos más virales de cada uno
3. Correr `supadata_scrape` en cada URL para extraer los comentarios
4. Clasificar cada comentario en las 5 categorías del sistema

---

## SISTEMA DE CLASIFICACIÓN DE COMENTARIOS

### CATEGORÍA 1: Preguntas sin responder (🔍)
**Qué son:** Preguntas directas que el video no respondió o respondió de forma incompleta.
**Cómo identificarlas:** Empiezan con "¿cómo...?", "¿cuándo...?", "¿dónde...?", "¿cuánto...?", "¿qué pasa si...?"
**Qué hacer con ellas:** Cada pregunta = un posible video completo dedicado solo a responder eso.

**Ejemplo:**
- Comentario: "¿pero cómo hago eso si no tengo seguidores todavía?"
- → Video idea: "Cómo aplicar esta estrategia cuando partes de cero seguidores"

---

### CATEGORÍA 2: Frustraciones explícitas (😤)
**Qué son:** Expresiones de frustración, cansancio o desesperación con el problema que trata el video.
**Cómo identificarlas:** "nadie me explica", "siempre me dicen X pero no cómo", "llevo meses intentando y nada"
**Qué hacer con ellas:** Son los dolores de mercado más calientes. Un video que empiece con "si llevas meses intentando X sin resultado..." tiene gancho garantizado.

**Ejemplo:**
- Comentario: "Esto ya lo intenté mil veces y no me funciona, nadie dice por qué"
- → Video idea: "Por qué [estrategia] no te está funcionando (y qué cambia todo)"

---

### CATEGORÍA 3: Deseos declarados (💡)
**Qué son:** Peticiones explícitas de más contenido, solicitudes directas al creador.
**Cómo identificarlas:** "¿harías un video de...?", "me encantaría ver...", "explícame más sobre..."
**Qué hacer con ellas:** Demanda confirmada. Prioridad alta. Crear ese video es casi garantía de engagement.

**Ejemplo:**
- Comentario: "¿puedes hacer uno explicando esto para negocios físicos?"
- → Video idea: "[tema del video original] aplicado a negocios físicos o locales"

---

### CATEGORÍA 4: Objeciones y miedos (⚠️)
**Qué son:** Resistencias, dudas, razones por las que el espectador cree que no le va a funcionar.
**Cómo identificarlas:** "sí pero...", "eso no funciona si...", "qué pasa con quienes...", "¿y si...?"
**Qué hacer con ellas:** Cada objeción es un video de refutación. También son los argumentos exactos a usar en contenido de venta para desarmar resistencias.

**Ejemplo:**
- Comentario: "sí pero eso solo funciona si ya tienes plata para invertir"
- → Video idea: "Cómo hacer X sin inversión inicial (para quienes empiezan desde cero)"
- → También usar en ventas: incluir este argumento y refutarlo en el guion del próximo reel de venta

---

### CATEGORÍA 5: Validaciones sociales (✅)
**Qué son:** Testimonios espontáneos, confirmaciones de que el contenido funcionó o es real.
**Cómo identificarlas:** "yo lo hice y...", "a mí me pasó exactamente eso", "esto es tan verdad que..."
**Qué hacer con ellas:** Son prueba social gratuita. Usar como ángulo de testimonial. Si muchas personas confirman la misma experiencia, ese es el gancho para el próximo video ("¿sabías que X personas dijeron que...?")

---

## ANÁLISIS DE VACÍOS EN COMPETIDORES

### Qué es un vacío de contenido
Un vacío = un tema que el mercado está preguntando activamente pero que nadie en el nicho está respondiendo de forma satisfactoria.

### Cómo detectarlo
1. Scrapear los top 3-5 videos virales de 2-3 competidores en el mismo nicho
2. Recolectar todas las preguntas (Categoría 1) y frustraciones (Categoría 2) de esos comentarios
3. Buscar patrones: ¿qué preguntas se repiten en múltiples videos de múltiples competidores?
4. Verificar si alguno de esos competidores ya tiene un video respondiendo esa pregunta
5. Si la pregunta se repite pero no hay video dedicado a responderla = **vacío confirmado**

### Priorización de vacíos
Ordenar por:
- **Frecuencia:** cuántas veces aparece esa pregunta o frustración
- **Urgencia:** qué tan emocional o urgente es el lenguaje del comentario
- **Fit con el creador analizado:** qué tan bien encaja con el ángulo y autoridad de quien analizamos

### Formato de entrega del análisis de vacíos

```
VACÍO DETECTADO #1
Pregunta recurrente: "[cita textual representativa]"
Aparece en: X videos de Y competidores
Competidores que lo ignoran: @comp1, @comp2
¿Alguien lo respondió?: [Sí/No — si sí, quién y qué tan bien]
Oportunidad: [descripción del video a crear]
Título sugerido: "[título específico]"
Ángulo ganador: [por qué el creador analizado puede responder esto mejor]
```

---

## PATRONES DE LECTURA AVANZADA

### Comentarios con múltiples respuestas o "hilos"
Si un comentario generó respuestas de otros usuarios = tocó un nervio colectivo.
Prioridad máxima: ese es el ángulo más candente del video.

### Comentarios del propio creador con muchos likes
Si el creador respondió un comentario y esa respuesta tiene muchos likes = la respuesta tiene más valor que el video. Crear un video completo desarrollando esa respuesta.

### Emojis como señal
- Comentarios con 🔥 o ❤️ en respuesta a una idea = validación fuerte
- Comentarios con 😭 o 😤 = dolor intenso → máxima prioridad para contenido de empatía
- Comentarios con 🤔 = confusión o curiosidad → video de clarificación

### Palabras clave de intención de compra en comentarios
Buscar activamente: "precio", "costo", "cómo contratar", "dónde comprar", "cuánto cuesta", "cómo empezar contigo", "link", "programa", "curso".
Estos comentarios = personas listas para comprar. El video que los generó = ángulo de venta directo.

---

## ERRORES A EVITAR

1. **No analizar solo los comentarios positivos** — los críticos y las preguntas difíciles son los más valiosos
2. **No ignorar comentarios con pocos likes** — pueden representar una minoría muy calificada
3. **No tomar una muestra demasiado pequeña** — analizar mínimo 30-50 comentarios por video para ver patrones reales
4. **No confundir spam con señal** — filtrar comentarios de bots ("great content!", "follow me") antes del análisis
5. **No olvidar el contexto del video** — la misma pregunta puede significar cosas distintas según el tema del video donde apareció
