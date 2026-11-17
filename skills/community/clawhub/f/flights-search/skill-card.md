## Description:

Searches Google Flights data for nonstop and connecting flight options with time, cabin, passenger, city or airport, and booking-link filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brennerspear](https://clawhub.ai/user/brennerspear)

### License/Terms of Use:


## Use Case:

External users and travel-planning agents use this skill to search real-time flight schedules and prices, compare route options, apply cabin and time filters, and obtain Google Flights booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed package is missing the claimed local scripts/flights-search CLI.

Mitigation: Do not rely on the skill until the package includes the CLI or the documentation is corrected and re-reviewed.

Risk: The skill depends on mutable external install and runtime code through uvx and fast-flights.

Mitigation: Install dependencies in a dedicated virtual environment and pin fast-flights to a reviewed version before use.

Risk: The documented uv install path uses a remote shell installer.

Mitigation: Prefer a verified package-manager installation path for uv.

## Reference(s):

- [fast-flights Python package](https://github.com/AWeirdDev/flights)
- [uv documentation](https://docs.astral.sh/uv/)
- [Flights skill page](https://clawhub.ai/brennerspear/skills/flights-search)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and tabular flight-search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight results may include route, departure and arrival times, airline, price, duration, result count, and optional Google Flights links.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
