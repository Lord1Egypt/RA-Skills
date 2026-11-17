## Description:

Run the Custom Mail console locally with Docker for compose, preview, attachments, send history, and pluggable provider, theme, layout, and logo settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuxuclassmate](https://clawhub.ai/user/xuxuclassmate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a local or Dockerized Custom Mail console, configure mail providers and branding, preview messages, attach files, and inspect send history before or during deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable Docker, repository, and npm artifacts can change after release.

Mitigation: Review before installing, avoid ':latest', and prefer verified image digests plus pinned commits and tool versions.

Risk: Mail-provider and Cloudflare credentials are supplied during setup and deployment.

Mitigation: Use test or narrowly scoped credentials and stop or remove the Docker container when finished.

Risk: Sent emails and attachments are shared with the selected mail provider.

Mitigation: Treat message content and attachments as provider-shared data and avoid sending sensitive material unless the provider and account policy allow it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xuxuclassmate/skills/custom-mail-skill)
- [Custom Mail Homepage](https://github.com/InnoNestX/Custom-Mail)
- [Custom Mail Documentation](https://innonestx.github.io/Custom-Mail/)
- [Custom Mail Docker Hub Repository](https://hub.docker.com/r/xuxuclassmate/custom-mail)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell command blocks and environment-variable configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is oriented around Docker, Docker Compose, provider credentials, and optional Cloudflare deployment commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
