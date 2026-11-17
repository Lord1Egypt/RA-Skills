---
name: fabrica-design-md
description: "Use when someone asks to build a brand design system file, extract their visual identity, or create a DESIGN.md. Dispara con \"hazme mi DESIGN.md\", \"arma mi sistema visual\", \"extrae mi identidad de marca\", \"quiero que todo lo que haga con IA se vea mío\", \"mis diseños salen genéricos\", \"define mi paleta y mi tipografía\", \"crea el archivo de marca\", \"design system para mi negocio\". EXTRAE el sistema de las piezas que ya le funcionan a la persona (capturas, código de su web, o entrevista si no tiene archivos) en vez de inventarlo o copiar el de otra marca. Mide el contraste en vez de estimarlo, entrega el DESIGN.md y una página de prueba con el sistema aplicado y medida en móvil. NO usar para diseñar una pieza suelta ni para auditar accesibilidad de una página ya hecha."
argument-hint: "[carpeta con capturas | ruta del repo | vacío para entrevista]"
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Las capturas de sus 9 piezas que mejor funcionaron te las manda por Telegram **como archivo** (así no pierden color); guárdalas en `cerebro/design/piezas/`. Nunca las saques entrando logueada a Instagram.
> - Si tiene web pública, el código lo lees con el navegador del agente o bajando su HTML/CSS: el `grep` de hex por frecuencia funciona igual sobre esos archivos. Si su repo es privado, pídele un `.zip`.
> - `python3 references/contraste.py` corre tal cual en el servidor. Nunca escribas un ratio que no salió del script.
> - `references/medir.mjs` necesita Playwright; no instales su Chromium sin ✅. Si no está, mide con el navegador del agente: abre `prueba.html` con viewport de 1280×900 y de 390×844 (emulación de viewport, no `--window-size`: headless por debajo de 500 px recorta y da desbordes falsos), corre en consola el mismo chequeo de desborde y `opacity:0` del script y toma las dos capturas.
> - `DESIGN.md`, `prueba.html` y las capturas van a `entregables/design/` y se mandan por Telegram. Copia además el `DESIGN.md` a `cerebro/DESIGN.md` para que las demás skills lo usen.

---

## Qué hace esta skill

Produce un `DESIGN.md`: un archivo de texto que la persona le entrega a cualquier IA
para que todo lo que construya salga con su identidad, sin repetírsela cada vez.

**El principio, y no es negociable: se EXTRAE, no se inventa ni se copia.**
El sistema visual de alguien que ya publica ya existe — está repartido en sus piezas.
El trabajo no es diseñarlo, es escribirlo. Un archivo copiado de otra marca produce
piezas fieles… a esa otra marca.

---

## Antes de empezar: ancla el rubro

Pregunta en una sola línea, y espera respuesta:

> «¿De qué es tu negocio y a quién le vendes?»

Todo lo que venga después —los ejemplos que uses, cómo nombres las cosas, qué
superficies asumas— se escribe en el mundo de esa persona. Si vende pastelería, los
ejemplos son de pastelería. Nunca uses ejemplos de otro rubro ni de otra marca.

---

## Paso 0 · Detecta con qué se puede trabajar

Mira qué hay antes de preguntar de más. En orden de precisión:

| Fuente | Cómo detectarla | Precisión |
|---|---|---|
| **Código** de su web o landing | `$1` es un repo, o la persona menciona uno | La más alta |
| **Capturas** de sus piezas | `$1` es una carpeta con imágenes | Alta |
| **Entrevista** | No hay ni lo uno ni lo otro | Suficiente |

Si hay código Y capturas, usa las dos: el código da los valores exactos, las capturas
dan la firma y el ritmo. Si no hay nada, no bloquees a nadie — ve a la entrevista.

---

## Paso 1 · Junta las piezas que SÍ funcionaron

Pide explícitamente:

> «Pásame tus 9 piezas que mejor funcionaron. No las que más te gustan — **las que la
> gente más guardó y compartió.** Si tienes menos, con 5 arrancamos.»

