## Description: <br>
Reads, summarizes, compares, extracts from, writes back to, and inserts local images into Feishu wiki and docx documents through Feishu OpenAPI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carryours](https://clawhub.ai/user/carryours) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to read Feishu documents, summarize or extract document content, compare Feishu pages, write results back to a Feishu document, or insert a local image into a Feishu document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read or modify Feishu documents that are accessible to the configured token. <br>
Mitigation: Use a least-privilege Feishu app or user account and verify target document links before running read, write, or upload commands. <br>
Risk: Reusable Feishu credentials may be saved locally in plaintext token and OAuth configuration files. <br>
Mitigation: Delete or tightly protect .feishu-user-token.json and .feishu-oauth-config.json when the workflow is finished. <br>
Risk: Document JSON output can expose sensitive document content in shared logs or transcripts. <br>
Mitigation: Prefer concise Markdown output for normal reading tasks and avoid dumping raw JSON into shared locations unless it is needed for debugging. <br>
Risk: Image insertion can upload an unintended local file to a Feishu document. <br>
Mitigation: Confirm the local image path and target Feishu document before running image insertion commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/carryours/feishu-doc-skill) <br>
- [Feishu OpenAPI endpoint](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON with shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Feishu document titles, source links, summaries, extracted content previews, write results, and error explanations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
