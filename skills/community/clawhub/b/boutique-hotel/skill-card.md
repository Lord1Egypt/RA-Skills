## Description: <br>
Book flights to boutique hotels and designer stay destinations, with related travel services powered by Fliggy and flyai CLI results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-assistant agents use this skill to search boutique-hotel travel routes, compare flight options, and format booking-ready Markdown from live flyai CLI results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install the flyai CLI globally if it is missing. <br>
Mitigation: Install or verify the flyai CLI from a trusted source before using the skill, and avoid allowing unattended global npm installation. <br>
Risk: The skill returns external commercial booking links. <br>
Mitigation: Treat booking links as third-party commercial destinations and review pricing, terms, and destination URLs before purchase. <br>
Risk: The security guidance notes an inconsistent command example involving direct-flight results. <br>
Mitigation: Confirm current flyai CLI support for the direct-flight flag before relying on direct-flight filtering. <br>


## Reference(s): <br>
- [Parameter Collection and Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on live flyai CLI results and include booking links for listed travel options.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
