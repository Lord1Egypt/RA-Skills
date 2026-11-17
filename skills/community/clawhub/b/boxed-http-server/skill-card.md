## Description:

Boxed HTTP Server is a WebAssembly sandbox static HTTP server with HTTP Basic authentication and proxy/reverse proxy support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guyoung](https://clawhub.ai/user/guyoung)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run static websites in an OpenClaw WebAssembly sandbox, add Basic authentication, and configure outbound proxy or reverse proxy routes for local development or deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to download and run a remote WebAssembly component.

Mitigation: Use only trusted upstream sources, pin and verify the downloaded component before execution, and review before installing.

Risk: Server or proxy configuration can expose local files or outbound network access beyond the intended scope.

Mitigation: Expose only the intended website directory, allow only required outbound hosts, and bind to localhost unless remote access is needed.

Risk: The examples include placeholder credentials and tokens.

Mitigation: Replace all example credentials and tokens with strong secrets managed outside static configuration.

## Reference(s):

- [Boxed HTTP Server Skill Page](https://clawhub.ai/guyoung/skills/boxed-http-server)
- [Boxed HTTP Server WebAssembly Component](https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/boxed-http-server/files/boxed_http_server_component.wasm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript, Bash, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command and configuration examples for OpenClaw WebAssembly sandbox server setup.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
