## Description:

Helps developers inspect or invoke locally registered ArkCLI actions when product commands do not cover a task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect registered ArkCLI actions, check their request and response contracts, and invoke raw actions for uncovered tasks or troubleshooting. It directs routine product tasks to stable commands and routes public API catalog or OpenAPI requests elsewhere.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw actions can write or delete resources or incur costs.

Mitigation: Inspect the final payload with the CLI --dry-run preview and get explicit user confirmation before write, delete, or cost-impacting actions.

Risk: The workflow relies on related shared, authentication, and configuration guidance outside the scanned artifact scope.

Mitigation: Review the referenced guidance and the verified action contract before invoking an action.

## Reference(s):

- [ArkCLI API reference](references/arkcli-api.md)
- [Evaluation cases](references/evals.md)
- [ClawHub skill release](https://clawhub.ai/jasonstarlight/skills/arkcli-api-explorer)
- [Publisher profile](https://clawhub.ai/user/jasonstarlight)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, JSON]

**Output Format:** [Markdown with shell command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include locally previewed request payloads or action responses; recommends filtering output to relevant fields.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
