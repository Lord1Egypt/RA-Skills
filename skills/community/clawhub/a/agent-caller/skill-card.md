## Description:

Call 179 professional agents on-demand from database

This skill is ready for commercial/non-commercial use.

## Publisher:

[717986230](https://clawhub.ai/user/717986230)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search, browse, and retrieve preconfigured specialist agent prompts from a local catalog for code, product, marketing, design, testing, strategy, and other workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled prompts may ask an agent to perform high-impact actions such as payments, public posting, shell commands, file edits, memory changes, or scheduling.

Mitigation: Review retrieved prompts before using them as agent or system instructions, and require explicit user approval with limited tool access for high-impact actions.

Risk: The artifact includes unsafe token-sharing guidance in login documentation.

Mitigation: Do not paste ClawHub tokens into chat; authenticate through the official CLI or a protected local prompt.

Risk: The security verdict is suspicious because safeguards around bundled high-impact prompts are not clearly documented.

Mitigation: Install only for local prompt-catalog use and scan or review selected prompts before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/717986230/skills/agent-caller)
- [Publisher Profile](https://clawhub.ai/user/717986230)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Python dictionaries, prompt text, Markdown examples, and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local SQLite database populated from bundled agent prompt data.]

## Skill Version(s):

1.0.3 (source: server release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
