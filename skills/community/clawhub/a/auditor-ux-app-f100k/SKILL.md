---
name: auditor-ux-app-f100k
description: "Auditor de la construcción de UX de una app (producto, no pixel) con la doctrina de FÓRMULA 100K y 22 cicatrices reales de apps en producción. Revisa CUALQUIER etapa: brief, spec/PRD, plan de implementación o la app ya construida. Recorre la app como usuaria con el navegador del agente (URL pública o proyecto en el workspace), la puntúa contra una rúbrica de 10 dimensiones (claridad, primer minuto, los 4+1 estados, feedback honesto, no perder el trabajo, la pantalla no miente, móvil de verdad, dashboard 1-3-5, puertas de acceso y dinero, salir al mundo), entrega un informe con termómetro 0-100 y hallazgos con evidencia, y —tras tu ✅— APLICA los arreglos en los archivos. Usar cuando digan \"revisa la UX de esta app\", \"audita mi app\", \"qué le falta a mi app\", \"revisa este spec/plan/brief antes de construir\", \"/audita-ux\", \"por qué mi app se siente a medias\". NO es la skill de diseño visual (ux-elevacion-formula100k); NO construye la app desde cero (crea-tu-app-f100k)."
argument-hint: "[ruta del repo, del documento, o URL de la app]"
disable-model-invocation: false
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - El recorrido de las 8 pruebas se hace con el navegador del agente (Chromium de OpenClaw) sobre la URL pública de su app o sobre el proyecto levantado en el workspace (`entregables/apps/<app>/`). Nunca inicies sesión con su Google ni con su contraseña personal: si la app pide login, pídele una cuenta de prueba creada para la auditoría, y otra sin acceso para la prueba 7.
> - Prueba de teléfono: emula el viewport de 390×844 en el navegador. No uses `--window-size`: Chrome headless por debajo de 500 px recorta y da desbordes falsos.
> - Si solo te pasa el link y no el código, audita lo que se ve y deja la lectura de código en «No verificado». Con documento (brief, spec, plan), te lo manda por Telegram como archivo.
> - Capturas y notas van a `informes/auditoria-ux/<app>/`. El informe se manda por Telegram como documento, con el termómetro y los 3 arreglos en el chat.
> - Fase 5: aplicar arreglos solo sobre archivos que están en el workspace, y después le mandas el `.zip` o el diff. Push y deploy solo con SU cuenta conectada y ✅.
> - Las cicatrices vienen anonimizadas («la app de guiones», «la app de retos»…): cítalas como «mismo patrón que la cicatriz C5», no como datos de su app.

---

# Auditor de UX de App — FÓRMULA 100K

Revisa **cómo está construida la experiencia**, no cómo se ve. Lo visual (tipografía, animación,
anti-slop, landings) es trabajo de `ux-elevacion-formula100k`; esta skill delega ahí y no lo duplica.

**Método: recorrido + rúbrica.** El recorrido descubre lo que nadie anticipó; la rúbrica garantiza
cobertura y pone el número. Es el método del artifact *Crea Tu Aplicación*: los rasgos son la rúbrica
y las pruebas ("borra los datos y mira", "refresca el navegador") son el recorrido.

## Regla que manda sobre todas

**Cada hallazgo cita evidencia o no existe.** `archivo:línea`, una captura, o la frase textual del
documento. Si no pudiste verificar algo, va en la sección **"No verificado"** — nunca lo reportes como
hallazgo ni inventes un número. Un informe con 6 hallazgos probados vale más que 20 sospechas.

---

## Fase 0 — Detectar la etapa de entrada

La skill es versátil por etapa. Lo primero es saber en cuál estás, porque cambia qué revisas y qué aplicas.

| Entrada | Cómo la reconoces | Qué revisas | Qué aplicas al final |
|---|---|---|---|
| **BRIEF** | Párrafos de idea, "quiero una app que…", sin pantallas definidas | Que las decisiones que definen la UX estén tomadas | Reescribes el brief con lo que faltaba |
| **SPEC / PRD** | Funciones, fronteras, pantallas, criterios | Que cada pantalla tenga sus estados y su acción principal | Reescribes el spec con las secciones ausentes |
| **PLAN** | Tareas numeradas, fases, archivos a tocar | Que existan tareas para estados, móvil y persistencia | Agregas las tareas que faltan, en su fase |
| **CÓDIGO** | Un repo, o una URL desplegada | Recorrido real en navegador + lectura de código | Editas los archivos |

