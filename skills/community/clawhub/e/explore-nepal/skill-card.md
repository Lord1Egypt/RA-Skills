## Description: <br>
Book flights to Nepal, including Kathmandu and Pokhara, using flyai CLI flight-search results with booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to search Nepal-related flights, compare recommended, cheapest, fastest, direct, and flexible-date options, and return Markdown results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run an unpinned global FlyAI CLI package. <br>
Mitigation: Install only after user approval, prefer a sandboxed environment, and verify the CLI before any flight search. <br>
Risk: Flight results and booking links depend on external flyai CLI output. <br>
Mitigation: Treat results as flight-search assistance, verify prices and booking details before purchase, and do not fabricate missing results. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/dingtom336-gif/explore-nepal) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for flight data and should not produce raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
