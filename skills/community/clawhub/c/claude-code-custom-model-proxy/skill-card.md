## Description: <br>
Configure Claude Code to work with custom model providers (like MiniMax, OpenAI-compatible APIs). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mark-heartflow](https://clawhub.ai/user/mark-heartflow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Claude Code for OpenAI-compatible custom model providers through a local Anthropic-to-OpenAI proxy, and to troubleshoot model validation, streaming, encoding, and connection issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The proxy includes a hardcoded third-party endpoint and API key. <br>
Mitigation: Remove the embedded key, configure a trusted upstream endpoint explicitly, and supply credentials through a safer secret mechanism before use. <br>
Risk: Prompt or repository content may be logged by the proxy. <br>
Mitigation: Disable request-body logging and avoid using the proxy with sensitive repositories or prompts unless logging and retention are controlled. <br>
Risk: Claude Code traffic can remain redirected through the local proxy after setup. <br>
Mitigation: Stop the proxy and revert the Claude Code base URL or environment configuration when the custom provider workflow is no longer needed. <br>
Risk: Local proxy access and permissive CORS can broaden exposure on the host. <br>
Mitigation: Bind only to localhost, restrict local access and CORS where possible, and run the proxy only for the duration needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mark-heartflow/claude-code-custom-model-proxy) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Proxy Script](artifact/scripts/claude_code_proxy.py) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON, Bash, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local proxy settings, environment variables, and troubleshooting commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
