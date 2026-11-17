## Description:

ClawGuard Shield v3 provides active defense with prompt injection detection, intent validation, zero-width character detection, and intent integrity verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stardreaming](https://clawhub.ai/user/stardreaming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to screen user input for prompt injection, role hijacking, jailbreak, chain hijacking, encoding, and intent drift risks before acting on the input. It can also suggest or produce hardened configuration output for supported agent settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the CLI depends on unaudited JavaScript outside the package.

Mitigation: Review before installing or running, and do not run the CLI unless the external shared rules file is trusted and packaged with the skill.

Risk: The security evidence says harden/fix can duplicate full configuration contents into output files.

Mitigation: Avoid using harden/fix on configurations containing tokens, passwords, or private endpoints unless output handling redacts secrets and restricts file permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stardreaming/skills/clawguard-shield)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style text reports and JSON configuration output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI output can include risk scores, threat findings, recommendations, validation results, and hardened configuration JSON.]

## Skill Version(s):

3.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
