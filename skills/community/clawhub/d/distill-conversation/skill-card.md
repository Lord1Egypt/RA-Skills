## Description:

Alembic distills ChatGPT shared links or pasted LLM conversations into structured, Obsidian-friendly Markdown knowledge notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyang-yao75](https://clawhub.ai/user/yuyang-yao75)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, external users, and knowledge workers use this skill to turn long AI conversations into reusable concept notes for Obsidian or another Markdown directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read a selected note vault for conflict checks and write Markdown files to the selected output location.

Mitigation: Install only when that local access is acceptable, set the output directory deliberately, and review the generated files.

Risk: ChatGPT shared-link parsing depends on user-supplied links and may fetch shared page HTML.

Mitigation: Use HTTPS ChatGPT share links from trusted sources, avoid untrusted links, or use pasted text or local HTML when network access is not desired.

Risk: Generated notes may omit nuance or introduce misleading summaries from the source conversation.

Mitigation: Review generated notes before relying on them or merging them into a knowledge base.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuyang-yao75/skills/distill-conversation)
- [Artifact README.en.md](artifact/README.en.md)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown knowledge notes with YAML frontmatter; optional JSON parse output for ChatGPT shared links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes one Markdown file per selected keyword to --output-dir, OBSIDIAN_VAULT_PATH/00.Inbox, or the current directory.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
