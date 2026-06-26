## Description: <br>
YunShi provides local, offline Chinese-language fortune readings with lucky directions, colors, numbers, items, daily do's and don'ts, focused fortune queries, and optional next-day scheduled delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elilin97](https://clawhub.ai/user/elilin97) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to generate culturally framed, entertainment-oriented Chinese daily fortune readings from a birthday, date, or pasted Zi Wei chart. It can also create and reuse a local chart profile and produce scheduled next-day fortune text when the host supports delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create and reuse a local user_chart_profile.json containing birth or chart details. <br>
Mitigation: Install only when local profile retention is acceptable, and review or delete the saved profile when it is no longer needed. <br>
Risk: Scheduled fortune pushes could expose personal readings if delivered to shared or unintended channels. <br>
Mitigation: Enable scheduled pushes only for private channels controlled by the user and verify the delivery target before use. <br>
Risk: Fortune outputs could be mistaken for decision-grade medical, legal, or financial advice. <br>
Mitigation: Keep outputs framed as entertainment and folk-culture reference, and use rational caution for high-stakes decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/elilin97/fortune-oracle) <br>
- [ClawHub Skills Directory](https://clawhub.ai/skills) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [fortune_rules.md](artifact/fortune_rules.md) <br>
- [user_chart_profile.md](artifact/user_chart_profile.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Chinese Markdown-style fortune text with fixed sections and optional local JSON profile data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are entertainment and folk-culture references; scheduled delivery may compress long detail sections to fit channel limits.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
