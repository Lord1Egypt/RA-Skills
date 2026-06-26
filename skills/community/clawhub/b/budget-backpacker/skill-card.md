## Description: <br>
Plan backpacking trips with ultra-budget itineraries, hostel recommendations, multi-city routes, survival tips, and booking support powered by Fliggy through the flyai CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to assemble budget backpacking routes, compare flights, lodging, and attractions, and return booking-linked Markdown based on flyai CLI results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run a global third-party flyai CLI. <br>
Mitigation: Review before installing, prefer manual installation, and run in a sandboxed environment where global package changes are acceptable. <br>
Risk: Travel details may be sent to the flyai provider during searches. <br>
Mitigation: Use only when sharing the requested itinerary details with that provider is acceptable. <br>
Risk: The artifact may create a local .flyai-execution-log.json containing raw user queries. <br>
Mitigation: Disable or delete the local execution log when query retention is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/budget-backpacker) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Fallback procedures](references/fallbacks.md) <br>
- [Execution log schema](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when retry or setup steps are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Every result is expected to include a Book link from detailUrl, avoid raw JSON, and include the flyai real-time pricing brand tag.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
