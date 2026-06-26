## Description: <br>
Downloads PDF documents from Chaoxing contest or platform viewer URLs and converts them to TXT, supporting single or batch downloads with page-count validation and OCR fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[artminding](https://clawhub.ai/user/artminding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve Chaoxing-hosted PDF documents from viewer URLs or object IDs, validate expected page counts, and create TXT extracts using native PDF text extraction with OCR fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may download remote documents and write files based on user-provided viewer URLs and names. <br>
Mitigation: Confirm the source URLs, expected page counts, and output filenames before running download commands. <br>
Risk: The skill may require installing PDF and OCR Python dependencies before TXT conversion. <br>
Mitigation: Install dependencies in an isolated Python environment and review package sources before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/artminding/chaoxing-download) <br>
- [Chaoxing getYunFiles API endpoint](https://contestyd.chaoxing.com/app/files/{objectid}/getYunFiles?key=allData) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Files, Markdown] <br>
**Output Format:** [Markdown guidance with bash and Python code blocks; downloaded PDF files and extracted TXT files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one PDF and one TXT file per requested Chaoxing document when executed successfully.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
