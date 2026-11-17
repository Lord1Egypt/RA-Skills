## Description:

A specialized skill for safely managing and testing OpenClaw configuration changes using a Blue/Green deployment pattern.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joshualeecowan33-ui](https://clawhub.ai/user/joshualeecowan33-ui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to stage, validate, promote, or roll back OpenClaw configuration changes without immediately overwriting the primary configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deployment script can replace the live OpenClaw configuration during validation.

Mitigation: Review and harden the script before use; validate Green without replacing the live configuration and require explicit confirmation before promotion.

Risk: Rollback and temporary-file handling are unsafe in the provided script.

Mitigation: Use per-run temporary files, separate validation from promotion, and remove the BLUE_LONG_NAME cleanup path before deployment.

## Reference(s):

- [Blue Green Deployer ClawHub page](https://clawhub.ai/joshualeecowan33-ui/skills/blue-green-deployer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and a Bash deployment script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires openclaw and jq; the deployment script can modify ~/.openclaw/openclaw.json.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
