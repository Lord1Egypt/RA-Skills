## Description: <br>
DeepRead OCR helps agents process PDFs and images through DeepRead's OCR API, extracting clean markdown and structured JSON with confidence flags for human review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uday390](https://clawhub.ai/user/uday390) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send selected documents to DeepRead for asynchronous OCR, structured field extraction, confidence flags, and human-in-the-loop review in document workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents are sent to DeepRead and, when configured, to the user's webhook endpoint. <br>
Mitigation: Use the skill only for documents approved for DeepRead processing, and secure webhook receivers before enabling webhook delivery. <br>
Risk: The DeepRead API key could be exposed if pasted into files, chats, logs, or shared prompts. <br>
Mitigation: Store DEEPREAD_API_KEY in the environment or a secret manager and avoid including it in documents, configuration files, or conversation text. <br>
Risk: Preview URLs may act as private bearer links for document previews or extracted results. <br>
Mitigation: Treat preview URLs as sensitive, share them only with intended reviewers, and revoke or rotate access if a link is exposed. <br>


## Reference(s): <br>
- [DeepRead homepage](https://www.deepread.tech) <br>
- [DeepRead OCR on ClawHub](https://clawhub.ai/uday390/deepread-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with bash and JSON examples; DeepRead API responses may include markdown text and structured JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY and sends selected documents to DeepRead; webhook and preview links may expose document contents.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
