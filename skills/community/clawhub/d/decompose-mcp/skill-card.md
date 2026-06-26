## Description: <br>
Decompose any text into classified semantic units: authority, risk, attention, and entities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[echology-io](https://clawhub.ai/user/echology-io) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers and document-analysis teams use this skill to classify text, specifications, contracts, policies, and regulations into structured semantic units before downstream review or agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional URL decomposition tool performs outbound HTTP requests to user-specified addresses. <br>
Mitigation: Use local text decomposition when network access is not needed, and avoid passing URLs that the agent should not contact. <br>
Risk: Sensitive environments may require stronger supply-chain controls for third-party packages. <br>
Mitigation: Review the decompose-mcp package before deployment and pin the package version during installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/echology-io/decompose-mcp) <br>
- [Documentation](https://echology.io/decompose) <br>
- [PyPI package](https://pypi.org/project/decompose-mcp/) <br>
- [When Regex Beats an LLM](https://echology.io/blog/regex-beats-llm) <br>
- [Why Your Agent Needs a Cognitive Primitive](https://echology.io/blog/cognitive-primitive) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent tool output is structured JSON containing classified semantic units when the MCP tools are used.] <br>

## Skill Version(s): <br>
0.1.2 (source: claw.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
