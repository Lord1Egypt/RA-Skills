## Description:

Fetches recent arXiv cs.AI paper metadata, translates titles and abstracts into Simplified Chinese, and appends a Markdown table to a configured Obsidian note.

This skill is ready for commercial/non-commercial use.

## Publisher:

[senrylee](https://clawhub.ai/user/senrylee)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and Obsidian users use this skill to collect the latest arXiv AI papers, translate their titles and abstracts into Simplified Chinese, and add them to a daily literature note.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write generated paper summaries into the wrong Obsidian vault or folder if local configuration is left at defaults or set incorrectly.

Mitigation: Configure the target vault, folder, and note before use, then run with DRY_RUN=1 to confirm the destination and generated content before allowing writes.

Risk: Paper metadata from the configured RSS feed is translated through the local Claude CLI and then inserted into an Obsidian note.

Mitigation: Use trusted RSS sources and review generated note content, especially because the security guidance says generated content is not strongly sanitized.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/senrylee/skills/arxiv-to-obsidian)
- [arXiv cs.AI RSS feed](https://export.arxiv.org/rss/cs.AI)
- [Obsidian](https://obsidian.md/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown table appended through Obsidian CLI, with optional shell command guidance and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output includes up to 10 papers with translated title, translated abstract, original link, and publication date.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
