## Description: <br>
Searches Egatee products by text or image through the Web2JDE Orchestrator, builds product cards, and can prepare RFQ candidates with optional MySQL-backed supplement lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahoyoshi](https://clawhub.ai/user/ahoyoshi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search the Egatee catalog from chat text or image URLs, present product cards, and stage RFQ details for later explicit saving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch user-provided image URLs before sending image searches to the Orchestrator. <br>
Mitigation: Do not provide internal, private-network, or otherwise sensitive image URLs; use trusted public image URLs only. <br>
Risk: The skill can store RFQ, contact, chat history, selected item, source payload, and API key-related data in MySQL when save_rfq is called. <br>
Mitigation: Require explicit user confirmation before saving RFQ data and use narrowly scoped database credentials. <br>
Risk: The skill depends on configured Egatee endpoints and database connections. <br>
Mitigation: Install only when the operator trusts the Egatee endpoints and the configured MySQL database. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ahoyoshi/egatee-china-search) <br>
- [Publisher profile](https://clawhub.ai/user/ahoyoshi) <br>
- [Default Egatee Orchestrator endpoint](http://121.40.43.22:3004) <br>
- [Egatee production API gateway](https://api.egatee.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, HTML, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON search results with product-card fields, Markdown/HTML card snippets, CLI output, and optional RFQ candidate data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calls external Egatee endpoints, may fetch user-provided image URLs, and requires explicit confirmation before saving RFQ data.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact frontmatter says 1.3.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
