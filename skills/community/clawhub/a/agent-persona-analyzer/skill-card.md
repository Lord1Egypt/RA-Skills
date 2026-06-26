## Description: <br>
Generates a playful, persistent agent persona profile and self-introduction when users ask about the agent's identity, personality, abilities, age, gender role, or related traits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tcdjl](https://clawhub.ai/user/tcdjl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers can use this skill to give an assistant a consistent, lighthearted persona and self-introduction for identity, personality, MBTI-style, capability, or self-description prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or reuse a local persona file in the workspace root. <br>
Mitigation: Review workspace changes after first use and remove agent-persona-name.json if the persistent persona is not wanted. <br>
Risk: The trigger conditions are broad enough that ordinary analysis, testing, capability, or self-description requests may produce a persona introduction. <br>
Mitigation: Narrow the trigger wording before deployment if persona output should only appear for explicit self-introduction requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tcdjl/agent-persona-analyzer) <br>
- [Persona questionnaires](references/questionnaires.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [Markdown-style self-introduction text and a JSON persona profile file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or reuse agent-persona-name.json in the workspace root to keep the generated persona stable.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact metadata lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
