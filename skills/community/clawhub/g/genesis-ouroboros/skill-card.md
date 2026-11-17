## Description:

Genesis Ouroboros helps agents clarify requirements, review existing approaches, and generate a constitution-centered scaffold for a new self-evolving agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckyz10](https://clawhub.ai/user/luckyz10)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to turn a request for a new agent into a minimal scaffold with AGENTS.md, CLAUDE.md, and one or two core skills after requirement clarification and existing-solution review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated agents may persist self-updating instructions or scripts without enough approval or safety boundaries.

Mitigation: Set distill_mode to confirm before use, review every generated AGENTS.md, CLAUDE.md, skill file, and script, and keep generated scaffolds in a contained project.

Risk: Generated scaffolds may retain secrets, personal data, credentials, or unreviewed web or user content.

Mitigation: Do not allow generated agents to persist sensitive or unreviewed content, and remove that material during review before deployment.

## Reference(s):

- [Server-resolved source provenance](https://github.com/LuckyZ10/genesis-ouroboros/tree/main/genesis-ouroboros)
- [ClawHub skill page](https://clawhub.ai/luckyz10/skills/genesis-ouroboros)
- [Publisher profile](https://clawhub.ai/user/luckyz10)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown files and scaffolded skill directories with concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates only the requested essentials: AGENTS.md, CLAUDE.md, and one to two core skills.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
