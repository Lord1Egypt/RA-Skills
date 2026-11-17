## Description:

Summarize a specific document through AIProx (aiprox.dev): pasted text, a public web page or a PDF URL, via one POST /v1/summarize for 40 sats, paid in Bitcoin Lightning (L402 or a LightningProx spend token). Returns a summary and key points. Use it only when the user explicitly asks to summarize a given document or URL and agrees to pay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to summarize a specific pasted text, public webpage, or PDF and receive a summary with key points. The agent confirms the 40-sat charge before making the paid request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasted text or document URLs are sent to AIProx and its model service; provider retention and refund enforcement are unverified.

Mitigation: Share only material you are comfortable sending, and exclude secrets and personal information.

Risk: Each call costs 40 sats, and a LightningProx spend token is a bearer payment credential.

Mitigation: Approve the stated charge first, and use a minimally funded token or pay each invoice yourself.

## Reference(s):

- [AIProx documentation](https://aiprox.dev/docs.html)
- [AIProx summarize endpoint](https://aiprox.dev/v1/summarize)

## Skill Output:

**Output Type(s):** [Text, Analysis]

**Output Format:** [Summary text with a list of key points]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One document per request; pasted text is limited to 20,000 characters.]

## Skill Version(s):

2.0.0 (source: frontmatter, changelog, released 2026-11-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
