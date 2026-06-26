## Description: <br>
Batch Format Converter helps agents convert files between CSV, Excel, JSON, PDF, Markdown, DOCX, HTML, PNG, JPG, and TXT formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiji0802](https://clawhub.ai/user/qiji0802) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, operations staff, finance teams, and document workers use this skill to batch-convert data and document files between common office, data, image, and web formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release under-discloses credential handling and remote license verification. <br>
Mitigation: Review before installing; use only a dedicated converter or 91Skillhub license token if the publisher endpoint is trusted, and avoid relying on OPENAI_API_KEY for this tool. <br>
Risk: Remote validation and optional delivery features may expose sensitive workflow context if enabled with untrusted endpoints or documents. <br>
Mitigation: Disable network access when only local conversion is needed, and do not enable Feishu delivery for sensitive documents unless the metadata or files being sent are understood. <br>
Risk: Cleanup commands documented with the artifact can remove files if copied into unrelated directories. <br>
Mitigation: Run cleanup commands only inside an intended disposable skill workspace after reviewing the target paths. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/qiji0802/batch-format-converter) <br>
- [Publisher Profile](https://clawhub.ai/user/qiji0802) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Description](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Converted files with CLI status text and JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require Python dependencies, system OCR tools for scanned PDFs, and optional configuration for webhook-based delivery.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
