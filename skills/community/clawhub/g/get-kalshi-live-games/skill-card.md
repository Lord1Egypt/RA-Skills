## Description:

Fetch up to five currently live Kalshi sports markets with game names and their probabilities using the browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kanakamedalasumanth](https://clawhub.ai/user/kanakamedalasumanth)

### License/Terms of Use:


## Use Case:

Agents use this skill to open Kalshi in a browser, find live sports markets, and return a concise list of game names and probabilities. It is intended for users who need current market information without trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live market information may change quickly or be unavailable while the agent is browsing.

Mitigation: Treat returned probabilities as a point-in-time readout and verify important decisions directly in Kalshi.

Risk: The skill directs the agent to open Kalshi in a browser to read market information.

Mitigation: Install only if browser access to Kalshi is acceptable in the deployment environment.

## Reference(s):

- [Kalshi](https://kalshi.com)
- [ClawHub skill page](https://clawhub.ai/kanakamedalasumanth/skills/get-kalshi-live-games)
- [Publisher profile](https://clawhub.ai/user/kanakamedalasumanth)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise text or Markdown list containing game names and probabilities]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to five live games and does not instruct the agent to place trades or use credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
