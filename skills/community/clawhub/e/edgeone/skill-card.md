## Description: <br>
Deploy HTML content to EdgeOne Pages, return the public URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcp](https://clawhub.ai/user/mcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to publish provided HTML or text to EdgeOne Pages and receive a public URL for the deployed content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted HTML or text is deployed to a public URL. <br>
Mitigation: Deploy only content intended for public access, and exclude secrets, tokens, proprietary code, private notes, and internal files. <br>
Risk: The skill relies on mcporter and an EdgeOne deployment endpoint to publish content. <br>
Mitigation: Use it only in environments where mcporter and the EdgeOne endpoint are approved, and review the content before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mcp/edgeone) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown with shell commands and returned URL text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Publishes the submitted HTML or text as publicly accessible content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
