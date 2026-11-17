## Description:

Monitors a Moltbook feed for new agents and posts, tracks keyword matches, and saves useful findings to Open Notebook or a local markdown file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nantes](https://clawhub.ai/user/nantes)

### License/Terms of Use:


## Use Case:

Agent operators and developers use this skill to monitor Moltbook activity, identify new or interesting agents by author or keyword, and preserve selected notes for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Moltbook API credentials may be exposed if copied into prompts, scripts, logs, or committed files.

Mitigation: Store the Moltbook API key in a secure environment variable and avoid hardcoding it in reusable files.

Risk: Notebook saves can create persistent records of feed content and user notes.

Mitigation: Confirm the target notebook ID and review saved entries when using Open Notebook or the local markdown fallback.

Risk: The optional Open Notebook API endpoint could send notes to an unexpected service if misconfigured.

Mitigation: Use a local or otherwise trusted Open Notebook API URL before enabling notebook saves.

## Reference(s):

- [Agent Watcher Skill on ClawHub](https://clawhub.ai/nantes/skills/agent-watcher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell and PowerShell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save selected notes to Open Notebook through a configured local API or append them to a local markdown file.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact version section states 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
