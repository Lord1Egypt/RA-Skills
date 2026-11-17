---
name: creadora-comunidades-skool
description: "Use when someone asks to create a Skool community, write an About Page for Skool, design an onboarding, write a VSL script, set up community structure, configure foro categories, leaderboard levels, pinned posts, cancellation video, design an irresistible offer for a community, build a vehículo único, or any copy or structure for a Skool community. Also triggers on: \"construye mi Skool\", \"About Page de Skool\", \"onboarding para mi comunidad\", \"VSL de comunidad\", \"estructura de Skool\", \"configura mi Skool\", \"descripción de comunidad\", \"vehículo único\", \"oferta de mi comunidad\", \"diseña mi oferta para Skool\", \"propuesta integral de Skool\", \"propuesta final para cliente Skool\", \"ármame el docx de la propuesta de comunidad\", \"entregable final de Skool\"."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Las preguntas van por Telegram, una tanda a la vez. Lo que ya esté en `cerebro/` (nicho, oferta, historia) confírmalo en vez de preguntarlo.
> - El `.docx` de la propuesta usa `build_docx.py` y necesita `python-docx`. Si no está, entrega la propuesta en `.md` y dilo.
> - `brief.schema.json` es el esqueleto vacío del brief: llénalo con los datos de la clienta real que te den. Los ejemplos de la versión de escritorio no vienen en este paquete.
> - El documento final va a `entregables/` y se manda por Telegram como archivo.

---

## Qué hace esta skill

Combina diseño estratégico, copywriting y construcción de ofertas para crear o completar cualquier pieza de una comunidad en Skool. Cubre todo el ciclo: desde la oferta central (vehículo único) hasta la retención (video de cancelación).

Principio base: una comunidad en Skool necesita un **vehículo único** — una oferta clara que justifica la membresía. Esa oferta debe mostrarse activamente dentro de la comunidad y en el lanzamiento para incentivar la compra.

Siempre trabaja en español, segunda persona (tú), con narrativa emocional, directa, aspiracional y clara. Nunca inventa métricas, precios, urgencias ni autoridad — si falta información, la solicita antes de escribir.

---

## Piezas que puede crear

| # | Pieza | Descripción |
|---|---|---|
| 1 | Vehículo único | Diseño completo de la oferta principal de la comunidad |
| 2 | Descripción corta | ~150 chars, posicionamiento + emojis |
| 3 | About Page | Texto debajo del video, máx. 1000 chars, orientado a conversión |
| 4 | Onboarding completo | 6 bloques estratégicos de activación |
| 5 | Posts fijados | 3 posts: Bienvenida, Reto principal, Reglas/Cultura |
| 6 | VSL | Guion de 8 bloques narrativos |
| 7 | Video de cancelación | Guion de 6 bloques de retención |
| 8 | Leaderboard | Niveles emocionales y progresivos |
| 9 | Categorías del foro | Estructura y nombres de secciones |
| 10 | Módulos / Fases | Títulos y descripciones motivadoras |
| 11 | Estructura completa desde cero | Todas las piezas en orden lógico |
| 12 | **Propuesta Integral Final (.docx)** | Documento consolidado para entregar al cliente — 16 secciones (ver [propuesta-integral.md](propuesta-integral.md)) |

---

## Proceso: Brief Guiado

Siempre seguir este flujo — nunca saltarse pasos:

1. **Si es inicio de conversación:** saludar y preguntar qué pieza necesita
2. **Si hay ambigüedad** (el usuario dice "About", "descripción", "texto de la comunidad"):
   - Preguntar: ¿Te refieres a A) el texto debajo del video del About Page (máx. 1000 chars) o B) la descripción corta (~150 chars)?
   - NO escribir nada hasta recibir confirmación
3. **Brief guiado:** hacer las preguntas de brief correspondientes, una por una (ver sección abajo)
4. **Confirmar:** presentar resumen y preguntar "¿Continúo?" o "¿Cambias algo?"
5. **Generar:** usar la plantilla correspondiente de [templates.md](templates.md)
6. **Ofrecer revisión:** "¿Ajustamos algo?"

---

## Brief por Pieza

### 1. VEHÍCULO ÚNICO (oferta principal)
1. ¿Qué problema urgente y costoso resuelve tu comunidad?
2. ¿Quién es tu cliente ideal? (describe con detalle)
3. ¿Cuál es la transformación principal — cómo está antes y cómo queda después?
4. ¿En cuánto tiempo pueden esperar ver ese resultado?
5. ¿Qué objeciones o miedos tiene tu cliente antes de comprar?
6. ¿Qué incluye la membresía? (sesiones, cursos, plantillas, comunidad, auditorías...)
7. ¿Cuál es el precio? ¿Y el valor total percibido?
8. ¿Tienes bonificaciones activas o quieres diseñarlas?
9. ¿Tienes prueba social o resultados de clientes anteriores para mencionar?
10. ¿Qué tipo de garantía quieres ofrecer?

