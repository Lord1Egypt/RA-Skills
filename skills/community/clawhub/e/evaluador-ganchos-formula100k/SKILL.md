---
name: evaluador-ganchos-formula100k
description: "Evalúa ganchos visuales a partir de capturas del primer segundo de videos O del video completo. Activar SIEMPRE que se pida 'evalúa este gancho', 'analiza mi primer segundo', 'revisa mi gancho', 'diagnostica este primer segundo', 'qué le falta a este gancho', 'puntaje de mi gancho', 'es viral este gancho', 'audita mi thumbnail', 'mejora este primer segundo', 'predice si va a viralizar', 'pásalo por virality predictor'. También cuando suban una captura O un archivo de video (.mp4/.mov) y quieran saber si funciona. Aplica la metodología de FÓRMULA 100K: Sistema E.N.C. (Estímulo Núcleo, Carga Cognitiva, Contextualización), las 5 Formas Visuales (F1-F5), los 15 Gatillos de Viralidad, el Gancho Textual del Top 1% y el Test del 1 Segundo. Cuando el input es VIDEO, complementa la lectura manual con el Virality Predictor de Higgsfield (hook strength, retention risk, engagement, atención)."
argument-hint: "[contexto del video opcional]"
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - La captura del primer segundo llega por Telegram (mejor como archivo, para que no pierda calidad). Si manda solo el video, pídele también la captura del segundo 1: en este servidor no se extraen fotogramas.
> - Virality Predictor (Paso 7): solo con el plugin de Higgsfield. Sube el video que mandó (`media_upload` → `media_confirm`), di el costo estimado y espera ✅ antes de `virality_predictor`. Sin plugin, entrega solo el diagnóstico manual y dilo en la primera línea.
> - El diagnóstico va entero al chat de Telegram; si es largo, resumen + `.md` en `informes/ganchos/`.

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

# Evaluador de Ganchos · FÓRMULA 100K

Diagnostica una captura del primer segundo de un video aplicando los frameworks de FÓRMULA 100K. Devuelve un análisis estructurado con score numérico, errores detectados y recomendaciones accionables.

## Cuándo se activa esta skill

- El usuario sube una captura de su primer segundo y pide evaluación
- Una alumna quiere saber si su gancho funciona antes de publicar
- Necesitan auditar el primer segundo de un competidor
- Quieren comparar dos versiones de gancho

## Contexto crítico

**Usuario:** creador/a de contenido hispano (tú o tu clienta). Audiencia hispana, español neutro obligatorio (NO voseo).

**Material de referencia (cargar en orden):**
- `criterios.md` — la rúbrica completa de evaluación con todos los frameworks
- `output-template.md` — el formato exacto del diagnóstico

**Material educativo:** la guía visual de ganchos de FÓRMULA 100K (en la comunidad) contiene la metodología completa que esta skill operacionaliza.

## Flujo paso a paso

### Paso 1: Recibir input

El input puede llegar de 4 formas:
1. **Imagen + texto explicativo** ("evalúa este gancho, es para un video sobre X")
2. **Solo imagen** ("¿qué tal está?")
3. **Video completo (.mp4/.mov)** — habilita el análisis cuantitativo con Virality Predictor además del manual
4. **Texto que pide subir material** ("quiero evaluar mi gancho")

Si NO hay imagen ni video adjunto, pide material antes de continuar:
> "Comparte la captura del primer segundo del video, o si lo tienes a mano, pásame el archivo de video completo (.mp4/.mov) — con el video puedo correr también el Virality Predictor de Higgsfield para sumar una lectura cuantitativa."

Si hay imagen pero falta contexto, haz UNA pregunta clave (no más):
> "¿De qué trata el video y para quién es? Eso me ayuda a evaluar si tu gancho comunica la promesa correcta."

Si el usuario aporta el contexto en el mensaje inicial, no preguntes nada — procede a evaluar.

**Si el input es un VIDEO (no solo screenshot):** habilita el Paso 7 (Virality Predictor). El análisis manual sigue siendo obligatorio sobre el primer cuadro — pídele la captura del segundo 1 (en este servidor no se extraen fotogramas del video) y aplica los criterios. Luego, en paralelo o al final, lanza el predictor para complementar.

### Paso 2: Cargar la rúbrica

Lee `criterios.md` completo. Contiene:
- Sistema E.N.C. con sub-criterios para evaluar cada componente
- Las 5 Formas Visuales con cómo identificar cuál se está usando
- Los 15 Gatillos de Viralidad con señales para detectarlos
- Reglas del Gancho Textual (palabras, contraste, zona segura, pacing)
- Test del 1 Segundo con criterio de aprobación
- Tabla de cálculo del score

