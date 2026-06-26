## Description: <br>
Book Indonesia travel options, including flights to Bali, Jakarta, and Surabaya, by collecting route parameters, running the flyai CLI, and formatting live results with booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search Indonesia travel routes, compare flight options, and produce Markdown summaries with booking links based on live flyai CLI output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install and run an unpinned global travel CLI package. <br>
Mitigation: Require explicit approval before any npm global install, prefer a pinned local or sandboxed install, and run travel-search commands only in a trusted environment. <br>
Risk: Flight and booking results depend on external CLI output and third-party booking links. <br>
Mitigation: Verify booking links and itinerary details before entering payment or personal information, and do not fabricate results when the CLI is unavailable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dingtom336-gif/explore-indonesia) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live flyai CLI results; each travel option should include a booking link when available.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
