## Description: <br>
Convert documents, spreadsheets, images, web pages, and structured files into clean Markdown for AI processing through markdown.new. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alaminrifat](https://clawhub.ai/user/alaminrifat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agents use this skill to convert public URLs or uploaded files into Markdown for RAG ingestion, knowledge base creation, summarization, dataset extraction, spreadsheet analysis, and web page conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send selected local files, private documents, authenticated URLs, or internal links to the external markdown.new service for processing. <br>
Mitigation: Use it only with files and URLs the user is permitted to share, and do not send secrets, credentials, regulated data, proprietary documents, internal-only URLs, or signed links unless the service privacy and retention behavior is acceptable. <br>
Risk: Converted output is optimized for AI consumption, so complex layouts or source formatting may not be preserved exactly. <br>
Mitigation: Review converted Markdown before relying on it for summaries, extraction, ingestion, or downstream automation. <br>


## Reference(s): <br>
- [ClawHub File to Markdown release](https://clawhub.ai/alaminrifat/file-to-markdown) <br>
- [markdown.new API endpoint](https://markdown.new) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown text, JSON response examples, and Markdown with curl, JavaScript, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The artifact notes no authentication is required and a 500 requests/day per IP service limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
