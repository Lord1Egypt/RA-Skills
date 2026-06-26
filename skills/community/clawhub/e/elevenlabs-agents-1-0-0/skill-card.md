## Description: <br>
Create, manage, and deploy ElevenLabs conversational AI agents. Use when the user wants to work with voice agents, list their agents, create new ones, or manage agent configurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sieyer](https://clawhub.ai/user/Sieyer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage ElevenLabs conversational agents through guided actions such as listing, creating, syncing, deploying, adding tools, and retrieving embed code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may silently initialize an ElevenLabs project or create local files such as agents.json. <br>
Mitigation: Require explicit approval before project initialization or file creation, and review generated files before committing them. <br>
Risk: The skill can push local agent changes to ElevenLabs. <br>
Mitigation: Preview deployment changes first and confirm with the user before running commands that publish or overwrite remote agent state. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Sieyer/elevenlabs-agents-1-0-0) <br>
- [Publisher profile](https://clawhub.ai/user/Sieyer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text summaries with optional HTML snippets and generated configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the elevenlabs CLI binary; may create or modify ElevenLabs project files in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
