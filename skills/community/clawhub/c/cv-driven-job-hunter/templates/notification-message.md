# Notification message — template

Formato sugerido para presentarle un match al usuario en chat. Usar este shape para que la respuesta sea escaneable en 5 segundos.

---

## Match individual (para `apply_priority`)

```
🔥 Match {{score}}/100 — {{title}} @ {{company}}
📍 {{remote_or_location}}   💰 {{salary_or_no_disclosed}}   🕒 posteado hace {{n}}d

Por qué te conviene:
  • {{rationale_line_1}}
  • {{rationale_line_2}}

{{flags_warning_si_aplica}}

🔗 {{url}}

¿Postulamos? Decime "sí <slug>" y armo CV/cover adaptados, o "skip" para descartar.
```

## Digest diario (varios matches)

```
📋 Digest cv-driven-job-hunter — {{date}}

⭐ {{n_high}} matches calientes (score ≥ {{threshold}}):
  1. {{title_1}} @ {{company_1}} — {{score_1}}/100
  2. {{title_2}} @ {{company_2}} — {{score_2}}/100
  ...

· {{n_medium}} matches a considerar (70-{{threshold-1}})

📞 {{n_pending}} follow-ups pendientes (corré pending-followups para detalle)

📊 Pipeline: {{drafted}} drafts | {{submitted}} submitted | {{interview}} en entrevista | {{offer}} ofertas

¿Querés que abra el detalle del top {{n}} o de algún follow-up específico?
```

## Alerta de oferta caliente fuera de digest

```
⚡ Oferta nueva que probablemente quieras ver YA:

{{score}}/100 — {{title}} @ {{company}}
💰 {{salary}}   🕒 posteado hace {{n}}h

{{rationale_super_corto}}

{{url}}

Si te interesa, avisame y empiezo a preparar materiales antes de que se llene.
```

## Notificación post-postulación (follow-up trigger)

```
📬 Follow-up sugerido: {{company}} — {{title}}

Postulaste hace {{days}}d ({{status}}). Triggeró el milestone día {{milestone}}.

Acción sugerida: {{action_per_milestone}}

¿Lo hacés vos o querés que prepare un mensaje?
```

## Reglas de uso

1. **Brevedad sobre completitud.** El usuario ve el digest todos los días — no querés que sea un muro de texto.
2. **Siempre incluir un call-to-action concreto.** "¿Postulamos?", "¿Abro el detalle?", "¿Lo hacés vos?". Nunca cierres con un párrafo informativo sin pregunta.
3. **Flags negativos antes que positivos.** Si una oferta tiene `below_minimum` o `seniority_stretch`, mostralo arriba del rationale, no escondido.
4. **Respeta los emojis del template** — son anclas visuales para skim. No agregues más.
5. **Salarios:** si no los expone, decí "💰 no expone" — no inventes rangos.
