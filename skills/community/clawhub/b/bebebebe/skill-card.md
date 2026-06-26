## Description: <br>
Set up Orthogonal for an AI agent to access premium APIs, curated skills, and OAuth-connected integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yshuolu](https://clawhub.ai/user/yshuolu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install and configure the Orthogonal CLI, discover curated skills and APIs, authenticate with an API key, and run Orthogonal integrations from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad API and integration access can allow paid API calls and actions in connected accounts. <br>
Mitigation: Require manual approval before paid API calls or actions that send messages, create calendar events, update repositories, or modify Drive, Sheets, Notion, Gmail, or Slack data. <br>
Risk: API keys and OAuth credentials can be exposed or overused if stored insecurely. <br>
Mitigation: Use secure secret storage or environment variables, protect the Orthogonal API key, and connect only required OAuth services. <br>
Risk: Installed skills and marketplace APIs may introduce separate behavior and permissions. <br>
Mitigation: Review and scan each added skill or API before deployment and verify parameters with `orth api show` before running new endpoints. <br>


## Reference(s): <br>
- [Orthogonal homepage](https://orthogonal.com) <br>
- [Orthogonal documentation](https://docs.orthogonal.com) <br>
- [Orthogonal skills](https://orthogonal.com/skills) <br>
- [Orthogonal API discovery](https://orthogonal.com/discover) <br>
- [Orthogonal integrations](https://orthogonal.com/integrations) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CLI setup, authentication, API discovery, billing, integration guidance, and support links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
