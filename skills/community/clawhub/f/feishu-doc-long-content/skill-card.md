## Description: <br>
Guides agents through creating Feishu documents and writing longer content in safe chunks to avoid truncation or write errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Josephyb97](https://clawhub.ai/user/Josephyb97) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill when writing long Markdown or note content into Feishu Docs. It helps them create an empty document, write concise chunks under the documented practical limit, verify the result, and fall back to local Markdown when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive content written through Feishu document actions may persist in the user's workspace. <br>
Mitigation: Confirm the content is appropriate for Feishu before writing, and verify the resulting document after each write. <br>
Risk: The local Markdown fallback can leave a copy of document content on disk. <br>
Mitigation: Write local fallback files only to an intentional location and remove them when they are no longer needed. <br>
Risk: Oversized content may be truncated or rejected by Feishu write actions. <br>
Mitigation: Split content into smaller chunks, keep each write under 800 bytes where practical, and read the document after writing to confirm completeness. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Josephyb97/feishu-doc-long-content) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, API call examples] <br>
**Output Format:** [Markdown guidance with JSON request examples and troubleshooting tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommends keeping Feishu write content below 800 bytes per request and validating writes after creation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
