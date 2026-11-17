# Voz y frases tipo F100K · Reporte de benchmark

El reporte debe sonar con la voz de la marca: **directa, cuantitativa, sin tecnicismos enterprise, español neutro**. Esta es la guía de estilo.

---

## ✅ FRASES PERMITIDAS — F100K voice

### Para abrir hallazgos

- "El mercado está saturado en [rango]. Hay vacío entre [X] y [Y]."
- "8 de 10 competidores hacen [X]. Eso es la regla, no la excepción."
- "Nadie en este nicho está haciendo [X]. Eso es un gap, no un descuido."
- "La promesa más repetida es '[X]'. Eso significa que ya no es diferenciación."
- "El precio anchor del mercado es $X. Subir o bajar mucho de ahí necesita justificación."

### Para presentar oportunidades

- "El movimiento más obvio: [X]."
- "Si haces [X], en [Y semanas] estás compitiendo con [tier superior]."
- "Esto es low-hanging fruit: bajo esfuerzo, alto impacto, evidencia clara."
- "Aquí hay $X/cliente sobre la mesa que la competencia está dejando."

### Para cerrar dimensiones

- "Score [X/5] — [una frase explicando por qué, con dato concreto]"
- "Fortaleza clara: [X]. Debilidad explotable: [Y]."
- "Lo que se debe replicar: [X]. Lo que se debe evitar: [Y]."

### Para recomendaciones tácticas

- "En 30 días: [acción]."
- "Esta semana: [acción]."
- "Antes de tocar el precio, primero [X]."
- "No copies [X] de [Marca]. Funciona para ellos por [razón específica que el cliente no tiene]."

---

## ❌ FRASES PROHIBIDAS — sonido enterprise

NO usar:

- "Aprovechar sinergias del mercado"
- "Maximizar el customer journey"
- "Estrategia de go-to-market"
- "Stakeholders"
- "Roadmap omnichannel"
- "Best-in-class"
- "Disruptivo"
- "Leverage"
- "Scalable"
- "Pain points" (decir "frustraciones" o "dolores")
- "Drive engagement" (decir "subir engagement" o ser específico)
- "Empower" (decir "darle herramientas a")
- "Insights" (decir "hallazgos" o "datos")

---

## 🚫 VOSEO ARGENTINO — PROHIBIDO

Memoria explícita: El usuario escribe en **español neutro**, no argentino.

PROHIBIDO (voseo): vos, sos, tenés, sabés, podés, querés, debés, copiá, pegá, elegí, llená, montá, mirá, hacé, andá, escogé, seleccioná, etc.

USAR: tú, eres, tienes, sabes, puedes, quieres, debes, copia, pega, elige, llena, monta, mira, haz, anda, escoge, selecciona.

Antes de guardar el reporte, hacer grep:
```
grep -nE "\bvos\b|\bsos\b|tenés|sabés|podés|debés|querés|aplicás|copiá|pegá|elegí|llená|montá" reporte.md   # busca voseo
```

Si encuentra algo, corregir antes de entregar.

---

## 📊 ESTILO CUANTITATIVO

**Siempre que se pueda, número o porcentaje.** Frases vagas → frases con dato.

| ❌ Vago | ✅ Cuantitativo |
|--------|----------------|
| "Muchos competidores usan Skool" | "7 de 10 competidores usan Skool" |
| "Los precios suelen ser bajos" | "El 60% se mueve entre $9-49/mes" |
| "Tienen buenos testimonios" | "Muestran 23 testimonios visibles con caso específico" |
| "La competencia está fuerte" | "5 competidores tienen score 40+, el cliente parte de 28" |

---

## 🎯 LONGITUD POR SECCIÓN

| Sección | Longitud objetivo |
|---------|-------------------|
| Resumen ejecutivo | 1 página (~400 palabras) |
| Ficha de competidor | 1 página (~600 palabras) |
| Tendencia | 5-8 líneas cada una |
| Oportunidad | 8-12 líneas cada una |
| Plan 30/60/90 | 1 página total |
| Apéndice | Tan largo como haga falta |

**Total del reporte completo:** 15-30 páginas dependiendo de profundidad.

---

## 🔥 EJEMPLOS DE PÁRRAFOS BIEN ESCRITOS

### Ejemplo 1 — Hallazgo cuantitativo

> "En este nicho, 8 de 10 competidores cobran entre $47-99/mes en plataforma Skool. Solo 2 se atreven al rango $200+ y ambos justifican el precio con coaching 1:1 incluido. **El rango $100-199 está completamente vacío.** Cualquiera que se posicione ahí con un buen vehículo único puede capturar al segmento que considera $97 muy barato (suena a 'curso básico') y $297 muy caro (suena a 'no me lo puedo permitir todavía')."

### Ejemplo 2 — Oportunidad accionable

> "**Oportunidad #3: Garantía de implementación (no de devolución).**
>
> Situación: 9 de 10 competidores ofrecen 'garantía de 7 o 14 días, devolvemos tu dinero'. Es genérico y no reduce la fricción real (la duda no es '¿y si no me gusta?' sino '¿y si no logro implementarlo?').
>
> Gap: Nadie ofrece 'garantía de implementación' — un compromiso de que si en 60 días aplicaste el método y no viste X resultado, te quedas otros 60 días gratis con acompañamiento 1:1.
>
> Movimiento: Reescribir la garantía actual a 'Garantía de Implementación 60+60' en la VSL y landing.
>
> Esfuerzo: bajo (solo copy + entender que vas a tener 1-2 alumnas alargadas)
> Impacto: alto (reduce la objeción #1 documentada en reviews de competidores)
> Tiempo: 1 semana"

---

## 🎨 EMOJIS — USO SOBRIO

Solo en headers de sección, no en el cuerpo del texto. Permitidos:

- 📊 datos / análisis
- 🎯 oportunidades / objetivo
- 🗺️ mapa / posicionamiento
- 📂 fichas
- 📈 tendencias
- 💎 oportunidades estratégicas
- 📅 planning
- 📎 apéndice
- ⚠ advertencias
- ✅ confirmaciones

NO usar emojis decorativos sin función (🚀, 🌟, 🎉, 💪, 🔥 en headers de marketing).
