## Description: <br>
Automatically scrapes, categorizes, and summarizes X bookmarks into actionable insights delivered inline, to a local archive, or to a configured messaging channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adambrainai](https://clawhub.ai/user/adambrainai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and individual users use this skill to turn saved X bookmarks into categorized summaries, searchable local archives, and optional daily reports. It is intended for users who want an agent to organize personal bookmark collections and surface useful items later. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and summarizes personal X bookmarks, which may include sensitive personal or work information. <br>
Mitigation: Install only if this access is acceptable, review summaries before sharing them, and periodically delete or prune the local bookmark archive. <br>
Risk: Webhook URLs and delivery channels can expose summaries if configured insecurely. <br>
Mitigation: Keep webhook URLs in environment variables, avoid committing secrets to files, and choose private delivery channels. <br>
Risk: Raw X session cookies or credentials could be mishandled if pasted into prompts or configuration files. <br>
Mitigation: Use the bird CLI for authentication and do not paste raw cookies or tokens into files or agent prompts. <br>


## Reference(s): <br>
- [ClawHub listing: ADHD X Bookmark Analyzer](https://clawhub.ai/adambrainai/adhd-bookmark-analyzer) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [bookmark-rules.md](artifact/bookmark-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with optional shell commands, configuration snippets, and local JSON archive files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read X bookmarks, write a local bookmark archive, and send summaries to user-configured delivery channels.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
