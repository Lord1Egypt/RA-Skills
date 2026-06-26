## Description: <br>
Create and operate ChatDOC Studio knowledge bases through pd_router using a Bearer API key and JavaScript helpers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paodingai](https://clawhub.ai/user/paodingai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to upload local PDF, DOC, or DOCX files into ChatDOC Studio knowledge bases through PDRouter, then retrieve, list, search, inspect, and read documents from those knowledge bases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected PDF, DOC, or DOCX content is uploaded to PaodingAI ChatDOC Studio using PAODINGAI_API_KEY. <br>
Mitigation: Review documents before upload and use narrow --file or --dir selections; avoid broad or sensitive folders unless approved. <br>
Risk: The skill requires a bearer API key for PDRouter requests. <br>
Mitigation: Store PAODINGAI_API_KEY in an environment or secrets manager and do not paste it into prompts, logs, or committed files. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/paodingai/chatdoc-studio-knowledgemate) <br>
- [PaodingAI PDRouter platform](https://platform.paodingai.com) <br>
- [Skill resource: knowledge-mate.mjs](./scripts/knowledge-mate.mjs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [JSON responses from the helper script, with Markdown usage guidance and shell commands in the skill documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads are limited to PDF, DOC, and DOCX files; folder scans are recursive; upload-and-create stops before upload when more than 300 supported files are found.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release metadata; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
