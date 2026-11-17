---
name: calendarizador-historias-formula100k
description: "Arma calendarios SEMANALES de SECUENCIAS DE HISTORIAS de Instagram (Lunes-Domingo) con la metodología FÓRMULA 100K. Activar SIEMPRE que el usuario pida 'calendariza mis historias', 'arma mi semana de stories', 'calendario de historias', 'planifica mis historias de la semana', 'organiza mis stories por día', 'calendario semanal de historias', 'arma 7 secuencias de stories para la semana', 'planifica las historias de mi lanzamiento', o cualquier variación que combine organizar/planear con el formato historias de IG semanal. NO confundir con calendarizador-contenido-formula100k (reels/videos/carruseles) ni calendarizador-urgencias-formula100k. Distribuye las secuencias por día según energía y propósito, lista para producir con guionizacion-historias-formula100k."
argument-hint: "<modo: lanzamiento|nutricion|mixto|urgencia> [+ ideas/objetivos opcionales]"
metadata: {"version": "1.0.0", "depends-on": ["guionizacion-historias-formula100k"], "openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Guarda el calendario en `guiones/historias/calendarios/` y los guiones en `guiones/historias/`.
> - El paso a imágenes (`historias-a-imagenes-nanobanana`) gasta créditos: ofrécelo con costo estimado y espera ✅.
> - El modo (lanzamiento, nutrición, mixto, urgencia) pregúntalo por Telegram con opciones numeradas si no vino en el pedido.

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

# Skill: Calendarizador de Historias FÓRMULA 100K

Arma un calendario semanal Lunes-Domingo con N secuencias de historias por día,
desarrollando cada secuencia completa internamente con `guionizacion-historias-formula100k`.

---

## ⚠️ ANTES DE EMPEZAR — LEE ESTOS REFERENCIALES

1. `references/distribuciones-semanales.md` — los 4 modos de calendario y su distribución por día
2. `references/orquestacion.md` — cómo coordinar las llamadas a la Skill A

Y también los referenciales de la Skill A (categorías, estructuras, formatos, CTAs) si vas a desarrollar guiones.

---

## QUÉ HACE

Toma las ideas/objetivos del usuario para la semana + un MODO de calendario, y entrega:

1. **Tabla maestra** Lun-Dom con cada secuencia asignada a un día y franja horaria
2. **N archivos .md individuales** (uno por secuencia, generados por Skill A)
3. **Archivo maestro .md** con toda la planificación y enlaces a los guiones individuales
4. **Archivo maestro .xlsx** con la misma info para el usuario/equipo

---

## INPUT

El usuario da alguna combinación de:

1. **Modo del calendario** (uno de los 4):
   - `lanzamiento` → semana de venta dura
   - `nutricion` → semana de calentamiento, lead magnets, autoridad
   - `mixto` → balance estándar (default)
   - `urgencia` → últimos 2-3 días de un lanzamiento

2. **Lote de ideas/objetivos** (opcional, una idea = una secuencia):
   ```
   - "vender el GPT del primer segundo"
   - "caso de éxito de Brenda"
   - "anunciar el banco de historias"
   - "interactuar para validar nuevo producto"
   - ...
   ```

3. **Cantidad de secuencias por día** (opcional, default = 1)
   - 1 → una secuencia/día (recomendado para no saturar)
   - 2 → dos secuencias/día (semanas intensivas)

4. **Fecha de inicio** (opcional, default = lunes próximo)

5. **Oferta principal a vender en la semana** (opcional)

Si el usuario NO da ideas, la skill las **genera ella misma** basándose en el modo + oferta:
- Lanzamiento → ideas tipo: caso de éxito, urgencia, prueba social, demo
- Nutrición → ideas tipo: educación, lead magnet, encuestas, lifestyle
- Etc.

---

## FLUJO DE 5 PASOS

### Paso 1 — Determinar la distribución del calendario

Lee `references/distribuciones-semanales.md`. Aplicar el modo elegido:

#### Modo "MIXTO" (default, balance estándar)
| Día | Categoría | Notas |
|---|---|---|
| Lunes | 📊 Encuestas | Activar audiencia |
| Martes | 💛 Libre / Educación | Mostrar autoridad sin vender |
| Miércoles | 💥 One-Shot | Reactivar vistas |
| Jueves | 🎁 Lead Magnet | Día top de conversión |
| Viernes | 💥 One-Shot o caso | Validación |
| Sábado | 💛 Libre | Humanización |
| Domingo | 🔥 Urgencia suave | Reflexión + CTA |

#### Modo "LANZAMIENTO"
| Día | Categoría |
|---|---|
| Lunes | 📊 Encuestas (calentar) |
| Martes | 💥 One-Shot (announcement) |
| Miércoles | 🎁 Lead Magnet (capturar leads) |
| Jueves | 💥 One-Shot caso (prueba social) |
| Viernes | 🔥 Urgencia (subida de precio) |
| Sábado | 🎁 Lead Magnet (segunda oportunidad) |
| Domingo | 🔥 Urgencia máxima (cierre) |

#### Modo "NUTRICIÓN"
| Día | Categoría |
|---|---|
| Lunes | 📊 Encuestas |
| Martes | 💛 Libre / Educación |
| Miércoles | 💛 Storytelling personal |
| Jueves | 🎁 Lead Magnet suave |
| Viernes | 💥 Caso/educación |
| Sábado | 💛 Libre |
| Domingo | 💛 Reflexión |

#### Modo "URGENCIA" (cierre de carrito, 2-3 días)
| Día | Categoría |
|---|---|
| Día 1 | 🔥 Urgencia suave + 🎁 Lead Magnet |
| Día 2 | 🔥 Urgencia media + 💥 Caso |
| Día 3 (cierre) | 🔥 Urgencia máxima (3-4 secuencias el mismo día) |

### Paso 2 — Asignar ideas a slots

Si el usuario dio ideas, asignarlas al slot que mejor encaje:
- Caso de éxito → slot de One-Shot o Lead Magnet
- Lanzamiento de producto → slot de One-Shot (announcement)
- Regalo gratis → slot de Lead Magnet (idealmente jueves)
- Etc.

Si SOBRAN slots sin ideas → la skill **genera ideas complementarias** acordes a la categoría asignada.

Si SOBRAN ideas → distribuirlas en una segunda semana (proponer al usuario).

### Paso 3 — Desarrollar cada secuencia con Skill A

Para cada slot del calendario:

1. Construir el prompt para Skill A:
   ```
   Categoría: [la del slot]
   Idea: [la idea asignada]
   Oferta a vender: [si aplica]
   Día/hora: [del calendario]
   Contexto: [resto del calendario para coherencia narrativa entre días]
   ```

2. Invocar `guionizacion-historias-formula100k` con ese prompt.

3. Recibir el .md generado y validar que tenga el bloque ⚙️.

4. Guardar el filename retornado para el calendario maestro.

### Paso 4 — Construir tabla maestra

Crear el archivo de calendario en MD y XLSX.

**Columnas del calendario maestro:**

| Día | Hora | Categoría | Estructura | Idea | Palabra clave CTA | Slides | Ruta del guion |
|---|---|---|---|---|---|---|---|
| Lunes | 10am | 📊 Encuestas | #11 Si haces X | Validar interés en GPT | YO | 4 | ./guiones/2026-05-06_encuestas_validar-gpt.md |
| Lunes | 6pm | 💛 Libre | #18 Diario Personal | Cierre del día | DIARIO | 3 | ./guiones/2026-05-06_libre_cierre-dia.md |
| Martes | 10am | ... | ... | ... | ... | ... | ... |

**Hora sugerida** según el patrón del usuario:
- 10am: primera secuencia del día (audience matutina)
- 1pm: secuencia de lunch break
- 6pm: prime time evening (la más fuerte)
- 9pm: cierre del día (storytelling reflexivo)

### Paso 5 — Generar outputs

#### Output 1: Calendario maestro .md

Ruta:
```
guiones/historias/calendarios/calendario-historias_[modo]_[YYYY-MM-DD].md
```

Estructura del archivo:

```markdown
---
modo: [lanzamiento|nutricion|mixto|urgencia]
fecha_inicio: 2026-05-06
fecha_fin: 2026-05-12
oferta_principal: [si aplica]
total_secuencias: 7
total_slides: 28
---

# Calendario Semanal de Historias — [Modo]

> Semana del [Lunes] al [Domingo]
> [Frase resumen del foco de la semana]

## 📅 Tabla maestra

| Día | Hora | Categoría | Estructura | Idea | CTA | Slides | Guion |
|---|---|---|---|---|---|---|---|
| Lunes | ... | ... | ... | ... | ... | ... | [📄](./guiones/...) |
| ... | ... | ... | ... | ... | ... | ... | ... |

## 🎯 Foco de la semana

[Resumen narrativo de cómo se conectan las secuencias entre sí: qué se calienta, qué se vende cuándo, qué bonus se dan]

## 📦 Producción consolidada

**Sesiones de grabación recomendadas:**
- Sesión A — [escenario]: graba clips para [secuencia 1, secuencia 3, secuencia 5]
- Sesión B — [escenario]: graba clips para [secuencia 2, secuencia 4]
- Sesión C — captura: prepara [dashboard X, mockup Y, screenshots Z]

**Total clips a grabar:** [N]
**Total fotos a tomar:** [N]
**Total mockups a crear:** [N]

## 📋 Guiones individuales

1. [Lunes 10am — Validar interés en GPT](./guiones/2026-05-06_encuestas_validar-gpt.md)
2. [Lunes 6pm — Cierre del día](./guiones/2026-05-06_libre_cierre-dia.md)
3. [Martes 10am — ...](./guiones/...)
...
```

#### Output 2: Calendario maestro .xlsx

Mismo contenido, en Excel para que el usuario lo comparta con su equipo.

Para generar XLSX: usa `openpyxl` o `pandas.DataFrame.to_excel`. Si no están disponibles, generar como CSV y avisar.

#### Output 3: Carpeta con todos los guiones individuales

Cada guion ya está guardado por la Skill A en:
```
guiones/historias/
```

Listar al usuario los nombres de archivos generados.

#### Output 4: Resumen al usuario

Mostrar en chat:

```
✅ Calendario generado.

📅 [Modo]: [N] secuencias en [N] días
📂 Calendario maestro: <ruta>
📄 Guiones individuales: [N] archivos en /HISTORIAS/guiones/
📊 Excel: <ruta>

🎬 Producción consolidada:
- [N] clips para grabar
- [N] capturas a preparar
- [N] mockups a crear

🚀 Próximo paso sugerido:
- ¿Quieres que pase TODOS estos guiones a imágenes con `historias-a-imagenes-nanobanana`?
- ¿O prefieres primero revisar y ajustar algún guion?
```

---

## ⚠️ ESPAÑOL NEUTRO OBLIGATORIO

El calendario maestro y el resumen al usuario deben estar en **español neutro**, NO argentino.
Tampoco uses voseo cuando construyas el prompt para Skill A (ej. "desarróllame este guion" en vez de "desarrollame").

Reemplazos: vos→tú, tenés→tienes, podés→puedes, querés→quieres, copiá→copia, escribí→escribe,
acá→aquí, laburo→trabajo, plata→dinero.

---

## NO HACER

- No desarrollar los guiones tú directamente — siempre usar `guionizacion-historias-formula100k` para coherencia.
- No mezclar este calendario con `calendarizador-contenido-formula100k` (son tablas distintas).
- No proponer más de 2 secuencias por día (el usuario satura a su audiencia si excede esto).
- No olvidar la sesión de **producción consolidada** — El usuario necesita saber cuántas sesiones de grabación tiene que hacer.
- No saltar el paso 5.4 (resumen al usuario).
- **No usar voseo ni argentinismos** en ningún output escrito (calendario, resumen, prompts a Skill A).
