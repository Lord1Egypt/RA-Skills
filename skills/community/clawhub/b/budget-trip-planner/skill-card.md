## Description: <br>
Plan trips on a tight budget with flight, hotel, attraction, itinerary, and related travel options powered by flyai and Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to collect budget travel parameters, run flyai CLI searches, and present low-cost itinerary, flight, hotel, and attraction options with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run a global third-party npm CLI. <br>
Mitigation: Review the CLI package and install it only in an environment where global npm packages are allowed. <br>
Risk: Travel-search details may be sent through flyai and Fliggy. <br>
Mitigation: Avoid entering passport, payment, or other sensitive personal details unless sharing them with the travel provider is intended. <br>
Risk: Raw travel requests may be saved in a local .flyai-execution-log.json file. <br>
Mitigation: Disable, delete, or periodically clear the local execution log when requests may contain sensitive details. <br>


## Reference(s): <br>
- [Parameter and Output Templates](references/templates.md) <br>
- [Budget Trip Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Parent flyai Skill](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when retry steps are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on flyai CLI results, include booking links for listed options, and avoid raw JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter states 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