Si te dan varias cosas a la vez (spec + código), audita el **código** y usa el spec como contrato:
todo lo que el spec promete y el código no cumple es hallazgo automático.

Si no está claro, pregunta una sola cosa: *"¿Reviso el documento o la app construida?"*

---

## Fase 1 — Enmarcar (5 minutos, no se salta)

Antes de juzgar nada, contesta por escrito estas tres. Sin esto, la auditoría juzga la app equivocada.

1. **¿Cuál es el único trabajo de esta app?** Una frase. Si no puedes escribirla, ese ya es el hallazgo #1.
2. **¿Quién la abre y desde dónde?** Casi siempre: una creadora, desde Instagram, en el teléfono.
3. **¿Cuál es la acción principal?** La cosa que si no pasa, la app no sirvió.

Con código, saca esto del README, del `page.tsx` de la raíz y de la navegación. Con documento, del texto.
Si el documento no lo dice, no lo inventes: anótalo como vacío y sigue.

---

## Fase 2 — Recorrido (descubrir)

**Con código:** el recorrido es de verdad, en navegador. Protocolo completo en
`references/recorrido-navegador.md`. Las 8 pruebas son innegociables:

1. **Primera vez** — entra sin datos. ¿Te invita a algo o te deja plantada?
2. **Teléfono real** — viewport 390px. ¿La navegación existe? ¿Se usa con una mano?
3. **Refresco** — llena algo, recarga. ¿Sigue ahí?
4. **Doble toque** — pulsa guardar dos veces rápido. ¿Se duplicó?
5. **Silencio** — pulsa cada botón. ¿La pantalla confirmó que pasó algo?
6. **Vacío falso** — ¿hay pantallas que dicen "no hay nada" mientras el contador dice que sí hay?
7. **Sin permiso** — entra como alguien sin acceso/sin pagar. ¿Entiende qué le pasa y qué hacer?
8. **Compartir** — abre el link público en otra sesión. ¿Se explica sola?

**Con documento:** el mismo recorrido, pero mental y contra el texto. Por cada prueba, busca la frase
del documento que la resuelve. Si no existe frase, es hueco.

Anota todo en crudo mientras recorres. No filtres todavía.

---

## Fase 3 — Rúbrica (cubrir y puntuar)

Pasa las 10 dimensiones de `references/rubrica.md`. Cada una trae sus ítems, la prueba concreta y
el arreglo típico. Mientras la recorres, cruza contra `references/cicatrices-produccion.md`: son los
fallos que ya costaron caro en apps reales del ecosistema F100K, con síntoma → causa → chequeo. Esa parte es la que
convierte esto en un auditor tuyo y no en un checklist genérico de internet.

Las 10 dimensiones:

| # | Dimensión | La pregunta que responde |
|---|---|---|
| 1 | Claridad y un solo trabajo | ¿Se entiende para qué sirve en 5 segundos? |
| 2 | Primer minuto | ¿Alguien llega a "ah, qué útil" en menos de 60s? |
| 3 | Los 4+1 estados | ¿Cada pantalla tiene vacío, cargando, error, con datos y sin permiso? |
| 4 | Feedback honesto | ¿La app nunca calla, y nunca miente? |
| 5 | No pierde el trabajo | ¿Cierro y vuelvo, y todo sigue? |
| 6 | La pantalla no miente | ¿Lo que muestra corresponde a lo que hay? |
| 7 | Móvil de verdad | ¿Se usa con una mano en un teléfono real? |
| 8 | Dashboard 1-3-5 | ¿Un número héroe con contexto, o doce que decoran? |
| 9 | Puertas: acceso y dinero | ¿Entrar, pagar y desbloquear se entiende y no rompe? |
| 10 | Salir al mundo | ¿Tiene link, se comparte y se explica sola? |

**Puntuación.** Cada dimensión vale 10. Suma 0-100 y aplica la banda:

| Puntos | Banda |
|---|---|
| 0-40 | 🔴 Todavía es una idea, no una app |
| 41-70 | 🟡 Funciona, pero se siente a medias |
| 71-90 | 🔵 Lista para mostrar |
| 91-100 | 🟢 Lista para que la usen a diario |

