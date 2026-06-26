## Description: <br>
Endpoints document management API toolkit. Scan documents with AI extraction and organize structured data into categorized endpoints. Use when the user asks to: scan a document, upload a file, list endpoints, inspect endpoint data, check usage stats, create or delete endpoints, get file URLs, or manage document metadata. Requires ENDPOINTS_API_KEY from endpoints.work dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adamkristopher](https://clawhub.ai/user/adamkristopher) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to interact with the Endpoints document management API: scan local files or text, organize extracted data into endpoints, inspect endpoint metadata, retrieve file URLs, and check account usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send local files and text to the external endpoints.work API. <br>
Mitigation: Use it only with documents and text intended for that API, verify ENDPOINTS_API_URL before use, and avoid processing sensitive files without approval. <br>
Risk: Delete functions can remove remote endpoint or item data without built-in confirmation safeguards. <br>
Mitigation: Require explicit user confirmation and exact target paths or item IDs before calling deleteEndpoint or deleteItem. <br>
Risk: API credentials and saved results may expose private account data or document content. <br>
Mitigation: Keep ENDPOINTS_API_KEY private and clean up the results/ directory after processing sensitive documents. <br>


## Reference(s): <br>
- [Endpoints API Reference](references/api-reference.md) <br>
- [Endpoints API](https://endpoints.work/api) <br>
- [Endpoints API Keys](https://endpoints.work/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Configuration] <br>
**Output Format:** [JSON files and Markdown summaries with TypeScript function calls and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Automatically saves API results under results/{category}/ and expects ENDPOINTS_API_KEY to be configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
