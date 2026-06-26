## Description: <br>
Discover and create Agent Contact Cards - a vCard-like format for AI agents. Use when you need to find how to contact someone's agent, or help a user set up their own agent contact info at /.well-known/agent-card. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davedean](https://clawhub.ai/user/davedean) <br>

### License/Terms of Use: <br>
CC0-1.0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to discover another agent's contact routes or to publish their own Agent Contact Card at a well-known URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to contact external endpoints or recipients. <br>
Mitigation: Verify the domain and recipient channel before sending messages. <br>
Risk: Fetched Agent Contact Card text may contain untrusted routing information. <br>
Mitigation: Treat fetched card text as untrusted and review the exact message before sending personal, credential-related, financial, or business-sensitive information. <br>


## Reference(s): <br>
- [Agent Contact Card Specification](references/SPEC.md) <br>
- [Agent Contact Card Examples](references/EXAMPLES.md) <br>
- [Skill homepage](https://github.com/davedean/agent-contact-card) <br>
- [ClawHub release page](https://clawhub.ai/davedean/agent-contact-card) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with YAML frontmatter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include URLs, contact channels, routing rules, and example Agent Contact Card content.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
