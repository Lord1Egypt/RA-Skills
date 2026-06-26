## Description: <br>
Transforms vague prompts into precise, structured AI instructions for prompt refinement, prompt engineering, system prompts, and more effective AI instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iliaal](https://clawhub.ai/user/iliaal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, prompt engineers, and agent builders use this skill to turn vague requests into precise markdown prompts, including system prompts and task instructions, while asking for clarification when intent is unclear. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt content may include secrets, private data, or other sensitive information. <br>
Mitigation: Avoid putting secrets or private data into prompts submitted for refinement, and review the refined prompt before reuse. <br>
Risk: The optional save step can store refined prompt content in the workspace. <br>
Mitigation: Approve saving only when workspace persistence is intended; otherwise use the refined prompt without writing it to .ai/PROMPT.md. <br>
Risk: Refining harmful or illegal requests could make unsafe instructions more actionable. <br>
Mitigation: Do not refine prompts for harmful or illegal tasks, and ask for clarification when the original intent is unclear. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown prompt text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs only the refined prompt unless the user explicitly asks for explanation; may offer to append the result to .ai/PROMPT.md after user confirmation.] <br>

## Skill Version(s): <br>
3.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
