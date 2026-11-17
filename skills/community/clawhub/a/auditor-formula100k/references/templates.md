# PLANTILLAS DE OUTPUT · AUDITOR F100K

> 3 plantillas embebidas. Usar literalmente sustituyendo los `[placeholders]`.

---

## PLANTILLA A · DOCUMENTO PRINCIPAL

**Ruta:** `entregables/auditorias/[CLIENTE]/[modo]-auditoria-[YYYY-MM-DD].md`

```markdown
# AUDITORÍA [SKOOL | CONTENIDO] · [NOMBRE CLIENTE]
> Realizada por Andrea Vega · F100K · [FECHA]
> Versión: v[N]

---

## 1. RESUMEN EJECUTIVO

- **Score global:** [X] / [60 si Skool, 50 si Contenido]
- **Lectura del score:** [interpretación según rango — madura / funcional / con fugas / inexistente]
- **Modo de matriz actual** (solo Contenido): [Experimentación / Crecimiento / Nutrición / Venta]
- **Modo recomendado** (solo Contenido): [...]

**Top 3 hallazgos críticos:**
1. [hallazgo concreto, 1–2 líneas, con cifra si aplica]
2. [...]
3. [...]

**3 acciones de la semana:**
1. [acción imperativa]
2. [...]
3. [...]

---

## 2. CONTEXTO

**Briefing recibido:**
- Cliente: [nombre]
- Activo auditado: [URL / archivo / perfil]
- Avatar declarado: [párrafo del cliente]
- Oferta actual: [precio + descripción]
- Métricas de partida:
  - [métrica 1]: [valor]
  - [métrica 2]: [valor]
- Hipótesis del cliente: [qué cree que está roto]

---

## 3. MAPEO DEL ESTADO ACTUAL

[Recorrer las 12 (Skool) o 10 (Contenido) dimensiones, una por una]

### Dimensión 1: [Nombre]
**Estado actual:** [descripción objetiva, 2–3 líneas]
**Evidencia:** [cita textual / captura / dato]
**Métricas:** [si aplica]

### Dimensión 2: [Nombre]
[...]

[continuar...]

---

## 4. SCORECARD

| # | Dimensión | Score | Palanca | Acción |
|---|---|---|---|---|
| 1 | [...] | X/5 | Alta/Media/Baja | [resumen acción] |
| 2 | [...] | X/5 | [...] | [...] |
| ... | | | | |

**SCORE GLOBAL:** [X] / [60 o 50]

**Lectura del score:** [rango interpretado]

---

## 5. MATRIZ DE REPOSICIONAMIENTO (solo modo Contenido)

|                    | HOY | META 90 DÍAS |
|---|---|---|
| Avatar | [...] | [...] |
| Pilar 1 | [...] | [...] |
| Pilar 2 | [...] | [...] |
| Pilar 3 | [...] | [...] |
| Modo de matriz | [...] | [...] |
| Plataforma principal | [...] | [...] |
| Voz | [...] | [...] |
| Oferta principal | [...] | [...] |

---

## 6. RECOMENDACIONES PRIORIZADAS

**Matriz Impacto × Esfuerzo:**

```
                  IMPACTO ALTO
                       │
   QUICK WINS          │   PROYECTOS GRANDES
   - Rec #N            │   - Rec #N
   - Rec #N            │   - Rec #N
                       │
ESF. BAJO ─────────────┼───────────── ESF. ALTO
                       │
   MARGINALES          │   (TRAMPAS — descartadas)
   - Rec #N            │
                       │
                  IMPACTO BAJO
```

### RECOMENDACIÓN #1 · [TÍTULO]

- **Cuadrante:** [Quick Win | Proyecto Grande | Marginal]
- **Palanca:** [Alta | Media | Baja]
- **Esfuerzo:** [Bajo (<2h) | Medio (1 sem) | Alto (1 mes+)]

**QUÉ:** [acción concreta en imperativo]

**POR QUÉ:** [vínculo con la brecha y el vehículo único]

**CÓMO:**
1. [paso]
2. [paso]
3. [paso]

**DEPENDENCIA:** [Ninguna / o lo que requiera previamente]

---

### RECOMENDACIÓN #2 · [TÍTULO]
[...]

---

## 7. PLAN 30/60/90

| Plazo | Acciones | Resultado esperado | Responsable |
|---|---|---|---|
| **7 días (Quick Wins)** | [Rec #N, #N, #N — máx 3] | [métrica que se mueve] | [Cliente / tú] |
| **30 días** | [Rec #N — 4 a 6 acciones] | [...] | [...] |
| **90 días** | [Rec #N — 1 a 3 proyectos] | Reposicionamiento [...] | [...] |

---

## 8. SKILLS COMPLEMENTARIAS RECOMENDADAS

Para ejecutar el plan se sugiere invocar:

- `[nombre-skill]` → [para qué]
- `[nombre-skill]` → [para qué]

[Solo listar las que aplican a las brechas reales encontradas]

---

## 9. CIERRE

Estos son los 3 pasos para esta semana. Si solo haces estos 3, el siguiente trimestre se ve diferente.

1. **[Acción 1]** — [una línea de contexto]
2. **[Acción 2]** — [...]
3. **[Acción 3]** — [...]

**Próxima revisión sugerida:** [FECHA + 90 días]

---

*Documento generado el [FECHA] por Andrea Vega · FÓRMULA 100K*
```

