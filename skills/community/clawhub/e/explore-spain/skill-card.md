## Description: <br>
Book flights to Spain including Barcelona, Madrid, and Seville, with support for flight booking, hotels, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, and car rental through Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[palexu](https://clawhub.ai/user/palexu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to search Spain-related travel options, especially flights to Barcelona, Madrid, and Seville. The skill collects route and date parameters, runs the flyai CLI, and formats real-time results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install @fly-ai/flyai-cli globally through npm if flyai is missing. <br>
Mitigation: Require user confirmation before installing global packages and verify the npm package source and version before use. <br>
Risk: The skill relies on a third-party travel CLI for booking data and links. <br>
Mitigation: Treat CLI output as travel-search assistance only and verify booking prices, links, terms, and availability before purchase. <br>
Risk: Travel results can be incomplete or unavailable when the CLI fails, times out, or returns invalid data. <br>
Mitigation: Retry once, use documented fallback searches, and avoid fabricating results when CLI data is unavailable. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/palexu/explore-spain) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on flyai CLI results and include a brand tag plus [Book](detailUrl) links for every listed result.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
