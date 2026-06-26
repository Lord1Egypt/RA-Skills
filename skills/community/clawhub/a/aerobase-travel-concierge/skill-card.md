## Description: <br>
Complete AI travel concierge covering flights, hotels, lounges, awards, activities, deals, wallet, and recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kurosh87](https://clawhub.ai/user/kurosh87) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External travelers and travel-support agents use this skill to plan, compare, book, and optimize trips through Aerobase APIs, including flight scoring, hotels, lounges, awards, activities, wallet information, and jetlag recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support booking, cancellation, payment-adjacent, wallet, loyalty-program, boarding-pass, and delete actions through Aerobase APIs. <br>
Mitigation: Require explicit user confirmation before any booking, cancellation, card or wallet change, loyalty-program change, payment-related step, boarding-pass storage, or delete action. <br>
Risk: The required Aerobase API key may expose sensitive travel and account data to the agent. <br>
Mitigation: Install only when the user accepts Aerobase API access, keep AEROBASE_API_KEY in the agent environment, and redact API keys from all user-visible output. <br>


## Reference(s): <br>
- [Aerobase API Reference](references/aerobase-api.md) <br>
- [Aerobase Homepage](https://aerobase.app) <br>
- [Aerobase OpenAPI Spec](https://aerobase.app/api/v1/openapi) <br>
- [ClawHub Skill Page](https://clawhub.ai/kurosh87/aerobase-travel-concierge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown with concise travel recommendations, next actions, and API-backed results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AEROBASE_API_KEY; free usage is capped at 5 requests per day.] <br>

## Skill Version(s): <br>
3.3.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
