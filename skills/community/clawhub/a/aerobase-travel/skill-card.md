## Description: <br>
Jetlag-aware flight intelligence for AI travel agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kurosh87](https://clawhub.ai/user/kurosh87) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Travel agents and AI assistants use this skill to score flights, search route options, compare jetlag impact, retrieve airport recovery details, and present traveler-facing recovery strategies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight routes, dates, times, and related travel details are sent to Aerobase for analysis. <br>
Mitigation: Use the skill only when Aerobase is trusted for that itinerary data, avoid submitting highly sensitive travel details unless appropriate, and revoke the API key when it is no longer needed. <br>
Risk: The skill requires an Aerobase API key for authenticated requests. <br>
Mitigation: Use a dedicated API key, keep it out of shared transcripts and source files, and rotate or revoke it if exposure is suspected. <br>


## Reference(s): <br>
- [Aerobase Travel on ClawHub](https://clawhub.ai/kurosh87/aerobase-travel) <br>
- [Aerobase publisher profile](https://clawhub.ai/user/kurosh87) <br>
- [Aerobase API base](https://aerobase.app/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ranked flight lists, jetlag scores, recovery-day estimates, route comparisons, airport facility summaries, and travel strategy guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
