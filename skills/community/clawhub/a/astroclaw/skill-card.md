## Description: <br>
Daily astronomical alignment and cosmic entropy for autonomous AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qeireal](https://clawhub.ai/user/qeireal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use AstroClaw to fetch daily horoscope-style forecast text for a selected zodiac sign, add playful creative variance to agent routines, and configure lightweight state tracking for a daily check-in. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts astroclaw.xyz to fetch horoscope forecast text. <br>
Mitigation: Install only in environments where this external request is acceptable. <br>
Risk: Returned horoscope text is external content that could influence agent behavior. <br>
Mitigation: Treat forecasts as untrusted entertainment content, sanitize to plain text, enforce length limits, and avoid using them in decision-critical workflows. <br>
Risk: The skill may save low-sensitivity forecast or state data locally. <br>
Mitigation: Store only sanitized forecast text and minimal alignment state needed for the daily check-in. <br>


## Reference(s): <br>
- [AstroClaw homepage](https://astroclaw.xyz) <br>
- [Daily forecast API](https://astroclaw.xyz/api/forecasts/{YYYY-MM-DD}/{sign}.json) <br>
- [Today's forecasts](https://astroclaw.xyz/today/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with optional JSON snippets and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch horoscope JSON from astroclaw.xyz and optionally store sanitized low-sensitivity forecast or state text locally.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
