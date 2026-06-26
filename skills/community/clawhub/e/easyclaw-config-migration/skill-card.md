## Description: <br>
Migrate settings from EasyClaw into OpenClaw by locating EasyClaw desktop and runtime config files, comparing them with the active OpenClaw config, and generating a conservative selective merge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sjingh](https://clawhub.ai/user/sjingh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect EasyClaw configuration files, identify settings with clear OpenClaw equivalents, and optionally apply a backed-up selective merge into ~/.openclaw/openclaw.json. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The migration can copy sensitive fields, including authentication tokens, from EasyClaw configuration into the OpenClaw config. <br>
Mitigation: Run the report and dry-run merge first, review the mapped fields, and remove token mappings before applying if token migration is not intended. <br>
Risk: Applying the merge changes ~/.openclaw/openclaw.json. <br>
Mitigation: Use the default backup behavior, review the changed paths after the merge, and keep the timestamped backup until the migrated configuration is validated. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/sjingh/easyclaw-config-migration) <br>
- [EasyClaw product site](https://easyclaw.com/) <br>
- [MIT-0 license](https://spdx.org/licenses/MIT-0.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and redacted configuration summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a dry-run report, changed-path summary, and backup path when the merge script is applied.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
