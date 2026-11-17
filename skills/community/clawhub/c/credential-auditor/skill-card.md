## Description:

Automates credential security audits with device default-credential lookup, password wordlist generation, and multi-protocol credential testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeanphorn](https://clawhub.ai/user/jeanphorn)

### License/Terms of Use:

MIT-0

## Use Case:

Security engineers, penetration testers, and auditors use this skill to support authorized credential assessments, including default-password checks, password dictionary generation, and credential-test planning across common protocols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated credential testing and brute-force workflows can be misused or run outside an authorized scope.

Mitigation: Install only for security testing on systems the operator is explicitly authorized to assess, and confirm the target scope before running any credential test.

Risk: External-tool workflows are high risk and can depend on mutable local tool installations.

Mitigation: Verify the exact release version, prefer an isolated environment, and avoid symlinking a mutable checkout into the agent workspace.

Risk: Some advertised credential-testing capabilities are incomplete.

Mitigation: Validate behavior on non-production test targets and review generated reports before using results for operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeanphorn/skills/credential-auditor)
- [Device default credential data](references/device_passwords.json)
- [Password generation rules](references/password_rules.json)
- [Protocol test configuration](references/protocol_configs.json)
- [Username dictionary](references/usernames.txt)
- [Password dictionary](references/passlist.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, generated text reports, JSON or list files, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local credential-audit artifacts and commands for optional external tools such as Hydra, Medusa, or Ncrack.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
