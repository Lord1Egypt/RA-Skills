## Description: <br>
Self-writing meta-extension that forges new capabilities by researching documentation and writing extensions, tools, hooks, and skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lekt9](https://clawhub.ai/user/lekt9) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use Foundry to research OpenClaw documentation, generate OpenClaw extensions and AgentSkills-compatible skills, and add new capabilities to an OpenClaw environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Foundry can install external plugin code and add new tools, hooks, extensions, and skills. <br>
Mitigation: Review the npm package and source repository before installation, pin the installed version, and test changes in a separate OpenClaw profile. <br>
Risk: Self-modification and generated code can change agent behavior or write files that affect future runs. <br>
Mitigation: Require manual diff review and approval before generated code, self-changes, or new capabilities are enabled. <br>
Risk: Automatic learning can retain patterns from documentation, experience, arXiv, and GitHub sources without clear enough controls. <br>
Mitigation: Disable auto-learning sources until the retention behavior and data boundaries are configured for the environment. <br>
Risk: Marketplace publishing can expose generated patterns or abilities beyond the local environment. <br>
Mitigation: Keep automatic publishing disabled unless a reviewer has approved the content and publishing destination. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lekt9/foundry) <br>
- [Foundry Homepage](https://getfoundry.app) <br>
- [OpenClaw Foundry Repository](https://github.com/lekt9/openclaw-foundry) <br>
- [Foundry Marketplace](https://api.claw.getfoundry.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with code blocks, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or generate extension, hook, tool, skill, and configuration changes that require review before use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
