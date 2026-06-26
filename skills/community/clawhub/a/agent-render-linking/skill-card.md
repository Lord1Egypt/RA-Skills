## Description: <br>
Creates zero-retention agent-render.com links for markdown, code, diffs, CSV, or JSON artifacts so agents can share browser-rendered artifacts instead of raw chat content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baanish](https://clawhub.ai/user/baanish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to package markdown, code, diffs, CSV, or JSON into Agent Render URLs for browser viewing. It is intended for sharing non-sensitive artifacts through supported chat surfaces or as raw URLs when linked text is unreliable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated URLs contain the artifact content, so anyone with the full link may be able to view the shared artifact. <br>
Mitigation: Use this workflow only for non-sensitive artifacts and avoid secrets, credentials, confidential files, or regulated data unless the user explicitly accepts that sharing model. <br>
Risk: Large artifacts may exceed practical URL-fragment or chat-surface budgets. <br>
Mitigation: Measure available encodings, choose the shortest valid codec, keep artifacts focused, and return a clear budget failure instead of silently truncating content. <br>
Risk: Linked-text syntax can render incorrectly on chat surfaces that do not support the chosen format. <br>
Mitigation: Use provider-specific link syntax only where it is supported; otherwise provide a short summary followed by the raw URL. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/baanish/agent-render-linking) <br>
- [Agent Render viewer](https://agent-render.com/) <br>
- [Agent Render ARX dictionary](https://agent-render.com/arx-dictionary.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown link text, raw URLs, and JSON envelope guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses URL fragments for artifact transport, prefers shortest valid codec, and provides budget-aware failure guidance instead of silent truncation.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
