## Description: <br>
Lightweight document utility designed to convert files to Markdown (MD), built specifically for intelligent agents to read and process content across common document, spreadsheet, presentation, image, ebook, and office formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haoyt27](https://clawhub.ai/user/haoyt27) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert user-provided documents into Markdown so the document content can be read, summarized, extracted, or analyzed. It supports single Markdown output and a full Markdown package with images and tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents are sent to the third-party lab.hjcloud.com conversion service. <br>
Mitigation: Require explicit user confirmation before upload and avoid confidential, regulated, credential-bearing, or customer documents unless the service's privacy and retention practices have been independently reviewed. <br>
Risk: The skill may be invoked for broad read, summarize, or analyze requests without a separate consent step. <br>
Mitigation: Ask the user to confirm the specific file and conversion mode before each upload, especially for sensitive or ambiguous document requests. <br>


## Reference(s): <br>
- [Doc2Markdown ClawHub listing](https://clawhub.ai/haoyt27/doc2markdown) <br>
- [Docchain document conversion service](https://lab.hjcloud.com/llmdoc) <br>
- [Docchain Skills support repository](https://github.com/wct-lab/docchain-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown files, extracted ZIP packages, and command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js. Conversion uploads the source document to lab.hjcloud.com, polls for completion, and may return a document ID for later checking.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
