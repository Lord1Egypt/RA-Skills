## Description: <br>
Fetches up-to-date, version-specific documentation and code examples for programming libraries and frameworks from Context7. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaylane](https://clawhub.ai/user/jaylane) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to resolve Context7 library IDs and fetch current API documentation, setup guidance, migration details, and code examples for specific libraries or framework versions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation questions and library identifiers are sent to Context7. <br>
Mitigation: Avoid including secrets, private code, customer data, credentials, or other sensitive details in documentation queries. <br>
Risk: A Context7 API key can be exposed if placed in prompts, logs, or shared command output. <br>
Mitigation: Use a Context7-specific CONTEXT7_API_KEY and keep it in the environment rather than in prompts or copied command text. <br>
Risk: Fetched documentation or examples may not fully match the user's project constraints. <br>
Mitigation: Review returned examples before applying them and prefer version-specific library IDs when the user names a version. <br>


## Reference(s): <br>
- [Context7 API Reference](references/API-REFERENCE.md) <br>
- [Context7 Library ID Format](references/LIBRARY-ID-FORMAT.md) <br>
- [Context7 API](https://context7.com/api) <br>
- [Context7 Dashboard](https://context7.com/dashboard) <br>
- [ClawHub Skill Page](https://clawhub.ai/jaylane/context7-docs) <br>
- [Publisher Profile](https://clawhub.ai/user/jaylane) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Context7 library IDs, selected documentation excerpts, API usage guidance, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
