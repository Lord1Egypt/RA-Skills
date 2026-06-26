## Description: <br>
URL or long-form text to social carousel generator via local CLI + MCP endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suinia](https://clawhub.ai/user/suinia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use Clawvisual to convert URLs or long-form text into social carousel jobs through a local CLI and MCP service, then poll and revise generated carousel output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be stored in plaintext local configuration. <br>
Mitigation: Use scoped or disposable keys and prefer environment variables over persistent CLI configuration where possible. <br>
Risk: The MCP endpoint can be pointed away from localhost. <br>
Mitigation: Keep CLAWVISUAL_MCP_URL set only to localhost or another trusted endpoint before running commands. <br>
Risk: Initialization or conversion can leave a local service running. <br>
Mitigation: Review process state after use and stop the service when the workflow is complete. <br>
Risk: Raw MCP tool-call access can invoke low-level tool behavior. <br>
Mitigation: Review raw tool names and JSON arguments before using the generic call command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suinia/clawvisual-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/suinia) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [JSON returned to stdout by CLI commands, with command guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Job-based workflow with status polling for conversion, revision, and cover regeneration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
