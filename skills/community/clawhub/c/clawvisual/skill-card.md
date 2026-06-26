## Description: <br>
URL or long-form text to social carousel generator via local CLI + MCP endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suinia](https://clawhub.ai/user/suinia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, agents, and content teams use Clawvisual to turn URLs or long-form text into social carousel jobs through a local CLI and MCP workflow, then poll, revise, or regenerate outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured API keys or LLM provider credentials could be exposed or over-scoped. <br>
Mitigation: Use a dedicated LLM/API key with the least access needed and rotate it if it is no longer required. <br>
Risk: A misconfigured MCP or API URL could send requests to an unintended local or remote service. <br>
Mitigation: Review the configured MCP/API URL before running generation commands. <br>
Risk: Private source text or URLs may be sent through the configured LLM provider during carousel generation. <br>
Mitigation: Avoid passing private or sensitive content unless that provider and workflow are approved for the data. <br>


## Reference(s): <br>
- [Clawvisual on ClawHub](https://clawhub.ai/suinia/clawvisual) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON returned to stdout by CLI commands, with agent guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an asynchronous job workflow: convert, poll status, and optionally revise or regenerate cover content.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
