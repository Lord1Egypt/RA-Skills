## Description:

Search Capterra for B2B software, read a full product profile with the complete pricing table and 25 reviews included, and page deeper reviews with per-criterion scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and software-selection researchers use this skill to search Capterra, retrieve structured product profiles, compare pricing and alternatives, and analyze buyer review content through Scavio's Capterra API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SCAVIO_API_KEY may be exposed if copied into source code, logs, or shared prompts.

Mitigation: Load the key from an environment variable or secret store and keep it out of source control.

Risk: Scavio is an external paid API provider, so repeated or redundant calls can consume credits.

Mitigation: Monitor credit usage, avoid calling the reviews endpoint for page 1, and limit deeper review pagination to pages the user actually needs.

Risk: Using SDK packages introduces supply-chain exposure for the runtime environment.

Mitigation: Use an isolated environment, pin SDK versions when installing packages, or use direct HTTPS calls when avoiding SDK dependencies is preferred.

Risk: Incorrect review slugs or page numbers above 100 can return duplicate page-one data that appears successful.

Mitigation: Pass the exact reviews_url or slug returned by a prior API response, keep review pages within 1-100, and check for duplicate rows before summarizing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scavio-ai/skills/capterra-reviews-api)
- [Scavio Capterra API documentation](https://scavio.dev/docs/capterra-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=capterra-reviews-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=capterra-reviews-api)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON request and response descriptions plus bash, Python, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; API responses are structured JSON from Scavio.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
