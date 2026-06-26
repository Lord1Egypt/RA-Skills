## Description: <br>
Create and publish social media launches via the Dropspace API, including launch creation, persona management, post analytics, scheduling, and AI-assisted content for multiple social platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jclvsh](https://clawhub.ai/user/jclvsh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through Dropspace workflows for drafting, scheduling, publishing, and measuring social media launches. It is suited for users who intend to connect an agent to a Dropspace account with an appropriately scoped API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward publishing or scheduling content on connected social accounts. <br>
Mitigation: Use a least-privilege Dropspace API key and add the publish scope only when autonomous publishing is explicitly intended. <br>
Risk: The skill documents destructive and administrative operations, including deleting posts, managing API keys, and creating or rotating webhooks. <br>
Mitigation: Review commands before execution and grant delete or admin scopes only for workflows that require those actions. <br>
Risk: The skill includes guidance for querying attribution data and using payment headers. <br>
Mitigation: Confirm that the agent is allowed to access attribution data or payment flows before permitting related commands. <br>


## Reference(s): <br>
- [Dropspace skill page](https://clawhub.ai/jclvsh/dropspace) <br>
- [Publisher profile](https://clawhub.ai/user/jclvsh) <br>
- [Dropspace documentation](https://www.dropspace.dev/docs) <br>
- [Dropspace machine-readable docs](https://www.dropspace.dev/llms.txt) <br>
- [Dropspace OpenAPI specification](https://www.dropspace.dev/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline curl commands, API request examples, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Dropspace API calls that publish, delete, manage webhooks or API keys, query analytics, or inspect attribution data.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
