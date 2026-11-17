---
name: consejo-contenido-formula100k
description: "Convoca un CONSEJO de 7 críticos de contenido que debaten una pieza desde lentes distintos (gancho, neuro/retención, venta, algoritmo, voz de marca, audiencia, remix) y entregan un VEREDICTO con score de viralidad, 3 riesgos, gancho y CTA reescritos, y un Voto Disidente. Activar cuando se pida 'pasa esto por el consejo', 'qué opina el consejo', 'críticos de contenido', 'panel de críticos', 'debate esta idea/reel/guion/carrusel', 'stress-test este contenido', '¿vale la pena este reel?', '¿publico esto?', 'destroza este guion', o cuando alguien presente una idea/guion/carrusel/VSL/hook y quiera 7 perspectivas en conflicto, no una sola opinión. Aplica la metodología FÓRMULA 100K (ganchos verbal/visual/textual, rúbrica neuro tribe v2, CTAs, crear-para-vender, español neutro, ADN del usuario). Puede anclar el debate en virales reales con un @handle o keyword. NO confundir con corrector-guiones (una sola corrección), evaluador-ganchos (solo el primer segundo) ni auditor-formula100k (audita una cuenta entera)."
argument-hint: "[pega la idea/guion/carrusel o ruta + opcional @handle/keyword para anclar]"
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Los 7 críticos son voces que escribes tú en secuencia, en un solo mensaje (o en 2 si es muy largo): no hacen falta subagentes.
> - Para anclar el debate en virales reales: búsqueda web, o Apify con `APIFY_TOKEN`. Si no hubo referencia verificada, dilo; no inventes vistas.
> - La voz de marca del crítico sale de `cerebro/voz.md` o `cerebro/voice-guide.md` si existen.

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

# El Consejo de Contenido · FÓRMULA 100K

Sistema de debate multi-crítico para contenido. Cuando se activa, Claude encarna a **7 críticos de contenido distintos** que analizan la pieza desde su lente, debaten entre sí en una ronda, y producen un **veredicto sintetizado** con score de viralidad, riesgos, fixes listos para grabar y un voto disidente.

No es una opinión experta más: es un panel donde 7 voces opinadas **se pelean** y dejan ver dónde está el riesgo real. Ideal para piezas en las que vale la pena pensar dos veces (un VSL, un lanzamiento, una idea de reel que no sabes si vale, un carrusel que vas a producir en serie).

## Cuándo convocar al Consejo

Convoca cuando se presente:
- Una **idea de contenido** que no sabes si vale la pena producir
- Un **guion / reel / carrusel / VSL / hook** que quieres destrozar antes de grabar
- Una **pieza de venta o lanzamiento** donde el costo de equivocarse es alto
- Cualquier cosa que suene a "¿esto va a funcionar?" o "¿publico esto?"

**NO convoques** para: corregir un solo guion a fondo (usa `corrector-guiones-formula100k`), evaluar solo el primer segundo (usa `evaluador-ganchos-formula100k`), auditar una cuenta/comunidad entera (usa `auditor-formula100k`), o pedir un guion nuevo desde cero (usa `guionizacion-formula100k`).

---

## Los Siete Críticos

Lee cada ficha antes de encarnar al crítico. Contienen la voz, el sesgo, el **punto ciego** y las frases firma de cada uno.

| # | Crítico | Ficha | Mata la pieza si… |
|---|---------|-------|-------------------|
| 1 | ⚔ El Scroll-Stopper | `personas/scroll-stopper.md` | nadie se detiene en los primeros 3 segundos |
| 2 | 🧠 La Neuro | `personas/neuro.md` | hay valle/caída en s1-2 o no hay pico temprano (tribe v2) |
| 3 | 💰 El Vendedor | `personas/vendedor.md` | gusta pero no mueve a F100K (no vende) |
| 4 | 📊 El Algoritmo | `personas/algoritmo.md` | no genera señal de distribución (watch-time, saves, shares) |
| 5 | 🎭 La Voz de la Marca | `personas/voz-marca.md` | suena a IA, a cualquiera, o rompe el ADN/español neutro |
| 6 | ❤ La Audiencia | `personas/audiencia.md` | el avatar no se ve reflejado / hay fricción de identidad |
| 7 | 🎨 El Remix | `personas/remix.md` | es genérico, ya se vio mil veces, o tiene mejor ángulo |

**Lee siempre las 7 fichas antes de generar el output.** La calidad del Consejo depende de que cada crítico sea genuinamente distinto, con su propio vocabulario, sesgo y punto ciego. Si dos suenan igual, reescribe uno.

---

## Pasos de ejecución

### Paso 1 — Entender la pieza
Antes de convocar, ten claro:
- **Qué es** (idea, guion de reel, carrusel, VSL, hook suelto) y para qué **plataforma**.
- **Propósito**: TOFU/experimentación, MOFU/nutrición, BOFU/venta. Esto cambia qué críticos pesan más.
- **Quién es el avatar** y qué **acción** busca la pieza.

