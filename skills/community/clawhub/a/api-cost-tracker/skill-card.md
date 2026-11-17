## Description:

Track AI API costs across OpenAI, Anthropic, Google AI with budget alerts, analytics, and optimization tips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[k5rs4n](https://clawhub.ai/user/k5rs4n)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use this skill to estimate AI API spend across OpenAI, Anthropic, and Google AI, monitor budgets, export reports, and identify cost optimization opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save fabricated demo spending records as if they were real, making reports and budget alerts unreliable.

Mitigation: Run it only in an isolated data directory until demo seeding is removed or corrected, and verify ledger contents before relying on reports or alerts.

Risk: Documented CLI options may not match the implemented command behavior.

Mitigation: Confirm supported commands against the current script before automating budget checks or reports.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/k5rs4n/skills/api-cost-tracker)
- [OpenClaw](https://openclaw.ai)
- [Node.js Documentation](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text and Markdown, with optional JSON or CSV reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local cost ledger files under the configured dataDir.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
