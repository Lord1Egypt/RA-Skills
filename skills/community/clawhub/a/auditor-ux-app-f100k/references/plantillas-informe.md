# Plantillas de salida

Una plantilla por etapa de entrada. Todas en español neutro. Si la auditoría es para una alumna, quita la
jerga y deja la frase-para-pegar de cada hallazgo.

---

## A · Informe de auditoría (entrada = código)

```markdown
# Auditoría de UX — <nombre de la app>
<fecha> · Entrada: código (<rama o URL>) · Recorrido: sí, navegador real

## Termómetro: <n>/100 — <banda>
<Una frase de qué significa esa banda para esta app.>

| Dimensión | Puntos | |
|---|---|---|
| 1. Claridad y un solo trabajo | 8/10 | |
| 2. Primer minuto | 4/10 | 🔴 |
| ... | | |
| **Total** | **<n>/100** | |

## Los 3 arreglos que más mueven la aguja
1. **<Título>** — <una línea de qué cambia para quien usa la app.>
2. **<Título>** — <...>
3. **<Título>** — <...>

## Hallazgos

### 🔴 ROMPE — se arregla antes que nada
**H1 · <Título en lenguaje de usuaria>**
- **Qué pasa:** <lo que ve la persona.>
- **Evidencia:** `archivo.tsx:120` · captura `p3-refresco.png`
- **Causa:** <técnica, una o dos líneas.>
- **Arreglo:** <qué se cambia.>
- **Cicatriz relacionada:** C4 (mismo patrón que la plataforma de cursos) ← solo si aplica de verdad

### 🟡 CUESTA USO
**H4 · <...>** (mismo formato)

### 🔵 PULIDO
**H7 · <...>** — si es visual: *"se pasa a `ux-elevacion-formula100k`"*.

## No verificado
- <Qué no se pudo probar y por qué.> — sin esto, el informe pretende una cobertura que no tuvo.

## Plan de aplicación
| # | Arreglo | Archivos | Prueba que lo verifica |
|---|---|---|---|
| 1 | H1 | `x.tsx`, `y.ts` | P3 · Refresco |
| 2 | H2 | `z.tsx` | P2 · 390px |

**¿Aplico este plan?**
```

**Orden obligatorio del plan:** no perder el trabajo → la pantalla no miente → estado vacío → acción
principal → feedback → móvil → el resto.

---

## B · Reescritura de un BRIEF

El brief es corto por naturaleza. No lo conviertas en un PRD: complétalo con lo que **define la UX** y nada más.

Lo que un brief debe tener antes de pasar a spec:

```markdown
# <Nombre de la app>

**Para quién:** <...>
**Problema:** <...>
**Qué hace:** <en una frase.>

**El único trabajo:** <la cosa que si no pasa, la app no sirvió.>
**Acción principal:** <el botón que manda.>
**Dispositivo principal:** <dónde se va a usar de verdad. Casi siempre: teléfono.>

**Funciones (v1):** <lista corta. Si no se puede construir en un día, sobra algo.>
**NO todavía:** <lo que queda fuera a propósito. Esta lista protege el lanzamiento.>

**Primer minuto:** <qué ve alguien que abre por primera vez, sin registrarse.>
**Datos de muestra:** <los 2-3 ejemplos que vienen precargados.>
**Persistencia:** <dónde se guarda y qué pasa al refrescar.>
```

Marca lo agregado con `<!-- agregado por la auditoría -->` para que se revise de un vistazo.

---

## C · Reescritura de un SPEC / PRD

El spec se audita pantalla por pantalla. La tabla de estados es lo que casi siempre falta, y es lo que evita
que la app nazca sin el 80% de su comportamiento.

Por **cada pantalla**, el spec debe traer:

```markdown
### Pantalla: <nombre>
**Para qué existe:** <una frase.>
**Acción principal:** <una sola.>
**Acciones secundarias:** <en gris / menú.>

| Estado | Qué se ve |
|---|---|
| Con datos | ... |
| Vacío | frase del para qué + botón de la acción principal + 1 ejemplo |
| Cargando | esqueleto con la altura real de las filas |
| Error | qué pasó + qué puede hacer, en español, sin jerga |
| Sin permiso | por qué está bloqueada + siguiente paso |

**En teléfono (390px):** <qué se apila, qué se esconde, dónde vive la navegación.>
**Qué confirma cada acción:** <el texto exacto de la confirmación.>
```

Y una sección global:

```markdown
## Puertas
- Formas de entrar: <cada una>. Todas llevan a los mismos datos porque <...>.
- Qué ve alguien sin acceso: <...>
- Si hay pago: qué desbloquea, y qué pasa si el cobro falla después de entregar el resultado.
```

---

## D · Tareas que faltan en un PLAN

Las tareas nuevas van **dentro de la fase que les corresponde**, nunca en un apéndice al final —
si van al final, se cortan cuando el tiempo aprieta, que es justo cuando más se necesitan.

Tareas que un plan de app casi nunca trae y casi siempre necesita:

- [ ] Estados vacíos de cada pantalla (frase + acción + ejemplo), con datos de muestra al primer arranque.
- [ ] Esqueletos de carga con la altura real del contenido.
- [ ] Mensajes de error en español, uno por causa, sin jerga.
- [ ] Estado "sin permiso / sin pagar" con su siguiente paso.
- [ ] Persistencia y prueba de refresco.
- [ ] Guardar que reemplaza en vez de duplicar (y forma de borrar).
- [ ] Botones deshabilitados mientras procesan.
- [ ] Paso de móvil a 390px con la navegación abierta y verificada.
- [ ] Verificación de que cada contador coincide con su lista.
- [ ] Recorrido completo de una identidad sin acceso.
- [ ] Prueba de humo antes de publicar: abrir el link en una ventana privada, en el teléfono.

---

## E · Formato para alumna (sin jerga)

Cuando la app es de una alumna, el informe cambia de forma. Sin tabla de puntos por dimensión: el termómetro,
tres cosas que arreglar, y **la frase exacta que le pega a Claude Code**.

```markdown
## Tu app: <n>/100 — <banda>
<Qué significa, en una frase.>

### 1. <Lo que le pasa a quien la abre>
**Lo que vi:** al refrescar la página, lo que habías escrito desapareció.
**Por qué importa:** una app que olvida no se usa dos veces.
**Pégale esto a Claude Code:**
> Guarda todo automáticamente en el navegador para que al cerrar y volver mis datos sigan ahí. Sin login.

### 2. <...>
### 3. <...>

**Lo demás puede esperar.** Estas tres son las que cambian si vuelven a abrirla o no.
```

Las frases-para-pegar salen de la columna "pedir" de cada rasgo en `rubrica.md`: están escritas para que
funcionen tal cual, sin que la alumna tenga que traducir nada.
