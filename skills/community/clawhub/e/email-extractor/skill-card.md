## Description:

Extract and deduplicate up to 20 email addresses from any webpage URL or plain text content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loverun321](https://clawhub.ai/user/loverun321)

### License/Terms of Use:


## Use Case:

Agents and users use this skill to extract email addresses from public webpage URLs or supplied text, deduplicate the results, and return up to 20 matches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches arbitrary URLs, which can expose private networks, metadata services, redirected restricted hosts, or oversized responses if URL access is not constrained.

Mitigation: Use only public URLs unless URL fetching is constrained with validation that blocks localhost, private networks, metadata services, unsafe redirects, and oversized responses.

Risk: The artifact exposes a credential-looking API key.

Mitigation: Remove the exposed key from the artifact and rotate it before installing or operating the skill.

Risk: The skill returns an undocumented paid status and advertises a per-extraction price.

Mitigation: Review billing and payment-status behavior before use, and document expected charging and response semantics for users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loverun321/skills/email-extractor)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [JSON object containing extracted email addresses and a count.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deduplicates results and limits output to 20 email addresses per extraction.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
