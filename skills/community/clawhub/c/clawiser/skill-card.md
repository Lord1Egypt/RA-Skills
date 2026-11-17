## Description:

ClaWiser is an agent memory and workflow enhancement suite with modules for memory capture, retrieval tuning, noise reduction, hypothesis-driven development, scenario planning, save/load handoffs, and project-skill pairing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattwenjun](https://clawhub.ai/user/mattwenjun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use ClaWiser to install persistent memory, retrieval, handoff, and planning workflows for OpenClaw or Claude Code agents. It is intended to improve continuity across sessions, structure uncertain work, and manage project context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a high-control memory and workflow layer that can persistently change future agent behavior through files such as AGENTS.md, SOUL.md, and HEARTBEAT.md.

Mitigation: Review proposed file changes before installation and require explicit approval for persistent behavior changes.

Risk: Scheduled conversation-history processing and broad memory indexing can process more local context than intended.

Mitigation: Disable cron or heartbeat automation by default, approve indexed paths explicitly, and review the configured retention and indexing scope.

Risk: Remote embedding providers may receive memory or transcript content when vector search is configured.

Mitigation: Require explicit approval for remote embedding providers and document which provider, endpoint, and data paths are used.

Risk: Automatic Git commits can capture unintended workspace changes.

Mitigation: Disable auto-commit by default, preview staged files, and remove or replace broad staging fallbacks such as git add -A.

## Reference(s):

- [ClaWiser ClawHub listing](https://clawhub.ai/mattwenjun/skills/clawiser)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Memory rules](artifact/assets/memory-deposit/references/memory-rules.md)
- [Noise categories](artifact/assets/noise-reduction/references/noise-categories.md)
- [Noise reduction common failures](artifact/assets/noise-reduction/references/common-failures.md)
- [Example noise classifier](artifact/assets/noise-reduction/references/example-classifier.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with inline bash and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces file edits, installation steps, scheduled-task guidance, and handoff documents depending on the module invoked.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
