## Description:

Tracks flights in real time with AviationStack, returning status, gate, schedule, delay, aircraft, and live position details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[copey02](https://clawhub.ai/user/copey02)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to look up IATA flight numbers and return readable flight status, schedule, gate, delay, aircraft, and live-position information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AviationStack free-tier requests may send the API key and flight lookup over unencrypted HTTP.

Mitigation: Use an HTTPS-capable AviationStack plan or another provider, rotate any key previously used over HTTP, and run the skill only after accepting this exposure.

Risk: The skill requires installing and running Python dependencies in the user's environment.

Mitigation: Install dependencies in an isolated environment with pinned versions where possible.

## Reference(s):

- [AviationStack API Setup](references/api-setup.md)
- [AviationStack Free Signup](https://aviationstack.com/signup/free)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration guidance]

**Output Format:** [Markdown-style terminal text or raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AVIATIONSTACK_API_KEY and the requests Python package; the AviationStack free tier uses HTTP.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
