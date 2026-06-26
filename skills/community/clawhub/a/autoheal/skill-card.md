## Description: <br>
Add AI-powered error monitoring and auto-fix generation to any project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hankmint](https://clawhub.ai/user/hankmint) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to add AutoHeal error monitoring to JavaScript and TypeScript projects, report runtime errors, check analysis status, and retrieve AI-generated fix prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Raw production errors may include secrets, customer data, request details, internal paths, or other sensitive context before they are sent to autohealai.com. <br>
Mitigation: Redact tokens, URLs, headers, request bodies, customer data, and internal paths before sending error reports. <br>
Risk: A long-lived API key may be exposed if copied into browser-side code. <br>
Mitigation: Use a server-side proxy or a scoped ingestion token instead of embedding a long-lived API key in client code. <br>
Risk: The release was flagged as suspicious by the authoritative security evidence. <br>
Mitigation: Review the integration and data handling path before installing in production. <br>


## Reference(s): <br>
- [AutoHeal AI ClawHub release](https://clawhub.ai/hankmint/autoheal) <br>
- [AutoHeal AI](https://autohealai.com) <br>
- [AutoHeal error ingest API](https://autohealai.com/api/errors/ingest) <br>
- [AutoHeal error status API](https://autohealai.com/api/errors/{ERROR_ID}/status) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with JavaScript snippets, shell commands, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AUTOHEAL_API_KEY and sends reported error data to autohealai.com.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
