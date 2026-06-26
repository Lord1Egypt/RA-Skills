## Description: <br>
Clawdbot documentation expert with decision tree navigation, search scripts, doc fetching, version tracking, and config snippets for all Clawdbot features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to find Clawdbot documentation, retrieve relevant pages, compare recent documentation changes, and produce configuration guidance for providers, gateway settings, automation, platforms, tools, and installation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may run local helper scripts or apply generated configuration without checking whether the referenced Clawdbot documentation is current for their environment. <br>
Mitigation: Refresh cached documentation, cite the source URL, and review configuration snippets against the live documentation before deployment. <br>
Risk: The skill includes shell-command workflows for searching, fetching, indexing, and tracking documentation. <br>
Mitigation: Review the scripts and requested permissions before installation, and run helper commands only in an intended local workspace. <br>


## Reference(s): <br>
- [Clawdbot Documentation](https://docs.clawd.bot/) <br>
- [Clawdbot Discord Provider Documentation](https://docs.clawd.bot/providers/discord) <br>
- [Common Config Snippets](snippets/common-configs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, links, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cited documentation URLs and JSON configuration examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
