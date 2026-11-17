## Description:

Daily Brief retrieves weather and Baidu hot-search headlines for a requested city and prints a terminal daily briefing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[piaomiao123](https://clawhub.ai/user/piaomiao123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to obtain a quick command-line daily brief with current weather and trending news for a city, without configuring API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts external weather and news providers, which may reveal city or usage context.

Mitigation: Avoid sensitive location details as city arguments and document the external providers before deployment.

Risk: Remote weather and news text is rendered in the terminal.

Mitigation: Review output before reusing it and prefer inert printf-style rendering in a future version.

Risk: The weather request should use explicit HTTPS for managed or sensitive environments.

Mitigation: Update provider calls to use explicit HTTPS before deployment where transport guarantees are required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/piaomiao123/skills/daily-brief)
- [wttr.in Weather Service](https://wttr.in)
- [Baidu Realtime Hot Search API](https://top.baidu.com/api/board?platform=wise&tab=realtime)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration guidance]

**Output Format:** [Plain terminal text with ANSI color sequences]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and network access to wttr.in and Baidu; no API keys are required.]

## Skill Version(s):

0.1.1 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
