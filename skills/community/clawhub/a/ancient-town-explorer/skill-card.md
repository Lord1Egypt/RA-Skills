## Description: <br>
Discover preserved ancient towns, water villages, and traditional settlements with real-time travel data and booking links from the flyai CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel-focused agent users use this skill to find ancient towns, water villages, traditional settlements, and related trip options using live flyai CLI results. The skill helps collect required parameters, run supported flyai commands, and format Markdown recommendations with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install the flyai CLI globally without a pinned version. <br>
Mitigation: Manually verify the CLI package and install a pinned version before enabling the skill in a shared or production environment. <br>
Risk: Travel searches are sent to the flyai service. <br>
Mitigation: Avoid submitting sensitive personal travel details unless the user is comfortable sharing them with that service. <br>
Risk: Raw travel queries can be stored locally in `.flyai-execution-log.json`. <br>
Mitigation: Disable, review, or delete the local execution log when retaining raw queries is not appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/ancient-town-explorer) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>
- [Parent flyai skill referenced by artifact README](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Formats flyai CLI results into comparison tables and avoids raw JSON in user-facing output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
