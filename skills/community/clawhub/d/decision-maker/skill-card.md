## Description:

Decision Maker helps agents structure decisions with pros-cons analysis, weighted matrices, blind-choice prompts, framework recommendations, and risk assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a decision prompt into structured comparison templates, scoring matrices, bias-reduction prompts, framework suggestions, and risk checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes an unrelated workflow helper that writes command history and arguments to local disk.

Mitigation: Review the package before installation, avoid passing sensitive values as arguments, and prefer a release that removes the helper or clearly documents and controls its logging behavior.

Risk: Decision-support templates may produce incomplete or misleading guidance if treated as a final decision.

Mitigation: Use the outputs as structured prompts for human review, and validate important decisions with appropriate domain expertise.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)
- [Decision Maker on ClawHub](https://clawhub.ai/ckchzh/skills/decision-maker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-like terminal text with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English decision templates; no API keys required.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
