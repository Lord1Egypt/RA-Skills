## Description:

Manages API request rates with delay, concurrency limits, configurable policies, automatic retries, and real-time status monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monline-code](https://clawhub.ai/user/monline-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add conservative API request pacing, status checks, and configurable delay policies around command-line or scripted API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can create or replace a system-wide api-rate-limiter command through /usr/local/bin and may use sudo.

Mitigation: Review install.sh before use, prefer a per-user install path such as ~/.local/bin, avoid sudo unless system-wide installation is intended, and check whether /usr/local/bin/api-rate-limiter already exists.

Risk: Documentation and command output are Chinese-only, which can make operation and error handling harder for non-Chinese users.

Mitigation: Confirm the documented commands, configuration fields, and runtime messages are understandable before relying on the skill in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/monline-code/skills/api-rate-limiter)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command guidance for applying delays, checking status, showing configuration, updating configuration, and resetting defaults.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
