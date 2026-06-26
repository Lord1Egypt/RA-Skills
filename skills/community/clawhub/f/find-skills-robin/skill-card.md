## Description: <br>
Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Robin797860](https://clawhub.ai/user/Robin797860) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to find installable skills for specialized tasks, present relevant options, and optionally install selected skills through the Skills CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead the agent to search broad third-party skill sources and recommend persistent skill installs. <br>
Mitigation: Review each skill source and install command before installing, and install only skills that match the user's requested capability. <br>
Risk: The documented global auto-confirm install command can persistently change the user's agent while skipping confirmation prompts. <br>
Mitigation: Avoid `-y` unless the user explicitly wants to skip prompts, and prefer scoped installs over global installs when available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Robin797860/find-skills-robin) <br>
- [Skills directory](https://skills.sh/) <br>
- [Example Vercel React best practices skill listing](https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include skill search results, installation commands, and links to skill listings.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
