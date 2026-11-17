## Description:

YunShi is an offline fortune-telling skill that generates daily lucky directions, colors, numbers, items, do's and don'ts, single-topic fortune readings, and next-day push-ready forecasts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elilin97](https://clawhub.ai/user/elilin97)

### License/Terms of Use:


## Use Case:

External users use YunShi to generate Chinese-language folk fortune readings from birthdays, dates, or pasted Zi Wei Dou Shu chart text. It supports repeat-use chart profiles and scheduled next-day forecast text when host automation is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private birth-chart details may be persisted in user_chart_profile.json for reuse.

Mitigation: Use the skill only in a private workspace, avoid saving raw chart text unless reuse is intended, and remove user_chart_profile.json when persistence is no longer wanted.

Risk: Scheduled forecasts may be sent repeatedly through messaging channels.

Mitigation: Confirm the delivery channel and recipient before enabling schedules, and disable host schedules when recurring pushes should stop.

Risk: Fortune readings may be mistaken for factual guidance in medical, legal, financial, or other high-stakes decisions.

Mitigation: Keep the entertainment and folk-culture disclaimer in user-facing output and advise users to rely on real-world judgment and qualified professionals for high-stakes decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/elilin97/skills/fortune-oracle)
- [ClawHub Skills Homepage](https://clawhub.ai/skills)
- [README](artifact/README.md)
- [Fortune Rules](artifact/fortune_rules.md)
- [User Chart Profile Template](artifact/user_chart_profile.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Chinese Markdown-like plain text with optional JSON profile data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local deterministic rules, may persist user_chart_profile.json when workspace write access is available, and can produce push-ready message text for host delivery tools.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
