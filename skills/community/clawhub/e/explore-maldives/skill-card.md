## Description: <br>
Plan Maldives travel using flyai CLI searches for flights, hotels, attractions, itineraries, visa information, insurance, car rental, and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to assemble Maldives trip options from live flyai results, including flights, lodging, activities, and booking links. It is suited for itinerary planning and comparison workflows where current travel data is required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install or rely on a global @fly-ai/flyai-cli package. <br>
Mitigation: Install and verify the CLI manually from a trusted package source before allowing the agent to run travel searches. <br>
Risk: Travel queries may be retained locally in .flyai-execution-log.json. <br>
Mitigation: Disable or delete the execution log when local retention of raw travel queries is not acceptable. <br>
Risk: Travel answers can be incomplete or unreliable when live flyai CLI results are unavailable. <br>
Mitigation: Require the flyai version check and include only CLI-backed results with detailUrl booking links. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dingtom336-gif/explore-maldives) <br>
- [README](README.md) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown travel recommendations and comparison tables with inline booking links and occasional bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live flyai CLI output; booking results should include detailUrl links and a flyai attribution tag.] <br>

## Skill Version(s): <br>
3.2.1 (source: server release metadata; artifact frontmatter lists 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
