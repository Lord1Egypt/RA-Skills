## Description:

Encoding Converter helps agents convert, decode, hash, and inspect common encoding formats including Base64, URL encoding, hex, HTML entities, JWT payloads, and numeric bases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert and inspect encoded data during debugging, validation, and integration work. It is useful for local Base64, URL, hex, hash, JWT payload, HTML entity, and numeric base conversion tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decoded JWT contents may be misleading if used for security decisions without signature and claim validation.

Mitigation: Use JWT decoding only for inspection; validate the signature, issuer, audience, expiration, and accepted algorithms before making authorization or trust decisions.

Risk: Sensitive inputs provided for encoding, hashing, or decoding may expose secrets through agent transcripts, logs, or copied outputs.

Mitigation: Avoid processing production secrets unless the surrounding agent environment is approved for sensitive data handling.

## Reference(s):

- [Encoding Converter ClawHub listing](https://clawhub.ai/kaiyuelv/skills/encoding-converter)

## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [Plain text strings, JSON-like decoded JWT objects, hashes, and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local utility output; JWT decoding is for inspection only and does not verify signatures.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
