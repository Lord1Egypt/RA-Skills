# Cover letter — template

Tono recomendado: directo, confiado, sin floreos. Máximo 250 palabras.

---

Hi {{hiring_manager_or_team}},

I'm applying for the **{{role_title}}** role at {{company_name}}. {{one_sentence_genuine_reason_for_this_company}}

In my last role at {{recent_company}} I {{top_relevant_achievement_with_metric}}. Two more reasons I'm a strong fit:

- **{{requirement_1_from_posting}}** — {{evidence_from_cv_max_2_lines}}
- **{{requirement_2_from_posting}}** — {{evidence_from_cv_max_2_lines}}

{{optional_sentence_about_why_now_or_career_direction}}

Available to chat at your convenience. CV attached, GitHub at {{github_url}}, and a few projects worth looking at: {{1_or_2_project_links_with_one_line_context}}.

Thanks for your time,
{{candidate_name}}

---

## Reglas para el agente al rellenar

1. **Investigar la empresa primero.** El `one_sentence_genuine_reason_for_this_company` no puede ser genérico. Buscá: blog técnico reciente, charla en conferencia, post de su CTO, valor declarado que conecte con algo del CV. Si no encontrás nada genuino en 5min, el match probablemente no era tan fuerte y vale repensarlo.

2. **Las dos `requirement_*` deben venir de la job description**, no de lo que el candidato querría destacar. Leé el posting, identificá los 2-3 requisitos top (suelen estar en bullets de "Requirements" o "What you'll do"), y para cada uno mapeá la evidencia más cercana del CV.

3. **Métricas obligatorias en el `top_relevant_achievement`.** Si el CV no tiene una métrica defendible para esa área, decile al usuario: "no tengo número fuerte aquí — ¿podés darme uno o reformulamos?". No inventes.

4. **`why_now`** es opcional. Usalo solo si hay una transición narrable (ej: "after 4 years scaling backend at X, I'm looking for Y"). Si suena forzado, dropeá esa línea.

5. **Project links** solo si son públicos y de calidad. README sólido, demo funcionando, código legible. Si los GitHub repos están abandonados o el README dice "WIP", saltá esta sección.

6. **No incluir información que no esté en el CV o sea verificable.** Si el usuario pide agregar una skill que no aparece, frená y pedile que la agregue al CV primero (y al `profile.json`).

7. **Idioma de la cover letter:** match con el del posting. Si el posting es en inglés, escribí en inglés aunque el CV esté en español. Si es bilingüe, usá inglés por default.

8. **Output final:** salva el draft en `data/applications/{slug}/cover-letter.md` y mostrale al usuario para review antes de cualquier acción.
