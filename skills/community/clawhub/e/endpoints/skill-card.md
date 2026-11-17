## Description:

Endpoints document management API toolkit for scanning documents with AI extraction, organizing structured data into categorized endpoints, managing endpoint metadata, retrieving file URLs, and checking usage stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamkristopher](https://clawhub.ai/user/adamkristopher)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to interact with the Endpoints.work document-management API: scan files or text, create and inspect endpoints, remove endpoint data, retrieve file URLs, and summarize saved JSON results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File scanning can upload selected local documents or text to the Endpoints.work service.

Mitigation: Confirm the selected file or text, account, API key, and intended HTTPS API host before running scan operations.

Risk: Delete operations can remove remote endpoints, associated files, or individual metadata items.

Mitigation: Require explicit confirmation of the exact endpoint path or item ID before calling deleteEndpoint or deleteItem.

Risk: An unintended ENDPOINTS_API_URL could send requests and bearer credentials to the wrong service.

Mitigation: Verify ENDPOINTS_API_URL is exactly the intended HTTPS host before using the skill.

## Reference(s):

- [Endpoints API Reference](references/api-reference.md)
- [Endpoints API](https://endpoints.work/api)
- [Endpoints API Keys](https://endpoints.work/api-keys)
- [ClawHub Skill Page](https://clawhub.ai/adamkristopher/skills/endpoints)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with TypeScript examples and JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ENDPOINTS_API_KEY and may write API responses under results/{category}/.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
