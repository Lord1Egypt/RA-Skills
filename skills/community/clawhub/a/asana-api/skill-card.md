## Description: <br>
Asana API integration with managed OAuth for accessing tasks, projects, workspaces, users, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage Asana work items, projects, workspaces, users, and webhooks through Maton-managed OAuth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill brokers Asana API traffic through Maton and requires a Maton API key. <br>
Mitigation: Install only if you trust Maton, connect only the intended Asana account, and keep MATON_API_KEY out of logs and shared terminals. <br>
Risk: Create, update, delete, and webhook actions can modify Asana resources. <br>
Mitigation: Confirm the target resource, account connection, and intended effect with the user before executing write or webhook operations. <br>
Risk: Multiple Asana connections can route requests to the wrong account. <br>
Mitigation: Specify the intended connection ID when more than one active Asana connection exists. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/asana-api) <br>
- [Asana API Documentation](https://developers.asana.com) <br>
- [Asana API Reference](https://developers.asana.com/reference) <br>
- [Asana LLM Reference](https://developers.asana.com/llms.txt) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with CLI commands, API paths, JSON examples, and Python or JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and an active Asana OAuth connection; API responses are JSON.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
