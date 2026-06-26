## Description: <br>
Search flights via Google Flights, including nonstop and connecting flights, time and cabin filters, booking links, and multi-airport city searches without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrennerSpear](https://clawhub.ai/user/BrennerSpear) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Travelers, assistants, and developers use this skill to search real-time flight schedules and prices, compare route options, filter by stops, departure time, cabin class, and passengers, and retrieve Google Flights booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses external flight-search services and Google Flights-related data, so travel searches may be sent to third-party services. <br>
Mitigation: Avoid entering travel details you are not comfortable sharing with those services, and review organizational privacy requirements before use. <br>
Risk: The documented workflow depends on uv and the fast-flights package, which are installed or executed outside the reviewed SKILL.md artifact. <br>
Mitigation: Install uv from a trusted source, run the dependency in an isolated environment when appropriate, and review the dependency before operational use. <br>
Risk: The artifact documents scripts/flights-search, but evidence guidance notes that this script was not present in the reviewed artifact. <br>
Mitigation: Confirm that scripts/flights-search exists after installation before relying on the skill. <br>


## Reference(s): <br>
- [Flights on ClawHub](https://clawhub.ai/BrennerSpear/flights-search) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>
- [fast-flights Python package](https://github.com/AWeirdDev/flights) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and plain-text flight search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight results may include route, departure and arrival times, airline, price in USD, duration, and optional Google Flights booking links.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
