## Description: <br>
Collects AI and automotive industry news from specified sources and organizes findings into structured Excel reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rouclaw](https://clawhub.ai/user/rouclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to gather recent AI and automotive industry developments, verify dates and sources, and produce structured spreadsheet reports for daily or weekly briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs fresh web searches and writes spreadsheet report files. <br>
Mitigation: Review Bash, Read, and Write permissions and confirm output paths before execution. <br>
Risk: Optional helper-skill installation commands or related API keys can expand the agent's access. <br>
Mitigation: Install helper skills and configure credentials only when they are needed and trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rouclaw/ai-content-collector) <br>
- [Publisher profile](https://clawhub.ai/user/rouclaw) <br>
- [Channel reference](artifact/references/channels.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated Excel or CSV report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report rows include category, source, title, publication date, summary, primary link, and corroborating sources.] <br>

## Skill Version(s): <br>
1.10.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
