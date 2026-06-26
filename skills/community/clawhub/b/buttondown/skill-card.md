## Description: <br>
Buttondown helps agents create, update, inspect, and send approved test previews of Buttondown newsletter emails through the Buttondown API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rayhollister](https://clawhub.ai/user/rayhollister) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to manage Buttondown newsletter drafts, inspect email metadata, and send preview emails only after approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send the Buttondown API key and newsletter content to any URL configured through BUTTONDOWN_API_BASE. <br>
Mitigation: Run it only where environment variables are controlled, do not set BUTTONDOWN_API_BASE unless it is a trusted Buttondown-compatible endpoint, and use the narrowest Buttondown API key available. <br>
Risk: Update and preview-send commands can change newsletter drafts or send email externally. <br>
Mitigation: Verify email IDs, draft status, and recipients before running update or preview-send commands, and require explicit user approval before any send, schedule, publish, delete, or preview-send action. <br>


## Reference(s): <br>
- [Buttondown skill page](https://clawhub.ai/rayhollister/buttondown) <br>
- [Publisher profile](https://clawhub.ai/user/rayhollister) <br>
- [Buttondown skill homepage](https://forge.rayhollister.com/rayhollister/buttondown) <br>
- [Buttondown API Reference](references/api.md) <br>
- [Buttondown OpenAPI specification](https://docs.buttondown.com/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses BUTTONDOWN_API_KEY and optional BUTTONDOWN_CONTEXT or BUTTONDOWN_API_BASE environment variables; create operations default to draft status.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
