## Description: <br>
Collects disclosure notices from 30 licensed consumer finance company websites, downloads related documents, extracts cooperation institution data, and writes the results into a local ontology graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linwumeng](https://clawhub.ai/user/linwumeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to monitor public consumer finance disclosures, collect announcement text and attachments, extract named cooperation institutions and phone numbers, and query the resulting relationship graph. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedded MiniMax/GLM credentials may be exposed or reused unintentionally. <br>
Mitigation: Remove bundled keys, rotate any exposed credentials, and provide fresh credentials through environment variables only when OCR or LLM features are intentionally enabled. <br>
Risk: OCR and LLM paths can upload disclosure documents, images, extracted phone numbers, or related text to third-party services. <br>
Mitigation: Review data handling requirements before enabling those paths and keep sensitive or unnecessary local data out of OCR/LLM queues. <br>
Risk: Downloaded documents, extracted phone numbers, and ontology entries persist in the local workspace. <br>
Mitigation: Run in an isolated workspace, apply retention controls, and delete generated raw data and ontology files when they are no longer needed. <br>
Risk: Browser diagnostic scripts use weakened browser settings and could be unsafe against untrusted pages. <br>
Mitigation: Limit runs to the intended public disclosure websites and avoid using diagnostic scripts on arbitrary URLs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/linwumeng/cfc-disclosure-monitor) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [companies.json](artifact/companies.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local announcement JSON files, downloaded attachments, extracted entity JSON files, VLM/OCR result JSON, and ontology graph JSONL when its scripts are executed.] <br>

## Skill Version(s): <br>
4.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
