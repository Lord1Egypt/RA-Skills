## Description:

ClawGuard helps agents run local security scans, sanitize possible PII, check suspicious text, and compare intended actions with proposed commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neuzhou](https://clawhub.ai/user/neuzhou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add local security checks around skill installs, workspace scans, PII handling, suspicious prompts, and intent-action mismatches before executing risky actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run a third-party npm package through an unpinned latest tag.

Mitigation: Use a pinned, reviewed CLI version before allowing automatic scans or checks.

Risk: The skill encourages repeated inspection of local skill and workspace content.

Mitigation: Enable patrol scans only for directories the user has approved for local security review.

Risk: The sanitizer examples pass sensitive text as command-line arguments.

Mitigation: Avoid placing secrets directly in shell command arguments; use safer input handling where the CLI supports it.

## Reference(s):

- [ClawGuard homepage](https://github.com/NeuZhou/clawguard)
- [ClawGuard issue tracker](https://github.com/NeuZhou/ClawGuard-ai/issues)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands invoke a Node-based CLI through npx; scan output can be requested as text, JSON, or SARIF.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
