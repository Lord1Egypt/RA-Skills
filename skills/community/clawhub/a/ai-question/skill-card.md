## Description: <br>
Generates or normalizes quiz question bank Excel files from uploaded study materials and can start or stop the local QuizAI practice service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lewis828](https://clawhub.ai/user/lewis828) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators, students, and developers use this skill in a QuizAI project workspace to extract study materials, generate JSON question banks, export or normalize Excel question banks, optionally import them into the local SQLite database, and control the local FastAPI practice service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Service-control scripts can change the local environment by creating a virtual environment, installing dependencies, or installing Python if it is missing. <br>
Mitigation: Review the PowerShell service scripts before use and run them only in the intended QuizAI project workspace. <br>
Risk: Stopping the service can terminate processes listening on local port 8000. <br>
Mitigation: Confirm the service PID or port ownership before invoking the stop command. <br>
Risk: The skill reads uploaded study materials and writes extracted text, generated question banks, and optional database records. <br>
Mitigation: Use appropriate source materials, review generated outputs, and import into the database only after confirming the action. <br>
Risk: Generated quiz content can be inaccurate or misleading if the model misreads the source material. <br>
Mitigation: Review the generated JSON or Excel question bank against the source material before using it for assessment. <br>


## Reference(s): <br>
- [Generation Guide](generation-guide.md) <br>
- [Question Bank Excel Format Reference](reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated JSON and Excel files when invoked.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read uploaded study materials, write extracted or generated files, import quiz banks into a local SQLite database after confirmation, and start or stop a local service.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
