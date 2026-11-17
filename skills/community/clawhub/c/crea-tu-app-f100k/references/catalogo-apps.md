# Catálogo de Apps IA — FÓRMULA 100K (menú de recomendación)

Las **36 apps** del artifact `f100k-catalogo-apps-ia.html`. Úsalo en **Fase 0** para recomendar 1–3 apps según el nicho/oferta/audiencia de la alumna. Cada ficha trae: **para quién encaja**, **qué construye**, **dificultad** y **qué llaves necesita** (lo que pedirás en Fase 4).

**Llaves típicas por tipo de app:**
- Apps de **texto/chat** → llave de IA (Anthropic Claude o Gemini) + Supabase + Stripe + Vercel.
- Apps de **visión/foto** (analizar imagen) → Gemini (visión) + Supabase + Stripe + Vercel.
- Apps que **generan imágenes** (retratos, logos, interiores, miniaturas) → API de imagen (Replicate o Fal) + Supabase + Stripe + Vercel. *(Las más caras por trabajo — avísale.)*
- Apps de **audio/video** (clips, subtítulos, podcast, reuniones) → Whisper (transcripción) + IA + Supabase + Stripe + Vercel.
- Apps tipo **"chatea con tu documento/web"** (RAG) → IA + Supabase con pgvector + Stripe + Vercel.

> Regla de recomendación: prioriza apps **Fáciles** para su primera vez, y que sirvan de **imán de leads** hacia SU comunidad/oferta. Una app que su audiencia usa = personas que terminan en su mundo.

---

## 🍎 Salud & Fitness
- **#1 Calorías por foto** — *Coaches fitness/nutrición.* Foto del plato → calorías y macros + diario. Dif: Media. Llaves: Gemini (visión), Supabase, Stripe.
- **#2 Escáner de etiquetas saludable** — *Nutrición, vida sana, mamás.* Foto de etiqueta → puntaje de salud 0-100 + alternativa. Muy compartible. Dif: Media. Llaves: Gemini (visión/OCR), Supabase, Stripe.
- **#3 Recetas con lo que tienes** — *Cocina, nutrición, hogar.* Foto del refri → 3 recetas con lo que ya hay. Dif: **Fácil**. Llaves: Gemini, Supabase, Stripe.

## 🎬 Contenido & Creadores
- **#4 Video largo → clips virales** — *Podcasters, creadores de video.* Sube video/YouTube → clips 9:16 con subtítulos. Dif: Avanzada. Llaves: Whisper, IA, Supabase, Stripe.
- **#5 Subtítulos animados para reels** — *Creadoras de reels.* Reel → subtítulos animados estilo TikTok. Dif: Media. Llaves: Whisper, Supabase, Stripe.
- **#6 Podcast → 10 piezas de contenido** — *Podcasters, repurposing.* Episodio → show notes, hilos, posts, newsletter. Dif: Media. Llaves: Whisper, Claude, Supabase, Stripe.
- **#7 Generador de posts LinkedIn/X** — *Marca personal, B2B.* Idea cruda → 3 variantes en tu voz + programar. Dif: **Fácil**. Llaves: Claude, Supabase, Stripe.
- **#8 Multiplicador 1 idea → 10 formatos** — *Cualquier creador/agencia.* Pieza madre → reel, carrusel, email, hilo. Dif: **Fácil**. Llaves: Claude, Supabase, Stripe.
- **#36 Miniaturas de YouTube con IA** — *Youtubers, creadoras.* Tema del video → miniaturas 16:9 que invitan al clic. Dif: Media. Llaves: API de imagen (Flux/SD), Supabase, Stripe.

## 🎨 Imagen & Diseño
- **#9 Headshots profesionales IA** — *Profesionales, LinkedIn.* 10 selfies → 100 retratos pro. Pago único. Dif: Avanzada. Llaves: Replicate/Fal, Supabase, Stripe. *(Costo por trabajo: avísale.)*
- **#10 Quitar/cambiar fondo de producto** — *E-commerce, tiendas.* Foto producto → fondo de estudio. Dif: Media. Llaves: API remove-bg + imagen, Supabase, Stripe.
- **#11 Rediseño de interiores por foto** — *Inmobiliaria, deco, hogar.* Foto de cuarto → rediseñado en estilo X. Dif: Media. Llaves: API imagen img2img, Supabase, Stripe.
- **#12 Generador de logos + branding** — *Negocios nuevos, emprendedoras.* Preguntas → logos + kit de marca. Dif: Media. Llaves: API imagen, Supabase, Stripe.
- **#13 Avatares y retratos IA personalizados** — *Creadoras, marca personal.* Entrena tu cara → fotos tuyas en cualquier escena. Dif: Avanzada. Llaves: Replicate/Fal, Supabase, Stripe. *(Costo por trabajo.)*
- **#31 Rediseña tu cuarto por foto** — *Deco, inmobiliaria.* Foto de espacio → 3-4 rediseños por estilo. Antes/después compartible. Dif: Media. Llaves: API imagen, Supabase, Stripe.

