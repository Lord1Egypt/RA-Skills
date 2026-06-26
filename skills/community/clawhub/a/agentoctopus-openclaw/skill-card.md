## Description: <br>
Routes task-oriented requests through AgentOctopus when the best downstream skill or tool is not obvious. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leiw5173](https://clawhub.ai/user/leiw5173) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to route tool-backed tasks, such as lookups, transformations, research, weather, translation, geolocation, finance, and API-backed requests, to AgentOctopus and its downstream community skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AgentOctopus can automatically choose and run community skills, which may send prompts or task data to downstream tools or services. <br>
Mitigation: Review the enabled skill set before use and avoid submitting secrets, private personal data, API keys, or confidential work content unless the downstream handling is understood. <br>
Risk: The skill depends on the local octopus command and may surface setup commands when dependencies, API keys, or rate limits block execution. <br>
Mitigation: Install AgentOctopus from the expected source, review setup commands before running them, and configure only the credentials required for trusted downstream skills. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/leiw5173/agentoctopus-openclaw) <br>
- [awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [String or Markdown, sometimes including inline shell commands or configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [AgentOctopus returns a single downstream result or setup guidance when a required API key, rate limit, or dependency blocks execution.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
