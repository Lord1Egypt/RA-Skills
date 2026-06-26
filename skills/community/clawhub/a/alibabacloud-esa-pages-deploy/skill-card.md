## Description: <br>
Deploy HTML pages, static directories, or custom edge functions to Alibaba Cloud ESA edge nodes and manage Edge KV for distributed key-value storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to deploy web pages, static site builds, edge functions, and Edge KV data to Alibaba Cloud ESA. It is intended for workflows where an agent may propose or run ESA deployment and management commands using Alibaba Cloud credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live production changes in Alibaba Cloud ESA. <br>
Mitigation: Use a dedicated least-privilege RAM role where possible, verify the active Alibaba Cloud account before running scripts, and review deployment content before production use. <br>
Risk: Deployment URLs may include short-lived esa_er_token values that grant access. <br>
Mitigation: Treat token-bearing URLs as secrets and do not post them to logs, chats, screenshots, or CI output. <br>
Risk: The skill requires sensitive Alibaba Cloud credentials. <br>
Mitigation: Use the Alibaba Cloud default credential chain with scoped credentials and confirm credential availability before deployment. <br>


## Reference(s): <br>
- [Functions & Pages API](references/pages-api.md) <br>
- [Edge KV API](references/kv-api.md) <br>
- [Alibaba Cloud SDK credential chain](https://www.alibabacloud.com/help/en/sdk/developer-reference/v2-manage-access-credentials) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance, API Calls] <br>
**Output Format:** [Markdown with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands or script invocations that make live Alibaba Cloud ESA changes when executed.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
