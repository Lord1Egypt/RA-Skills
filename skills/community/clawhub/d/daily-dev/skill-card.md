## Description: <br>
Overcome LLM knowledge cutoffs with real-time developer content. daily.dev aggregates articles from thousands of sources, validated by community engagement, with structured taxonomy for precise discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[idoshamun](https://clawhub.ai/user/idoshamun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to access current developer content through the daily.dev API, personalize feeds, research technical topics, build profile context, and synthesize recent community discussions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A daily.dev API token grants access to personalized account content. <br>
Mitigation: Store the token securely, treat the dda_ prefix as sensitive, and send it only to api.daily.dev. <br>
Risk: The skill can guide profile, feed, bookmark, and stack changes through daily.dev endpoints. <br>
Mitigation: Require user confirmation before account, profile, feed, or bookmark changes. <br>
Risk: Repository scans and scheduled or background runs can expose more user context than intended. <br>
Mitigation: Run GitHub scans or scheduled workflows only with a clear user-approved scope. <br>


## Reference(s): <br>
- [daily.dev Skill Page](https://clawhub.ai/idoshamun/daily-dev) <br>
- [daily.dev Public API Base URL](https://api.daily.dev/public/v1) <br>
- [daily.dev Public API OpenAPI Spec](https://api.daily.dev/public/v1/docs/json) <br>
- [daily.dev Plus](https://app.daily.dev/plus) <br>
- [daily.dev API Token Settings](https://app.daily.dev/settings/api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with shell commands, API endpoint references, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a daily.dev Plus subscription and API token; daily.dev documents a 60 request per minute per-user rate limit.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
