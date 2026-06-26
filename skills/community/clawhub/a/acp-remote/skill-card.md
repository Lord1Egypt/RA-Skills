## Description: <br>
Connect to remote ACP server and execute commands via imclaw-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallnest](https://clawhub.ai/user/smallnest) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure imclaw-cli for connecting to a remote ACP server, sending prompts to a selected agent, reusing sessions, and controlling remote file or shell access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote ACP connections can execute agent-driven shell commands or file operations on the target environment. <br>
Mitigation: Use only trusted servers, restrict --allowed-tools and --cwd, and avoid --approve-all unless the environment is isolated and remote file or shell changes are acceptable. <br>
Risk: Default examples include ws:// transport and servers may be started without an auth token. <br>
Mitigation: Prefer wss:// or an SSH tunnel, bind servers to localhost or private interfaces where possible, and require a strong token for remote access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smallnest/acp-remote) <br>
- [imclaw project homepage](https://github.com/smallnest/imclaw) <br>
- [imclaw releases API](https://api.github.com/repos/smallnest/imclaw/releases/latest) <br>
- [imclaw install script](https://raw.githubusercontent.com/smallnest/imclaw/main/scripts/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command-line parameter tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports text, JSON, or quiet output from imclaw-cli depending on the selected command options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
