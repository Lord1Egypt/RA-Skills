## Description:

Formora Survey helps agents create, preview, publish, distribute, and export Formora surveys, polls, and forms, with optional organic distribution and paid ad planning or launch flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davideuler](https://clawhub.ai/user/davideuler)

### License/Terms of Use:

MIT-0

## Use Case:

External users, product teams, researchers, and marketers use this skill to draft Formora surveys, review generated questions before publishing, distribute surveys across configured channels, and retrieve response data. It can also prepare or submit paid ad campaigns when explicitly configured and confirmed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid-ad launch safeguards can fail and allow repeated live campaigns beyond the stated shared budget caps.

Mitigation: Review carefully before connecting real Google Ads or Meta Ads accounts, keep ads disabled unless needed, leave paused creation enabled, use small test budgets, and rely on platform-side spend controls.

Risk: Exported survey responses and the ads state file can contain sensitive local data.

Mitigation: Store exports and campaign output directories in access-controlled locations, remove stale local files when they are no longer needed, and avoid sharing raw response exports.

Risk: QR generation can fall back to a third-party QR service.

Mitigation: Install local QR generation support when possible and review the survey URL before using or sharing QR assets created through the fallback.

## Reference(s):

- [Formora Survey on ClawHub](https://clawhub.ai/davideuler/skills/formora-survey)
- [Publisher profile: davideuler](https://clawhub.ai/user/davideuler)
- [Formora web app](https://formora.dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance, shell commands, JSON command results, distribution copy, QR image files, and CSV or XLSX exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FORMORA_API_KEY; optional channel and ads credentials enable Telegram, email, X, Google Ads, and Meta Ads actions.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
