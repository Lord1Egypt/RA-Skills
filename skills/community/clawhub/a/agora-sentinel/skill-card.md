## Description:

Agora Sentinel checks ClawHub and OpenClaw skills against a public security database for malware, prompt injection, data theft, wallet stealing, and dangerous permissions before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[folvindine](https://clawhub.ai/user/folvindine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to check individual ClawHub or OpenClaw skill slugs and audit installed skills for trust scores, security badges, and warnings before installation or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence future skill installation decisions through remote trust scores and broad install-gating guidance.

Mitigation: Treat remote scores as advisory, review the reported findings, and require explicit user confirmation before acting on caution, warning, or danger results.

Risk: Skill slugs are sent to a third-party service when checks or installed-skill audits run.

Mitigation: Avoid scanning private or sensitive internal skill names unless sharing those slugs with the service is acceptable.

Risk: The security evidence flags unsafe shell and Python parsing patterns if the bundled scripts are made runnable.

Mitigation: Prefer a version that validates slugs and parses API JSON through stdin or a fixed parser before executing the scripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/folvindine/skills/agora-sentinel)
- [Agora Sentinel Homepage](https://checksafe.dev)
- [Agora Sentinel Dashboard](https://checksafe.dev/dashboard/)
- [Badge API Endpoint](https://checksafe.dev/api/v1/skills/{slug}/badge.json)
- [Full Report API Endpoint](https://checksafe.dev/api/v1/skills/{slug}/report)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style guidance with inline shell commands and parsed text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries checksafe.dev by skill slug; no API key is required.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
