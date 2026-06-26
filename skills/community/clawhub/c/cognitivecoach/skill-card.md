## Description: <br>
Cognitive Coach ingests exported chat history, filters for high-value knowledge, creates private Feynman review prompts, and schedules a next-morning recall challenge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DearChenzj](https://clawhub.ai/user/DearChenzj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technically curious users use this skill to turn prior AI chat sessions into concise self-explanation prompts and follow-up feedback that support long-term retention. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes exported chat records that may contain secrets, personal information, or confidential work material. <br>
Mitigation: Review and minimize chat exports before use, and avoid providing sensitive conversations unless the deployment is approved for that data. <br>
Risk: The skill keeps hidden review prompts and schedules a later review, which can create stored content or reminders the user may not expect. <br>
Mitigation: Confirm the OpenClaw environment allows users to view, cancel, or delete scheduled reviews and stored cards before relying on the workflow. <br>
Risk: Silent value filtering may omit context or produce a review prompt that does not match what the user intended to retain. <br>
Mitigation: Use the review flow to inspect the selected topic and revise or clear cards that are off-target. <br>


## Reference(s): <br>
- [Cognitive Coach on ClawHub](https://clawhub.ai/DearChenzj/cognitivecoach) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Configuration] <br>
**Output Format:** [Concise chat messages and stored review-card fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May schedule a next-day 9:00 review trigger and keep reference answers hidden until feedback.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
