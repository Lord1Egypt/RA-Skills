## Description: <br>
This skill helps an agent collect public international, economic, and technology news, filter items with keyword rules, and produce a daily Markdown news brief for personal use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to have an agent gather public news links, apply lightweight keyword filtering, and generate a consistent daily Markdown brief. It is intended for personal news review, industry tracking, and content research workflows rather than deterministic or high-stakes decision-making. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may make outbound requests to public news websites. <br>
Mitigation: Review the source list and adapt or restrict it before use in environments with network policy constraints. <br>
Risk: The skill may install Python packages and write generated brief or cache files in the working directory. <br>
Mitigation: Run it in an appropriate workspace, review package installation commands, and keep output and cache paths under user-controlled directories. <br>
Risk: Generated briefs may be incomplete or misleading because source sites can change and free-version filtering is keyword based. <br>
Mitigation: Review generated news summaries before publishing, sharing, or relying on them for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/daily-news-brief-tool-free) <br>
- [Detailed reference examples](references/detail.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown briefs with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install Python packages and write generated brief or cache files in the working directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
