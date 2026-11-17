# Criterios de Generación · LAB de Ganchos FÓRMULA 100K

Reglas para diversificar N variantes de gancho de modo que el Virality Predictor pueda comparar hipótesis genuinamente distintas (no variaciones cosméticas del mismo concepto).

---

## 1. REGLA MAESTRA · Diversificación obligatoria

Cuando generes N variantes (2-4), cada una DEBE diferir de las otras en AL MENOS dos de estas tres dimensiones:

1. **Forma Visual** (F1-F5)
2. **Estructura de copy** (Curiosidad / Dolor / Resultado / Susurro)
3. **Ángulo de promesa** (qué subpromesa del guion se pone delante)

Si dos variantes solo cambian palabras del texto manteniendo Forma + ángulo iguales → es A/B de texto, no es lab de hipótesis. Re-diseña.

---

## 2. COMBINACIONES RECOMENDADAS por número de variantes

### 2 variantes
- **Variante 1:** F1 (sujeto+texto) + Curiosidad
- **Variante 2:** F4 (imagen viral/simbólica) + Dolor

> Combinación clásica "explicativa vs. impactante". Cubre la mayoría de hipótesis sin saturar.

### 3 variantes (default recomendado)
- **Variante 1:** F1 (sujeto+texto) + Curiosidad — la "segura"
- **Variante 2:** F4 (imagen viral/simbólica) + Dolor — la "rompedora"
- **Variante 3:** F2 (acción simbólica) + Susurro — la "íntima"

> Cubre 3 ejes muy distintos. Ideal para descubrir cuál pega con esta audiencia.

### 4 variantes (deep test)
- **Variante 1:** F1 + Curiosidad
- **Variante 2:** F4 + Dolor
- **Variante 3:** F2 + Susurro
- **Variante 4:** F3 (título dominante) + Resultado

> 4 hipótesis máximas. No agregues una 5ta sin razón fuerte — los rendimientos diminishen.

### Reglas de override
- Si la promesa del guion es **transformación personal con métricas** → siempre incluir F3+Resultado.
- Si la promesa es **revelación / secreto / contracorriente** → siempre incluir F2+Susurro o F1+Susurro.
- Si la promesa es **shock / contraste extremo** → siempre incluir F4+Dolor o F4+Curiosidad.

---

## 3. COMPOSICIÓN VISUAL · Especificación obligatoria por variante

Cada variante debe especificar la composición visual con este nivel de detalle (es el prompt que se pasa a Nanobanana):

### Estructura del prompt para Nanobanana

```
[FORMA]: F1/F2/F3/F4/F5
[SUJETO]: [persona/objeto/escena] · [gesto/acción] · [expresión]
[POSICIÓN]: [centro / regla de tercios izq/der / superior / inferior]
[FONDO]: [limpio / contextual / sorpresivo] · [paleta dominante]
[ELEMENTOS SECUNDARIOS]: [máx 2 — flecha, prop, rótulo, número grande, post-it]
[TEXTO EN PANTALLA]: "[texto exacto del gancho]" · [posición] · [tamaño 7-12% del frame] · [tipografía]
[ESTILO]: Instagram reel first frame, 9:16, high contrast, [paleta]
[LUZ]: [natural diurna / ringlight / dramática / suave]
```

### Reglas duras de composición

- **Carga cognitiva ≤ 3 elementos principales en pantalla.** Si el conteo es 4+, simplificar.
- **Texto ≤ 8 palabras.** Si no cabe, dividir en dos líneas o reducir.
- **Contraste alto entre texto y fondo.** Negro sobre crema, blanco sobre azul oscuro, amarillo sobre negro.
- **Zona segura:** texto a mínimo 8% de los bordes verticales (evita corte por UI de IG).
- **Tipografías:** una de [Inter Bold, Poppins Bold, Helvetica Neue Bold, Caveat para acentos manuscritos]. NO Arial. NO Times. NO Comic Sans (jamás).
- **Paletas permitidas:**
  - Crema/beige + negro + acento amarillo (estilo F100K)
  - Negro puro + blanco + acento rojo o amarillo
  - Azul oscuro + blanco + acento naranja
  - Verde oscuro + crema + acento dorado
- **NO usar paletas de baja saturación o pasteles tipo "wellness" salvo que el nicho lo pida.**

---

## 4. GANCHO TEXTUAL · Estructuras de copy

### A — Curiosidad (Loop abierto)
- "Lo que nadie te dijo de [X]"
- "El error que cometí con [X]"
- "Esto cambió mi forma de [verbo]"
- "Si hicieras [X] como yo, [resultado]"

