## Description: <br>
frompdf helps agents send PDFs to api.frompdf.dev to extract structured content as semantic JSON, Markdown, HTML, plain text, or LLM-ready chunks, with semantic diff and readability-score endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[techtonicllc](https://clawhub.ai/user/techtonicllc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill when they need structured, typed PDF content for extraction, RAG preparation, document comparison, or readability scoring. It is useful when raw text extraction is insufficient or when large, encrypted, or complex PDFs need cloud processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF contents, API credentials, and encrypted-PDF passwords may be sent to frompdf.dev for processing. <br>
Mitigation: Use the skill only with documents and credentials approved for that external service, and avoid confidential, regulated, or encrypted files unless the service has been reviewed for the intended use. <br>
Risk: The skill requires a FROMPDF_API_KEY environment variable. <br>
Mitigation: Store the API key in the agent environment or secret manager and avoid pasting it into prompts, logs, or shared shell history. <br>


## Reference(s): <br>
- [frompdf API homepage](https://api.frompdf.dev) <br>
- [ClawHub skill page](https://clawhub.ai/techtonicllc/frompdf-api) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FROMPDF_API_KEY; API responses may include JSON semantic AST, Markdown, HTML, plain text, LLM-ready chunks, semantic diffs, or readability scores.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
