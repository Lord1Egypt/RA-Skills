## Description:

Pay-per-call tasks on AIProx (aiprox.dev), paid in Bitcoin Lightning sats. Use it when the user asks to run a task through AIProx or to buy one of its capabilities. Orchestrate is 50 sats: one task, up to 4 steps on AIProx's own bots, one summarized answer. Single capabilities have their own prices: AI web answer 35, page text extract 20, summarize 40, translate 40. Payment is a LightningProx spend token or L402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yebdmo2](https://clawhub.ai/user/yebdmo2)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents use AIProx when a user wants to purchase a task such as web search, page extraction, summarization, or translation, or orchestrate up to four steps and receive a summarized answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task text and any supplied URLs, text, or image URLs are sent to AIProx and may be passed to AI model providers or other services; calls also use a payment credential.

Mitigation: Review each request before sending, omit secrets and personal data, protect the spend token as a bearer credential, and confirm the Lightning price before a paid call.

## Reference(s):

- [AIProx documentation](https://aiprox.dev/docs.html)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Concise text response with findings or transformed content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Orchestrated calls return one summary; search results may include up to five source links.]

## Skill Version(s):

4.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
