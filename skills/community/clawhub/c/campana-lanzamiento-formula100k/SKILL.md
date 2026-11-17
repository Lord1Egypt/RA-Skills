---
name: campana-lanzamiento-formula100k
description: "Planificación y ejecución de campañas de lanzamiento completas para comunidades Skool, cursos, productos digitales o servicios con la metodología F100K. Usar cuando una creadora va a lanzar algo nuevo o relanzar algo existente y necesita: posicionamiento, guiones de reels, secuencia de historias, emails, landing copy y calendario. Orquesta los demás skills F100K para producir todo el arsenal de lanzamiento desde un solo brief."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Skill de texto: corre tal cual. Fechas, oferta y precios salen de `cerebro/`; si faltan, pregúntalos por Telegram antes de armar la campaña.
> - Si la usuaria quiere que la campaña quede agendada, crea automatizaciones (recordatorios de lives, cuenta regresiva) solo después de su ✅ y dile la lista con fechas y horas.
> - Correos y mensajes de la campaña se entregan como borradores por Telegram: nada se envía solo.

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

# Campaña de Lanzamiento — Fórmula 100K

Planifica y ejecuta lanzamientos que convierten — no solo lanzamientos que salen.

## Cuándo activar

- Lanzamiento de una comunidad Skool nueva o relanzamiento de una existente
- Lanzamiento de un curso, programa o membresía
- Lanzamiento de un lead magnet o producto de entrada
- Necesita todo el arsenal de contenido desde un solo brief de producto

## Reglas que no se negocian

1. Definir posicionamiento ANTES de escribir cualquier copy. Todo el contenido fluye del ángulo.
2. Investigar la audiencia antes de asumir que conoces su lenguaje o sus miedos. Usar `investigacion-nicho-formula100k` si no se ha hecho.
3. Cada pieza de contenido sirve a UNA función clara en el arco del lanzamiento.
4. Especificidad gana a adjetivos en todos los formatos y canales.
5. La misma voz y el mismo ángulo tienen que correr por TODO el lanzamiento.
6. Nada sale sin pasar el gate de calidad.

## Flujo de trabajo del lanzamiento

### Fase 1: Investigación (si no se tiene brief de nicho)

Delegarla a `investigacion-nicho-formula100k`:
- perfil de audiencia objetivo (trabajos que intenta hacer, miedos, lenguaje real, qué ya intentó)
- mapa de 2-3 competidores directos/adyacentes (posicionamiento, huecos, mensajes débiles)
- 1-3 insights de audiencia que el ángulo del lanzamiento va a explotar

Entregable: brief de investigación (perfil de audiencia + resumen competitivo + insights clave).

### Fase 2: Posicionamiento (no tocar copy hasta aquí)

Producir:
- Declaración de beneficio central: una oración, sin lista de features, sin jerga
- Fórmula de posicionamiento: "[Producto/comunidad] ayuda a [audiencia] a [lograr resultado] a través de [mecanismo único]"
- Ángulo de campaña: la tensión, insight o momento específico en el que vive todo el lanzamiento
- Voz del lanzamiento: tono, palabras prohibidas, cómo suena la creadora en modo venta

No escribir ninguna pieza de contenido hasta que el posicionamiento esté aprobado.

### Fase 3: Producción de contenido

Producir en este orden — cada capa informa a la siguiente:

1. **Copy de landing** (si aplica): headline, problema, solución, cómo funciona, prueba social, CTA
2. **Secuencia de emails/DMs** (si aplica): cada mensaje tiene un propósito; arco = problema → educación → agitación → solución → prueba → urgencia → CTA final
3. **Guiones de reels de lanzamiento**: usar `guionizacion-formula100k` con el ángulo aprobado
4. **Secuencia de historias**: usar `calendarizador-historias-formula100k` para los días de lanzamiento
5. **Audios de venta para historias** (si aplica): usar `audios-venta-f100k`
6. **Calendario de lanzamiento**: día por día, con canal, tipo de contenido, horario y dependencias

### Fase 4: Revisión

Gate cada pieza antes de entregar:
- Test de 5 segundos en todo el copy hero/principal (¿está claro para quién es, qué hace, por qué actuar ahora?)
- Auditoría de CTAs: uno por pieza, específico, ganado — no demandado
- Consistencia de voz en todos los canales
- Auditoría de afirmaciones: cada claim es específico y sostenible con evidencia real
- Consistencia cruzada: lo que dice el reel coincide con la landing; el email coincide con lo prometido

## Contrato de output

Una campaña completa entrega:

1. **Brief de posicionamiento** — ángulo, declaración de beneficio central, perfil de voz
2. **Copy de landing** (si aplica) — hero, problema, solución, cómo funciona, prueba, CTA
3. **Secuencia de comunicación** — emails o DMs con propósito por día
4. **Guiones de reels** — mínimo 3 reels de lanzamiento con gancho, desarrollo, CTA
5. **Secuencia de historias** — storyboard del arco de lanzamiento (anticipación → revelación → urgencia → cierre)
6. **Audios de venta** (si aplica) — scripts para historias de audio
7. **Calendario de lanzamiento** — día por día con canal, tipo de contenido, horario y dependencias

## Gate de calidad

Antes de entregar cualquier pieza:
- Todas las piezas suenan al mismo autor/creadora
- No quedan adjetivos vacíos ni superlativos huecos
- Cada CTA es específico y ganado (nunca "haz clic aquí" o "descúbrelo")
- Ningún copy está duplicado verbatim entre canales
- El copy hero pasa el test de 5 segundos
- Los claims de emails coinciden exactamente con los claims de la landing
- Ninguna pieza funciona igual si se le cambia el nombre del producto (si sí funciona, es demasiado genérico)

## Palabras prohibidas en todo lanzamiento F100K

Eliminar y reescribir cualquier:
- "revolucionario", "transformador", "único en su tipo", "sin igual"
- "En el mundo de hoy..."
- Urgencia falsa no respaldada por fecha real
- Prueba social hueca sin especificidad ("miles de personas lo usan")
- CTAs genéricos ("aprende más", "descubre más", "haz clic aquí")
- Copy que podría funcionar para cualquier otro producto del mismo nicho sin cambios

## Skills F100K que orquesta este skill

Llamar según lo que requiera el lanzamiento:
- `investigacion-nicho-formula100k` — investigación de audiencia y competencia
- `guionizacion-formula100k` — guiones de reels de lanzamiento
- `calendarizador-historias-formula100k` — arco de historias del lanzamiento
- `audios-venta-f100k` — audios para historias de venta
- `generador-ganchos-formula100k` — ganchos para reels de lanzamiento
- `constructor-ofertas-f100k` — estructurar la oferta antes del copy
- `calendarizador-contenido-formula100k` — calendario completo de publicación
