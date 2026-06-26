## Description: <br>
Run curl requests safely in a sandbox, supporting GET/POST/HTTP headers, with complete network isolation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guyoung](https://clawhub.ai/user/guyoung) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to let an agent make curl-like HTTP requests through a WASM sandbox with per-host outbound network controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and runs an unpinned WASM component. <br>
Mitigation: Verify or pin the downloaded WASM component before allowing the agent to run it. <br>
Risk: User-provided headers and request bodies can be sent to external hosts. <br>
Mitigation: Use only trusted destinations and avoid sending secrets unless they are intended for that host. <br>
Risk: Outbound network access is part of normal skill behavior. <br>
Mitigation: Review before installing and set allowed outbound hosts to the exact destination required for the request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guyoung/boxed-curl) <br>
- [Publisher profile](https://clawhub.ai/user/guyoung) <br>
- [WASM component download](https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/boxed-curl/files/boxed_curl_component.wasm) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell and JavaScript tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces wasm-sandbox-run and wasm-sandbox-download tool-call guidance for agent execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
