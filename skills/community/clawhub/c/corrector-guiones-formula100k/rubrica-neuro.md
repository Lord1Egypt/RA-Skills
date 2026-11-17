# Rúbrica Neuro — destilada de tribe v2 (Higgsfield virality_predictor)

> **Qué es esto:** el modelo `tribe v2` (`brain_activity`) de Higgsfield predice la viralidad de un
> video real leyendo la "actividad cerebral" estimada del espectador. Aquí destilamos su razonamiento
> en **6 reglas aplicables sobre el TEXTO de un guion**, para predecir y arreglar ANTES de grabar.
>
> ⚠️ Esto es una **predicción heurística sobre texto**, no la medición real. La medición real (correr
> tribe v2 sobre el video grabado) vive en la skill `remix-viral-formula100k` (`medicion-tribe-v2.md`).
> Usan el mismo vocabulario a propósito: lo que predices al escribir se lee igual que lo que mides al grabar.

## Las 5 regiones que mide tribe v2 (para traducir su lenguaje)
- **Visual (occipital)** — interés por lo que se VE. Premia novedad visual temprana.
- **Auditivo / Temporal** — la VOZ / narración. Suele ser el ancla que más sostiene.
- **Lenguaje (frontotemporal)** — qué tan seguible es lo que se dice.
- **Frontoparietal / Atención** — control atencional (si el arranque "agarra" o no).
- **Default Mode (DMN)** — divagación mental. **Mejor BAJO.** Alto = mente dispersa, no enganchada.

Scores clave que devuelve: `viral_potential/overall`, `hook_score` (ventana 0-3s),
`brain_engagement`, `peak_second` (cuándo llega el pico) y `sustain`.

---

## Las 6 reglas neuro (aplícalas en orden sobre el guion)

### Regla 1 — Hook 0-3s manda
- **Origen tribe v2:** `hook_score` + Atención mínima en s1.
- **Qué revisa:** que el arranque dispare **resultado concreto o pattern-interrupt en s0-2**, no una
  frase-categoría de relleno ("un truco que nadie conoce", "te voy a contar algo").
- **Veredicto:** ALTO = resultado/imagen impactante en la primera frase · MEDIO = promesa pero genérica
  · BAJO = relleno/categoría antes de los 2s.
- **Reescritura:** abre con el payoff o la prueba. Patrón: *"[resultado deseado] … mira:"* y corta.

### Regla 2 — Pico temprano, no tardío
- **Origen tribe v2:** `peak_second`. Pico al final = mal (la gente ya se fue antes de llegar).
- **Qué revisa:** que el "wow" (mejor dato, mejor demo, giro) esté en el **primer tercio**, no guardado al final.
- **Veredicto:** ALTO = wow en s0-5 · MEDIO = a la mitad · BAJO = recién al final / en el CTA.
- **Reescritura:** front-load. Mueve el mejor momento al inicio; deja el detalle para después.

### Regla 3 — Anti-Default-Mode (mata la divagación)
- **Origen tribe v2:** `DMN` alto (lower-better) = mente dispersa.
- **Qué revisa:** que el estímulo **cambie cada 2-3s** (giro, número, nuevo visual, corte, cambio de tono).
  Listas largas y planas, monólogo sin cambios → DMN sube.
- **Veredicto:** ALTO = cambios frecuentes y variados · MEDIO = algunos tramos planos · BAJO = monótono.
- **Reescritura:** trocea bloques largos; intercala un dato/visual/giro cada par de segundos.

### Regla 4 — Visual temprano
- **Origen tribe v2:** Córtex visual (suele picar ~s5 cuando aparece lo visual; cae si no hay nada nuevo).
- **Qué revisa:** si hay demo/pantalla/objeto/resultado, que **aparezca antes de s2**, no a media pieza.
- **Veredicto:** ALTO = visual fuerte en s0-2 · MEDIO = aparece a mitad · BAJO = puro talking-head sin visual.
- **Reescritura:** marca en el guion el B-roll/demo en el segundo 0-2 (no solo al explicar).

### Regla 5 — Voz = ancla
- **Origen tribe v2:** Auditivo/Temporal (suele ser la región más alta; sostiene aunque lo visual falle).
- **Qué revisa:** narración **clara, densa y con ritmo**; sin muletillas ni frases vacías que bajen energía.
- **Veredicto:** ALTO = cada frase aporta y fluye · MEDIO = algún relleno · BAJO = divagante/plano.
- **Reescritura:** corta muletillas, junta ideas, sube densidad por segundo. Lee en voz alta para validar ritmo.

### Regla 6 — Sin valle en s1-2
- **Origen tribe v2:** caída de la curva global justo tras el gancho (zona de scroll).
- **Qué revisa:** que NO haya relleno/saludo/contexto lento inmediatamente después del gancho.
- **Veredicto:** ALTO = del gancho salta directo al valor · MEDIO = un respiro corto · BAJO = "hola, hoy les traigo…".
- **Reescritura:** elimina el puente lento; encadena gancho → primera prueba/valor sin pausa.

---

## Salida del Chequeo Neuro (formato sugerido)
```
🧠 Chequeo Neuro (predicho)
- Hook 0-3s: ALTO/MEDIO/BAJO — [por qué]
- Pico estimado: temprano / medio / tardío
- Riesgo mente-dispersa (DMN): bajo / medio / alto
- Visual temprano: sí / no   · Voz/ritmo: ok / flojo   · Valle s1-2: no / sí
➜ Arranque ajustado: "[reescritura de los primeros 2-3s]"
```

---

## Tabla síntoma → regla → variable (puente con REMIX VIRAL)
Conecta los hallazgos neuro con las 7 variables del Mapa en T de `remix-viral-formula100k`:

| Síntoma (predicho o medido) | Regla neuro | Variable T a atacar |
|---|---|---|
| Hook bajo / atención mínima en s1 | R1, R6 | **Gancho** (visual/verbal/textual) |
| Pico tardío / DMN alto a la mitad | R2, R3 | **Estructura / Ritmo** |
| Visual aparece tarde o cae tras s5 | R4 | **Edición / B-roll** (recursos-de-video) |
| Llega al final pero sin "wow" guardable | R2 | **Ángulo / valor** |
| Voz plana / sin densidad | R5 | **Ritmo y edición** |
| Buen recorrido pero sin acción al final | — | **CTA** |
