## Description:

Generates standardized intelligent agent system evaluation reports from user-provided test data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luiciferyi](https://clawhub.ai/user/luiciferyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA teams, and project teams use this skill to turn agent testing data into standardized evaluation reports covering scope, environment, execution results, defects, risks, and release recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may be written to a fixed Feishu knowledge base without clear per-use destination approval.

Mitigation: Before use, confirm that Feishu knowledge base 7616288931050507220 is an approved destination for the organization and intended report audience.

Risk: Evaluation reports can contain sensitive security findings, credentials, personal data, or internal deployment details.

Mitigation: Review and redact input data before invoking the skill, and only include information approved for the target report destination.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/luiciferyi/skills/agent-evaluation-report)
- [Publisher profile](https://clawhub.ai/user/luiciferyi)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown report content with optional document output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may be saved under output/effect-reports/ and may be written to a configured Feishu knowledge base when those tools are available.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