### 2. DESCRIPCIÓN CORTA
1. ¿Cómo se llama tu comunidad?
2. ¿A quién va dirigida?
3. ¿Cuál es el resultado principal que promete?
4. ¿Tienes algún número o logro real que incluir? (no inventar)

### 3. ABOUT PAGE
1. ¿Cómo se llama tu comunidad?
2. ¿Para quién es y qué resultado principal promete?
3. ¿Cuál es la objeción más común de quien duda en entrar?
4. ¿Tienes número de alumnos, casos reales o tiempo de transformación?
5. ¿Cuántas sesiones en vivo por semana y quién las da?
6. ¿Qué incluye la comunidad? (cursos, plantillas, herramientas, retos, auditorías...)
7. ¿Cuál es el precio actual y el valor percibido?
8. ¿Tienes bonos activos? ¿Cuáles?
9. ¿Hay urgencia real (cupos, fecha límite)?

### 4. ONBOARDING (6 bloques)
1. ¿Cuál es la promesa central en una frase?
2. ¿Cómo se llaman las fases o módulos principales?
3. ¿Qué recursos clave recibe el miembro al entrar?
4. ¿Cuál es el primer desafío de activación? (acción corta y emocional)
5. ¿Tienes video de bienvenida o es solo texto?
6. ¿Cómo se llama el canal o hashtag donde se presentan los miembros?

### 5. POSTS FIJADOS (3 posts)
1. ¿Nombre de la comunidad y tono general?
2. ¿Cuáles son las 3 reglas o valores más importantes de la cultura?
3. ¿Cuál es el reto principal o primer desafío para nuevos miembros?
4. ¿Hay alguna frase, lema o mantra de la comunidad?

### 6. VSL (8 bloques)
1. ¿Cómo se llama la comunidad y quién la lidera?
2. ¿Cuál es el estado actual (dolor) de quien entra?
3. ¿Qué intentan normalmente que no funciona?
4. ¿Cómo se llama tu método o sistema y cuál es su lógica simple?
5. ¿Qué estados mentales o cambios vive el miembro dentro?
6. ¿Tienes 2-3 casos de transformación reales?
7. ¿Cuál es el CTA final?

### 7. VIDEO DE CANCELACIÓN (6 bloques)
1. ¿Cómo se llama la comunidad?
2. ¿Cuál suele ser la razón por la que alguien quiere cancelar?
3. ¿Hay una alternativa antes de cancelar? (pausa, módulo clave, semana ligera)
4. ¿A quién pueden escribir para reactivarse?

### 8. LEADERBOARD
1. ¿Cuántos niveles quieres? (recomendado: 5-8)
2. ¿Cuál es el tema o universo de tu comunidad?
3. ¿Nombres en español, inglés o combinados?

### 9. CATEGORÍAS DE FORO
1. ¿Qué tipo de interacciones quieres fomentar? (preguntas, logros, feedback, networking...)
2. ¿Tienes sesiones en vivo? ¿Canal de anuncios?
3. ¿Hay retos o entregas que necesiten sección propia?

### 11. ESTRUCTURA COMPLETA DESDE CERO
Seguir este orden y confirmar con el usuario antes de pasar a cada pieza:
**Vehículo único → Descripción → About Page → Onboarding → Posts Fijados → Leaderboard → Categorías Foro → VSL → Video Cancelación**

### 12. PROPUESTA INTEGRAL FINAL (.docx)
Este es el **formato de entrega final** para clientes (Skool premium: Truelany, Adriana, Barbara, Ana Romero, Florencia, Felipe, Sol, Aaron Khaleb, etc.). NO se entrega como chat ni como pieza suelta — se entrega como UN documento .docx con las 16 secciones consolidadas.

