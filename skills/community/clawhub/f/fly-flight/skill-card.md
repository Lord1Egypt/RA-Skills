## Description:

Fly Flight queries China domestic flight and high-speed rail options from public web sources, routes requests by transport mode, and returns a shared response shape.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baizhexue](https://clawhub.ai/user/baizhexue)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to compare China domestic flight and high-speed rail options, including departure and arrival times, stations or airports, airlines or train details, and public reference fares.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The flight parser executes external flight-page data as local JavaScript.

Mitigation: Review before installing, run only in an isolated environment, and replace eval-based parsing before treating the skill as safe for normal agent use.

Risk: HTTPS protection is weakened for train queries.

Mitigation: Do not rely on train results over untrusted networks until TLS verification is fixed.

Risk: Optional HTTP mode can expose lookup behavior if bound beyond localhost.

Mitigation: Keep HTTP mode on localhost and avoid exposing it to remote networks.

## Reference(s):

- [Fly Flight on ClawHub](https://clawhub.ai/baizhexue/skills/fly-flight)
- [Provider Public Web Notes](references/provider-public-web.md)
- [Tongcheng Public Flight Pages](https://www.ly.com/flights/)
- [12306 Public Train Endpoints](https://kyfw.12306.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown summaries backed by JSON transport results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns flight or train options with mode-specific details; public fares are reference prices and may differ from checkout prices.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
