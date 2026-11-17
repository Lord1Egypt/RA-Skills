## Description:

Helps agents track long conversations, prepare recovery summaries, hand off active work, and archive session state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use it to preserve context across long-running work by tracking conversation usage, creating recovery packs, and organizing handoffs and archives. Real-time checks require explicit invocation or a supported host hook; scheduled scans are periodic checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags project-step orchestration and filesystem-scanning behavior beyond the described memory and handoff purpose, including approval behavior that may imply user approval when manual confirmation is required.

Mitigation: Review the handoff approval behavior and project-execution and filesystem-scanning scope before installation; confirm user-approval controls.

Risk: The security assessment has medium confidence and is partial because some referenced paths were not present in the supplied bundle.

Mitigation: Review the complete release bundle and resolve missing referenced paths before relying on the assessment.

## Reference(s):

- [English README](artifact/README.en.md)
- [Recovery pack templates](artifact/references/templates.md)
- [Agent handoff capabilities](artifact/references/agent-gateways.md)
- [ClawHub release page](https://clawhub.ai/lisong2003-lgtm/skills/codex-memory-orchestrator)
- [Publisher profile](https://clawhub.ai/user/lisong2003-lgtm)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown recovery packs and summaries, JSON session state, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workflow artifacts are created locally when the skill is invoked or scanned.]

## Skill Version(s):

1.9.4 (source: frontmatter, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