### Paso 3: Analizar la imagen con visión

Aplica los criterios en este orden estricto:

**A) Test del 1 Segundo (eliminatorio)**
Mira la captura como si fuera la primera vez. Sin contexto. ¿Entiendes en menos de 1 segundo de qué va el video? Si NO, el gancho está roto desde la base — anótalo y sigue evaluando los detalles para identificar dónde está el fallo.

**B) Identificar la Forma Visual (F1-F5 o híbrida)**
Usa la guía de identificación en `criterios.md`. Cada forma tiene marcadores visuales claros:
- F1: rostro/cuerpo + texto contextual
- F2: acción simbólica (verbo visible) + subtítulo
- F3: título grande + sujeto secundario
- F4: imagen sorprendente/viral + texto guía
- F5: movimiento disruptivo + corte (más difícil de evaluar en captura, requiere video)

**C) Evaluar E.N.C. componente por componente**

Para **E (Estímulo Núcleo)**:
- ¿Hay UN protagonista visual claro?
- ¿Está nítido, contrastado, posicionado correctamente?
- ¿Hay un verbo/gesto visible?

Para **N (Carga Cognitiva)**:
- Cuenta elementos en pantalla. ≤3 = bajo. 4-6 = medio. 7+ = alto (mal).
- ¿El fondo está limpio o caótico?
- ¿Hay 1 sola idea visible?

Para **C (Contextualización)**:
- ¿Cuántos apoyos secundarios hay? Máx 2 ideal.
- ¿Compiten con el E o lo refuerzan?
- ¿Apuntan o señalan algo?

**D) Detectar Gatillos de Viralidad**
De los 15 gatillos, identifica cuáles activa el gancho actual. Sé honesto: si solo activa 0-1, el video no viralizará.

**E) Evaluar Gancho Textual** (si hay texto en pantalla)
- Cuenta palabras (ideal ≤8)
- Evalúa contraste, tamaño (7-12% del frame), zona segura
- ¿El quiebre de línea es lógico?
- ¿La tipografía es nativa, premium o genérica?
- ¿Tiene paréntesis tipo "Susurro"?

### Paso 4: Calcular el score

Usa la tabla de scoring en `criterios.md`. El score es sobre 100:
- Test del 1 Segundo: 25 pts (binario: pasa/no pasa)
- E.N.C.: 30 pts (10 cada componente)
- Gatillos: 20 pts (proporcional al número activado, máx 3 gatillos cuentan)
- Gancho Textual: 15 pts (si aplica; si no hay texto, redistribuir)
- Forma Visual ejecutada correctamente: 10 pts

**Bandas de calidad:**
- 85-100: Listo para publicar (top 10%)
- 70-84: Viable, con ajustes menores
- 50-69: Necesita iteración significativa
- <50: Reconstruir desde cero

### Paso 5: Generar el diagnóstico

Usa EXACTAMENTE el formato de `output-template.md`. No te saltes secciones. El diagnóstico debe ser:
- **Honesto** — si está mal, dilo. No inflar puntajes.
- **Específico** — referencia elementos visuales concretos ("la planta del fondo", "el texto azul")
- **Accionable** — cada recomendación debe ser implementable hoy
- **En español neutro** — usa "tú", "tienes", "puedes" — NUNCA voseo

### Paso 6: Cerrar con propuesta de mejora

Al final, ofrece una **versión mejorada concreta**:
- Si el problema es el texto: reescribe el gancho textual aplicando las 4 estructuras de copywriting (Curiosidad/Dolor/Resultado/Susurro)
- Si el problema es visual: describe la composición ideal paso a paso (qué eliminar, qué añadir, dónde colocar cada elemento)
- Si el problema es la forma: sugiere cuál de las F1-F5 funcionaría mejor para ese contenido

### Paso 7: Análisis cuantitativo con Virality Predictor (solo si hay VIDEO)

Este paso **complementa** el diagnóstico manual; no lo reemplaza. La rúbrica F100K es el veredicto principal — el Predictor aporta una segunda lectura medida por modelo (engagement, retención, fuerza del hook).

**Cuándo activarlo:**
- El usuario subió un archivo de video (.mp4/.mov) — no solo un screenshot.
- O el usuario pidió explícitamente "pásalo por virality predictor", "predice si va a viralizar", "score de Higgsfield", etc.

**Flujo:**

