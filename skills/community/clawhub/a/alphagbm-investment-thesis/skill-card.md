## Description:

Records the buy thesis for each stock position and tracks structured sell conditions so an agent can review active, triggered, or closed investment theses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create, update, list, and review AlphaGBM investment theses tied to company profiles, including buy reasons and sell triggers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deleting a thesis by numeric ID may permanently remove investment research records.

Mitigation: Confirm the target thesis ID and user intent before delete operations; list or retrieve the thesis first and warn that recovery may not be available.

Risk: The AlphaGBM API key grants access to thesis records.

Mitigation: Use only an API key intended for this skill, avoid exposing thesis content unnecessarily, and keep the credential out of user-visible output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clementgu/skills/alphagbm-investment-thesis)
- [AlphaGBM](https://alphagbm.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration guidance]

**Output Format:** [Markdown summaries with JSON-shaped API request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ALPHAGBM_API_KEY and an existing company profile for thesis creation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
