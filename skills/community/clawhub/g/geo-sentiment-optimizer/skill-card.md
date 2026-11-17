## Description:

Audits and optimizes brand messaging to improve how AI platforms portray a brand by identifying negative sentiment signals and strengthening positive associations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoly-geo](https://clawhub.ai/user/geoly-geo)

### License/Terms of Use:


## Use Case:

Marketing teams, brand owners, and SEO/GEO practitioners use this skill to audit brand messaging for signals that may affect AI-search sentiment and to draft prioritized copy improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented --brand, --output, and --pages examples do not match the bundled script, which requires --content.

Mitigation: Run the script only with its implemented --content argument, or treat the skill primarily as markdown guidance until the command examples are corrected.

Risk: The audit script uses simple keyword checks, so its score can miss context or overstate sentiment quality.

Mitigation: Review generated recommendations against real customer feedback, third-party coverage, and current brand facts before publishing revised content.

## Reference(s):

- [Sentiment Signals Reference](references/sentiment-signals.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown audit reports with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sentiment signal checklists, risk prioritization, and suggested content rewrites.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