Brief consolidado (preguntar lo que falte, NO inventar):
1. Nombre de la fundadora + identidad (historia personal, autoridad real, libros/TEDx/medios, portafolio o credenciales)
2. Nombre tentativo de la comunidad + tagline
3. Avatar específico (edad, profesión, ingresos, dolores verbatim)
4. Insight estratégico (la tesis: "el mercado vende X, nosotros vendemos Y")
5. Top 5-7 competidores con plataforma + promesa + debilidad
6. Vehículo único propio (framework, leyes, reglas, fases — todo lo registrable)
7. Promesa central + transformación Estado A → Estado B en X meses
8. Módulos (M0 a M6 o equivalente) con objetivo, temas, resultado y entregable de la miembro
9. Lista de videos pregrabados (código, título, duración, formato TH/SC/MX/MC, hook, promesa, estructura)
10. Dinámicas exclusivas (accountability, hot seats, investment club, deal flow, etc.)
11. Ritmo semanal (lunes-domingo + mensual/trimestral/anual)
12. Categorías del foro (propósito, quién publica, tipo de post)
13. Leaderboard + retos por módulo + recompensas
14. Estética visual (paleta hex, tipografías, sí/no fotográfico, metáfora visual)
15. Propuestas de portada (prompt base IA + specs + concepto por módulo)
16. Roadmap de grabación por meses

Ver estructura detallada en [propuesta-integral.md](propuesta-integral.md).

**Flujo de generación automática (end-to-end):**

1. Recolectar el brief completo en conversación (sección por sección, una pregunta a la vez, NO formularios).
2. Confirmar con la usuaria que está todo bien antes de generar.
3. Volcar el brief consolidado a un archivo `brief.json` siguiendo el esqueleto de [`brief.schema.json`](brief.schema.json) (vacío a propósito — usarlo como referencia de estructura).
4. Ejecutar:
   ```bash
   python3 skills/creadora-comunidades-skool/build_docx.py /ruta/a/brief.json
   ```
5. El script aplica automáticamente todas las reglas de formato del memory `feedback-docx-formato`:
   - Sin tabla de contenidos.
   - Texto justificado en todo el documento (incluido dentro de celdas).
   - Bordes solo en tablas reales (single, sz=6, color `#4B5563`). Nunca `pBdr` ni `shd` en párrafos sueltos.
   - Sin bullets decorativos (●, o, •). Solo listas numeradas 1, 2, 3.
   - Sin emojis decorativos en el cuerpo (excepción intencional: el copy de posts fijados de Skool en sección 13 SÍ los conserva porque va a publicarse dentro de Skool).
   - Párrafos vacíos consecutivos colapsados.

**Output por defecto:** `entregables/<CLIENTE> - Propuesta Skool FINAL.docx`. Para forzar otra ruta: `--out /ruta/custom.docx`.

**Dependencias:** `python-docx` y `emoji` (ya instaladas en el entorno del usuario). Si una alumna corre la skill y faltan, instalar con `pip install python-docx emoji`.

**Notas de uso:**
- El schema de `brief.json` lleva 16 claves principales (`cliente`, `tagline`, `subtitle`, `s1_resumen`, `s2_brief`, ..., `s16_roadmap`). Cualquier sección omitida no aparece en el .docx — útil para entregas parciales.
- Si el cliente entrega su propio brand kit (paleta, tipografías, logos), respetarlo en `s14_estetica` — no imponer el azul/dorado del ejemplo.
- El brief mínimo viable debe tener al menos: `cliente`, `s1_resumen`, `s2_brief`, `s4_identidad`, `s5_vehiculo`, `s5b_oferta`, `s6_modulos`. Si faltan piezas, devolver una pregunta concreta antes de generar.

---

## Reglas Globales

- **NUNCA inventar** métricas, precios, número de alumnos, urgencias, plazos ni autoridad. Si falta, preguntar.
- **Siempre en español neutro**, segunda persona (tú), narrativa Skool: emocional, directa, aspiracional, clara. Nunca jerga argentina (vos/tenés/copiá/acá).
- **Siempre confirmar** el tipo de pieza antes de escribir cuando hay ambigüedad
- **Una pregunta a la vez** — nunca lanzar formularios
- **Confirmar antes de generar** — presentar resumen, esperar "Sí, continúa"
- **Nunca descuentos** — siempre apilar bonificaciones para mantener valor percibido
- **Nunca presentar bonos antes del precio** — siempre después
- **Siempre garantía** — en ofertas premium, mínimo 2 tipos combinados
- **Ofrecer ajuste** después de entregar
- **Formato de entrega final:** cuando el cliente contrata el armado completo de su Skool, el entregable NO es chat ni piezas sueltas — es un .docx integral con las 16 secciones de [propuesta-integral.md](propuesta-integral.md) aplicando las reglas del memory `feedback-docx-formato` (sin TOC, justificado, bordes solo en tablas, sin emojis decorativos, sin bullets `●`).

---

## Referencia de Plantillas

- [templates.md](templates.md) — plantillas exactas por pieza (1-11).
- [propuesta-integral.md](propuesta-integral.md) — estructura completa de las 16 secciones del .docx final que se entrega al cliente (pieza 12).
