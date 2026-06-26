## Description: <br>
Web search grounding via Azure Foundry and Bing Grounding Search tool for agents that need up-to-date answers with URL citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bowang306](https://clawhub.ai/user/bowang306) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run real-time web searches through Azure AI Agents and Bing Grounding, then return synthesized answers with source URL citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User queries and surrounding context may be processed by Azure and Bing services. <br>
Mitigation: Do not use the skill with secrets, confidential internal data, personal data, or regulated information unless organizational policy permits that cloud processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bowang306/azure-bing-grounding) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Raw JSON or Markdown with URL citations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Azure AI Foundry project configuration, Bing Grounding connection ID, model deployment name, and Azure credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
