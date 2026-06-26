## Description: <br>
Guides agents in using the Ex-Coder Autonomy CLI for model-backed coding workflows, sub-agent delegation, session management, snapshots, LSP support, HTTP API use, and MCP integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lordmahakaal](https://clawhub.ai/user/lordmahakaal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to operate Ex-Coder Autonomy through structured sub-agent workflows, choose external models, manage long sessions, and apply CLI features such as snapshots, LSP diagnostics, MCP tools, and the local HTTP API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad coding-agent workflows with file writes, shell commands, package installation, MCP tools, and HTTP API control. <br>
Mitigation: Start in read-only or plan mode, scope filesystem and MCP access to the active project, and avoid exposing the HTTP API beyond localhost without strong authentication. <br>
Risk: Snapshot revert and cleanup examples can modify or discard workspace changes. <br>
Mitigation: Review snapshot diffs and changed-file lists before reverting or cleaning snapshots. <br>
Risk: The artifact includes examples for configuring API keys and installing external npm packages. <br>
Mitigation: Verify package provenance and keep API keys scoped, revocable, and out of committed files or shared logs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lordmahakaal/excoder-autonomy) <br>
- [Excoder GitHub](https://github.com/ex-coder/ex-coder) <br>
- [OpenRouter API Docs](https://openrouter.ai/docs) <br>
- [OpenRouter Models](https://openrouter.ai/models) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions, Code] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command examples that install packages, configure API keys, launch a local HTTP API, connect MCP servers, or revert snapshots.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
