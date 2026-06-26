## Description: <br>
Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. Powered by evolink.ai <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evolinkai](https://clawhub.ai/user/evolinkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this instruction-only skill to process PDFs locally: extracting text, tables, images, and metadata; merging or splitting documents; creating PDFs; filling forms; applying OCR; and running common PDF command-line tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes optional EvoLink API configuration while also claiming local-only operation, which could cause users to unintentionally send document content or metadata to a third-party service. <br>
Mitigation: Keep sensitive PDFs local unless the user explicitly enables EvoLink, understands what may be transmitted, and accepts the third-party service risk. <br>
Risk: PDF operations can overwrite, decrypt, merge, split, or otherwise alter user documents. <br>
Mitigation: Use explicit output filenames, keep original PDFs unchanged, and review generated files before replacing source documents. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/evolinkai/evolink-pdf) <br>
- [EvoLink Claude Messages API Documentation](https://docs.evolink.ai/en/api-manual/language-series/claude/claude-messages-api?utm_source=github&utm_medium=skill&utm_campaign=pdf-toolkit) <br>
- [EvoLink Website](https://evolink.ai?utm_source=github&utm_medium=skill&utm_campaign=pdf-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only PDF processing guidance; generated files depend on the user's chosen local tools and filenames.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
