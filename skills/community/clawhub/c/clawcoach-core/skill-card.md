## Description: <br>
AI health coach with dual personality modes that tracks nutrition, provides data-driven coaching, and helps users stay accountable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[authoredniko](https://clawhub.ai/user/authoredniko) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users and developers use this skill as a conversational health coach for meal logging, daily macro summaries, meal suggestions, persona switching, and nutrition accountability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores diet, profile, and meal-history data under ~/.clawcoach/. <br>
Mitigation: Install only if local storage of this health-related data is acceptable, and avoid entering sensitive medical or eating-disorder information unless external processing and retention behavior are clear. <br>
Risk: The skill includes a privacy claim that conflicts with its API-backed LLM requirement. <br>
Mitigation: Review the configured LLM backend and companion setup and food-analysis skills before relying on the full workflow. <br>


## Reference(s): <br>
- [ClawCoach Core on ClawHub](https://clawhub.ai/authoredniko/clawcoach-core) <br>
- [Publisher Profile](https://clawhub.ai/user/authoredniko) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown conversational responses with concise data summaries and coaching guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and writes ClawCoach profile and food-log data under ~/.clawcoach/ and requires ANTHROPIC_API_KEY for the configured LLM backend.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
