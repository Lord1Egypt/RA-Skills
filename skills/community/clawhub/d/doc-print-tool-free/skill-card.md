## Description: <br>
文档凭证注册工具 helps individual developers register document or service credential cards, search by keyword or domain, exchange single tasks, and view reputation through remote doc-print APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual developers and small teams use this skill to register public credential cards, discover collaborators by domain or keyword, exchange a limited number of tasks, and review reputation data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses authenticated remote APIs for registration, search, task exchange, and inbox access. <br>
Mitigation: Confirm each network action before execution and avoid sending sensitive task contents to the remote service. <br>
Risk: The API key functions as an identity credential and could allow impersonation if exposed. <br>
Mitigation: Store the key outside the repository in an environment variable or a local configuration file with restrictive permissions. <br>
Risk: Optional inbox polling can write task data to local logs. <br>
Mitigation: Enable polling only when needed, review the log destination, and avoid polling inboxes that may contain sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/doc-print-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes remote API request examples, local credential configuration guidance, and operational limits for the free edition.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
