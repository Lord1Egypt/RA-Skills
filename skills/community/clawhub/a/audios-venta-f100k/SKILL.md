---
name: audios-venta-f100k
description: "Escribe guiones de AUDIOS DE VENTA (notas de voz comerciales, audios de cierre en DM, voicenotes de objeción, audios de seguimiento, audios de aplicación a high ticket) para grabar en WhatsApp / Instagram DM / Telegram. Convierte una oferta ya construida en una secuencia hablada de máximo 50 segundos que cierra la venta en privado. Activar SIEMPRE que se pida 'haz un audio de venta', 'guion para nota de voz', 'audio para cerrar en DM', 'voicenote para vender', 'audio de cierre', 'audio de seguimiento', 'audio para esa prospecta', 'audio para responder objeción', 'audio de aplicación', 'audio para que compre', 'guion de audio de IG', 'audio de bienvenida a high ticket', o cualquier variación que combine vender + formato hablado privado 1-on-1. NO usar para guiones de video público (guionizacion-formula100k), VSL ni landing (vsl-expert-f100k), ni construir la oferta (constructor-ofertas-f100k)."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Skill de texto: corre tal cual. La oferta, el precio y el dolor de la prospecta salen de `cerebro/`; lo que falte, pregúntalo por Telegram.
> - Los guiones de audio se guardan en `entregables/audios-venta/` (o `entregables/clientes/<nombre>/audios-venta/`) y se entregan por Telegram listos para grabar.
> - Nunca mandes el audio ni el mensaje a la prospecta: la usuaria lo graba y lo envía ella.

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

## Qué hace esta skill

Convierte una oferta + un contexto de conversación 1-on-1 en un guion de audio breve, cálido y persuasivo, listo para grabarse en WhatsApp / Instagram DM. Cubre 6 tipos de audio:

> ⛔ **TOPE DURO: ningún audio puede pasar de 50 segundos.** Todos los rangos de abajo respetan ese máximo. Si un guion no entra en 50 s al leerlo en voz alta, hay que recortarlo — nunca entregarlo largo.

| # | Tipo | Duración | Cuándo usarlo |
|---|---|---|---|
| 1 | **Audio de apertura caliente** | 30-40 s | Cuando una prospecta acaba de entrar al DM por un lead magnet o anuncio |
| 2 | **Audio de cierre** | 45-50 s | Cuando ya hubo conversación, conoce la oferta y falta el empujón final |
| 3 | **Audio de objeción** | 40-50 s | Para responder UNA objeción específica (precio, tiempo, "ya probé") |
| 4 | **Audio de seguimiento** | 30-45 s | Para retomar conversaciones paradas hace 2-7 días sin presión |
| 5 | **Audio de aplicación / agendar llamada** | 45-50 s | Para mover prospecta a aplicación de high ticket o llamada de calificación |
| 6 | **Audio de bienvenida post-compra** | 40-50 s | Justo después de la compra, para retención inmediata y onboarding emocional |

Trabaja en español neutro (NO argentino — [[feedback_espanol_neutro]]). Tono cálido pero seguro. Conversacional. Como si el usuario estuviera grabando en el sofá, no en un estudio.

**Pre-requisito:** una oferta clara. Si no existe, derivar primero a [[constructor-ofertas-f100k]].

---

## Diferencias clave entre AUDIO de venta y VSL/landing

| | Audio (1-on-1) | VSL / landing (1-to-many) |
|---|---|---|
| Audiencia | Una persona específica con nombre | Tráfico genérico |
| Tono | Conversacional, segunda persona, nombre propio | Profesional, narrativo |
| Estructura | 4-6 micro bloques | 8-18 bloques completos |
| Hook | Saludo + nombre + razón específica | Etiqueta + promesa pública |
| Prueba social | 1 cliente muy parecido a ELLA | Múltiples casos diversos |
| CTA | Pregunta abierta o acción concreta inmediata | Botón + urgencia |
| Duración | 30-50 segundos (tope 50 s) | 5-15 minutos |

**Regla:** un audio de venta NUNCA es un VSL recortado. Tiene su propia gramática.

---

## Anatomía de un audio de venta ganador (4 capas)

Toda nota de voz comercial tiene siempre estas 4 capas, en este orden. El presupuesto de tiempo está calculado para que las 4 sumen ≤ 50 s:

### Capa 1 — APERTURA PERSONAL (3-5 segundos)
- Saludar por nombre propio
- Mencionar UN detalle específico del contexto (algo que dijo en el chat, su perfil, su nicho)
- Tono cálido, sonrisa audible

