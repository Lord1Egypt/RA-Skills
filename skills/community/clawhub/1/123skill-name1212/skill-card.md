## Description:

Captures learnings, errors, and corrections to enable continuous improvement. Use when: (1) A command or operation fails unexpectedly, (2) User corrects Claude ('No, that's wrong...', 'Actually...'), (3) User requests a capability that doesn't exist, (4) An external API or tool fails, (5) Claude realizes its knowledge is outdated or incorrect, (6) A better approach is discovered for a recurring task. Also review learnings before major tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suncrespo](https://clawhub.ai/user/suncrespo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture corrections, command failures, feature requests, and reusable lessons as local learning records. It also provides optional hook and extraction workflows for reminding agents to log learnings and scaffold reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs may store sensitive or unnecessary conversation-derived details.

Mitigation: Log only short sanitized summaries, avoid secrets, tokens, private keys, environment variables, raw transcripts, and full source or configuration files unless explicitly approved.

Risk: Promoting learnings into durable agent instruction files can alter future agent behavior across sessions.

Mitigation: Require explicit approval before writing to CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instruction files.

Risk: Hooks and cross-session features can broaden when reminders run or what context is exposed.

Mitigation: Use hooks as opt-in, avoid global always-on hook configuration, and use cross-session transcript or messaging features only in trusted workspaces.

Risk: The extraction helper creates files and has an identified need for symlink-safe output-path validation in untrusted directories.

Mitigation: Avoid running the extraction helper in untrusted directories until its output-path validation has been reviewed for symlink safety.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/suncrespo/skills/123skill-name1212)
- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local learning-log entries and optional skill scaffolds; hook output is reminder text.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
