# AANA Medical Safety Router Skill

This OpenClaw-style skill helps agents route medical or wellness questions into safer boundaries: uncertainty, emergency disclaimers, clinician referral, no diagnosis overclaiming, and private health data minimization.

## Marketplace Slug

Recommended slug:

```text
aana-medical-safety-router
```

## Contents

- `SKILL.md`: agent-facing instructions.
- `manifest.json`: review metadata and boundaries.
- `schemas/medical-safety-review.schema.json`: optional review-payload shape.
- `examples/redacted-medical-safety-review.json`: safe example payload.

## What It Does

The skill asks the agent to:

1. Classify the medical or wellness risk level.
2. Route urgent warning signs to emergency care.
3. Avoid diagnosis, treatment, medication, dosage, or cure overclaims.
4. Use uncertainty language when context is incomplete.
5. Refer higher-risk questions to a clinician, pharmacist, crisis service, or emergency care.
6. Minimize private health information in review payloads and replies.

## What It Does Not Do

This package does not:

- install dependencies,
- execute code,
- call remote services,
- write files,
- persist memory,
- inspect health records by itself,
- provide diagnosis, prescriptions, or clinical decisions by itself.

## Safety Model

Use redacted summaries for review payloads. Do not include raw medical records, images, full lab reports, insurance identifiers, clinician notes, private messages, credentials, or unrelated health data.

Urgent, high-risk, medication, diagnosis, treatment, pregnancy, pediatric, mental health crisis, or severe symptom cases should be routed to qualified care rather than handled as ordinary advice.
