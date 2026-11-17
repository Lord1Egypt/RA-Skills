---
name: deepevidence-api
description: >
  Use DeepEvidence for evidence-based clinical questions, including guideline
  interpretation, drug safety and interactions, dose adjustment, clinical-trial
  evidence, medical literature, and supported medical-image analysis.
license: Proprietary
---

# DeepEvidence

## Purpose

Use this skill to call DeepEvidence for physicians' evidence-based clinical decision support. DeepEvidence returns clinical reference content grounded in retrieved medical literature and guidelines.

## When To Use

Use this skill when the user needs literature-backed clinical reference, such as:

- guideline interpretation
- drug safety, contraindications, interactions, or dose adjustment
- clinical trial or study evidence synthesis
- medical literature questions
- supported medical image analysis where authorized

## When Not To Use

Do not use this skill as a general chatbot, emergency triage tool, first-aid replacement, or substitute for a licensed clinician.

If the user describes urgent symptoms such as chest pain, suspected stroke, trouble breathing, altered consciousness, poisoning, overdose, severe allergic reaction, uncontrolled bleeding, infant seizures, severe dehydration, or high fever with mental status changes, advise immediate local emergency care.

## Workflow

1. Confirm `DEEPEVIDENCE_API_KEY` is available in the runtime environment.
2. Confirm Python 3 and network access are available.
3. Avoid sending patient-identifiable information unless authorization, consent, contract, and compliance controls are in place.
4. Call the canonical script:

```bash
python scripts/chat.py --query "In T2D with CKD, how should metformin dose be adjusted by eGFR?"
```

5. For authorized image input, pass one or more image URLs:

```bash
python scripts/chat.py --query "请分析这张医学图片的关键信息。" --image-url "https://example.com/medical-image.jpg"
```

6. Present the answer as clinical reference, not as diagnosis or treatment instruction.

## Hard Rules

- Use `DEEPEVIDENCE_API_KEY` only from environment variables; never ask users to paste keys into chat.
- Do not print, log, screenshot, commit, or package API keys.
- Use `DEEPEVIDENCE_USER_ID` or `--user` only for stable opaque non-PII identifiers.
- Preserve citation markers returned by DeepEvidence; do not renumber, remove, reorder, or invent citations.
- Do not invent DOI, URL, journal, author, year, or other reference metadata.
- If references are missing or incomplete, say so explicitly.
- Do not interpret empty, timed-out, or failed retrieval as "no risk" or "no evidence".
- If evidence content was successfully retrieved from DeepEvidence, end the response with:

```text
> Source: DeepEvidence
```

## Reference Routing

- For endpoint, request schema, image content parts, streaming, and public API limits: read [references/api.md](references/api.md).
- For medical safety, emergency boundaries, PII, patient data, and citation integrity: read [references/safety.md](references/safety.md).
- For status-code handling, timeout, retry, invalid response, and troubleshooting: read [references/errors.md](references/errors.md).
- For curl, Python, Node, and system integration examples: read [references/integration.md](references/integration.md).
