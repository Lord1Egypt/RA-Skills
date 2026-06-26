## Description: <br>
Generates a structured Chinese morning brief about LLM and agent industry news from RSS, search, and arXiv sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[519989179](https://clawhub.ai/user/519989179) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and AI-industry readers use this skill to generate a daily Chinese Markdown brief that summarizes selected AI news, KOL posts, and papers with source links. It can also be scheduled or paired with delivery tooling when recurring external distribution is intended. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTTPS certificate verification is disabled during network fetching. <br>
Mitigation: Restore default certificate and hostname verification before running the skill against external sources. <br>
Risk: Unattended delivery can send generated briefs to an external chat destination. <br>
Mitigation: Enable push delivery only after the operator explicitly configures and reviews the recipient. <br>
Risk: Sensitive environment tokens may be available to the skill. <br>
Mitigation: Provide only the tokens required for the selected run mode and remove unused credential access such as optional GitHub tokens. <br>
Risk: Recurring cron execution can repeatedly fetch and distribute content without further review. <br>
Mitigation: Install scheduled jobs only when recurring delivery is intended and keep logs available for audit. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/519989179/ai-industry-morning-brief) <br>
- [Publisher Profile](https://clawhub.ai/user/519989179) <br>
- [Source Configuration](artifact/config/sources.json) <br>
- [Prompt Templates](artifact/config/prompts.md) <br>
- [Sample Output](artifact/samples/sample-output.md) <br>
- [Installation Guide](artifact/install.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with source links, optional shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write dated Markdown reports and optional MP3 narration files when supporting tooling is configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
