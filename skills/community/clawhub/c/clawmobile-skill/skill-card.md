## Description:

ClawMobile helps agents operate Android automation workflows through AutoX.js, including workflow execution, task recording, AI-assisted recovery, membership checks, and HTTP API interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miyan1221](https://clawhub.ai/user/miyan1221)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and RPA teams use this skill to configure, test, record, and run Android automation workflows against an AutoX.js service. It is intended for mobile testing, batch operations, workflow replay, and app interaction automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default networking and token handling could expose the AutoX.js service or automation token if deployed broadly.

Mitigation: Replace default tokens before use, bind services to localhost, and require TLS plus authentication before exposing port 8765 beyond a trusted local network.

Risk: Workflow execution and recording can interact with apps, accounts, screenshots, UI trees, and local files.

Mitigation: Use an isolated test device or trusted local environment, and review workflows and recording actions before running them against accounts or apps containing sensitive data.

Risk: Persisting API tokens in shell startup files can leak credentials to other sessions or tools.

Mitigation: Use a scoped environment, secret manager, or temporary token injection instead of storing CLAWMOBILE_API_TOKEN in ~/.bashrc.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/miyan1221/skills/clawmobile-skill)
- [ClawMobile documentation](https://docs.clawmobile.com)
- [AutoX.js](https://autoxjs.com/)
- [Artifact README](artifact/README.md)
- [Artifact skill guide](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, shell, JSON, and YAML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide calls to a configured local AutoX.js HTTP API and Android device connection.]

## Skill Version(s):

1.0.1 (source: target metadata, release evidence, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
