## Description: <br>
Boxed Fetch is a WebAssembly-based sandboxed web fetcher for retrieving URL content and extracting readable text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guyoung](https://clawhub.ai/user/guyoung) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to fetch HTTPS webpage content, extract readable text from HTML, and make sandboxed HTTP requests through the openclaw-wasm-sandbox plugin. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads a WASM component from a mutable GitHub URL before use. <br>
Mitigation: Install only when the WASM component source and the openclaw-wasm-sandbox plugin are trusted. <br>
Risk: Sandboxed fetching can contact unintended destinations if outbound hosts are too broad. <br>
Mitigation: Keep allowedOutboundHosts limited to the exact HTTPS host needed for the request. <br>
Risk: Custom headers may expose secrets to the requested destination. <br>
Mitigation: Do not pass secrets in custom headers unless the destination is trusted and authentication is intentional. <br>


## Reference(s): <br>
- [Boxed Fetch on ClawHub](https://clawhub.ai/guyoung/boxed-fetch) <br>
- [Usage Guide](references/usage.md) <br>
- [WASM Component Download](https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/boxed-fetch/files/boxed-fetch-component.wasm) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions and sandbox command examples; fetched content is returned as text or formatted JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit HTTPS outbound host allowlists and a downloaded WASM component.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
