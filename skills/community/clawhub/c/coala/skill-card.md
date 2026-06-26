## Description: <br>
Guides use of the coala-client CLI for LLM chat, MCP servers, CWL toolset imports, MCP tool calls, and skill loading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hubentu](https://clawhub.ai/user/hubentu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to configure and operate coala-client for interactive or single-prompt LLM chat, MCP tool management, and skill import workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing coala-client or importing remote MCP toolsets and skills can persist files under local coala configuration paths and influence later chats. <br>
Mitigation: Install the CLI and imports only from trusted sources, review imported ZIPs, CWL files, and skills before loading them, and remove unneeded entries from local coala configuration. <br>
Risk: Provider API keys may be exposed if copied into shared logs, committed files, or improperly handled configuration. <br>
Mitigation: Keep provider keys in protected environment variables or local-only config, avoid sharing `~/.config/coala/env`, and rotate keys if exposure is suspected. <br>


## Reference(s): <br>
- [Coala Client ClawHub release](https://clawhub.ai/hubentu/coala) <br>
- [Coala Client homepage](https://github.com/coala-info/coala_client) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local coala configuration paths, provider environment variables, and MCP or skill import commands.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
