## Description:

Detect AI flavor in long-form Chinese and English articles by auto-detecting language, applying language-specific indicators, and judging whether text reads like AI-generated or human-written.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivian8725118](https://clawhub.ai/user/vivian8725118)

### License/Terms of Use:

MIT-0

## Use Case:

External users and writers use this skill to evaluate Chinese or English long-form articles for AI-like writing patterns and receive a dimension scorecard, quoted evidence, source-likelihood judgment, and revision suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL inputs may cause remote content fetching.

Mitigation: Paste article text directly when privacy matters, and do not submit private, internal, or sensitive URLs unless remote fetching is acceptable.

Risk: AI-authorship verdicts are writing heuristics, not proof of authorship.

Mitigation: Review the quoted evidence and dimension-level findings before relying on the verdict.

## Reference(s):

- [AI flavor evaluation examples](references/evaluation-examples.md)
- [AI flavor indicator checklist](references/indicator-checklist.md)
- [ClawHub skill page](https://clawhub.ai/vivian8725118/skills/detect-ai-flavor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown with dimension score tables, quoted evidence, verdicts, and improvement suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Language-adaptive output for Chinese, English, or bilingual input]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
