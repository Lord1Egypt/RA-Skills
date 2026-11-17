## Description:

Diagnoses Chinese drafts for AI-like writing patterns by quoting suspicious passages, explaining concrete issues, flagging false alarms, and suggesting priority fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cellinlab](https://clawhub.ai/user/cellinlab)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and agents use this skill to inspect Chinese drafts for overly smooth, formulaic, generic, or authorless passages before deciding whether to revise. It is diagnosis-first and avoids whole-piece rewrites unless requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill quotes passages from user-provided drafts in its diagnosis report, which can expose sensitive text if the report is shared.

Mitigation: Review and redact confidential passages before sharing reports or logs.

Risk: AI-writing diagnosis can produce false alarms for formal or intentionally polished genres.

Mitigation: Apply the skill's genre and false-alarm checks before asking for revision; treat weak signals as advisory.

## Reference(s):

- [AI writing pattern catalog](references/pattern-catalog.md)
- [Rewrite guidance](references/rewrite-guidance.md)
- [Diagnosis report template](assets/report-template.md)
- [ClawHub metadata homepage](https://github.com/cellinlab/cell-skills/tree/main/skills/ai-writing-diagnosis)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese Markdown diagnosis report with quoted passages and prioritized revision guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quotes user-provided passages in reading order; defaults to diagnosis before rewriting.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
