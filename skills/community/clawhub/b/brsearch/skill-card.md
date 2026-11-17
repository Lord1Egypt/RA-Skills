## Description:

Brsearch directs an agent to use a logged-in DeepSeek browser session for information search while disabling normal web and memory retrieval tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siysun](https://clawhub.ai/user/siysun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use Brsearch to route information queries through DeepSeek in a browser session, then summarize the model response for follow-up work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries may include private, work, personal, regulated, or credential-like information sent to DeepSeek under a logged-in account.

Mitigation: Use the skill only when the query content is approved for DeepSeek, and avoid submitting sensitive or credential-like information.

Risk: The skill disables normal retrieval tools and relies on an online model response, which can produce incomplete or misleading answers.

Mitigation: Verify important answers with authoritative sources before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/siysun/skills/brsearch)
- [DeepSeek Chat](https://chat.deepseek.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance and summarized search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a browser session with access to DeepSeek Chat.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
