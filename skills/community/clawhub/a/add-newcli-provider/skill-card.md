## Description: <br>
Configures OpenClaw to use NewCLI as a provider for Claude, GPT, and Gemini models, including provider definitions, aliases, fallback routing, validation, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jooey](https://clawhub.ai/user/jooey) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw administrators use this skill to add NewCLI-backed Claude, GPT, and Gemini model routes to an OpenClaw configuration and verify that each provider works. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reroute OpenClaw model traffic through NewCLI/code.newcli.com, a third-party proxy. <br>
Mitigation: Review the provider and fallback edits before applying them and confirm that organizational policy allows prompts, code, and metadata to pass through the proxy. <br>
Risk: The workflow handles API keys and edits the OpenClaw configuration file. <br>
Mitigation: Avoid exposing raw API keys in shell history or shared logs, and restrict permissions on the OpenClaw config file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jooey/add-newcli-provider) <br>
- [NewCLI service](https://code.newcli.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration snippets and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OpenClaw provider, alias, fallback, validation, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
3.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
