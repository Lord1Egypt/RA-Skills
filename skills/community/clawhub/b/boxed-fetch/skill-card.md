## Description:

Boxed Fetch is a WebAssembly-based sandboxed web fetcher that retrieves HTTPS URL content and extracts readable text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guyoung](https://clawhub.ai/user/guyoung)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch HTTPS web pages, extract readable text from HTML, and run constrained HTTP requests through the openclaw-wasm-sandbox plugin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to download and run a mutable remote WASM binary without integrity verification.

Mitigation: Review before installing; prefer a release that bundles the reviewed WASM file or pins it to an immutable artifact with a published SHA-256 or signature.

Risk: The skill can make outbound web requests to hosts allowed at runtime.

Mitigation: Keep allowedOutboundHosts limited to the exact destination needed for the fetch.

## Reference(s):

- [Usage Guide](references/usage.md)
- [Boxed Fetch on ClawHub](https://clawhub.ai/guyoung/skills/boxed-fetch)
- [WASM Component Download](https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/boxed-fetch/files/boxed-fetch-component.wasm)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Fetched web content, readable text, or pretty-printed JSON returned from WASM sandbox runs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires openclaw-wasm-sandbox, an HTTPS target URL, and explicit allowedOutboundHosts.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
