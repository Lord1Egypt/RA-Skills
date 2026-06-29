## Description: <br>
Project onboarding for game development. Detects project state, asks guided questions to determine user context, and routes to the correct workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toilanguyen2910](https://clawhub.ai/user/toilanguyen2910) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to start or assess a game project, choose a suitable path based on project state and experience level, and capture onboarding decisions in a project context file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases may start the onboarding flow during a more general game-development conversation. <br>
Mitigation: Use the skill deliberately when project onboarding is intended and confirm the user's goal before creating or changing project files. <br>
Risk: The skill may inspect workspace files and create a persistent context.md artifact as part of onboarding. <br>
Mitigation: Run it in the intended project workspace and review generated file content before relying on it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/toilanguyen2910/skills/game-dev-start) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with questions, routing recommendations, optional shell commands, and a context.md template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a context.md file when the agent environment supports workspace writes; chat-only environments receive the file content as markdown.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
