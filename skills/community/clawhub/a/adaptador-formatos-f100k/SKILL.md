---
name: adaptador-formatos-f100k
description: "Toma un video/post viral de CUALQUIER nicho (incluso uno random y ajeno) — por enlace de Instagram, TikTok o YouTube — DECODIFICA su formato/mecánica viral (no su tema) y lo ADAPTA al RUBRO DE QUIEN LO PIDE (cualquiera: se lee del Segundo Cerebro o se pregunta), proponiendo 2-3 ángulos listos para guionizar. Activar SIEMPRE que alguien diga \"adapta este formato a lo nuestro\", \"roba el formato de este reel\", \"este video random me gustó, sirve para mi nicho?\", \"convierte este viral en algo mío\", \"decodifica este formato\", \"qué formato tiene este video y cómo lo uso\", \"hazme algo como este pero de mi tema\", o cualquier variación que combine un ENLACE de video viral (de tema ajeno o no) con la intención de reutilizar su ESTRUCTURA/MECÁNICA. NO confundir con investigacion-contenido-formula100k (caza referencias por keyword) ni con remix-viral-formula100k (relanza contenido PROPIO). Esta skill parte de UN video ajeno y extrae su esqueleto viral para trasplantarlo."
argument-hint: "[URL del video viral] (+ tema/ángulo opcional)"
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Paso 1 SIN navegador logueado. Link de Instagram: Apify con `APIFY_TOKEN` (`apify~instagram-scraper` con la URL del post trae caption, autor, vistas, miniatura y comentarios). TikTok: `clockworks~tiktok-scraper` con la URL. YouTube: tu navegador o tu herramienta web sobre la página pública, y la transcripción con `transcripcion-youtube-formula100k` si está.
> - El «frame» del Paso 1 es la miniatura (`displayUrl`/cover) que devuelve Apify: mírala. No descargues el video ni saques cuadros con ffmpeg en el servidor.
> - Sin `APIFY_TOKEN`, o si el post es privado: pide por Telegram 2 o 3 capturas (primer cuadro con el texto en pantalla + comentarios) o una grabación de pantalla corta. La regla de la skill se mantiene: si no puedes confirmar la mecánica, lo dices y no la adivinas.
> - «Cerrar el navegador y borrar capturas» no aplica aquí; las capturas que mande la usuaria no se guardan salvo que lo pida (entonces en `ideas/formatos/`).
> - Los ángulos se guardan en `ideas/formatos-adaptados.md` (uno debajo del otro, con el link original) y por Telegram mandas el bloque de salida. El Paso 5 sigue con `guionizacion-formula100k`, que guarda en `guiones/`.

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

El insight central: **un formato viral es independiente de su tema.** Un reel sobre películas animadas, gatos o autos puede esconder una mecánica (reto de niveles, plot twist, versus, máquina de comentarios) que funciona igual de bien en CUALQUIER rubro. Esta skill separa el **esqueleto** (la mecánica que genera el engagement) de la **carne** (el tema random) y trasplanta el esqueleto al rubro de quien lo pide.

Salida: la **decodificación del formato** + **2-3 ángulos** adaptados al nicho, listos para que el usuario elija uno y se desarrolle el guion completo.

---

## El nicho de destino (a dónde se adapta TODO)

El negocio de la usuaria: su rubro, su audiencia, su oferta y sus pilares están en `USER.md` y `cerebro/`. Voz: la de `cerebro/voice-guide.md` si existe; si no, directa, "tú", nivel sexto grado.

Si el usuario da un tema/ángulo específico en los argumentos, ese manda. Si no, se proponen ángulos basados en los pilares de su negocio.

---

## Proceso (5 pasos)

### Paso 1 — Decodificar la referencia (observar, NO inventar)

Abrir el enlace **logueada** con `agent-browser` (Instagram/TikTok requieren login). Regla de oro: nunca inventar el formato; siempre confirmarlo con evidencia real del post.

```bash
agent-browser open "<URL>"      # esperar ~4s a que cargue
agent-browser snapshot -c       # leer caption, autor, hashtags
agent-browser screenshot ref.png  # ver el/los frame(s) del video
```

Extraer y **leer los comentarios** (a menudo el clic en "Cargar más comentarios" revela la mecánica): los comentarios delatan POR QUÉ la gente interactúa ("solo pasé 3 niveles", "lloré", "yo soy team X"). Esa reacción ES la mecánica viral.