---

## PLANTILLA B · SCORECARD CSV

**Ruta:** `entregables/auditorias/[CLIENTE]/scorecard.csv`

### Modo Skool (12 filas)

```csv
Dimension,Score,Palanca,Brecha,Accion
Avatar y nicho,X,Alta/Media/Baja,Resumen brecha 1 linea,Resumen accion 1 linea
Vehiculo unico,X,...,...,...
Promesa y oferta,X,...,...,...
About Page,X,...,...,...
Estructura de modulos,X,...,...,...
Onboarding,X,...,...,...
Foro y categorias,X,...,...,...
Leaderboard y niveles,X,...,...,...
Pinned posts,X,...,...,...
VSL video bienvenida,X,...,...,...
Video de cancelacion,X,...,...,...
Sesiones en vivo,X,...,...,...
SCORE GLOBAL,X/60,,,
```

### Modo Contenido (10 filas)

```csv
Dimension,Score,Palanca,Brecha,Accion
Avatar y nicho,X,Alta/Media/Baja,Resumen brecha,Resumen accion
Pilares de contenido,X,...,...,...
Matriz Viralidad Valor Venta,X,...,...,...
Formatos,X,...,...,...
Calendario y ritmo,X,...,...,...
Voz y tono,X,...,...,...
Sistema de ganchos ENC,X,...,...,...
Conversion a oferta,X,...,...,...
Metricas y aprendizaje,X,...,...,...
Ecosistema y omnicanalidad,X,...,...,...
SCORE GLOBAL,X/50,,,
```

**Notas técnicas:**
- Sin tildes en nombres de columnas/filas (compatibilidad con Excel sin BOM)
- Comas separadoras (no punto y coma)
- Sin comillas en celdas a menos que contengan comas
- Encoding UTF-8

---

## PLANTILLA C · RESUMEN EJECUTIVO

**Ruta:** `entregables/auditorias/[CLIENTE]/resumen-ejecutivo.md`

> Una sola página. Sirve para que el cliente lo comparta con su equipo sin abrir el documento completo.

```markdown
# RESUMEN EJECUTIVO · [CLIENTE]
> Auditoría [Skool | Contenido] · v[N] · [FECHA]

---

## 📊 SCORE GLOBAL

**[X] / [60 o 50]** — [interpretación: madura / funcional / con fugas / inexistente]

---

## 🔴 LOS 3 HALLAZGOS QUE MÁS IMPORTAN

1. **[Hallazgo 1]**
   [1–2 líneas con cifra si aplica]

2. **[Hallazgo 2]**
   [...]

3. **[Hallazgo 3]**
   [...]

---

## ✅ LOS 3 PASOS DE ESTA SEMANA

1. **[Acción 1]**
   [una línea de contexto · responsable · fecha límite si aplica]

2. **[Acción 2]**
   [...]

3. **[Acción 3]**
   [...]

---

## 🛡 LO QUE ESTÁ FUNCIONANDO (proteger)

- [Dimensión con score 4–5 y por qué es activo]
- [...]

---

## 📅 PRÓXIMA REVISIÓN

[FECHA + 90 días]

---

*Andrea Vega · FÓRMULA 100K · [fecha]*
```

---

## REGLAS ANTI-FALLA AL GENERAR LOS 3 ARCHIVOS

1. **Crear la carpeta del cliente antes** de escribir cualquier archivo:
   ```bash
   mkdir -p "entregables/auditorias/[CLIENTE]"
   ```

2. **Nombre del cliente en kebab-case:** `barbara-organiza-y-vende`, `florencia-interview-lab`, `sol-traverso`. Sin espacios, sin tildes, sin mayúsculas.

3. **Fecha en formato ISO:** `2026-05-06`. Nunca `06/05/2026`.

4. **Si el archivo ya existe** (re-auditoría), incrementar versión:
   - `skool-auditoria-2026-05-06.md` (v1)
   - `skool-auditoria-2026-08-06-v2.md` (v2 con fecha posterior)

5. **Encoding UTF-8** para los 3 archivos. Markdown en `.md`, CSV plano en `.csv`.

6. **NUNCA** sobrescribir un archivo de auditoría anterior. Versiones se acumulan, no se reemplazan.
