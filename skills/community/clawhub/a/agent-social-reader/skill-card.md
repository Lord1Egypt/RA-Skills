## Description:

Agent Social Reader helps an agent read, summarize, analyze, extract, and explicitly archive specific public web, social media, video, article, and RSS links across major platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hermiod99-vibe](https://clawhub.ai/user/hermiod99-vibe)

### License/Terms of Use:

MIT-0

## Use Case:

External users, knowledge workers, product managers, and agent developers use this skill to retrieve and summarize specific public links from web and social platforms, then archive the current item to Notion, Obsidian, or ima only when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and destination credentials could be exposed through chat, memory, shell profiles, Custom Instructions, or plaintext local configuration.

Mitigation: Prefer platform secret storage or environment variables, use plaintext local configuration only after explicit user approval, and never print or archive full tokens.

Risk: Archive actions can send retrieved content to Notion or ima, or write files into an Obsidian vault.

Mitigation: Perform saves only when the current user request explicitly names the destination, and confirm the target database, knowledge base, or vault before writing.

Risk: Bundled save scripts and optional install helpers may need hardening before use with important files or knowledge bases.

Mitigation: Review and harden the scripts before deployment, and avoid optional zip helpers unless their contents and source are verified.

Risk: Temporary media cleanup could delete files if file matching is too broad.

Mitigation: Limit cleanup to /tmp files with the asr_ prefix, preview matching files first, and delete only after explicit user confirmation.

## Reference(s):

- [Agent Social Reader homepage](https://github.com/hermiod99-vibe/Agent-Social-Reader)
- [Platform Tool Details](references/tool-details.md)
- [Save Scripts](references/save-scripts.md)
- [AgentLens API](https://agentlensapi.io)
- [AgentLens pricing](https://agentlensapi.io/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown and plain text with inline code blocks, API request examples, and optional archive file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce temporary media files under /tmp with the asr_ prefix and user-requested Markdown archives for Notion, Obsidian, or ima.]

## Skill Version(s):

2.0.1 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
