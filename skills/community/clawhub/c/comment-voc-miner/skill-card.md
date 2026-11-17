## Description:

Analyzes public or user-supplied social comments and organizes their language into a same-day voice-of-customer brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing teams use the skill to turn a public post, a named category, or supplied comments into a source-grounded voice-of-customer brief. It organizes objections, verbatim lines, purchase concerns, FAQ answers, live-commerce replies, and spoken hooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting the account grants Beatra permissions beyond the comment-analysis workflow, including media and voice capabilities.

Mitigation: Review the full Beatra permission set before connecting, and revoke the shared device authorization in Beatra Console when access is no longer wanted.

Risk: Paid lookup approval relies on the agent following instructions.

Mitigation: Require explicit confirmation for each lookup; use pasted comments for analysis that does not need a paid lookup.

Risk: Registration sends installation and runtime information.

Mitigation: Review the registration disclosure before connecting and revoke the shared device authorization when access is no longer wanted.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/beatra-ai/skills/comment-voc-miner)
- [Beatra skill page](https://beatra.ai/skills/comment-voc-miner)
- [Comment lookup guidance](artifact/references/comment-lookup.md)
- [Writing the brief](artifact/references/brief.md)
- [Updates and security](artifact/references/updates-and-security.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Markdown voice-of-customer brief with sourced comment excerpts, objections, FAQs, replies, and hooks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sections depend on available comments; looked-up material is attributed, and missing figures are stated rather than estimated.]

## Skill Version(s):

0.2.4 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
