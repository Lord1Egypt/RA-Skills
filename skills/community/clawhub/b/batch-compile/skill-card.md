## Description:

Batch Compile helps agents batch-compile Gitea repositories, Obsidian Git repositories, or uploaded zip archives into personal or team knowledge bases with preview, confirmation, job tracking, source archiving, codebase overviews, and import reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base operators use this skill to ingest existing repository or archive material into personal or team knowledge bases after preview and explicit confirmation. It is intended for OpenClaw/Gitea environments that need repeatable batch import, progress tracking, and import reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A batch job may start without enforcing or revalidating the confirmer identity.

Mitigation: Require run_batch.py to receive a mandatory confirmer identity and revalidate that identity before any background job or knowledge-base write starts.

Risk: A powerful Gitea token may be sent to a default HTTP endpoint.

Mitigation: Use HTTPS and replace the site-admin token with a narrowly scoped service account before deployment.

Risk: Unpinned Python dependencies can change behavior across installations.

Mitigation: Pin dependency versions and install only in a controlled OpenClaw/Gitea environment.

## Reference(s):

- [Batch Compile ClawHub skill page](https://clawhub.ai/myd2002/skills/batch-compile)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON script outputs, generated summaries, codebase overviews, and import reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an OpenClaw/Gitea environment, GITEA_URL, GITEA_ADMIN_TOKEN, and user or group context for routing and authorization.]

## Skill Version(s):

1.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
