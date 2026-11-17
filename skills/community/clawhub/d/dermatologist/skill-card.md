## Description:

Track skin lesions, rashes, photos, treatment response, and dermatology visit prep with conservative triage, case-based records, and privacy guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and care-supporting agents use this skill to organize skin-concern timelines, standardized photo comparison notes, treatment-response logs, and dermatologist visit summaries. It supports conservative triage and documentation, not diagnosis or prescribing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive skin-health records may be stored locally under ~/dermatologist/.

Mitigation: Use ask-first activation, approve storage only for cases that should be retained, and delete or export records directly from the local folder when no longer needed.

Risk: Photo-handling guidance contains a conflict around minors or intimate-area photos.

Mitigation: Apply the stricter boundary: do not request or store photos or metadata for minors or intimate areas, and redirect those cases to in-person or secure clinician workflows.

Risk: Skin photos or symptom descriptions can lead to overconfident medical conclusions.

Mitigation: Use the skill for organization, conservative triage, and visit preparation only; do not diagnose, prescribe, or replace clinician review, biopsy, pathology, or emergency care.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/dermatologist)
- [Skill homepage](https://clawic.com/skills/dermatologist)
- [Dermatology Triage](artifact/triage.md)
- [Legal and Privacy Boundaries](artifact/legal-boundaries.md)
- [Photo Protocol](artifact/photo-protocol.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with occasional shell command blocks and local file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Markdown records under ~/dermatologist/ only after user approval.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
