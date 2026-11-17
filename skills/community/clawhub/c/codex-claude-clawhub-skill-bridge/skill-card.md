## Description:

Convert one portable skill idea into a runtime-neutral SKILL.md core plus safe adapter notes for Codex, Claude Code, ClawHub, and OpenClaw, without installing global skills or degrading active projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to turn a portable skill concept or existing SKILL.md into a runtime-neutral core plus safe adapter notes for Codex, Claude Code, ClawHub, and OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated adapter notes may propose scripts, install destinations, publishing steps, or subagent use that should not be applied automatically.

Mitigation: Review those recommendations before execution and require explicit approval before publishing, non-local installation, hook use, browser-login automation, package installation, service restarts, or workspace-wide rewrites.

Risk: A source skill idea may contain private names, local paths, credentials, private links, screenshots, paid lessons, or unverified claims.

Mitigation: Replace sensitive or unsupported material with placeholders, public excerpts, source-owned notes, or synthetic examples before producing a public adapter.

Risk: Runtime-specific assumptions could be hidden inside a supposedly portable skill core.

Mitigation: Keep the canonical core runtime-neutral and put provider-specific commands, packaging notes, sandbox details, and verification notes in separate adapter sections.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zack-dev-cm/skills/codex-claude-clawhub-skill-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown with structured sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a bridge verdict, adapter notes, safety checks, verification gate, and smallest safe next step.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
