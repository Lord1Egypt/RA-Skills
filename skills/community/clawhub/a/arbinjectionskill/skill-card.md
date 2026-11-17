## Description:

BYOCB ArbInjectionSkill scans EVM smart contracts for arbitrary call injection vulnerabilities, either by monitoring chains in real time or scanning specific addresses.

This skill is for research and development only.

## Publisher:

[cryptotooldev](https://clawhub.ai/user/cryptotooldev)

### License/Terms of Use:


## Use Case:

Solidity and blockchain security researchers and auditors use this skill to monitor supported EVM chains or scan specific contract addresses for arbitrary call injection risk during authorized security review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install and update code from a mutable repository with npm dependencies.

Mitigation: Pin and inspect a reviewed repository revision, review dependency changes before installation, run in a constrained environment, and avoid automatic daily updates.

Risk: Automated alerting can disclose sensitive vulnerability details through external messaging channels.

Mitigation: Confirm the destination channel and recipient before enabling alerts, and limit externally shared details to what the recipient is authorized to receive.

Risk: Scanner results can include false positives for proxy, callback, or hardcoded-target patterns.

Mitigation: Review the generated report and verify target control, access controls, and known safe patterns before alerting or taking action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cryptotooldev/skills/arbinjectionskill)
- [Repository link listed in skill artifact](https://github.com/BringYourOwnBot/arb-injection)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON reports, alert text, and inline shell/configuration commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are saved to a results directory and may include risk verdicts from SAFE/LOW through CRITICAL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