Insiste en esa distinción. Es el paso donde casi todo el mundo entrega lo que le
gustaría ser en vez de lo que ya le funciona, y el archivo entero se tuerce ahí.

Si la persona no tiene todavía piezas con datos, dilo claro: este no es su paso.
Primero publica, después extrae. En ese caso, haz la entrevista y márcale el archivo
como **provisional** en el campo `sources`.

---

## Paso 2 · Saca los colores por FRECUENCIA

**Si hay código:** cuenta el uso real, no leas el archivo de tema — casi siempre es
el arranque de una plantilla y no dice la verdad de la marca.

```bash
# hex más usados en los componentes
grep -rhoE '#[0-9a-fA-F]{6}\b' <rutas> | tr 'A-F' 'a-f' | sort | uniq -c | sort -rn | head -20
# clases de color de utilidad, si usa un framework de utilidades
grep -rhoE '\b(bg|text|border)-[a-z]+-[0-9]{2,3}' <rutas> | sort | uniq -c | sort -rn | head -20
```

**Si hay capturas:** míralas y anota los colores que se repitan entre piezas.

En los dos casos, la regla es la misma: **lo que aparece en 7 de 9 es la marca; lo que
aparece una vez, no entra.** Ordena el resultado en tres grupos y solo tres:

- **Lienzo** — el fondo y una o dos variantes para cajas
- **Tinta** — titular, cuerpo, secundario
- **Acento** — **uno solo**. Si salen dos, pregunta cuál manda; el otro es ruido

---

## Paso 3 · Encuentra la firma

La firma es lo que se repite sin que la persona se dé cuenta y hace que una pieza se
reconozca de lejos. **Casi nunca es el color** — un color lo copia cualquiera en dos
minutos. Suele estar en:

- una mezcla tipográfica (dos familias conviviendo en la misma frase)
- un encuadre o una composición que repite
- un gesto: un subrayado, un marco, un tipo de recorte, una manera de tratar la prueba

La prueba para saber si la encontraste:

> **Si le quito el logo, ¿por qué se sigue notando que es de esta persona?**

Si la respuesta es «por el color», sigue buscando. Escríbela como una orden ejecutable,
no como un adjetivo. «Se siente premium» no sirve. «Titular en peso 800 con interletrado
negativo, partido con serif itálica en la misma frase» sí sirve.

---

## Paso 4 · Escribe las REGLAS DE USO

Es el paso que casi todo el mundo se salta y el que separa un sistema de una lista.

Una lista dice *qué* colores hay. Un sistema dice **cuándo** cada cosa tiene derecho a
aparecer. Sin eso, la IA usa el acento en todo y el resultado sale con cara de plantilla.

Por cada elemento del sistema escribe: dónde SÍ va, y dónde NUNCA va.

Escribe también el bloque `prohibido`. Es tan útil como lo permitido, porque la IA
vuelve sola a sus manías: degradado morado, héroe centrado sobre malla oscura, tres
tarjetas iguales en fila, todo centrado, sombras en vez de bordes.

---

## Paso 5 · MIDE el contraste. No lo estimes.

Obligatorio. Aquí se caen los sistemas bonitos: un color puede ser precioso y ser
ilegible, y eso no se ve mirando — se ve midiendo.

```bash
python3 <ruta-de-esta-skill>/references/contraste.py "<lienzo>" "<tinta>" "<tinta-secundaria>" "<acento>"
```

Interpretación:

- **4.5** es el mínimo para texto normal; **3.0** para texto grande o negrita
- El color que suele fallar es la **tinta secundaria**. Si no pasa, súbela y anota el
  piso nuevo en `rules.contraste`
- Un acento puede fallar como texto y funcionar perfecto **como relleno** con texto
  oscuro encima. El script lo dice. Ese matiz va escrito en el archivo, o la IA lo va
  a usar mal

Nunca escribas un ratio que no salió del script.

