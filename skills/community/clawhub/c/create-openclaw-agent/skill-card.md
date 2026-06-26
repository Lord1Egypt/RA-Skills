## Description: <br>
Creates configured OpenClaw agents with identity files, workspace setup, team integration, model selection, and channel routing in interactive or command-line modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mengwuzhi](https://clawhub.ai/user/mengwuzhi) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to scaffold new agents, generate identity and workspace files, and update OpenClaw routing and team configuration with preview support through dry-run mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent changes to OpenClaw agent, routing, channel account, and team configuration files. <br>
Mitigation: Run with dry-run first, back up openclaw.json and TEAM.md, and review the selected workspace path before executing. <br>
Risk: The artifact includes guidance for obtaining browser or session tokens. <br>
Mitigation: Avoid extracting tokens from headers, cookies, or local storage; prefer official scoped API tokens or supported login flows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mengwuzhi/create-openclaw-agent) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [GET_TOKEN.md](artifact/GET_TOKEN.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance, generated Markdown files, JSON configuration updates, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run in dry-run mode before making persistent OpenClaw configuration changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
