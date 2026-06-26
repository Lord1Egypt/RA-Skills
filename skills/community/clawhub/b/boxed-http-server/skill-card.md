## Description: <br>
WebAssembly sandbox static HTTP server with HTTP Basic auth and proxy support for serving static files, protecting sites, configuring proxies, and running local development servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guyoung](https://clawhub.ai/user/guyoung) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run a sandboxed static HTTP server, add Basic authentication, and configure proxy or reverse-proxy routes for local development or static site deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill serves local or static content through a downloaded WASM component. <br>
Mitigation: Inspect the source before use, prefer a pinned release or checksum, and bind the server only to the needed interface. <br>
Risk: Proxy and authentication examples include placeholder credentials and outbound host settings. <br>
Mitigation: Replace example secrets, avoid admin/admin credentials, and keep allowedOutboundHosts limited to required destinations. <br>


## Reference(s): <br>
- [Boxed HTTP Server on ClawHub](https://clawhub.ai/guyoung/boxed-http-server) <br>
- [Boxed HTTP Server WASM component](https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/boxed-http-server/files/boxed_http_server_component.wasm) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes WASM component paths, work directory settings, Basic auth variables, proxy rules, and allowed outbound host configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
