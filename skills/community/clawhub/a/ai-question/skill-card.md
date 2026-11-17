## Description:

AI Question helps agents generate or normalize quiz-bank Excel files from study materials and start or stop a local QuizAI practice service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lewis828](https://clawhub.ai/user/lewis828)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and QuizAI operators use this skill inside a QuizAI project to turn study materials or existing question banks into standardized Excel quiz banks. It can also guide importing generated banks into the local practice app after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Service startup scripts can install Python and pip dependencies before starting the local QuizAI service.

Mitigation: Review the PowerShell scripts before use and prepare Python and dependencies manually when automatic installation is not acceptable.

Risk: The stop script can force-stop the process tree recorded in the PID file or any listener on port 8000.

Mitigation: Confirm the PID file and port 8000 listener belong to QuizAI before running the stop workflow.

Risk: Question-bank workflows process local files and can write generated banks into a local SQLite database.

Mitigation: Run the skill only in the intended QuizAI project, inspect generated questions before import, and confirm database writes with the user.

## Reference(s):

- [AI Question ClawHub release](https://clawhub.ai/lewis828/skills/ai-question)
- [Generation guide](generation-guide.md)
- [Excel format reference](reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with command snippets, JSON question-bank payloads, Excel .xlsx files, and local service status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a QuizAI project root with run.py and app/main.py; workflows may write data/generated-bank.json, Excel files, and data/quizai.db.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