**Cuándo usar:** cuando la promesa es revelar información oculta o contraintuitiva.

### B — Dolor (Punto de fricción)
- "Por qué tu [X] no funciona"
- "Si te pasa [X], esto es por qué"
- "Deja de [verbo] — no funciona"
- "[X] sin [Y] es perder el tiempo"

**Cuándo usar:** cuando la audiencia ya intentó algo y falló; conectas con su frustración.

### C — Resultado (Antes/después)
- "Cómo pasé de [A] a [B] en [tiempo]"
- "[Métrica] en [tiempo corto] haciendo solo esto"
- "Esto me sacó de [estado] a [estado]"

**Cuándo usar:** cuando hay una transformación con números o tiempo concreto que demostrar.

### D — Susurro (Confidencial / paréntesis)
- "Hazlo así (nadie habla de esto)"
- "El truco de [X] (lo aprendí cuando [evento])"
- "Si supieras esto antes de [X]..."

**Cuándo usar:** cuando el contenido es íntimo, contracultural o "secret weapon" en el nicho.

### Reglas de copy
- **NO usar clickbait vacío:** evita "no creerás lo que pasó", "espera a ver esto". Aplica solo si el resto del video lo respalda.
- **Verbos en presente o imperativo**, no en infinitivo. "Haz" no "hacer". "Pasé" no "pasar".
- **Sin signos de exclamación dobles** (!!). Como máximo uno.
- **Sin emojis en el gancho** salvo que sean parte de la Forma Visual (ej: flecha → como prop).

---

## 5. PROMPT TEMPLATE para Seedance (animación 3-4s)

Una vez la imagen base está generada, se anima con Seedance. Plantilla:

```
Animate this first frame as the opening of an Instagram reel.

Duration: 3 seconds.
Movement: [uno de los siguientes según la Forma]
  - F1: subject performs the gesture described, micro-zoom-in 5%, natural lighting
  - F2: hands complete the action (pour/cut/touch), camera stays still
  - F3: text remains static, subject in background shifts slightly, subtle parallax
  - F4: subject of impact moves into final position, slight camera dolly
  - F5: rapid disruptive movement: object enters from edge, hard cut, jolt
Camera: locked or very subtle handheld feel
Style: matches first frame exactly, no style drift
Text overlay: must remain readable and in same position throughout
Aspect: 9:16
```

### Reglas duras de animación
- **NO transiciones extravagantes.** El Predictor mide pacing real de reel, no demo reel de VFX.
- **El texto en pantalla debe estar legible los 3 segundos.** Si la animación lo tapa o lo deforma, simplificar.
- **El sujeto principal NO debe cambiar de identidad** entre frame 1 y frame 90 (60fps × 1.5s). Seedance puede driftear; vigilarlo.

---

## 6. SCORING PONDERADO del Predictor

**Motor real del Virality Predictor de Higgsfield:** modelo `brain_activity`. Devuelve scores agregados + activación de 5 regiones cerebrales por frame. Validado en el primer LAB real (2026-05-15, tema "tokens Claude") — el Default Mode resultó ser el mejor discriminador entre variantes.

### Métricas reales que devuelve el predictor

**Scores agregados** (escala 0-100):
- `hook_score` — fuerza del hook en ventana 0-3s
- `overall_score` — score agregado tipo "creative performance"
- `viral_potential` — potencial viral predicho
- `brain_engagement` — engagement neural agregado
- `sustain` — retención; **atención: satura a 100 en clips ≤4s** (poco discriminante en clips cortos)

**Regiones cerebrales** (cada una con `mean_score`, `peak_score`, `values_by_frame` — escala 0-1, multiplicar × 100):
- `visual_occipital` — procesamiento visual
- `auditory_temporal` — preparación auditiva (anticipación de voz)
- `language_frontotemporal` — redes de lectura/lenguaje
- `frontoparietal_attention` — atención sostenida
- `default_mode` — **lower better**. Default Mode alto = cerebro divagando = malo.

### Tabla de pesos del score ponderado

| Métrica | Peso | Justificación |
|---------|------|---------------|
| `hook_score` | 30% | Score directo del modelo en ventana 0-3s. Los AI clips lo subestiman ~10-15 pts vs grabación real con rostro/charisma reales. |
| `overall_score` | 20% | Score agregado del modelo, proxy de creative performance. |
| `default_mode` invertido | 15% | **MÁS IMPORTANTE EN PRÁCTICA.** DMN alto = cerebro idle = malo. Invertir: `100 - default_mode.mean_score × 100`. |
| `brain_engagement` | 12% | Engagement neural — proxy de likes/comentarios/shares. |
| `sustain` | 10% | Retención. Pesarlo más (15-20%) en clips de 8-10s donde sí discrimina. |
| `frontoparietal_attention` | 8% | Atención sostenida (mean × 100). |
| `language_frontotemporal` | 5% | Activación de redes de lectura del texto en pantalla (mean × 100). |