---

## Paso 6 · Documenta la excepción

Casi toda marca tiene dos superficies: una para **vender** y otra para **enseñar** o
para la herramienta. Suelen no verse igual, y está bien que no se vean igual.

Pregunta: «¿tienes algún sitio donde tu marca se vea distinta a propósito?». Si lo hay,
escríbelo con su razón funcional (no estética), y la regla de no mezclarlas en una misma
página. Si de verdad no existe, borra el bloque en vez de inventarlo.

---

## Paso 7 · Escribe el archivo

Usa `references/plantilla-design-md.md`. Guarda en la raíz del proyecto de la persona,
o donde te indique, como `DESIGN.md`.

**Si un valor no salió de una pieza real, no entra.** Nada de rellenar campos para que
se vea completo. Un archivo corto y verdadero vale más que uno largo e inventado.
Los campos sin datos se dejan fuera, no se adivinan.

---

## Paso 8 · Constrúyele la prueba viva y MÍDELA

Un `DESIGN.md` que nadie ha visto aplicado es una hipótesis. Ciérrala:

1. Construye una página de muestra de un solo archivo `prueba.html` siguiendo el
   `DESIGN.md` al pie de la letra. Contenido **real de la persona** (su oferta, sus
   palabras), nunca relleno de mentira ni testimonios inventados.
2. Mídela:

```bash
node <ruta-de-esta-skill>/references/medir.mjs <ruta>/prueba.html <carpeta-salida>
```

3. **Abre las capturas y míralas.** Pasar la medición no prueba que se vea bien —
   solo prueba que no está rota. Este paso no se salta.
4. Si algo se ve mal, el error suele estar en el `DESIGN.md`, no en la página.
   Corrige el archivo y vuelve a construir.

Si `web-design-guidelines` está instalada, pásale la página de prueba antes de entregar.

---

## Qué entregar

```
DESIGN.md                  ← el archivo, en la raíz del proyecto
prueba.html                ← la página de muestra con el sistema aplicado
prueba_escritorio.png      ← capturas medidas
prueba_movil.png
```

Y en el mensaje final, en prosa corta:

- La **firma** en una frase — es lo que más le va a servir saber
- Los ratios que se midieron, sobre todo cualquiera que haya obligado a cambiar un color
- Cómo se usa: «arrastra el `DESIGN.md` a la conversación y di: *sigue estrictamente el
  DESIGN.md, sobre todo el bloque de reglas*». Funciona en cualquier asistente de código
- Los dos límites, sin adornarlos:
  - gobierna **cómo se ve**, no **si funciona**
  - es descriptivo: nadie verifica que se cumpla, por eso conviene una revisión aparte

---

## Lo que esta skill NO hace

- **No inventa** una identidad. Si no hay piezas ni respuestas, no hay archivo:
  se hace la entrevista y se marca como provisional.
- **No copia** el sistema de otra marca. Los sistemas publicados de empresas conocidas
  sirven para robarles la **estructura** del archivo y el vocabulario — nunca los valores.
- **No arregla** una página rota. Para accesibilidad y errores de código va una
  auditoría aparte.
- **No estima** contrastes. Si no salió del script, no se escribe.
- **No diseña** una pieza suelta. Esto produce el sistema, no el entregable.

## Notas

- Toda ruta, color, fuente y nombre sale de la persona que está usando la skill.
  No traigas valores por defecto de ninguna marca.
- Si la persona pide directamente «cópiame el sistema de <marca conocida>», explícale
  en una frase por qué eso le va a dar la cara de esa marca, ofrécele la extracción, y
  si aun así lo pide, hazlo — pero déjalo escrito en `sources`.
- Herramientas necesarias: `python3` para el contraste (viene en macOS y Linux) y
  Playwright para la medición (`npx playwright install chromium`). Si Playwright no
  está disponible, entrega igual el `DESIGN.md` y la `prueba.html`, y dilo claro:
  la página quedó sin medir.
