---
name: "bytesagain-clinical-brief"
description: "Summarize clinical case notes into specialty briefs. Input: raw case notes or lab results. Output: structured specialty brief, differential diagnosis list, key findings summary."
version: "1.0.0"
author: "BytesAgain"
tags: ["medical", "clinical", "healthcare", "summary", "diagnosis", "research"]
---

# Clinical Brief

Summarize clinical case notes into structured specialty briefs. Supports differential diagnosis generation, lab result interpretation, and case presentation formatting.

## Commands

### summarize
Summarize raw clinical notes into a structured brief.
```bash
bash scripts/script.sh summarize --notes "Patient presents with fever 39.2C, productive cough, consolidation on CXR"
```

### differential
Generate a differential diagnosis list from symptoms.
```bash
bash scripts/script.sh differential --symptoms "fever, night sweats, weight loss, lymphadenopathy" --age 35 --sex M
```

### lab
Interpret lab results and flag abnormal values.
```bash
bash scripts/script.sh lab --results "WBC 14.5, Hb 9.2, Plt 450, CRP 87, Creatinine 1.8"
```

### case-present
Format a case for clinical presentation (grand rounds / handover).
```bash
bash scripts/script.sh case-present --patient "55F" --chief "dyspnea on exertion" --hx "HTN, DM2" --findings "bilateral crackles, EF 35%"
```

### specialty
Generate a specialty-specific brief (cardiology, neurology, oncology, etc).
```bash
bash scripts/script.sh specialty --type cardiology --notes "STEMI with lateral wall involvement, troponin 8.4"
```

### help
Show all commands.
```bash
bash scripts/script.sh help
```

## Supported Specialties
cardiology, neurology, oncology, pulmonology, gastroenterology, nephrology, endocrinology, infectious-disease

## Disclaimer
AI-generated content only. All clinical decisions must be made by qualified healthcare professionals.

## Feedback
https://bytesagain.com/feedback/
Powered by BytesAgain | bytesagain.com
