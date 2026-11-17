## Description:

Claw Pet calls a configured remote pet backend API to trigger a catch action and formats pet, item, empty, or error responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aileaile](https://clawhub.ai/user/aileaile)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to trigger a catch action against a pet backend they control and receive a concise result summary. It is useful for pet, loot, empty-result, and backend-error response flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured backend URL can receive the API key, and HTTPS is not enforced by the skill.

Mitigation: Configure only a backend you control, use an HTTPS URL, and keep the API key narrowly scoped to the catch action.

Risk: Broad catch or fish phrasing may trigger an authenticated request unintentionally.

Mitigation: Review ambiguous catch or fish requests before running the skill and confirm when the user intent is unclear.

Risk: Production secrets could be placed in _meta.json.

Mitigation: Prefer environment variables for secrets and keep _meta.json empty or development-only before sharing or publishing the skill.

## Reference(s):

- [Catch Pet API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/aileaile/skills/claw-pet)

## Skill Output:

**Output Type(s):** [text, configuration guidance]

**Output Format:** [Plain text summaries and error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Formats pet, item, empty, and error responses without exposing secrets.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
