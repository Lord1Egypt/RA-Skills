## Description: <br>
Integrates Dub Links API endpoints to create, update, delete, retrieve, list, count, and run bulk operations on short links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ferminrp](https://clawhub.ai/user/ferminrp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage Dub short links in an authenticated workspace, including creation, updates, lookup, listing, counting, and bulk link operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dub API keys can grant access to the authenticated workspace if exposed. <br>
Mitigation: Use a least-privilege Dub API key where possible, keep it out of chat and logs, and pass it through an environment variable such as DUB_API_KEY. <br>
Risk: Delete, update, and bulk operations can modify or remove many short links. <br>
Mitigation: Require the agent to show exact link IDs, domains, selectors, and payloads before update, delete, or bulk requests are executed. <br>


## Reference(s): <br>
- [Dub Links API create endpoint](https://dub.co/docs/api-reference/endpoint/create-a-link) <br>
- [Dub API tokens](https://dub.co/docs/api-reference/tokens) <br>
- [Local OpenAPI snapshot](references/openapi-spec.json) <br>
- [ClawHub skill page](https://clawhub.ai/ferminrp/dub-links-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should summarize affected link IDs, domains, short links, destination URLs, and bulk-operation counts when relevant.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
