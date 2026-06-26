## Description: <br>
Discover, vet, and install agent skills by searching major registries including skills.sh, clawhub.ai, and GitHub, showing native ranking signals, scanning top candidates for risky patterns, and flagging skills that are already installed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to find suitable published skills for a task, compare registry-native popularity and relevance signals, and decide whether a candidate should be reviewed or installed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Registry search results may include untrusted third-party skills. <br>
Mitigation: Review any recommended skill, including its SKILL.md and bundled scripts, before approving installation. <br>
Risk: Broad capability-discovery prompts can trigger external public registry lookups. <br>
Mitigation: Use the skill for intentional skill discovery and rely on its disclosed behavior: it queries public sources and does not auto-install skills or access secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kalvinrv/agentspace-find-skills) <br>
- [AgentSpace homepage](https://agentspace.so) <br>
- [skills.sh search API](https://skills.sh/api/search?q=${ENC_QUERY}&limit=${LIMIT}) <br>
- [ClawHub search API](https://clawhub.ai/api/search?q=${ENC_QUERY}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown-style terminal report or machine-readable JSON, with inline shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq and curl; gh and unzip are optional and degrade gracefully when absent.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
