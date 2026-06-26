## Description: <br>
Scans installed skills and AGENTS.md to generate a routing config that maps conversation intents to skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ordo-tech](https://clawhub.ai/user/ordo-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent workspace maintainers use this skill to build or refresh skill-routing configuration from installed skill descriptions, especially when a workspace has many skills or newly installed skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated routing configuration can replace an existing AGENTS.md Skill Routing section, which may remove manual edits in that section. <br>
Mitigation: Back up AGENTS.md or write router.yml first, and keep custom routing rules outside the regenerated block before applying changes. <br>
Risk: Broad or ambiguous triggers may cause an agent to select the wrong skill after routing is enabled. <br>
Mitigation: Review the generated trigger list and resolve reported conflicts before relying on the routing configuration. <br>
Risk: Native auto-invoke behavior depends on the installed OpenClaw version. <br>
Mitigation: Confirm the target OpenClaw release supports skill_routing before treating the generated configuration as automatic behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ordo-tech/auto-invoke-router) <br>
- [Publisher profile](https://clawhub.ai/user/ordo-tech) <br>
- [Skill homepage](https://clawhub.com/@ordo-tech/auto-invoke-router) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and YAML routing configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update AGENTS.md or write router.yml, then reports mapped skills, skipped skills, and ambiguous triggers.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
