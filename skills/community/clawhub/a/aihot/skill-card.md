## Description:

Aihot Skill Lite lets an agent fetch current AI HOT news from aihot.virxact.com and produce concise Chinese Markdown briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kkkkhazix](https://clawhub.ai/user/kkkkhazix)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve recent AI industry news, AI HOT daily reports, category updates, and keyword-specific AI news, then present the results as readable Chinese Markdown briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-news search terms and timing parameters may be sent to aihot.virxact.com.

Mitigation: Avoid using confidential or sensitive search terms, and deploy only where sending those queries to the disclosed public service is acceptable.

Risk: The skill relies on live public AI news data, which may be incomplete, unavailable, or changed after retrieval.

Mitigation: Keep source URLs in the briefing and review important claims before using them in business-critical decisions.

Risk: The skill instructs curl to use a browser-like User-Agent for public API calls.

Mitigation: Limit calls to the disclosed AI HOT service and ensure usage follows the service's access expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kkkkhazix/skills/aihot)
- [Publisher profile](https://clawhub.ai/user/kkkkhazix)
- [AI HOT public site](https://aihot.virxact.com)
- [AI HOT OpenAPI specification](https://aihot.virxact.com/openapi.yaml)
- [Full AI HOT skill documentation](https://github.com/KKKKhazix/khazix-skills/tree/main/aihot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Chinese Markdown briefing with source links and optional inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should summarize current AI news in plain language and preserve source URLs.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
