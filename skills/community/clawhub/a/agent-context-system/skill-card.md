## Description:

Agent Context System helps AI coding agents maintain persistent project context through a shared AGENTS.md file and a gitignored local scratchpad.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreagriffiths11](https://clawhub.ai/user/andreagriffiths11)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use this skill to set up and maintain shared, reviewable project context for AI coding agents while keeping personal session notes local and gitignored.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent project memory can capture secrets, private incident details, or misleading session notes.

Mitigation: Review proposed .agents.local.md entries before writing and avoid storing secrets or private operational details.

Risk: Promotion workflows can move unreviewed scratchpad content into shared AGENTS.md instructions.

Mitigation: Manually review every AGENTS.md promotion and treat scratchpad content as session data until accepted by a human.

Risk: The repository publishing script can push private files or credentials from a working tree.

Mitigation: Do not run scripts/publish-template.sh from a tree that may contain credentials or private files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/andreagriffiths11/skills/agent-context-system)
- [LangChain: Context Engineering for Agents](https://blog.langchain.com/context-engineering-for-agents/)
- [HumanLayer: Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [GitHub: How to Write a Great AGENTS.md](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- [Vercel: AGENTS.md Outperforms Skills](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- [Anthropic: Equipping Agents for the Real World with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local scratchpad updates and setup commands; user review is expected before writing persistent context.]

## Skill Version(s):

1.3.2 (source: ClawHub release metadata; skill frontmatter lists 1.3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