Capturar:
- **Gancho** (caption + primer frame + texto en pantalla)
- **Mecánica de engagement** (¿qué hace comentar/compartir/guardar?)
- **Estructura** (¿lista? ¿niveles? ¿versus? ¿historia con giro? ¿reacción?)
- **Disparador emocional** (identidad/tribu, ego, curiosidad, sorpresa, validación)

Si el video está silenciado o tras login-wall y no se puede confirmar la mecánica con caption + frame + comentarios, **decirlo** y pedir contexto al usuario en vez de adivinar.

### Paso 2 — Nombrar el formato explícitamente

Escribir en 3-4 líneas la "receta" del formato, despegada del tema. Ejemplo real:

> **Formato = RETO DE NIVELES POR TRIBU (tier-list gamificada).**
> Gancho de tribu ("¿dónde están mis X reales?") → escala ítems de Fácil→Moderado→Difícil→Nivel final (lo más obscuro) → el espectador se auto-mide y comenta hasta qué nivel llegó → la gente se reta entre sí. = máquina de comentarios por ego + identidad.

### Paso 3 — Mapear a la metodología F100K

Conectar el formato decodificado con:
- **1 de los 7 Pilares de Valor** de F100K (Revelación, Utilidad, Validación Emocional, Desafío/Gamificación, Actualidad, Curaduría, Disrupción).
- **1-2 estructuras** del catálogo de `guionizacion-formula100k` (ej. #30 Máquina de Comentarios, #19 Desafío Contracorriente, #29 Versus, #18 Momento WTF, #20 Efecto Boomerang).

Esto garantiza que el ángulo adaptado herede una estructura ya probada, no solo una imitación superficial.

### Paso 4 — Proponer 2-3 ángulos adaptados

Cada ángulo = **misma mecánica del Paso 2** + **tema del RUBRO de quien lo pide** (el que declaraste en el anclaje). Para cada uno entregar:
- **Título/promesa** del ángulo
- **Gancho** reescrito (manteniendo el patrón viral del original)
- **Cómo se ejecuta la mecánica** con contenido de ESE rubro (los "niveles", el "versus", el "giro", etc.)
- **CTA de engagement** que replica el disparador del original
- 1 frase de **por qué funciona** / cómo posiciona a quien lo publica

Marcar una **recomendación** (la que mejor conserve el espíritu del original + mejor calce con el diferenciador de quien lo publica, según su Segundo Cerebro).

### Paso 5 — Handoff al guion completo

Cuando el usuario elija un ángulo, **invocar `guionizacion-formula100k`** para desarrollar el guion completo (verificación de viralidad con referencias reales + sistema de 3 ganchos verbal/visual/textual + guion paso a paso). Esta skill termina al entregar los ángulos; el guion final lo construye la skill de guionización.

---

## Formato de salida

```
🎬 REFERENCIA: @autor — "<caption>" (<nicho original>)

🔍 FORMATO DECODIFICADO
<receta del formato en 3-4 líneas, despegada del tema>
- Mecánica de engagement: <...>
- Disparador emocional: <...>

🧬 MAPEO F100K
- Pilar de valor: <1 de 7>
- Estructura base: <#N nombre del catálogo de guionización>

🎯 ÁNGULOS ADAPTADOS
A) <título> — Gancho: "<...>" | Mecánica: <...> | CTA: "<...>" | Por qué: <...>
B) ...
C) ...

⭐ Recomendación: <A/B/C> — <razón en 1 frase>
→ Dime cuál eliges y lo desarrollo completo con guionizacion-formula100k.
```

---

## Notas y guardarraíles

- **El tema del original es irrelevante; la mecánica lo es todo.** Nunca descartar una referencia por ser "de otro nicho" — ese es justo el punto de esta skill.
- **NO inventar el formato.** Confirmar con caption + frame + comentarios reales (memoria: "NUNCA inventar data"). Si no se puede ver/confirmar, preguntar.
- **NO copiar el tema** del original (eso sería off-niche). Solo se trasplanta el esqueleto.
- No es `investigacion-contenido-formula100k` (esa caza referencias por keyword dentro del nicho) ni `remix-viral-formula100k` (esa relanza contenido propio de la creadora).
- Cerrar el navegador al terminar (`agent-browser close`) y borrar capturas temporales.
- Mantener la voz F100K: directa, "tú". Los tecnicismos del rubro NO se eliminan: se usan y se traducen en su primera mención.
