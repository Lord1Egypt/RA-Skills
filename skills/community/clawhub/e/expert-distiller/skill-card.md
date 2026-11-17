## Description:

Conducts adaptive, multi-round interviews with domain experts to extract structured Q&A pairs, decision frameworks, and cognitive boundaries through progressive questioning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billb13](https://clawhub.ai/user/billb13)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to run structured adaptive interviews with domain experts, turning implicit expertise into standardized question-and-answer records for later analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on interview_engine.py and prompt templates that are referenced but not included in the artifact evidence.

Mitigation: Review and trust those helper files separately before running the Python commands.

Risk: The workflow writes local interview state, backup, and JSONL result files that may contain expert-provided sensitive information.

Mitigation: Run it in an appropriate workspace and handle generated files according to the user's data policy.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/BillB13/expert-distiller)
- [ClawHub skill page](https://clawhub.ai/billb13/skills/expert-distiller)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash commands and JSON/JSONL interview records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates adaptive interview questions, response analyses, state updates, snapshots, and JSONL exports through a local Python interview workflow.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
