# Audit rubric

Use this rubric for comparable audits. Score a criterion only when there is direct evidence. Report unavailable criteria as `Unknown` and show both the earned score and the maximum verified score.

| Category | Points | What to verify |
| --- | ---: | --- |
| Offer and message clarity | 15 | Audience, problem, promise, differentiation, price or next step, and consistency with the traffic source |
| Mobile experience and trust | 15 | Readability, speed signals, visual hierarchy, proof, policy/contact details, accessibility, and absence of intrusive friction |
| CTA and WhatsApp handoff | 20 | CTA visibility, action-oriented copy, destination accuracy, prefilled-message context, operator availability, and fallback behavior |
| Lead capture and qualification | 15 | Minimum necessary fields, validation, consent, spam controls, qualification data, useful error states, and thank-you behavior |
| Tracking and attribution | 20 | PageView/ViewContent, lead or contact event, purchase event, UTM/click-ID retention, browser/server deduplication, test-event evidence, and ownership of each pixel |
| Routing and follow-up | 10 | Correct operator assignment, response-time expectation, templates, status changes, reminders, and lost-lead recovery |
| Learning loop | 5 | Defined primary metric, diagnostic metrics, experiment hypothesis, sample window, and decision rule |

## Severity

- **Critical:** conversion is blocked, leads are lost, sensitive data is exposed, or purchase/lead events are materially wrong.
- **High:** a major source of traffic cannot complete or be attributed reliably.
- **Medium:** meaningful friction or ambiguity is likely, but the journey still works.
- **Low:** polish, maintainability, or a lower-impact optimization.

## Confidence

- **High:** directly observed in the live flow, supplied analytics, or a reproducible test.
- **Medium:** supported by partial evidence or consistent screenshots/configuration.
- **Low:** inference that needs validation. Phrase it as a hypothesis, not a fact.

## Measurement map

For every recommended event, record:

1. Event name and business meaning.
2. Exact trigger and page or system responsible.
3. Required parameters, with personal data minimized or hashed as required.
4. Browser-side, server-side, or both.
5. Deduplication identifier when the same conversion is sent through both paths.
6. Test procedure and expected evidence in the destination platform.
7. Failure monitoring and the person or team responsible.
