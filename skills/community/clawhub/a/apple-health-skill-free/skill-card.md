## Description: <br>
Helps agents retrieve daily workout plans and query Apple Health-style workout history and athlete profile data through a health data sync service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request generated workout plans, retrieve recent workout records, and fetch athlete profile information for basic fitness data review. It is intended for normal ClawHub use, with care around health data and external API access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive health, workout, heart-rate, and profile data through an external API. <br>
Mitigation: Install only when the health data sync service is trusted, confirm before sending sensitive data externally, and avoid exposing health data in logs or shared outputs. <br>
Risk: Authenticated features depend on API keys and broad agent permissions including command execution. <br>
Mitigation: Store API keys in environment variables, review proposed commands and callback URLs before allowing execution, and run the agent in a constrained workspace. <br>
Risk: The server security verdict is suspicious because the skill combines sensitive health data access with an unrelated Security trigger. <br>
Mitigation: Do not use this skill for Security tasks; review activation behavior and intended scope before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/apple-health-skill-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request examples and structured health or workout data summaries.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
