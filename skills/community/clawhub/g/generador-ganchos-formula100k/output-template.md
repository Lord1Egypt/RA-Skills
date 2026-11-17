# Template del Reporte LAB

Usa este formato EXACTO para entregar el reporte de LAB. Sustituye los `[placeholders]`. No te saltes secciones — si no aplica, escribe "N/A" pero mantén la estructura.

El reporte se entrega DOS veces:
1. **Resumen en chat** (versión condensada — bloque al final del mensaje)
2. **Archivo completo** guardado en `ideas/lab-ganchos/YYYY-MM-DD_<slug>/LAB.md` (versión completa abajo)

---

## VERSIÓN COMPLETA (para `LAB.md`)

```markdown
# 🧪 LAB DE GANCHOS · FÓRMULA 100K

**Fecha:** [YYYY-MM-DD]
**Tema:** [resumen del video en 1 línea]
**Promesa central:** [qué resuelve / qué descubrimiento promete el video]
**Avatar:** [a quién va dirigido]
**Modo:** [Guion existente / Referencia viral]
**Variantes testeadas:** [N]

---

## 🏆 GANADORA · Variante [N]

**Score ponderado:** [XX.X / 100] · **Banda:** [TOP / Viable / Mediocre / Reconstruir]

### Forma Visual
- **Forma asignada:** [F1 / F2 / F3 / F4 / F5]
- **Estructura de copy:** [A Curiosidad / B Dolor / C Resultado / D Susurro]
- **Molde de gancho:** [nº y nombre del banco de 15 · elegido por ajuste al tema, no por rendimiento]

### Composición visual del primer cuadro
- **Sujeto principal:** [descripción + gesto + expresión]
- **Posición:** [centro / regla de tercios izq / der / etc.]
- **Fondo:** [descripción + paleta]
- **Elementos secundarios:** [enumerar máx 2]
- **Texto en pantalla:** "[texto exacto]"
- **Tipografía y tamaño:** [fuente · tamaño % del frame]
- **Luz:** [tipo de iluminación]

### Gancho textual final
> "[TEXTO DEL GANCHO]"

**Justificación:** [por qué este texto · qué gatillos activa · qué loop abre]

### Métricas del Virality Predictor
| Indicador | Valor | Banda |
|-----------|-------|-------|
| Hook Strength | [XX] | [Alto / Medio / Bajo] |
| Creative Performance | [XX] | [..] |
| Retention Risk | [XX] | [..] |
| Engagement | [XX] | [..] |
| Attention | [XX] | [..] |
| Audience Response | [XX] | [..] |

🔗 **Dashboard:** [URL de Higgsfield]

---

## 🎬 BRIEF DE PRODUCCIÓN · Cómo grabar la ganadora

### Setup
- **Encuadre:** [plano medio / plano americano / primer plano]
- **Cámara:** [vertical 9:16] · [altura sugerida]
- **Distancia:** [cuántos metros / cm del sujeto]
- **Luz:** [ringlight / luz natural ventana / dramática]
- **Fondo real recomendado:** [pared blanca / oficina / exterior]

### Acción del primer segundo
1. [Acción 1 — qué hace el sujeto en frame 1]
2. [Acción 2 — qué hace al medio segundo]
3. [Acción 3 — dónde termina al segundo 1]

### Texto en pantalla
- **Cuándo aparece:** [desde frame 1 / aparece al 0.3s / fade in al 0.5s]
- **Posición:** [arriba / centro / inferior]
- **Animación:** [estático / pop-in / typewriter / slide-from-side]
- **Color:** [hex] sobre [hex]
- **Fuente:** [Inter Bold / Poppins Bold / etc.]

### Audio (si aplica)
- **Tono de voz:** [enérgico / íntimo / serio / sorprendido]
- **Primera palabra:** "[palabra]"
- **Volumen de fondo:** [silencio / música baja / sonido ambiente]

### Edición post
- **Overlay scrapbook:** [SÍ / NO] · [si SÍ: estilo crema con washi tape, caja blanca de énfasis al centro]
- **Subtítulos:** [word-level abajo, fuente Inter Bold blanca sobre caja semi-transparente]
- **Watermark:** @tuhandle en esquina inferior izquierda (zona segura)

---

## 📊 COMPARATIVA DE TODAS LAS VARIANTES

| # | Forma | Estructura | Molde | Gancho textual | Score | Banda |
|---|-------|-----------|-------|----------------|-------|-------|
| 1 | F[X] | [A/B/C/D] | [nº] | "[texto]" | [XX.X] | [banda] |
| 2 | F[X] | [A/B/C/D] | [nº] | "[texto]" | [XX.X] | [banda] |
| 3 | F[X] | [A/B/C/D] | [nº] | "[texto]" | [XX.X] | [banda] |

### Detalle por variante

#### Variante 1 · F[X] + [Estructura]
- **Gancho:** "[texto]"
- **Composición:** [resumen 1 línea]
- **Hipótesis:** [por qué pensábamos que podía ganar]
- **Métricas:** Hook [XX] · Creative [XX] · Retention Risk [XX] · Engagement [XX] · Attention [XX]
- **Score ponderado:** [XX.X]
- **Dashboard:** [URL]
- **Lectura:** [1-2 frases · qué funcionó, qué no]

#### Variante 2 · F[X] + [Estructura]
[mismo formato]

#### Variante 3 · F[X] + [Estructura]
[mismo formato]

---

## 🔍 ANÁLISIS DEL RANKING

[Párrafo 3-5 líneas explicando POR QUÉ ganó la ganadora vs las otras. ¿Fue por Hook Strength bruto? ¿Por mejor retención? ¿Por el ángulo de promesa elegido? Sé honesto: si la diferencia es marginal (<5 pts), dilo.]

### Insights cruzados
- [Observación 1 sobre patrones que se ven al comparar variantes]
- [Observación 2 — ej: las variantes con texto en zona alta ganaron, o las con F4 fallaron retención]
- [Observación 3 si aplica]

---

## 📋 SIGUIENTE PASO

Una sola acción concreta a ejecutar HOY:

> **[Ej: "Graba la variante ganadora con el setup descrito en el brief. Cuando tengas el .mp4 final, pásalo por evaluador-ganchos-formula100k para validar score real vs predicción."]**

---

## 📦 ARTEFACTOS GUARDADOS

Carpeta: `ideas/lab-ganchos/[YYYY-MM-DD_slug]/`

- `LAB.md` — este reporte
- `variant-1.png` ... `variant-N.png` — imágenes generadas (Nanobanana)
- `variant-1.mp4` ... `variant-N.mp4` — clips de test (Seedance)
- `predictor-jobs.json` — mapping variante → job_id del Predictor

### `predictor-jobs.json` contenido

```json
{
  "lab_date": "[YYYY-MM-DD]",
  "topic": "[tema]",
  "variants": [
    {
      "id": 1,
      "form": "F[X]",
      "copy_structure": "[A/B/C/D]",
      "hook_text": "[texto]",
      "image_job_id": "[uuid Nanobanana]",
      "video_job_id": "[uuid Seedance]",
      "predictor_job_id": "[uuid Virality Predictor]",
      "dashboard_url": "[URL]",
      "scores": {
        "hook_strength": [XX],
        "creative_performance": [XX],
        "retention_risk": [XX],
        "engagement": [XX],
        "attention": [XX],
        "audience_response": [XX],
        "final_weighted": [XX.X]
      },
      "is_winner": [true/false]
    }
  ]
}
```
```

