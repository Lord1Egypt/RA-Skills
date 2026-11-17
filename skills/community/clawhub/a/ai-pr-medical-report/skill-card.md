## Description:

Interprets uploaded medical test report PDFs, identifies key indicators and abnormal values, searches medical literature, and produces structured health explanation reports with optional visual cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to understand medical test reports in plain language, compare results with reference ranges, and prepare structured summaries they can discuss with a clinician. It is informational and does not replace medical diagnosis or treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded reports may contain sensitive health information and personal identifiers.

Mitigation: Use only reports the user is comfortable processing through AI and search tools, and remove names, IDs, hospital numbers, dates, and other identifiers where possible.

Risk: Generated health explanations may be mistaken for diagnosis or treatment advice.

Mitigation: Present outputs as informational summaries and require clinician review for diagnosis, treatment decisions, or urgent abnormal results.

Risk: Optional publishing workflows may expose private medical details.

Mitigation: Manually review and redact all health-derived content before publishing or sharing.

Risk: Medical literature summaries may become outdated or may not apply to the user's clinical context.

Mitigation: Check current clinical guidance and treat literature summaries as supporting context rather than patient-specific medical advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/ai-pr-medical-report)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown or structured text, with optional image card files and social-post drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include health explanations, literature summaries, suggested next steps, and optional publication-ready content; medical advice requires human clinician review.]

## Skill Version(s):

1.0.0 (source: release evidence and workflow.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
