## Description: <br>
This skill uses BaZi, Zi Wei Dou Shu, major-luck, and annual-flow rules to generate fortune-style career direction, health-theme analysis, and short summaries from birth details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devioslang](https://clawhub.ai/user/devioslang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or agents use this skill to turn birth date, birth time, optional lunar-calendar status, and gender into Chinese fortune-style career guidance, wellness themes, and either a five-sentence summary or a full report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes birth date, birth time, and gender, which may be sensitive personal context. <br>
Mitigation: Use only with data the user intentionally provides, avoid unnecessary retention, and do not share the inputs outside the local analysis flow. <br>
Risk: Health output could be mistaken for medical diagnosis or treatment guidance. <br>
Mitigation: Present health results as entertainment or general wellness commentary and direct users to qualified clinicians for symptoms, treatment decisions, or urgent concerns. <br>
Risk: Running the artifact depends on the external Python package sxtwl. <br>
Mitigation: Install missing dependencies only from trusted package sources and review the local environment before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/devioslang/fortune-career) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese Markdown report or five-line plain-text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires birth date and birth time; optional inputs include gender and lunar-calendar wording. Health content is fortune-style wellness commentary, not medical diagnosis or treatment advice.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
