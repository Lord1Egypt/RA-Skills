## Description: <br>
Provides a Node.js command-line Baidu web search tool that returns ranked search results with titles, summaries, and links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wsh66660](https://clawhub.ai/user/wsh66660) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and agent builders use this skill to run Baidu web searches from a Node.js script and return ranked result text for downstream review or summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Baidu and may expose secrets, credentials, or confidential project details. <br>
Mitigation: Avoid using sensitive or confidential information as search queries, and notify users that queries are sent to Baidu. <br>
Risk: The documented execSync integration can allow crafted search queries to execute unintended local shell commands. <br>
Mitigation: Use execFile or spawn with an argument array, validate the requested result count, and avoid constructing shell command strings from user input. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/wsh66660/baidu-search-node) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [package.json](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Code] <br>
**Output Format:** [Plain text search results with setup guidance in Markdown and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include rank, title, abstract, and URL; result count and debug mode are command-line options.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
