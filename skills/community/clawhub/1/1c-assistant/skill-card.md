## Description: <br>
Russian-language assistant for answering 1C ERP, accounting, payroll, BSL development, administration, and document-ingestion questions through local RAG and scripted integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wint71rus](https://clawhub.ai/user/wint71rus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, administrators, and business users working with 1C use this skill to route Russian-language questions to relevant 1C knowledge collections, request help, and ingest images, PDFs, URLs, or text into a knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release requires sensitive credentials and includes a Qdrant API key in artifact evidence. <br>
Mitigation: Rotate the exposed key before use, move credentials into a secret store or environment variables, and restrict Qdrant network access to trusted hosts. <br>
Risk: The skill can send questions, documents, OCR text, images, and metadata to fixed webhook and Telegram flows. <br>
Mitigation: Use only in an environment you control, review all configured destinations, and avoid uploading screenshots, PDFs, or 1C business documents unless their contents and metadata are approved for those flows. <br>
Risk: The watcher artifact can monitor session logs and trigger calendar, email/report, Ollama, system-status, and RAG actions. <br>
Mitigation: Remove or separately permission watcher features that are not required, especially calendar, email/report, system-status, and broad session-monitoring behavior. <br>
Risk: Image ingestion can copy uploaded files to a public-serving directory. <br>
Mitigation: Disable public image serving or protect it with access controls before ingesting private screenshots or business documents. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/wint71rus/1c-assistant) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Knowledge base cheatsheet](artifact/CHEATSHEET_KNOWLEDGE_BASE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Russian-language Markdown with shell commands and JSON/cURL payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send request results and ingestion status through configured Telegram and webhook flows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
