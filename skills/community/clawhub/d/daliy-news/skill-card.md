## Description: <br>
Use when users need daily news summaries, current events, or want to stay informed about world news in Chinese. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JaceyMarvin99](https://clawhub.ai/user/JaceyMarvin99) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill to fetch daily or recent Chinese news briefings from the 60s API, including standard daily summaries, historical date requests, and alternate response formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts a third-party news API when used. <br>
Mitigation: Use it only where outbound access to the 60s API is acceptable and disclose that dependency to users. <br>
Risk: News availability and freshness depend on the external service and recent-date coverage. <br>
Mitigation: Check the returned status and request a nearby recent date when no data is returned. <br>
Risk: The output is primarily oriented toward Chinese daily news summaries. <br>
Mitigation: Confirm the language and format fit the user request, and verify high-impact facts against authoritative sources. <br>


## Reference(s): <br>
- [60s API endpoint used by the skill](https://60s.viki.moe/v2/60s) <br>
- [Daily News on ClawHub](https://clawhub.ai/JaceyMarvin99/daliy-news) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [stdout from a shell script; JSON, plain text, Markdown, or image URLs depending on the encoding option] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calls the third-party 60s API and supports optional encoding and YYYY-MM-DD date parameters.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
