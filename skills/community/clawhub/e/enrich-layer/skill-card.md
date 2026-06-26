## Description: <br>
Enrich company, person, and contact data with 25 tools via the Enrich Layer API. Look up companies, find decision-makers, get work emails, search employees, verify contacts, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicest-michael](https://clawhub.ai/user/nicest-michael) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business users use this skill to enrich company, person, contact, school, and job data through Enrich Layer MCP tools. It supports lead enrichment, decision-maker lookup, contact verification, company research, employee and student searches, and related data-enrichment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retrieve personal contact data, perform reverse lookups, and search people or student lists without clear consent or acceptable-use guardrails. <br>
Mitigation: Use these features only for legitimate authorized purposes, follow applicable privacy and data-handling requirements, and avoid requests that lack a valid basis for handling personal data. <br>
Risk: External enrichment calls may consume paid Enrich Layer credits, especially for bulk searches and list endpoints. <br>
Mitigation: Check the credit balance before large operations, estimate costs before proceeding, and prefer lower-cost or cached tools when they satisfy the request. <br>
Risk: The skill depends on an external npm MCP package and an API key. <br>
Mitigation: Use a dedicated Enrich Layer API key, verify the npm MCP package and version before installation, and monitor usage for unexpected activity. <br>


## Reference(s): <br>
- [Enrich Layer Homepage](https://enrichlayer.com) <br>
- [Enrich Layer API Docs](https://enrichlayer.com/docs) <br>
- [Enrich Layer Dashboard](https://enrichlayer.com/dashboard) <br>
- [@verticalint-michael/enrich-layer-mcp npm package](https://www.npmjs.com/package/@verticalint-michael/enrich-layer-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries, structured text, and MCP tool call results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ENRICH_LAYER_API_KEY and Node.js; some tool calls consume Enrich Layer credits.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
