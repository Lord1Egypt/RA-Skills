## Description: <br>
Search Google Flights for prices, times, and airlines. No API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awlevin](https://clawhub.ai/user/awlevin) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to query flight options from the command line or Python and compare prices, schedules, airlines, stops, and seat classes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The README documents a curl-to-bash installation path. <br>
Mitigation: Prefer uvx, uv tool install, pipx, or pip so the package manager handles installation from a trusted package source. <br>
Risk: The --upgrade command can modify the local installation. <br>
Mitigation: Use --upgrade only when intentionally updating the installed flight-search package. <br>
Risk: Flight search details are sent through the Google Flights scraping library. <br>
Mitigation: Avoid submitting sensitive travel details unless this data flow is acceptable for the deployment context. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/awlevin/flight-search) <br>
- [Flight Search GitHub Repository](https://github.com/Olafs-World/flight-search) <br>
- [Flight Search PyPI Package](https://pypi.org/project/flight-search/) <br>
- [fast-flights Underlying Library](https://github.com/AWeirdDev/flights) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Code, Guidance] <br>
**Output Format:** [Plain text flight summaries or JSON records, with optional Markdown examples and shell commands in documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight result fields include origin, destination, dates, current price signal, airline, departure and arrival times, duration, stop count, price, and best-flight flag.] <br>

## Skill Version(s): <br>
0.1.7 (source: pyproject.toml, CHANGELOG, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