---

## VERSIÓN CONDENSADA (para el chat)

Al final del mensaje en el chat, entrega este bloque corto:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧪 LAB DE GANCHOS · GANADORA

⚡ Variante [N] · Score [XX.X]/100 · [Banda]

📐 Forma: F[X] + [Estructura de copy]
✍️ Gancho: "[TEXTO]"
🎯 Composición clave: [1 frase]

📊 Ranking completo:
  1. V[N]: [score] ← ganadora
  2. V[N]: [score]
  3. V[N]: [score]

🔗 Dashboards:
  · V1: [URL]
  · V2: [URL]
  · V3: [URL]

📦 Archivos: /FORMULA100K/LAB-GANCHOS/[YYYY-MM-DD_slug]/

🚀 Siguiente paso: graba la ganadora con el brief de LAB.md.
   Cuando tengas el .mp4, pásalo por evaluador-ganchos-formula100k.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Notas sobre el tono del reporte

- **Veredicto del Predictor manda.** Si la variante ganadora es la que "personalmente menos te gusta", entrégala igual. El usuario decide al final.
- **Honesto en márgenes pequeños.** Si la ganadora gana por <3 pts, dilo: "ranking ajustado, las 2-3 son viables, recomendamos la #1 por desempate de Hook Strength puro".
- **Específico en el brief.** Cada instrucción de cámara, gesto, texto, luz debe ser implementable en la grabación de hoy.
- **Español neutro** — usa "tú", "tienes", "puedes", "haz" — NUNCA "vos", "tenés", "podés", "hacé".
- **NO pongas emojis dentro del gancho textual final**, salvo que la Forma Visual lo justifique.

## Adaptaciones por banda del ganador

**Score 85-100 (TOP):**
- Entrega clara, ganadora con margen. Brief de producción detallado.
- No re-correr lab. Grabar y publicar.

**Score 70-84 (Viable):**
- Entrega ganadora con 1-2 ajustes sugeridos en el brief (ej: cambiar palabra del gancho, mover texto 5% arriba).
- Recomendar correr `evaluador-ganchos-formula100k` post-grabación.

**Score 50-69 (Mediocre):**
- Entrega ganadora del lab PERO advierte: "ninguna variante alcanzó banda viable".
- Sugerir revisar la promesa del guion antes de grabar.
- Ofrecer correr un segundo lab con variantes nuevas que partan de un ángulo de promesa diferente.

**Score <50 (Reconstruir):**
- NO entregar "ganadora". Mensaje claro:
> "Las N variantes cayeron en banda débil. El problema no es el gancho — es el ángulo del guion. Sugiero replantear la promesa central antes de re-correr el lab."
- No grabar nada todavía.
