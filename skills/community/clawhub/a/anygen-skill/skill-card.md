## Description: <br>
AnyGen is an AI-powered content creation suite that uses the AnyGen CLI to generate slides, documents, diagrams, websites, images, research, financial analysis, and other content server-side. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[logictortoise](https://clawhub.ai/user/logictortoise) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content teams use this skill through an agent to create presentations, documents, diagrams, websites, images, research reports, data visualizations, and financial analysis outputs with the AnyGen hosted service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill tells the agent to install the additional anygen-workflow-generate skill when it is not available, which can persistently change agent behavior. <br>
Mitigation: Review and approve that separate skill and its source/version before allowing installation. <br>
Risk: The skill uses a hosted AnyGen service for content generation. <br>
Mitigation: Use AnyGen only for content appropriate to send to that service, and use a revocable API key when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/logictortoise/anygen-skill) <br>
- [Publisher profile](https://clawhub.ai/user/logictortoise) <br>
- [AnyGen service](https://www.anygen.io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated content outputs from the AnyGen CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ANYGEN_API_KEY and the anygen CLI; generated content is produced by the hosted AnyGen service.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
