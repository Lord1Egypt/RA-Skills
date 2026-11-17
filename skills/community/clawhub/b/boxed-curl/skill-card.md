## Description:

Run curl requests safely in a sandbox, supporting GET/POST/HTTP headers, with complete network isolation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guyoung](https://clawhub.ai/user/guyoung)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to translate curl-like HTTP requests into sandboxed WASM tool calls with explicit outbound host allowlists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to download and run an unverified remote WASM component.

Mitigation: Review before installing and prefer a release that bundles or pins the WASM file with a published hash.

Risk: Requests may include sensitive tokens, cookies, Authorization headers, personal data, or other confidential payloads.

Mitigation: Use only trusted URLs and non-sensitive request data unless the WASM component and sandbox plugin have been independently verified.

Risk: The security summary says the skill overstates network isolation.

Mitigation: Do not rely on the skill text alone for isolation guarantees; confirm sandbox behavior and allowedOutboundHosts enforcement before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guyoung/skills/boxed-curl)
- [WASM component download](https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/boxed-curl/files/boxed_curl_component.wasm)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with JavaScript tool-call examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl-like arguments, allowedOutboundHosts, and a local boxed_curl_component.wasm file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
