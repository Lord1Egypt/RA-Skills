## Description: <br>
Guides users through binding 1688 distribution buyer shops in the Newton Electron client, including platform selection, authorization login, and shop binding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators and support agents use this skill to guide a user through selecting a distribution platform, authorizing access, and completing shop binding inside the Newton client. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive 1688 API or OpenClaw configuration credentials. <br>
Mitigation: Install and run it only in trusted environments, provide credentials through approved configuration, and rotate credentials if exposure is suspected. <br>
Risk: The shop-binding flow opens authorization pages and asks the user to log in or approve access. <br>
Mitigation: Verify the destination domain and requested authorization scope before logging in or approving access. <br>
Risk: The workflow queries shop and tool metadata through the 1688 gateway. <br>
Mitigation: Use the skill only when the publisher and the 1688 gateway are trusted for the intended shop-binding workflow. <br>


## Reference(s): <br>
- [Command Reference](references/commands.md) <br>
- [Output Schema](references/output_schema.md) <br>
- [API Reference](references/api_reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/1688aiinfra/1688-distribution-shop-bind-newton) <br>
- [Publisher Profile](https://clawhub.ai/user/1688aiinfra) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON responses with Markdown user guidance and optional browser action parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stdout carries structured responses; stderr may carry tracking logs.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
