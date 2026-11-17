## Description:

Chaoxing Auto Grade helps course staff download Chaoxing/Learning Tong homework review HTML, extract subjective questions, use a configured LLM API for grading, apply scores, and generate cleaned HTML summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenghaozhangswu](https://clawhub.ai/user/chenghaozhangswu)

### License/Terms of Use:

MIT-0

## Use Case:

Educators and course operations staff use this skill to collect Chaoxing homework review pages, grade subjective responses with an external LLM API, write resulting scores into local HTML copies, and produce compact reviewable HTML outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles teacher credentials and student records.

Mitigation: Install and run it only when authorized to process the relevant student records, protect config.json, and prefer environment or OS credential storage over plaintext passwords and API keys.

Risk: The download step uses Chrome remote debugging and may be configured with broad remote-origin access.

Mitigation: Use a dedicated temporary Chrome profile, avoid --remote-allow-origins=* when possible, and close the debugging browser after use.

Risk: Subjective answers may be sent to the configured external LLM API for grading.

Mitigation: Confirm institutional policy permits external LLM grading of student submissions before sending records to the provider.

Risk: The score application step updates original local HTML files.

Mitigation: Keep backups before applying scores and review outputs before relying on them for official grading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenghaozhangswu/skills/chaoxing-auto-grade)
- [ClawHub publisher profile](https://clawhub.ai/user/chenghaozhangswu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples; scripts produce JSON and HTML files in configured directories.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Chrome remote debugging, local HTML files, and a configured external LLM API for subjective grading.]

## Skill Version(s):

2.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
