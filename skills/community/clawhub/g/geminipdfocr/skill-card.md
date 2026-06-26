## Description: <br>
Extract text from PDFs using Google Gemini OCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AshtonIzmev](https://clawhub.ai/user/AshtonIzmev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to OCR scanned or image-based PDF documents with Google Gemini and return extracted text for downstream review, summarization, or processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF page contents are uploaded to Google Gemini for OCR. <br>
Mitigation: Use the skill only for documents whose cloud-processing data flow is acceptable for the user's privacy and compliance requirements. <br>
Risk: Python dependencies are listed without pinned versions. <br>
Mitigation: Use an isolated environment and consider pinning reviewed dependency versions before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AshtonIzmev/geminipdfocr) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, files] <br>
**Output Format:** [Plain text or JSON written to stdout or to a specified output file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON output includes per-document and per-page OCR status, extracted text, character counts, and errors when present.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
