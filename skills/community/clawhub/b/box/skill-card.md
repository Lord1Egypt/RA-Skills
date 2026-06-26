## Description: <br>
Box API integration with managed OAuth for managing files, folders, collaborations, shared links, and cloud storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to access Box through Maton's managed OAuth gateway for file, folder, sharing, collaboration, search, trash, webhook, and upload workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage, share, and delete Box files through the user's authorized Maton/Box connection. <br>
Mitigation: Require explicit user confirmation before deleting items, permanently deleting trash, creating open shared links, or changing collaborators. <br>
Risk: Multiple active Box connections can cause the wrong account or workspace to be used. <br>
Mitigation: Authorize only the intended Box account and set the Maton-Connection header when more than one Box connection exists. <br>
Risk: The MATON_API_KEY is a sensitive credential required for gateway access. <br>
Mitigation: Store the key in the environment, avoid exposing it in prompts or logs, and rotate it if disclosure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/box) <br>
- [API Gateway Skill](https://clawhub.ai/byungkyu/api-gateway) <br>
- [Box API Reference](https://developer.box.com/reference) <br>
- [Box Developer Documentation](https://developer.box.com/guides) <br>
- [Box Authentication Guide](https://developer.box.com/guides/authentication) <br>
- [Box SDKs and Tools](https://developer.box.com/sdks-and-tools) <br>
- [Maton](https://maton.ai) <br>
- [Maton Control Plane](https://ctrl.maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance, API request guidance] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an explicitly authorized Box OAuth connection.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter metadata.version is 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
