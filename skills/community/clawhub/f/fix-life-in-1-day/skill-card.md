## Description:

Guides users through 10 structured self-reflection sessions based on Dan Koe's article.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evgyur](https://clawhub.ai/user/evgyur)

### License/Terms of Use:

MIT

## Use Case:

External ClawHub or Clawdbot users use this skill to work through English or Russian self-reflection sessions, save responses, track progress, and generate a final Markdown summary of insights and a one-day reset protocol.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive psychological reflections, summaries, reminders, and exports may remain in plaintext workspace files.

Mitigation: Use only in a private workspace, avoid entering highly sensitive details, and add clear consent notices plus restrictive file permissions before deployment.

Risk: The shell handler has a command-injection risk.

Mitigation: Review and harden the shell handler before installation by validating inputs, avoiding unsafe command construction, and testing command paths with hostile input.

Risk: Users may treat self-help prompts as mental-health advice.

Mitigation: Add explicit mental-health safety notices, crisis-resource direction, and boundaries that the skill is for reflection rather than diagnosis or treatment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/evgyur/skills/fix-life-in-1-day)
- [Life Architect Sources](artifact/references/sources.md)
- [10 Sessions Overview](artifact/references/sessions.md)
- [Dan Koe original post](https://x.com/thedankoe/status/2010751592346030461)
- [Alex Prompter 10 prompts](https://x.com/alex_prompter/status/2011566578152661139)
- [Clawdbot](https://github.com/clawdbot/clawdbot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prompts and JSON status or progress responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes session progress, user reflections, insights, reminders, and final exports to workspace memory files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
