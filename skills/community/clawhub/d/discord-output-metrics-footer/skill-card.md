## Description: <br>
Install, configure, maintain, or troubleshoot a compact Discord output footer for OpenClaw that shows live context usage, output tokens, Codex quota remaining, model used, and optional subagent token aggregate under each Discord response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[udaymanish6](https://clawhub.ai/user/udaymanish6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw workspace maintainers use this skill to install and operate a Discord footer that shows token usage, context percentage, Codex quota, model name, and optional subagent usage under agent responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The extension reads a local Codex OAuth profile and uses the token to fetch ChatGPT quota information. <br>
Mitigation: Review the bundled TypeScript before installing, enable it only in workspaces where credential-backed quota lookup is acceptable, and avoid sensitive workspaces unless that behavior is approved. <br>
Risk: Footer telemetry can expose operational usage details such as token counts, context usage, quota percentage, and model name in Discord. <br>
Mitigation: Use the disabled conversation configuration for channels where runtime metrics should not be posted, and keep the built-in privacy guardrails that suppress tokens, emails, profile names, and auth file paths. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Implementation](references/implementation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown instructions with bash snippets, JSON configuration, and bundled TypeScript extension files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When deployed, the extension appends a one-line Discord footer; Codex quota lookups are cached and omitted when unavailable.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and bundled package/plugin metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
