## Description: <br>
Catch a pet or loot item by calling a configured remote pet backend API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aileaile](https://clawhub.ai/user/aileaile) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Claw Pet to trigger an authenticated catch action against a pet backend they control and receive a concise pet, item, empty, or error result summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Catch, fishing, or luck prompts send an authenticated remote request to the configured backend. <br>
Mitigation: Configure CATCH_API_URL only to a trusted HTTPS endpoint that you control and confirm that users expect the remote catch action before use. <br>
Risk: The skill requires a bearer API key for the pet backend. <br>
Mitigation: Use a dedicated low-scope API key, prefer environment variables for runtime configuration, and do not publish production secrets in _meta.json. <br>
Risk: Backend responses can be malformed, non-JSON, or shaped differently from the documented contract. <br>
Mitigation: Keep the backend aligned with references/api.md and treat error or malformed responses as user-visible failure categories rather than successful catches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aileaile/claw-pet) <br>
- [Publisher profile](https://clawhub.ai/user/aileaile) <br>
- [Catch Pet API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown summary of a remote catch result, including pet, item, empty, or error status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured backend URL and bearer API key before use.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
