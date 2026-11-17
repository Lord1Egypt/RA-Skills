## Description:

360 Zhiniao helps agents gather and summarize public 360 Zhiniao product, pricing, announcement, and documentation information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to summarize public 360 Zhiniao model capabilities, pricing details, service notices, and documentation links. It is limited to lightweight public-page information gathering and does not perform account actions or API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may browse or summarize information outside the intended public 360 Zhiniao product and documentation pages.

Mitigation: Limit use to disclosed public product, pricing, announcement, and documentation pages.

Risk: Users may attempt to use the skill for account actions, private data, API calls, or permission bypass.

Mitigation: Do not provide account operations, API invocation, private-data handling, or permission-bypass assistance.

Risk: Public pages may be dynamically loaded or rate limited, causing incomplete or stale summaries.

Mitigation: Wait for page content to load, respect platform access limits, and present retrieved information with source links.

## Reference(s):

- [360 Zhiniao homepage](https://ai.360.cn/)
- [ClawHub skill release page](https://clawhub.ai/codekungfu/skills/360-zhiniao-hot-trend)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text summaries with extracted links and lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based only on public 360 Zhiniao pages and should avoid sensitive or account-specific information.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
