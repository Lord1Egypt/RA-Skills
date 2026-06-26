## Description: <br>
AI-powered content monitoring and summarization tool that monitors RSS feeds, blogs, and news sources with automatic summarization and daily digest generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[su707181393-del](https://clawhub.ai/user/su707181393-del) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to monitor selected RSS feeds, blogs, and news sources, summarize newly fetched articles, and generate a digest for review or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The npm package source and installed dependencies must be trusted before installation. <br>
Mitigation: Install only from a trusted package source and review package provenance before use. <br>
Risk: Configured feeds can cause the tool to fetch linked article URLs. <br>
Mitigation: Add only feeds and sources that the user intends to monitor. <br>
Risk: The --output option writes the digest to the exact path provided by the user. <br>
Mitigation: Choose output paths deliberately and avoid overwriting important files. <br>
Risk: Source history and seen URLs persist in local configuration storage. <br>
Mitigation: Review or remove ~/.config/content-watcher/ when source history should not persist. <br>


## Reference(s): <br>
- [Content Watcher ClawHub release page](https://clawhub.ai/su707181393-del/content-watcher) <br>
- [Publisher profile](https://clawhub.ai/user/su707181393-del) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown digest or console text, with CLI commands and JSON configuration snippets in documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write a digest to a user-specified output path and persists source configuration and seen URLs under ~/.config/content-watcher/.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
