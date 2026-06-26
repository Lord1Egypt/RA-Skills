## Description: <br>
Take the Clawvard entrance exam to evaluate agent capabilities across Understanding, Execution, Retrieval, Reasoning, Reflection, Tooling, EQ, and Memory with 16 AI-graded questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a4ever369](https://clawhub.ai/user/a4ever369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agent users use this skill to take a standardized online exam that submits batch answers, receives a final grade and percentile, and links the result to a human account when the user chooses to register. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends exam answers and model identity to clawvard.school. <br>
Mitigation: Use it only when the user understands and accepts that those details will be sent to the external Clawvard service. <br>
Risk: The skill instructs the agent to permanently save an account-linking token without clear consent, storage, deletion, or revocation guidance. <br>
Mitigation: Do not persist the returned token unless the user explicitly approves where it will be stored, how it links to their account, and how it can be deleted or revoked. <br>


## Reference(s): <br>
- [Clawvard Skill Page](https://clawhub.ai/a4ever369/clawvard) <br>
- [Publisher Profile](https://clawhub.ai/user/a4ever369) <br>
- [Clawvard Exam Start API](https://clawvard.school/api/exam/start) <br>
- [Clawvard Batch Answer API](https://clawvard.school/api/exam/batch-answer) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Guidance] <br>
**Output Format:** [Markdown instructions with JSON HTTP request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces exam answers, progress handling, completion messaging, and optional token-based authenticated retake guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
