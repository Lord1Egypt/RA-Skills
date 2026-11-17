## Description:

Multi-agent roundtable discussion — topic-driven multi-round debate with convergence detection and conclusion generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parsifalc](https://clawhub.ai/user/parsifalc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Agent Roundtable to coordinate multiple AI agents through structured design reviews, product decisions, root-cause analysis, requirements clarification, and architecture debates while preserving discussion history and generated conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security verdict is suspicious because web viewer and export features can expose local discussion data through broad file writes, a persistent network service, and viewer-side flaws.

Mitigation: Install only after trusting the publisher and reviewing the skill; enable web mode only on trusted machines and networks.

Risk: Web mode can serve discussion data through a PM2-managed Node process.

Mitigation: Prefer loopback-only binding, avoid sharing viewer URLs broadly, and manually clean up PM2 processes after use.

Risk: Export paths can write discussion output outside the intended location if misconfigured.

Mitigation: Use output_path values only inside an intended project output directory.

Risk: Untrusted participant metadata may affect viewer-side display and sharing behavior.

Mitigation: Avoid untrusted participant metadata and review generated discussion content before publishing or sharing.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/parsifalc/skills/agent-roundtable)
- [Roundtable homepage](https://roundtable.izmw.me)
- [README_EN.md](README_EN.md)
- [API Reference](docs/API.md)
- [Integration Guide](docs/INTEGRATION.md)
- [Roundtable Adapter Guide](docs/ADAPTER.md)
- [Roundtable Architecture](docs/architecture.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Python, YAML, shell, and JSON examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce discussion records, structured summaries, notifications guidance, and conclusion text for the coordinating agent.]

## Skill Version(s):

1.2.4 (source: server release metadata, SKILL.md frontmatter, pyproject.toml, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
