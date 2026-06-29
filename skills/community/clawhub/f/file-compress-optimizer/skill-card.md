## Description: <br>
Compresses natural language memory files such as CLAUDE.md, todos, and preferences into shorter markdown while preserving technical substance, code, URLs, and structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyafeichina](https://clawhub.ai/user/liyafeichina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to reduce token usage in natural-language memory and notes files while keeping technical details, code blocks, URLs, headings, and paths intact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected memory or notes files may be sent to Claude/Anthropic for compression. <br>
Mitigation: Use only on files whose contents are acceptable to share with that service; avoid confidential notes, credentials, customer data, and files that must stay local. <br>
Risk: Successful compression overwrites the selected file. <br>
Mitigation: Keep the generated .original.md backup and review the compressed result before relying on it. <br>
Risk: Compression can change natural-language phrasing and may lose nuance even when validation passes. <br>
Mitigation: Review important instructions, requirements, and technical context after compression. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liyafeichina/file-compress-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown status text and modified natural-language files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a .original.md backup before overwriting the selected file when compression succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
