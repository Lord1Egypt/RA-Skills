## Description: <br>
Inspect containers, logs, and images via podman. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect local containers, logs, and images through podman while preserving guardrails around command injection and sensitive container data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Container identifiers can contain shell metacharacters that may lead to command injection if interpolated unsafely. <br>
Mitigation: Quote container names and IDs in shell commands, and refuse requests that clearly attempt command injection. <br>
Risk: Container logs and inspect output can contain secrets or infrastructure details. <br>
Mitigation: Display container data locally in the terminal, avoid bulk environment-variable disclosure, and do not persist output to disk unless explicitly requested. <br>
Risk: Sending logs, inspect output, environment variables, or image metadata to network endpoints can leak sensitive data. <br>
Mitigation: Keep container data on the local machine and refuse piping or transmitting it with tools such as curl, wget, or netcat. <br>
Risk: The examples use docker-ctl while the declared runtime dependency is podman. <br>
Mitigation: Confirm that docker-ctl exists on the target system or deliberately adapt commands to podman before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/snazar-faberlens/docker-ctl-hardened) <br>
- [Publisher profile](https://clawhub.ai/user/snazar-faberlens) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/docker-ctl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides local inspection guidance; container data should stay in-terminal unless the user explicitly requests file output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
