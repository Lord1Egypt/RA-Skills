## Description: <br>
Control browser automation agents via the Bits MCP server for web scraping, form filling, data extraction, and browser-based automation tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robbiethompson18](https://clawhub.ai/user/robbiethompson18) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation users use this skill to connect an assistant to the Bits MCP server for browser navigation, page reading, interaction, form filling, authentication flows, and structured data extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act on websites through browser automation, including forms, OAuth flows, 2FA, and stored credentials. <br>
Mitigation: Confirm target domains and actions before use, avoid privileged accounts when possible, and handle authentication flows and credentials cautiously. <br>
Risk: The MCP setup runs an unpinned npm package and requires a Bits API key. <br>
Mitigation: Review or pin the npm package before use and store the Bits API key only in the configured MCP environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/robbiethompson18/bits) <br>
- [Bits Web App](https://app.usebits.com) <br>
- [Bits API Docs](https://api.usebits.com/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets, TypeScript SDK code, and structured extraction results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Bits API key and MCP server configuration; automation may act on websites and return extracted page data or workflow results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
