## Description:

OpenClaw-only sidecar for the original follow-builders skill that takes over scheduling and digest delivery without modifying the upstream skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amortalsodyssey](https://clawhub.ai/user/amortalsodyssey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to take over scheduling for the original follow-builders workflow, configure digest frequency and delivery mode, inspect sidecar status, and roll back to the original cron when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle reusable Feishu credentials and may store direct Feishu app credentials locally.

Mitigation: Use trusted Feishu accounts, prefer OpenClaw account reuse, avoid direct_credentials unless necessary, and check permissions on ~/.follow-builders-sidecar.

Risk: Configurable Feishu domains can increase network routing risk.

Mitigation: Use only the standard feishu or lark domains and avoid custom Feishu domains.

Risk: Predictable temporary file paths may expose digest payloads on shared systems.

Mitigation: Run in a trusted local environment and update the implementation to use private per-run temporary directories.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/amortalsodyssey/skills/follow-builders-sidecar)
- [Publisher Profile](https://clawhub.ai/user/amortalsodyssey)
- [Original follow-builders Project](https://github.com/zarazhangrui/follow-builders)
- [Configuration Schema](artifact/config/config-schema.json)
- [Default Source Configuration](artifact/config/default-sources.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration; runtime delivery can produce OpenClaw messages or Feishu card payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, python3, and openclaw; reads the original follow-builders config once and writes sidecar state under ~/.follow-builders-sidecar.]

## Skill Version(s):

1.0.9 (source: server release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