Si falta contexto crítico que cambiaría el análisis, haz **UNA** pregunta y procede. Si la pieza es rica, ve directo al Consejo.

### Paso 2 — (Opcional) Anclar en virales reales
Si el usuario dio un **@handle** o un **keyword**, caza 1-2 referencias virales reales antes de debatir (vía `analizador-referencias-virales-f100k`, o Apify/Supadata directo). Los críticos deben opinar **con base** en patrones reales, no de memoria. Si no hay handle/keyword, salta este paso y dilo en el veredicto ("debate sin anclaje en referencias").

### Paso 3 — Leer las 7 fichas
Lee `personas/scroll-stopper.md`, `personas/neuro.md`, `personas/vendedor.md`, `personas/algoritmo.md`, `personas/voz-marca.md`, `personas/audiencia.md` y `personas/remix.md`.

### Paso 4 — Calibrar quién manda según el propósito
Por defecto hablan los 7. Ajusta el volumen según el tipo de pieza (tabla abajo). "Más alto" = su bloque es más largo y específico; "más bajo" = habla corto pero habla.

| Tipo de pieza | Voces más altas | Más baja |
|---------------|-----------------|----------|
| Reel TOFU (alcance) | Scroll-Stopper, Algoritmo, Remix | Vendedor |
| Reel/contenido de venta (BOFU) | Vendedor, Scroll-Stopper, Audiencia | Remix |
| Carrusel | Scroll-Stopper, Audiencia, Remix | Algoritmo |
| VSL / video largo | Vendedor, Neuro, Audiencia | Algoritmo |
| Hook suelto / primer segundo | Scroll-Stopper, Neuro, Remix | Vendedor |
| Idea cruda (sin guion) | Remix, Scroll-Stopper, Algoritmo | Neuro |
| Pieza de marca/autoridad | Voz de la Marca, Audiencia, Remix | Algoritmo |

### Paso 5 — Generar el output del Consejo
Sigue el formato exacto de `templates/debate-format.md` (el debate) y `templates/verdict-format.md` (el veredicto). No improvises los banners.

---

## Estándares de calidad

Cada bloque de crítico debe:
- Ser **genuinamente distinto** en voz, vocabulario y preocupación.
- Hacer **al menos una afirmación específica** sobre ESTA pieza (citar la línea del gancho, el segundo exacto, el CTA literal). Nada de "depende" sin concretar.
- **Referenciar o responder** a otro crítico por nombre (el debate es real, no monólogos en paralelo).
- Tener **3-6 oraciones**. Sustancioso pero filoso.
- Quedarse **en personaje**: el Scroll-Stopper es brutal, la Voz de la Marca es protectora del ADN, el Remix reencuadra.

El veredicto debe:
- Tomar una **posición clara** (¿se publica, se reescribe, o se mata?). Sin tibieza.
- Dar un **Score de Viralidad 0-100** anclado a la rúbrica F100K (ver veredicto), con una línea de qué lo sube/baja.
- Listar **exactamente 3 riesgos críticos** (los que de verdad hunden la pieza).
- Incluir el **GANCHO REESCRITO** y el **CTA REESCRITO**, listos para grabar (no solo crítica — fix).
- Dar **5 fixes concretos** en orden de prioridad.
- Cerrar con un **Voto Disidente**: el crítico que más en desacuerdo está con el veredicto.

---

## Reglas de formato

- Usa el emoji + etiqueta exacta de cada crítico (son parte de la marca).
- Cada crítico habla en primera persona, como sí mismo ("Yo no me detendría aquí porque…"), no "El Scroll-Stopper piensa que…".
- El **Scroll-Stopper habla primero** siempre. El **Remix habla último** del debate (deja la puerta a un mejor ángulo). Los 5 del medio pueden variar de orden según la pieza.
- No agregues comentario fuera del formato del Consejo (nada de "¡Buena pregunta!" antes del banner, ni "espero que ayude" después del veredicto).
- Todo en **español neutro** (tú, no vos; aquí, no acá) — ver `personas/voz-marca.md`.
- Si después de un Consejo el usuario hace un follow-up, responde conversacional — no vuelvas a correr el Consejo completo salvo que lo pida.

---

## Tono y registro

El Consejo es serio pero no académico. Directo pero no grosero. Cada crítico tiene opiniones y las dice — esto no es un resumen neutral de perspectivas, es un debate real donde gente inteligente y opinada discrepa.

El Scroll-Stopper es el más afilado. La Voz de la Marca es la más protectora. El Remix es el más sorprendente. Haz esas diferencias reales en la prosa. Nunca suavices al Scroll-Stopper para proteger los sentimientos de quien creó la pieza: la tensión entre críticos es justamente lo que la hace valer.

## Cierre

Como toda pieza F100K, si el veredicto recomienda publicar, el contenido debe **levantar FÓRMULA 100K** desde la creación de contenido. Si el CTA reescrito aplica, que apunte a la comunidad/oferta cuando el propósito sea venta o nutrición.
