## Description: <br>
Automation skill package for multi-engine web search, JSON search-result output, and local reflection notes with reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xunet2025](https://clawhub.ai/user/xunet2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to run multi-engine searches, save ranked results as JSON, record lessons learned, and generate local reflection reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to external search engines. <br>
Mitigation: Do not submit secrets, credentials, private project details, or sensitive personal data as search terms. <br>
Risk: Reflection entries are stored locally under ~/.qclaw/memory. <br>
Mitigation: Avoid recording sensitive personal data, credentials, or private project details in reflection notes, and review local memory files before sharing the environment. <br>
Risk: The skill can help search for additional skills to install. <br>
Mitigation: Review any additional skill and its security status before installing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xunet2025/automation-skill) <br>
- [Publisher profile](https://clawhub.ai/user/xunet2025) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON search results, and Markdown reflection reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search queries may be sent to external search engines; reflection notes are stored locally under ~/.qclaw/memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
