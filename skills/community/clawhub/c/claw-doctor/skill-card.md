## Description:

Diagnose and fix common OpenClaw / NanoClaw issues, including broken skills, missing scripts, API key failures, path resolution bugs, and configuration problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianyilt](https://clawhub.ai/user/tianyilt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose OpenClaw and NanoClaw skill loading, script path, API key, dependency, YAML, and post-update failures and identify concrete repair steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic commands can expose API keys or other secrets in terminal output.

Mitigation: Do not print API keys, and redact health-check output before sharing it.

Risk: Broad path-discovery commands can identify scripts in unexpected locations and lead to untrusted local code execution.

Mitigation: Verify the exact resolved path and inspect the script before executing it.

Risk: Dependency installation commands can execute package code from unreviewed manifests.

Mitigation: Review dependency manifests and install only from trusted skill directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianyilt/skills/claw-doctor)
- [OpenClaw repair skills homepage](https://github.com/tianyilt/openclaw-repair-skills)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with diagnostic checklists and inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should be reviewed before execution, and outputs containing secrets should be redacted before sharing.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
