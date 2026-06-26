## Description: <br>
Explains how Openclaw should use Codex CLI as a non-interactive coding engine for installation, authentication, sandboxing, workspace setup, troubleshooting, and `codex exec` task runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minchocoin](https://clawhub.ai/user/minchocoin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation maintainers use this skill to answer practical questions about running Codex CLI through Openclaw. It focuses on safe non-interactive `codex exec` usage, authentication recovery, workspace scoping, approvals, sandboxing, and command examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad workspace permissions or additional writable directories can expose unrelated files to agent edits. <br>
Mitigation: Use dedicated workspaces, keep sandboxing enabled where practical, and avoid broad `--add-dir` paths. <br>
Risk: Non-interactive approvals and API-key authentication can grant more access than intended in shared or uncontrolled environments. <br>
Mitigation: Use `Always allow`, `-a never`, and API-key login only in controlled environments where the granted access is understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/minchocoin/codex-cli-exec) <br>
- [Publisher profile](https://clawhub.ai/user/minchocoin) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; does not execute commands itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