Con brief o spec, la puntuación mide **el documento**, no la app: se puntúa si la decisión está tomada
por escrito. Dilo así en el informe para que nadie confunda un spec de 90 con una app de 90.

---

## Fase 4 — Informe y checkpoint (aquí PARAS)

Formato completo en `references/plantillas-informe.md`. Estructura:

1. **Termómetro** — el número, la banda, y la frase de qué significa.
2. **Los 3 arreglos que más mueven la aguja** — no más de tres. Todo lo demás va después.
3. **Hallazgos por severidad**, cada uno con evidencia:
   - 🔴 **ROMPE** — pierde datos, miente, o no se puede usar en el teléfono. Se arregla antes que nada.
   - 🟡 **CUESTA USO** — fricción, silencio, vacío sin salida. Es lo que hace que no vuelvan.
   - 🔵 **PULIDO** — mejora real pero no bloquea. Si es visual, se pasa a `ux-elevacion-formula100k`.
4. **No verificado** — lo que no pudiste probar y por qué.
5. **Plan de aplicación** — qué archivos (o qué secciones del documento) vas a tocar, en orden.

**Orden de arreglo, siempre el mismo** (del artifact, y coincide con lo que te ha roto apps de verdad):

> **1. No perder el trabajo → 2. La pantalla no miente → 3. Estado vacío → 4. Acción principal →
> 5. Feedback → 6. Móvil → 7. El resto.**

Un detalle visual nunca va antes que un dato que se pierde.

**PARA aquí.** Presenta el informe y el plan, y espera el OK. No edites nada antes.

---

## Fase 5 — Aplicar y verificar

Con el OK, aplica en el orden del plan.

**Si es código:**
- Un cambio por arreglo, cada uno verificable por separado. Nada de una pasada gigante.
- Después de cada arreglo 🔴, **vuelve a correr la prueba del recorrido que lo detectó**. Un arreglo sin
  la prueba re-corrida no está arreglado, está escrito.
- Respeta los patrones de la codebase: lee 2-3 componentes vecinos antes de escribir.
- Si tocas migraciones, créditos o gates, revisa `cicatrices-produccion.md` §Puertas: en apps así esos
  cambios tocan tres lugares a la vez y revientan si tocas solo uno.
- Al final: `tsc` / tests / build según el repo. Reporta el resultado real, aunque falle.

**Si es documento (brief / spec / plan):**
- Reescribe el documento completo con lo que faltaba **integrado en su lugar**, no como apéndice.
- Marca lo agregado para que se pueda revisar de un vistazo.
- En un plan, las tareas nuevas van dentro de la fase que les corresponde, no al final.

**Cierre.** Reporta: qué se aplicó, qué quedó fuera y por qué, y el termómetro re-estimado. Si quedó
algo sin arreglar, dilo explícito — bajar el alcance es decisión de quien pidió la auditoría, no tuya.

---

## Guardarraíles

- **Español neutro** en todo lo que la usuaria vea (textos de la app, del informe, del spec). Nada de voseo.
- **No inventes data.** Ni métricas, ni "el 80% de las apps…", ni un hallazgo que no probaste.
- **No amplíes el alcance.** Auditas UX; si de paso ves un problema de arquitectura, se menciona en una
  línea y sigue. No lo refactorizas.
- **Lo visual se delega.** Si el hallazgo es "se ve genérico / sin jerarquía / sin animación", el arreglo
  es invocar `ux-elevacion-formula100k`, no improvisar CSS aquí.
- **No toques producción sin permiso explícito.** Aplicar arreglos ≠ desplegar. El deploy se pide aparte.
- **Si la app es de una alumna**, el informe se escribe sin jerga: "la pantalla no te dice que se guardó",
  no "falta feedback de estado en el mutation handler". Y cada hallazgo cierra con la frase exacta que
  ella le puede pegar a Claude Code.

## Referencias

- `references/rubrica.md` — las 10 dimensiones con ítems, pruebas y arreglos típicos.
- `references/cicatrices-produccion.md` — fallos reales de la app de guiones, la app de agencia, la plataforma de cursos, la app de retos y la app de escritorio con licencias.
- `references/recorrido-navegador.md` — protocolo del recorrido real con navegador.
- `references/plantillas-informe.md` — formatos de salida por etapa de entrada.
