## Description:

Professional REAL demo video generation with PM-driven scenario decomposition and region-aware recording. Uses Playwright native recording + bmad-agent-pm integration for intelligent video production.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosscui-chy](https://clawhub.ai/user/rosscui-chy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation teams use this skill to produce narrated demo videos from web pages, local HTML, templates, or product scenarios through CLI, Python API, Web UI, and VS Code workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the release suspicious and notes a mismatch between production claims and inspected prototype-grade behavior.

Mitigation: Review the package carefully before installation and validate generated outputs before using them in customer-facing or production workflows.

Risk: The bundled web UI may introduce local or network exposure risk if run on a reachable interface.

Mitigation: Run the web UI only in a trusted local environment and avoid exposing it to shared or public networks until it has been reviewed.

Risk: Template installation or import can introduce untrusted content into the generation workflow.

Mitigation: Use only trusted templates and inspect template archives before installing or importing them.

Risk: The security guidance warns against using the VS Code extension until external script path and environment handling are fixed.

Mitigation: Disable or avoid the VS Code extension unless those handling paths have been reviewed and corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rosscui-chy/skills/auto-video-generator)
- [ClawDIS homepage](https://github.com/avg-team/auto-video-generator)
- [Documentation](https://auto-video-generator.readthedocs.io)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [CHANGELOG.md](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, configuration examples, and generated video workflow instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to produce MP4/WebM video artifacts, narration files, PRD-derived scenario data, and local configuration files.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
