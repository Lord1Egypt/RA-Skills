---
name: "bytesagain-medical-scribe"
description: "Generate medical documents from clinical notes. Input: patient info, symptoms, diagnosis. Output: SOAP notes, discharge summaries, referral letters, prescription drafts."
version: "1.0.0"
author: "BytesAgain"
tags: ["medical", "healthcare", "documentation", "clinical", "soap-notes", "ehr"]
---

# Medical Scribe

Generate structured medical documents from raw clinical notes. Supports SOAP notes, discharge summaries, referral letters, and prescription drafts.

## Commands

### soap
Generate a SOAP note from clinical observations.
```bash
bash scripts/script.sh soap --patient "John Doe, 45M" --chief "chest pain 2 days" --findings "BP 140/90, HR 88"
```

### discharge
Generate a discharge summary.
```bash
bash scripts/script.sh discharge --patient "Jane Smith, 62F" --diagnosis "Type 2 Diabetes" --stay "3 days" --treatment "Metformin 500mg"
```

### referral
Generate a referral letter to a specialist.
```bash
bash scripts/script.sh referral --patient "Bob Lee, 38M" --from "GP" --to "Cardiologist" --reason "suspected arrhythmia"
```

### prescription
Generate a prescription draft.
```bash
bash scripts/script.sh prescription --patient "Alice Wong, 29F" --drug "Amoxicillin" --dose "500mg" --frequency "3x daily" --duration "7 days"
```

### template
List all available document templates.
```bash
bash scripts/script.sh template --list
```

### help
Show all commands.
```bash
bash scripts/script.sh help
```

## Output Format
All documents output as structured plain text, ready to paste into EHR systems.

## Disclaimer
AI-generated drafts only. Must be reviewed and approved by a licensed medical professional before use.

## Feedback
https://bytesagain.com/feedback/
Powered by BytesAgain | bytesagain.com
