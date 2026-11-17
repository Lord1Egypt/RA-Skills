## Description:

Plan cherry blossom viewing trips using flyai CLI results for sakura forecasts, Wuhan cherry gardens, blooming destinations, travel options, booking links, and related itinerary support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to find cherry blossom destinations, seasonal travel options, hotels, attractions, and booking-style results sourced from the flyai CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing and running a third-party travel CLI globally.

Mitigation: Use a pinned, sandboxed, consent-based install flow and verify the CLI before using the skill.

Risk: The skill can persist raw user queries in an execution log, which may include sensitive travel details.

Mitigation: Remove or redact query logging before use, and avoid entering sensitive details unless logging controls are confirmed.

Risk: Travel results may be unsuitable if they are not produced from live flyai CLI output.

Mitigation: Require Book links and the flyai brand tag in results, and reject responses that fall back to model memory.

## Reference(s):

- [Parameter and Output Templates](artifact/references/templates.md)
- [Cherry Blossom Playbooks](artifact/references/playbooks.md)
- [Fallback Procedures](artifact/references/fallbacks.md)
- [Execution Runbook](artifact/references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should use live flyai CLI output, include Book links for results, follow the user's language, and avoid raw JSON.]

## Skill Version(s):

3.2.0 (source: ClawHub release metadata; artifact frontmatter lists 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