## 💼 Negocios & Ventas
- **#14 Chatbot entrenado con tu web** — *Negocios con web, B2B.* URL/docs → chatbot de soporte embebible (RAG). Dif: Media. Llaves: IA + Supabase pgvector, Stripe.
- **#15 Constructor de landing con IA** — *Solopreneurs, agencias.* Describe negocio → landing publicable. Dif: Media. Llaves: Claude, Supabase, Stripe.
- **#16 Presentaciones desde un prompt** — *Consultoras, educadoras, ventas.* Tema → presentación con diseño. Dif: Avanzada. Llaves: Claude, Supabase, Stripe.
- **#17 Generador de propuestas y cotizaciones** — *Freelancers, agencias.* Describe proyecto → propuesta comercial en PDF. Dif: **Fácil**. Llaves: Claude, Supabase, Stripe.
- **#30 Descripciones de producto para tiendas** — *E-commerce, Shopify.* Foto producto → título SEO + descripción + bullets en lote. Dif: **Fácil**. Llaves: Visión + LLM, Supabase, Stripe.

## 📚 Educación & Estudio
- **#18 Apuntes → quizzes y flashcards** — *Educadoras, estudiantes, cursos.* PDF/apuntes → quiz + flashcards + resumen. Dif: **Fácil**. Llaves: Claude, Supabase, Stripe.
- **#19 Asistente de escritura académica** — *Universitarios, investigadores.* Editor con autocompletado + citas. Dif: Media. Llaves: Claude, Supabase, Stripe.
- **#20 Resumidor de papers, libros y YouTube** — *Estudiantes, profesionales.* PDF/YouTube → resumen + ideas clave. Dif: **Fácil**. Llaves: Whisper (video) + Claude, Supabase, Stripe.
- **#21 Tutor IA por materia** — *Educadoras, autodidactas.* Tema → mini-curso con lecciones y ejercicios. Dif: Media. Llaves: Claude, Supabase, Stripe.
- **#35 Resuelve tareas por foto** — *Estudiantes, tutoras.* Foto de ejercicio → solución paso a paso. Dif: Media. Llaves: Gemini (visión), Supabase, Stripe.

## ⚡ Productividad & Notas
- **#22 Voz a notas estructuradas** — *Cualquiera. Ideal primera app.* Hablas → nota limpia y ordenada. Dif: **Fácil**. Llaves: Whisper + Claude, Supabase, Stripe.
- **#23 Chat con tus PDFs y documentos** — *Abogadas, estudiantes, consultoras.* Sube PDF → pregúntale, responde citando página (RAG). Dif: Media. Llaves: IA + Supabase pgvector, Stripe.
- **#24 Minuta de reuniones + tareas** — *Equipos, agencias.* Grabación → minuta + tareas asignadas. Dif: Media. Llaves: Whisper + Claude, Supabase, Stripe.
- **#34 Notas de reuniones automáticas** — *Equipos, consultoras.* Audio reunión → transcripción + resumen + tareas. Dif: Avanzada. Llaves: Whisper + LLM, Supabase, Stripe.

## 📊 Datos & Finanzas
- **#25 Lenguaje natural → fórmulas Excel/SQL** — *Oficina, finanzas. Ideal primera app.* Describe el cálculo → fórmula lista. Dif: **Fácil**. Llaves: Claude, Supabase, Stripe. *(Demo viva: formulaia.vercel.app.)*
- **#26 Chat de análisis de datos (sube tu CSV)** — *Analistas, negocios.* Sube CSV → pregunta y la IA grafica. Dif: Avanzada. Llaves: LLM + sandbox de ejecución, Supabase, Stripe. *(Ejecuta código solo en sandbox aislado.)*

## 🌙 Vida & Carrera
- **#27 Coach de citas / mejora tus chats** — *Audiencia joven, lifestyle.* Captura de chat → 3 respuestas sugeridas. Dif: **Fácil**. Llaves: Visión + LLM, Supabase, Stripe.
- **#28 Optimizador de CV con IA** — *Coaches de carrera, RRHH.* CV + oferta → CV optimizado ATS + carta. Dif: **Fácil**. Llaves: Claude, Supabase, Stripe.
- **#29 Diario emocional con IA** — *Bienestar, coaching, mindfulness.* Escribes cómo te sientes → IA acompaña + patrones. Dif: **Fácil**. Llaves: Claude, Supabase, Stripe. *(Enfoque bienestar, no terapia clínica.)*
- **#32 Identifica plantas y dales cuidado** — *Lifestyle, hogar, jardinería.* Foto de planta → nombre + cuidados + riego. Dif: Media. Llaves: Gemini (visión), Supabase, Stripe.
- **#33 Asistente para responder mensajes** — *Ventas, networking, citas.* Captura de chat → 3 respuestas con tono. Dif: **Fácil**. Llaves: Visión + LLM, Supabase, Stripe.

---

## Cómo recomendar (Fase 0)

1. Cruza nicho + oferta + audiencia con la columna "para quién encaja".
2. Ofrece **1–3** opciones, y para cada una di **por qué para SU caso** y cómo le sirve de imán de leads.
3. Si es su **primera** app, sesga a las marcadas **Fácil**.
4. Si su idea no está en el catálogo, trátala igual: define qué construye, su dificultad aproximada y qué llaves necesitará.
