## Description: <br>
Bazi Full Fortune Telling generates Chinese astrology charting outputs and guided fortune-telling reports across family, health, career, wealth, relationships, education, and inner life. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laurc2004](https://clawhub.ai/user/laurc2004) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to calculate Bazi charts from solar or lunar birth data, query Chinese calendar details, reverse-search dates from four pillars, and draft calibrated Chinese astrology readings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask for private birth, family, health, relationship, and financial context during calibration. <br>
Mitigation: Share only the minimum information needed, skip calibration questions when preferred, and keep sensitive answers high level. <br>
Risk: Fortune-telling reports can be speculative or misleading if treated as factual advice for major life decisions. <br>
Mitigation: Treat outputs as cultural or entertainment guidance and do not rely on them as medical, legal, financial, or safety advice. <br>
Risk: The workflow may save a generated report as a text file. <br>
Mitigation: Ask the agent to show the report inline or confirm the exact save path before writing files. <br>


## Reference(s): <br>
- [Bazi Fundamentals](references/bazi-fundamentals.md) <br>
- [Analysis Guide](references/analysis-guide.md) <br>
- [Family Patterns](references/family-patterns.md) <br>
- [Pitfalls](references/pitfalls.md) <br>
- [Development Operations](references/dev-ops.md) <br>
- [cantian-tymext package](https://www.npmjs.com/package/cantian-tymext) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional plain text report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI scripts print chart, calendar, and reverse-search results to stdout; the agent workflow may draft a full reading and optionally save it as a .txt report.] <br>

## Skill Version(s): <br>
1.1.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