### Fórmula
```
score_final = (hook_score × 0.30)
            + (overall_score × 0.20)
            + ((100 - default_mode.mean_score × 100) × 0.15)
            + (brain_engagement × 0.12)
            + (sustain × 0.10)
            + (frontoparietal_attention.mean_score × 100 × 0.08)
            + (language_frontotemporal.mean_score × 100 × 0.05)
```

Todos los valores en escala 0-100 antes de aplicar pesos.

### Insight clave heredado del primer LAB real

> En el test "tokens Claude" (2026-05-15), la diferencia entre V1 ganadora (61.8) y V2 perdedora (52.3) se explicó casi enteramente por **Default Mode**: V1 = 48.7 (cerebro enfocado), V2 = 60.7 (cerebro divagando). Hook_score absoluto fue bajo en ambas (43 vs 33) porque la mujer AI no replica charisma real — esperar lift de 10-15 pts al grabar con el usuario. Conclusión: **mira siempre la curva del DMN antes de declarar ganador.**

### Bandas de calidad del score_final

| Score | Banda | Recomendación |
|-------|-------|---------------|
| 85-100 | TOP — graba esta YA | Variante ganadora con margen claro |
| 70-84 | Viable | Graba pero anota ajustes menores del template |
| 50-69 | Mediocre | Si TODAS las variantes caen aquí, re-diseña el guion antes de re-correr el lab |
| <50 | Reconstruir | El concepto base no funciona; cuestiona la promesa del video |

---

## 7. DESEMPATES y CASOS BORDE

- **Empate ≤3 pts entre top 2:** gana la que tenga mejor `hook_score` puro. Es el indicador más confiable del modelo en ventana 0-3s.
- **Empate ≤3 pts con hook_score igual:** gana la que tenga **Default Mode más bajo**. Es el mejor desempate de profundidad.
- **Una variante con `hook_score` altísimo pero `sustain` bajo o DMN alto:** bajarla un puesto. El hook engancha pero el cerebro se cae.
- **Todas las variantes ≤ 50:** no entregues "ganadora" — entrega un mensaje claro: "Las N variantes caen en banda débil. Sugiero revisar la promesa del guion antes de grabar." Recomienda reescribir y volver a correr el lab.
- **Variante con score muy disperso entre métricas** (ej: hook_score 90, brain_engagement 30): anótalo en el reporte. Puede ser un hook que engancha pero no genera comentarios — útil para crecimiento, no para venta.
- **`sustain` = 100 en todas las variantes:** estás en clip ≤4s donde el indicador satura. Considera regenerar clips a 8-10s para discriminar retención real.

---

## 8. DIVERSIDAD VS OVERFITTING al Predictor

El Virality Predictor es un modelo. Hay que evitar dos sesgos:

1. **No re-correr con variantes parecidas hasta sacar score alto.** Si una variante saca 60, no tunees 3 versiones de ella hasta que saque 80. El modelo se puede engañar; el algoritmo de IG/TikTok no.
2. **No descartar Formas Visuales solo porque históricamente sacan menos.** A veces F2 con un tema concreto rompe el patrón. Mantén la diversificación obligatoria del paso 1.

---

## 9. CHECKLIST FINAL antes de entregar el reporte

- [ ] N variantes generadas con Formas Visuales distintas
- [ ] Cada variante tiene composición visual detallada
- [ ] Cada variante tiene gancho textual ≤ 8 palabras
- [ ] Cada variante tiene estructura de copy identificada (A/B/C/D)
- [ ] Cada variante tiene 3-5 gatillos justificados
- [ ] N clips generados con Nanobanana + Seedance
- [ ] N llamadas al Virality Predictor completadas (o N-1 con disclaimer)
- [ ] Score ponderado calculado para cada variante usando los pesos reales del modelo `brain_activity` (sección 6)
- [ ] Curva de Default Mode revisada por variante (debe ser <50 idealmente, alarma si >55)
- [ ] Ranking con tie-breakers aplicados
- [ ] Brief de producción de la ganadora listo para grabar
- [ ] Carpeta `/FORMULA100K/LAB-GANCHOS/YYYY-MM-DD_tema/` con todos los artefactos
- [ ] LAB.md guardado siguiendo `output-template.md`
- [ ] Links a dashboards de Higgsfield incluidos
