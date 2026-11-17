## Description:

Use when the user needs a China domestic rental-car reference price, especially for same-day or holiday travel where train-station or airport store choice matters and OneHai peak-period minimum-rental rules can be mistaken for zero inventory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tengjiaozhai](https://clawhub.ai/user/tengjiaozhai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to check China domestic self-drive rental-car reference prices from OneHai. It is especially useful when the pickup store should match a train-station or airport arrival scene and when holiday minimum-rental rules need to be separated from true zero-inventory results.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill automates a logged-in OneHai Chrome session.

Mitigation: Install and run it only when the user explicitly requests a China rental-price lookup and is comfortable with agent automation of that authenticated browser session.

Risk: Security evidence reports a confirmed JavaScript interpolation flaw that could run unintended page scripts.

Mitigation: Avoid untrusted city, store, or location text until the interpolation flaw is fixed, and review query arguments before execution.

Risk: Output may include a preview snippet from an authenticated booking page.

Mitigation: Review generated JSON before sharing it outside the session and avoid exposing account-specific or booking-page details that are not needed for the rental-price answer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tengjiaozhai/skills/china-rental-price)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reference prices, booking URLs, selected-store details, availability counts, vehicle samples, booking restrictions, and warnings; prices are captured at query time and are not guaranteed final checkout prices.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
