## Description:

Automatically retries ACP vendors in priority order on failure and returns the first successful result with fallback logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engibarian](https://clawhub.ai/user/engibarian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route ACP execution through a prioritized fallback chain across supported vendors and models. It is intended to improve task resilience by retrying with the next configured provider after failures, timeouts, authentication errors, or rate limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a referenced relative shell script that is not included in the artifact.

Mitigation: Install or pin a trusted acp-fallback.sh implementation before use and review it before sourcing it in an agent environment.

Risk: Automatic provider fallback may send task content to additional ACP or model vendors.

Mitigation: Enable only approved providers, document provider order, and confirm that task data is allowed to be processed by each configured vendor.

Risk: Fallback logging can expose operational details or sensitive task context if logs are retained broadly.

Mitigation: Review logging behavior, restrict access to fallback logs, and avoid sending secrets in task descriptions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engibarian/skills/acp-fallback)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and fallback execution results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the selected vendor, retry count, elapsed time, and success or failure status.]

## Skill Version(s):

1.0.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
