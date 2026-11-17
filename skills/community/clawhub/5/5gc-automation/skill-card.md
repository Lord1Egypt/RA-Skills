## Description:

Automates bulk creation, editing, and default policy setup for 5GC network functions and policy objects through a Flex web dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuwei120](https://clawhub.ai/user/liuwei120)

### License/Terms of Use:

MIT-0

## Use Case:

Network developers and lab engineers use this skill to run CLI-driven browser automation for AMF, UDM/AUSF, SMF/PGW-C, UPF/PGW-U, GNB, UE, PCF, NRF, QoS, Traffic Control, PCC, and SMPolicy configuration in an authorized 5GC management dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates sensitive 5GC console changes.

Mitigation: Run it only in an isolated lab or explicitly authorized 5GC management environment and review changes before execution.

Risk: The security evidence reports shared credentials in the release.

Mitigation: Rotate exposed credentials, avoid shared accounts, and use environment-specific secrets before installation or use.

Risk: The security evidence reports disabled TLS checks.

Mitigation: Require valid TLS certificates and remove or tightly control TLS verification bypasses before use.

Risk: The security evidence reports session caching.

Mitigation: Disable or protect cached browser sessions and clear session state after authorized automation runs.

Risk: The security evidence reports policy mutations without strong safeguards.

Mitigation: Add confirmation, dry-run, backup, or change-approval controls before policy replacement or bulk edits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuwei120/skills/5gc-automation)
- [ClawHub publisher profile](https://clawhub.ai/user/liuwei120)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke Playwright-driven browser automation against a 5GC web dashboard.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