1. **Subir el video a Higgsfield** (si aún no está en la cuenta):
   - `mcp__higgsfield__media_upload` con la ruta local → obtienes `upload_url` + `media_id` pendiente.
   - `mcp__higgsfield__media_confirm` con el `media_id` para dejarlo en estado `confirmed`.
   - Si el video YA fue generado en Higgsfield (Seedance/Kling), usa directamente su `job_id` — no hace falta re-subir.

2. **Lanzar el análisis:**
   ```
   mcp__higgsfield__virality_predictor
   action: "create"
   params:
     model: "virality_predictor"
     medias: [{ role: "video", id: "<media_id o job_id>" }]
   ```

3. **Guardar el `job_id`** que devuelve. Es necesario para reabrir el dashboard después con `action: "preview"`.

4. **Leer resultados** (el predictor entrega un dashboard interactivo con):
   - **Hook Strength** — fuerza del primer cuadro/segundo. Cotejar contra el Test del 1 Segundo manual.
   - **Retention Risk** — dónde se cae la audiencia (curva de retención).
   - **Engagement** — predicción de likes/comentarios/shares relativos.
   - **Attention** — atención sostenida.
   - **Audience Response** — respuesta esperada del público.
   - **Creative Performance** — score creativo agregado.

5. **Integrar la lectura en el diagnóstico:**
   - Añade la sección "LECTURA CUANTITATIVA · VIRALITY PREDICTOR" del template (entre Gatillos y Aciertos).
   - **Cruzar con el score manual:**
     - Si el score F100K es alto pero Hook Strength es bajo → el gancho engaña visualmente pero el video pierde fuerza → revisar segundos 2-5.
     - Si el score F100K es bajo pero Engagement predicho es alto → puede ser un hook plano que igual genera comentarios polarizados — investigar por qué.
     - Si Retention Risk está alto en los primeros 3s → el gancho NO está reteniendo → priorizar reconstruir primer segundo aunque el manual lo apruebe.
   - **Mantén el veredicto del score manual como principal.** El Predictor es señal complementaria, no juez final. Si entran en conflicto, decláralo y explica la hipótesis de por qué.

6. **Entregar el link del dashboard** al usuario al final del diagnóstico para que pueda explorar la curva de retención y los frames críticos por su cuenta.

**Si el Predictor falla o no está disponible:** indica claramente "Análisis cuantitativo no disponible en esta corrida" y entrega solo el manual. Nunca inventes números del Predictor.

## Reglas anti-error

- **NO inventes elementos** que no estén en la imagen. Si no ves el texto claramente, dilo.
- **NO uses voseo argentino** — El usuario ya corrigió esto en otras skills. Usa "tú", "tienes", "puedes", "haz" — NUNCA "vos", "tenés", "podés", "hacé".
- **NO seas complaciente** — si el gancho está mal, ponle puntaje bajo. El usuario valora la honestidad.
- **NO recomiendes cosas genéricas** ("mejora la calidad", "ponle más onda"). Sé técnico: "elimina la planta del fondo derecho", "reduce el texto de 12 a 6 palabras", "cambia la fuente Arial por una bold tipo Inter".
- **NO uses el bot de ganchos visuales** — esta skill ES el reemplazo manual del bot.
- **NO evalúes audio** — solo lo visual. Si la usuaria menciona audio, recuerda que evaluamos solo el primer cuadro.
- **NO inventes números del Virality Predictor.** Si el tool falla, no devuelve scores, o el usuario solo dio screenshot, indica que no hay lectura cuantitativa y sigue con el diagnóstico manual.
- **NO dejes que el Virality Predictor sobrescriba el veredicto manual.** El score F100K manda; el Predictor complementa. Si entran en conflicto, declara el conflicto y explícalo.

## Casos especiales

- **Imagen borrosa o de baja calidad:** Pide otra captura antes de evaluar. No adivines.
- **Imagen no es del primer segundo:** Pregunta al usuario si capturó al segundo 1 o más adelante. La evaluación cambia.
- **Imagen es un thumbnail de YouTube:** Aplica los mismos criterios pero menciona que YouTube tiene reglas distintas (más texto permitido, contraste extremo importa más).
- **Múltiples imágenes (variantes A/B):** Evalúa cada una y entrega comparativa con cuál ganaría.

## Output del proceso

Mientras evalúas, comunica brevemente:
1. "Cargando rúbrica de evaluación"
2. "Analizando E.N.C. en la imagen"
3. (Si hay video) "Lanzando Virality Predictor de Higgsfield"
4. (Generar diagnóstico)

Luego entrega el diagnóstico completo siguiendo el template, incluyendo la sección de Virality Predictor si corresponde y el link del dashboard al final.
