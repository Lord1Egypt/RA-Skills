## Description: <br>
Finds hotels near a specified attraction, landmark, or scenic spot by verifying the point of interest and searching FlyAI/Fliggy hotel results sorted by distance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to find accommodation close to a named attraction, confirm the POI, and present nearby hotel options with distance, pricing, ratings, and booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install an unpinned global FlyAI CLI package and fallback material can escalate to sudo. <br>
Mitigation: Require a manually reviewed, non-privileged or sandboxed installation path, and do not allow the agent to run sudo or global npm installation automatically. <br>
Risk: Hotel and POI searches send travel-search details to FlyAI/Fliggy. <br>
Mitigation: Limit prompts to the minimum travel details needed for search and avoid unnecessary personal, identity, passport, payment-adjacent, or sensitive itinerary information. <br>
Risk: The artifact instructs internal raw query logging without clear privacy controls. <br>
Mitigation: Disable, minimize, or review logging before deployment, and avoid retaining raw user travel queries unless the deployment has appropriate privacy controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/flyai-find-hotel-near-attraction) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Runbook](references/runbook.md) <br>
- [Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with CLI command examples, POI context, hotel comparison tables, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses FlyAI CLI results as the source for POI details, hotel distance, price, rating, and booking links.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
