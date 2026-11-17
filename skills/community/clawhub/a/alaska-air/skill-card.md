## Description:

Scrapes Alaska Airlines award calendar and flight data to check miles, award availability, and prices for one-way trips on alaskaair.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iskwang](https://clawhub.ai/user/iskwang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search Alaska Airlines one-way mileage award availability for specified routes and months, then return available dates, mileage prices, cash prices, and direct booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flight-search details and booking links may be sent through Telegram or processed by external worker models.

Mitigation: Ask for confirmation before sending results to a Telegram destination, and offer a default path that returns results in the main conversation.

Risk: The artifact uses shell commands and predictable files in shared /tmp paths.

Mitigation: Validate airport/date inputs and use isolated temporary files or directories before executing scraping or parsing commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iskwang/skills/alaska-air)
- [Alaska Airlines award calendar search endpoint](https://www.alaskaair.com/search/calendar)
- [Alaska Airlines airport lookup endpoint](https://www.alaskaair.com/search/api/citySearch/getAllAirports)
- [Alaska Airlines discounts endpoint](https://www.alaskaair.com/search/api/discounts)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with JSON snippets, shell commands, and booking URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are intended to include available award dates sorted by mileage, cash prices, and direct booking links; the artifact also directs immediate Telegram delivery when a message destination is provided.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
