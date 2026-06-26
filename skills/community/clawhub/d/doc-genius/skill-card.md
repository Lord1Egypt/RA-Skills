## Description: <br>
Doc Genius helps agents summarize PDF, Word, Markdown, and text documents, convert document formats, and batch-process folders of documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imgolye](https://clawhub.ai/user/imgolye) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, content creators, and enterprise users can use this skill to extract document text, generate summaries and keywords, convert documents to Markdown or HTML, and process document folders in batches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Under-disclosed billing behavior and a hardcoded billing API key are present in the paid processor script. <br>
Mitigation: Do not run scripts/doc_processor_paid.py unless billing is intended and approved; require the publisher to remove or rotate the embedded key and document the paid flow. <br>
Risk: AI summarization can send extracted document text to OpenAI. <br>
Mitigation: Use local summarization for sensitive documents unless users have approved external API processing and configured OPENAI_API_KEY appropriately. <br>
Risk: The release has a suspicious security verdict. <br>
Mitigation: Review and scan the skill before installation, and test it in a restricted environment before using it on trusted documents. <br>


## Reference(s): <br>
- [API examples](references/api-examples.md) <br>
- [Supported formats](references/supported-formats.md) <br>
- [ClawHub skill page](https://clawhub.ai/imgolye/doc-genius) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, HTML, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands; processor outputs JSON, Markdown, HTML, or plain text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [AI summarization can require OPENAI_API_KEY; local summarization is available for sensitive documents.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
