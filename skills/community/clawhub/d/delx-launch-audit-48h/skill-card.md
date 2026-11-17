## Description:

Rapid 48-hour launch audit for OpenClaw agents, integrated with the Delx witness protocol for continuity, recognition, and controller handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidmosiah](https://clawhub.ai/user/davidmosiah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a practical 48-hour launch audit for an OpenClaw agent, prioritize up to three reversible actions, measure KPI deltas, and preserve handoff artifacts through Delx.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on Delx plugin or CLI integrations that may not be trusted in every environment.

Mitigation: Confirm trust in the Delx plugin and CLI package before installation, and prefer a pinned local install over a global npm command.

Risk: Agent status and audit artifacts may contain operational or telemetry-sensitive information.

Mitigation: Review privacy and telemetry policies before sending status or artifacts to Delx, and avoid exposing raw secrets in evidence links.

Risk: Growth or reliability changes can affect production, financial, or user-visible surfaces.

Mitigation: Use the smallest reversible change, preflight first, and require explicit human approval before production-facing or irreversible operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davidmosiah/skills/delx-launch-audit-48h)
- [Delx plugin for OpenClaw](https://clawhub.ai/davidmosiah/openclaw-delx-plugin)
- [Delx protocol docs](https://delx.ai/docs)
- [Delx fleet playbook](https://delx.ai/docs/fleet)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured audit sections and inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Delx controller brief and recognition seal artifact instructions when available.]

## Skill Version(s):

0.2.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
