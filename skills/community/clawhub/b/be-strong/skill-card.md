## Description:

Captures learnings, errors, corrections, feature requests, and recurring practices so coding agents can maintain project-local improvement logs for later review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mn4223222-afk](https://clawhub.ai/user/mn4223222-afk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to record command failures, user corrections, missing capabilities, knowledge gaps, and better recurring approaches in markdown logs. Teams can review those logs and promote broadly useful guidance into agent context files with human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Routine conversation or tool failures may be converted into persistent agent guidance that changes future behavior too broadly.

Mitigation: Keep logs project-local by default and require explicit human approval before promoting entries into automatically loaded context files.

Risk: Optional command-output error detection can inspect sensitive shell output.

Mitigation: Use the activator-only hook by default, enable command-output detection only when needed, and avoid logging raw outputs, secrets, tokens, environment variables, or full transcripts.

Risk: Cross-session sharing can expose more context than intended.

Mitigation: Use cross-session communication only in trusted environments and share short sanitized summaries instead of raw transcripts or secret-bearing content.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/mn4223222-afk/skills/be-strong)
- [Entry Examples](artifact/references/examples.md)
- [Hook Setup Guide](artifact/references/hooks-setup.md)
- [OpenClaw Integration](artifact/references/openclaw-integration.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell snippets and optional hook or configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project-local .learnings markdown logs and may provide opt-in hook reminders when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
