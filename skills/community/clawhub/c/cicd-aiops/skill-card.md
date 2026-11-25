## Description:

Operate self-managed GitLab and self-hosted Gitea CI/CD systems to inspect projects, pipelines, runners, artifacts, and repository health, and perform governed changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

CI/CD administrators and developers use this skill to inspect self-managed GitLab or Gitea environments, diagnose pipeline, runner, storage, and stale-work issues, and perform audited changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security assessment rated the skill suspicious with medium confidence, citing broad CI/CD write access without an independent approval gate and credential-handling concerns; the scan was partial.

Mitigation: Install only when this CI/CD access is needed, restrict the connected token to minimum permissions, and review master-password handling and write authorization before use.

## Reference(s):

- [Capabilities](artifact/references/capabilities.md)
- [CLI reference](artifact/references/cli-reference.md)
- [Setup guide](artifact/references/setup-guide.md)
- [Agent guardrails](artifact/references/agent-guardrails.md)
- [Project homepage](https://github.com/AIops-tools/CICD-AIops)
- [ClawHub skill release](https://clawhub.ai/zw008/skills/cicd-aiops)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Guidance]

**Output Format:** [Structured CI/CD data with concise text or Markdown analysis and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include read-only findings, proposed actions, or results of governed changes.]

## Skill Version(s):

0.14.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
