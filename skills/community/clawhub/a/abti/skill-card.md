## Description: <br>
ABTI (AI-Based Type Indicator) analyzes how users talk to AI to assign one of 28 personality types and generate a roast-style personality result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindy-youmind](https://clawhub.ai/user/mindy-youmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users ask an agent to analyze the chat context available to it for entertainment, identify an ABTI personality type, and produce a roast-style result or shareable card without exposing raw chat content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to review chat context that may contain sensitive information. <br>
Mitigation: Use a fresh or minimized conversation and avoid running it where unrelated sensitive history is available. <br>
Risk: The skill relies on instructions that may be missing or changeable. <br>
Mitigation: Inspect the prompt or reference instructions before use and stop if they request broader access or unexpected actions. <br>
Risk: The skill can create a shareable result through YouMind. <br>
Mitigation: Require confirmation before posting and verify that only the personality type and roast text are shared. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindy-youmind/abti) <br>
- [ABTI homepage](https://youmind.com/abti) <br>
- [Manual ABTI card generator](https://youmind.com/abti/g) <br>
- [YouMind](https://youmind.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls] <br>
**Output Format:** [Markdown personality result or shareable URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send only the derived personality result to YouMind when HTTP posting is available; raw chat content should not be included.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release evidence; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
