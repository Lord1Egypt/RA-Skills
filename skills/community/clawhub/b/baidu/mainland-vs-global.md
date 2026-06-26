# Mainland Versus Global

Use this file whenever the answer could change by region, language, or source accessibility.

## Decision Axes

| Axis | Mainland-first default | Global or cross-border default |
|------|------------------------|--------------------------------|
| Documentation language | Chinese source may be the source of truth | Prefer English docs when they exist, then reconcile with Chinese originals |
| Search expectations | Baidu Search and Baike may reflect local intent and terminology | International users may need translated queries and secondary confirmation |
| Maps workflows | Baidu Maps is often the relevant local map surface | Global mapping habits may need cross-checks with non-Baidu tools |
| Cloud and AI workflows | Product naming and rollout details may be China-first | Availability, onboarding, and docs parity may differ outside mainland |
| Compliance and rollout | Local regulations and operator ownership matter early | Cross-border assumptions must be stated, not implied |

## What To Clarify Early

- target users and region
- preferred documentation language
- whether Chinese-first evidence is acceptable
- whether the user needs planning only or account execution
- whether a mainland-only recommendation is acceptable

## Typical Failure Modes

- Using English summaries as if they are the freshest source
- Assuming search ranking means the same thing for all geographies
- Recommending Qianfan or Maps steps without checking where the team operates
- Mixing public-web research with cloud rollout constraints

## Output Contract

For any region-sensitive answer, state:
- assumed geography
- assumed language
- what would likely change in another region
