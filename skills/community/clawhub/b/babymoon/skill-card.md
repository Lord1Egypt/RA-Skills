## Description: <br>
Book flights for babymoon trips and pre-baby vacations, including route searches, booking links, and related travel-planning guidance powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect travel parameters, run flyai flight searches, and format babymoon-friendly flight options with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install an unpinned global npm CLI before use. <br>
Mitigation: Review the flyai npm package and publisher before installation, require explicit approval, and prefer a sandbox, container, or local project install over a global install. <br>
Risk: Flight results and booking links can influence travel purchases and disclose route or date details. <br>
Mitigation: Share only the route and date details needed for the search, use only flyai CLI output for results, and verify booking links before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/babymoon) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Follows the user's language and requires booking links for reported flight results.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