### Capa 2 — PUENTE EMOCIONAL (8-13 segundos)
- Espejar lo que está sintiendo / problema actual
- Validar (sin condescendencia)
- Una micro-historia o un caso de cliente con MUY parecido contexto

### Capa 3 — OFERTA / CIERRE (12-24 segundos)
- Lo que tienes para ella en concreto
- Solo UN bono / UN punto de la oferta (no apilar 5)
- Mencionar precio SOLO si ya hubo conversación previa o el audio es de cierre

### Capa 4 — CTA EN PREGUNTA (4-8 segundos)
- NUNCA "compra ahora" en frío
- Siempre pregunta abierta o acción mínima ("¿te parece si te paso el link?", "¿lo vemos en 15 min de llamada?")
- Esperar respuesta antes del próximo audio

---

## Brief obligatorio (preguntas una por una)

NO escribir ningún audio sin estos datos. Hacer las preguntas UNA por UNA.

1. ¿Qué tipo de audio necesitas? (apertura · cierre · objeción · seguimiento · aplicación · bienvenida)
2. ¿Cuál es el nombre y contexto específico de la prospecta? (cómo llegó, qué dijo en el chat, su negocio/nicho)
3. ¿Qué oferta específica estás vendiéndole? (precio, qué incluye)
4. Si es objeción, ¿cuál es exactamente?
5. ¿Tienes algún caso de cliente con contexto parecido al de ella que puedas mencionar?
6. ¿Cuál es el siguiente paso concreto que quieres que dé después del audio? (responder, click en link, agendar llamada, pagar)
7. ¿Cuánta confianza ya hay con esta prospecta? (frío · ya conversaron · ya la conoces personalmente)

---

## Reglas de tono (las que diferencian un audio profesional de uno robot)

- **Llamarla por su nombre** mínimo 1 vez (sin abusar, máximo 2)
- **No leer**: hablar como si lo estuvieras pensando en el momento
- **Pausas estratégicas** marcadas con `…` para que respire
- **Una sola pregunta** al final — más confunde
- **Cero corporativismo**: no "estimada", no "le agradezco", no "es un placer"
- **Frases cortas** (audio se procesa más lento que texto)
- **Cero clichés** ("transforma tu vida", "el momento es ahora", "no esperes más")
- **Mencionar dinero específico** si ya hay confianza ("son $560 al año, no $560 al mes" — anclar el alivio)
- **No prometer lo que no puedes cumplir** — ni en privado
- **Cerrar con sonrisa audible**

---

## Plantillas

Las 6 plantillas completas de audio (con guion palabra por palabra y notas de entrega) están en [templates.md](templates.md).

Cada plantilla incluye:
- Duración objetivo
- Capa por capa con el copy literal
- Indicaciones de entonación / pausa / sonrisa
- Variaciones según el nivel de calor de la prospecta

---

## Reglas absolutas

- **TOPE DURO de 50 segundos** — ningún audio, de ningún tipo, puede pasar de 50 s. Si al leerlo en voz alta no entra, recortar la Capa 3 (un solo punto de oferta) hasta que entre. Como referencia: 50 s ≈ 120-130 palabras habladas con pausas.
- **Brief completo siempre** — sin contexto específico, el audio suena genérico
- **Una sola pregunta al final**
- **Nunca apilar 5 bonos en un audio** — eso es para VSL
- **Nombre propio mínimo 1 vez, máximo 2**
- **Cero clichés ni corporativismo**
- **Español neutro siempre** — ver [[feedback_espanol_neutro]]
- **Si la conversación está muerta hace +14 días**, no usar "audio de seguimiento" — proponer reabrir con texto primero, audio después
- **Si la prospecta es high ticket ($2K+)**, el CTA SIEMPRE es agendar llamada — nunca pagar por DM
- **Nunca grabar el audio**, solo entregar el GUION (el usuario / el usuario lo graba)

---

## Output

Guardar siempre en `entregables/audios-venta/YYYY-MM-DD_<tipo>_<nombre-prospecta>.md`. Si es para un cliente, en `entregables/clientes/<nombre>/audios-venta/`.

Formato del archivo:
- Tipo de audio
- Prospecta (nombre + contexto)
- Duración objetivo
- Guion palabra por palabra con marcas de entonación
- 1-2 variaciones por si la primera no cuaja
- Notas de entrega (pausas, sonrisa, ritmo)

Si después del audio la prospecta avanza, ofrecer continuar la conversación en DM, o pasar a [[creadora-comunidades-skool]] si el destino es onboarding a Skool.
