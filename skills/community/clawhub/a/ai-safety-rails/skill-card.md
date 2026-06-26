## Description: <br>
Automatically configures safety rules, trust levels, prompt-injection defenses, and approval workflows to secure OpenClaw agent actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[casperzinou](https://clawhub.ai/user/casperzinou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate safety configuration for OpenClaw agents, including trust levels, hard action limits, prompt-injection defenses, and approval workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aggressive autonomy settings can permit broader agent action if allowed actions and stop conditions are not explicit. <br>
Mitigation: Define allowed actions, stop conditions, and a private verified approval channel before enabling higher trust levels. <br>
Risk: The skill recommends installing ai-sentinel and skill-guard, which are separate skills with their own security posture. <br>
Mitigation: Review and scan ai-sentinel and skill-guard separately before installing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/casperzinou/ai-safety-rails) <br>
- [Publisher profile](https://clawhub.ai/user/casperzinou) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown safety configuration with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The agent asks for risk tolerance, hard rules, and a verified messaging channel before generating the configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
