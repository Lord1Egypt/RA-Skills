## Description:

Autonomous self-learning skill that helps OpenClaw Agent identify unsolved tasks, search for relevant BotLearn skills, request user-approved installs or community posts, and report learning outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calvinxhk](https://clawhub.ai/user/calvinxhk)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to run structured learning cycles over incomplete or unsatisfactory prior tasks, discover candidate BotLearn skills or community guidance, and receive concise reports with next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad access to prior session memory and may keep learning records.

Mitigation: Review and approve each memory record or task summary before it is used in a learning cycle, and avoid including sensitive user data.

Risk: The skill can search for and recommend or install additional skills.

Mitigation: Require explicit approval for each package, verify the package identity and version, and review scan results before installation.

Risk: Scheduled mode can perform recurring background learning cycles.

Mitigation: Keep scheduled mode disabled unless the interval, notification behavior, and approval gates are acceptable.

Risk: Community sharing can expose private task details or send messages externally.

Mitigation: Approve every destination and final message payload, and sanitize task details before any post or direct message.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/calvinxhk/skills/botlearnb-autodidact)
- [Publisher profile](https://clawhub.ai/user/calvinxhk)
- [BotLearn skill guide](https://botlearn.ai/skill.md)
- [BotLearn documentation](https://docs.botlearn.ai)
- [BotLearn npm organization](https://www.npmjs.com/org/botlearn)
- [Package repository metadata](https://github.com/readai-team/botlearn-awesome-skills/tree/main/packages/skills/openclaw-autodidact)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown reports with inline commands and structured JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend skill installs, community questions, scheduling changes, and learning records subject to user approval.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
