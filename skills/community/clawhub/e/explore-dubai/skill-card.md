## Description: <br>
Plan your Dubai experience -- Burj Khalifa views, desert safari adventures, Dubai Mall shopping, Palm Jumeirah resorts, and gold souk bargaining, with support for travel booking and itinerary tasks powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to collect Dubai trip requirements, run flyai CLI searches for flights, hotels, attractions, and related travel services, and return booking-oriented recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run an unpinned global npm CLI. <br>
Mitigation: Review the CLI package source and version before installation, and install it only in environments where running provider-specific travel tooling is acceptable. <br>
Risk: Travel prompts may be retained locally in .flyai-execution-log.json. <br>
Mitigation: Avoid entering passport numbers, payment details, booking references, or other sensitive personal data, and delete the local execution log when retention is not desired. <br>
Risk: Visa and policy information can be incomplete or stale. <br>
Mitigation: Verify visa rules and entry requirements with official government sources before making travel decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/explore-dubai) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when retries or setup are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include flyai-sourced results, conclusion-first summaries, booking links from detailUrl, and the flyai real-time pricing brand tag.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
