## Description: <br>
doc-extract-filter extracts text from common document formats and filters extracted content by keywords or regular expressions, with batch processing and optional OCR for scanned PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigclawd](https://clawhub.ai/user/bigclawd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to extract text from user-specified PDF, Word, Excel, text, CSV, Markdown, and WPS files, then return full text or filtered matches for downstream review and automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the documents and folders supplied by the user, which can expose sensitive document contents to the agent workflow. <br>
Mitigation: Use narrow input paths, review the selected files before execution, and process only documents you are comfortable allowing the agent to read. <br>
Risk: Batch mode and merged output can collect text from many documents into JSON files, increasing the impact of accidental disclosure. <br>
Mitigation: Choose an output directory you control, avoid merged batch output for sensitive collections, and delete generated results when they are no longer needed. <br>
Risk: PDF, OCR, and image parsing dependencies can carry security exposure when processing untrusted files. <br>
Mitigation: Pin or update parsing dependencies and process untrusted documents in a controlled environment before using the extracted text in broader workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bigclawd/doc-extract-filter) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files] <br>
**Output Format:** [JSON responses containing success status, extracted text, filtered text, match metadata, errors, and optional batch summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Batch mode can write per-file JSON results or a merged JSON result to a user-selected output directory.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
