---
name: "academic-paper-writer"
description: "Guided academic paper writing: IMRaD section drafting, citation lookup from Zotero, iterative revision."
---

# jenni-mode — Asistente de escritura académica (a demanda)

Activa este skill cuando Juan Antonio quiera ayuda para redactar, completar o mejorar secciones de un paper científico o revisión sistemática — especialmente con integración de citas desde Zotero.

**Trigger explícito:** `/jenni`, "modo jenni", "ayúdame a escribir el paper", "escribe la introducción/métodos/resultados/discusión".

---

## Fase 0 — Contexto inicial (si no fue dado)

Antes de escribir, recopila lo mínimo necesario. Pregunta en un solo mensaje:

1. **¿Qué sección necesitas?** Introduction / Methods / Results / Discussion / Abstract / otro
2. **¿Cuál es la pregunta de investigación o hipótesis?** (PICO si aplica)
3. **¿Tienes notas, outline o texto previo?** (pégalo o describe)
4. **¿Target journal o estilo?** (APA, Vancouver, ICMJE, otro — default: Vancouver)
5. **¿Idioma?** (default: español médico formal)

Si Juan Antonio ya dio contexto suficiente, omite las preguntas ya respondidas y procede.

---

## Fase 1 — Búsqueda de referencias

### 1a. Consultar Zotero local

```bash
python3 /home/juan/.openclaw/workspace-jd/scripts/zotero_helper.py search "<términos clave>" --limit 10
```

Si `zotero_helper.py search` no existe, usa la API Zotero directamente:

```bash
curl -s "https://api.zotero.org/users/<USER_ID>/items?q=<query>&limit=10&format=json" \
  -H "Zotero-API-Key: <KEY>"
```

Prioriza artículos de las colecciones relevantes al tema (ERC, AKI, Glomerulopatias, etc.).

### 1b. Complementar con PubMed si Zotero no alcanza

Usa el skill `pubmed` o `literature-review` para buscar 3-5 referencias adicionales de alta calidad (guideline, meta-análisis, RCT) relevantes a la sección y el tema.

Registra para cada referencia:
- Título, autores, año, revista, PMID/DOI, URL directa
- Por qué es relevante para esta sección

---

## Fase 2 — Borrador de sección

### Plantillas por sección

#### Introduction
1. Párrafo 1: Contexto epidemiológico y relevancia clínica (con cita de prevalencia/incidencia)
2. Párrafo 2: Problema específico que aborda el estudio (gap en la evidencia)
3. Párrafo 3: Objetivo del estudio (una oración clara: "El objetivo de este estudio fue...")
4. *No incluir resultados ni métodos aquí.*

#### Methods
1. Diseño de estudio (tipo, centro, período, aprobación ética)
2. Población (criterios de inclusión/exclusión)
3. Variables principales y desenlaces (primarios y secundarios)
4. Análisis estadístico (software, tests, nivel de significancia)
5. *Usa tiempos verbales en pasado. Sin interpretación.*

#### Results
1. Descripción de la muestra (tabla 1 si existe)
2. Desenlace primario con valores exactos (n, %, IC95%, p)
3. Desenlaces secundarios
4. *Solo datos, sin interpretación. Remitir a tablas/figuras cuando corresponda.*

#### Discussion
1. Resumen del hallazgo principal (1 párrafo)
2. Comparación con literatura previa (2-3 estudios clave con cita)
3. Mecanismos explicativos plausibles
4. Limitaciones del estudio
5. Implicancias clínicas y/o para investigación futura
6. Conclusión

#### Abstract
Usa estructura IMRAD comprimida: Contexto (1-2 oraciones) → Objetivo → Métodos (diseño, n, período) → Resultados principales → Conclusión. Max 250 palabras, estilo journal target.

---

## Fase 3 — Integración de citas

- Insertar citas en formato Vancouver (números superíndice) o APA según lo indicado.
- Al final del borrador, lista las referencias en el formato solicitado con DOI/URL.
- Si Juan Antonio usa Zotero, ofrecer guardar referencias nuevas:

```bash
python3 /home/juan/.openclaw/workspace-jd/scripts/zotero_helper.py add-doi <DOI> --collection <tema>
```

---

## Fase 4 — Iteración

Después del borrador, preguntar:
- "¿Ajusto el tono, extensión o énfasis de algún párrafo?"
- "¿Agrego o cambio referencias?"
- "¿Paso a la siguiente sección?"

Mantener el contexto del paper completo en la sesión para coherencia entre secciones.

---

## Reglas de calidad

- **No inventar citas.** Si no hay referencia verificada, decirlo explícitamente.
- **No exagerar hallazgos.** Distinguir evidencia que cambia práctica de señal preliminar.
- **Lenguaje clínico preciso.** Evitar eufemismos, jerga informal y frases vacías ("es importante destacar que...").
- **Aplicar `anti-ai-writing-patterns`** en todo texto producido.
- **Citar fuentes con URL directa** cuando sea posible (PubMed, DOI, journal).
- Para claims estadísticos o epidemiológicos, verificar con fuente primaria antes de incluir.

---

## Notas de implementación

- Este skill es exclusivo de JD (`workspace-jd`). No instalar en otros bots.
- Complementa (no reemplaza) el skill `escritura-medica-clinica` — úsalo junto a él.
- Si el paper es de nefrología, activar también `nefrologia-clinica` para razonamiento clínico de dominio.
- La búsqueda en Zotero es silenciosa — no reportar cada resultado, solo los seleccionados para el borrador.
