## Description:

Helps an agent use the emq-cli command line for installation, authentication, market queries, portfolio creation and orders, quota checks, raw command pass-through, and common troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[greapi](https://clawhub.ai/user/greapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to produce concrete emq-cli commands for environment setup, login, market data retrieval, portfolio operations, quota checks, raw SDK-style calls, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentialed portfolio, order, and raw commands can affect real accounts or expose sensitive account data if run in the wrong environment.

Mitigation: Use a dedicated virtual environment or container, keep EMQ credentials out of shared shells and logs, verify authentication status first, and run account-changing commands only against approved accounts or sandboxes.

Risk: Installing or invoking emq-cli without package review can introduce dependency or command behavior risk.

Mitigation: Pin and verify the emq-cli package before installation, review command help for required flags, and inspect generated commands before execution.

## Reference(s):

- [EMQ CLI Command Recipes](references/command-recipes.md)
- [ClawHub skill page](https://clawhub.ai/greapi/skills/choice-emquantcli-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/greapi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance should verify authentication before credentialed market, portfolio, quota, or raw commands.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
