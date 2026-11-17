## Description:

Dewu helps agents organize public information from Dewu e-commerce pages, including merchant onboarding requirements, event details, marketing tools, and service rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeclaw007](https://clawhub.ai/user/mikeclaw007)

### License/Terms of Use:

MIT-0

## Use Case:

External operators, analysts, and agents use this skill to summarize public Dewu merchant onboarding, campaign, marketing-tool, logistics, after-sales, and policy information. The skill is intended to keep merchant-side and consumer-side rules separate and preserve source links and dates where available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill with non-public merchant backend sessions, order records, payment data, or private account information could expose sensitive information and exceed the skill's intended scope.

Mitigation: Use only public Dewu pages and do not provide merchant backend sessions, order records, payment data, or private account information.

Risk: Dewu campaign pages and service rules may change frequently, so summaries can become stale.

Mitigation: Retain original links and dates in outputs, and verify current platform pages before acting on merchant, campaign, logistics, after-sales, or policy information.

## Reference(s):

- [Dewu homepage](https://www.dewu.com/)
- [ClawHub skill page](https://clawhub.ai/mikeclaw007/skills/dewu)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Concise Markdown summaries, checklists, and tables with source links and dates when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps public source links and dates in outputs; separates merchant-side and consumer-side rules.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
