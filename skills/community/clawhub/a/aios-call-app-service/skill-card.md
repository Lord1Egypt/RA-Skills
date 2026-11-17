## Description:

AIOS App Service helps agents read AIOS ontology, invoke AIOS, OpenClaw, and Forguncy business interfaces through a controlled CLI workflow, and continue analysis from live system results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kadbbz](https://clawhub.ai/user/kadbbz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business-system agents use this skill when a request requires live AIOS, OpenClaw, or Forguncy data, business interface calls, binding reads, or user-confirmed system actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be invoked implicitly to read live business-system data.

Mitigation: Install only where implicit live business-system reads are acceptable and review deployment permissions before release.

Risk: The skill can support mutating business actions such as creating, editing, submitting, approving, or deleting records.

Mitigation: Require independent user confirmation and backend authorization controls before any mutating action is executed.

Risk: The artifact includes an unpinned npx fallback for a CLI used in real business operations.

Mitigation: Provide a pinned, trusted aios-apps-invoke-cli installation instead of downloading an unversioned package at runtime.

## Reference(s):

- [AIOS App Service on ClawHub](https://clawhub.ai/kadbbz/skills/aios-call-app-service)
- [AIOS application invocation rules](references/invoke-rules.md)
- [AIOS data processing rules](references/data-processing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and structured explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ontology references, command type, assumptions, missing fields, skipped data, and uncertainty notes.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
