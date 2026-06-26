## Description: <br>
Search the x402 bazaar for paid API services when the user wants to find APIs, discover services, browse the marketplace, or needs an external service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search, browse, and inspect paid x402 API services before deciding whether to use a separate payment skill for requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad automatic activation may cause this marketplace search helper to run as a fallback when a more specific skill would be better. <br>
Mitigation: Install and enable it only when x402/API marketplace discovery is intended, and review whether fallback activation is appropriate for the agent. <br>
Risk: The skill runs an external Agnic npm CLI at runtime. <br>
Mitigation: Run it only in environments where fetching and executing the Agnic CLI is trusted and allowed by policy. <br>
Risk: The details command can inspect arbitrary URLs for x402 payment requirements. <br>
Mitigation: Review target URLs before running details checks and avoid using the skill as a general URL inspection fallback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agnicpay-prog/agnicpay-search-for-service) <br>
- [Publisher profile](https://clawhub.ai/user/agnicpay-prog) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may be cached locally by the Agnic CLI and refreshed from the x402 bazaar.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
