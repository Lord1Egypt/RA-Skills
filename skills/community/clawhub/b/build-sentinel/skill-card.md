## Description:

Security scanning and transaction simulation for Solana AI agents

This skill is ready for commercial/non-commercial use.

## Publisher:

[buildsentinel-dev](https://clawhub.ai/user/buildsentinel-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Sentinel to screen Solana-related user instructions for threats and simulate transactions before execution. It supports policy checks for spending limits, allowlists, blocklists, time bounds, and risk thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's activation scope and shell-style user-input command need review before installation.

Mitigation: Limit use to Solana transaction and policy-review workflows, and review the skill before installing.

Risk: User messages passed into shell command strings can create command-construction risk.

Mitigation: Pass user messages to the Sentinel CLI with structured arguments or stdin instead of building shell command strings.

Risk: Sentinel CLI failures can leave a transaction without a completed scan or simulation.

Mitigation: Fail closed on CLI errors, report the error to the user, and check configuration with `sentinel config show` before retrying.

## Reference(s):

- [Sentinel ClawHub Skill Page](https://clawhub.ai/buildsentinel-dev/skills/build-sentinel)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON result interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fail closed on Sentinel CLI errors; outputs guide the agent to proceed, block, or report a specific risk.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
