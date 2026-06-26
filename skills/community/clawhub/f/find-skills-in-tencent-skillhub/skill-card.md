## Description: <br>
Search, install, upgrade, and manage agent skills using skillhub CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuhonglei](https://clawhub.ai/user/wuhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to search ClawHub skill data, install skills by slug, list installed skills, and check or apply skillhub CLI and skill upgrades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently install, overwrite, bulk-upgrade, and self-upgrade agent skill tooling. <br>
Mitigation: Review actions before execution, prefer search and check_only modes first, approve each install or upgrade explicitly, and avoid force unless overwriting is intended. <br>
Risk: Upgrade-all and self-upgrade actions can change future agent behavior. <br>
Mitigation: Run check_only before applying upgrades and review the reported changes before allowing the command to proceed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuhonglei/find-skills-in-tencent-skillhub) <br>
- [Skillhub CLI installation guide](https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/skillhub.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON input examples and shell command output from skillhub] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires skillhub and jq binaries; install, upgrade, upgrade-all, force, and self-upgrade actions can change local agent skill state.] <br>

## Skill Version(s): <br>
1.0.4 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
