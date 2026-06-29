## Description: <br>
Gaokao 360To3 guides Gaokao candidates and families through structured questions about family context, academic level, interests, and risk preference to recommend three suitable career and major directions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zify9000](https://clawhub.ai/user/zify9000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External students and families use this skill after Gaokao scores are available, or during high-school planning, to structure application choices and compare career and major directions. The skill asks one question per round, then combines family resources, student traits, score tier, and risk preference into three recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for personal and family context, including income, location, family work background, academic level, and career preferences. <br>
Mitigation: Share only information needed for planning and avoid unnecessary sensitive details in transcripts or downstream records. <br>
Risk: School, salary, employment, and industry claims may be inaccurate or stale if the referenced data files are missing or outdated. <br>
Mitigation: Verify school, salary, and employment claims independently before making application decisions. <br>
Risk: The artifact references `references/industries.md`, `references/majors.md`, `references/employment.md`, and `references/framework.md`, but those files are not included in this package. <br>
Mitigation: Treat recommendations as lower-confidence until the referenced data files are supplied and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zify9000/skills/gaokao-360to3) <br>
- [Server-resolved source repository](https://github.com/zify9000/gaokao-360To3) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Analysis] <br>
**Output Format:** [Conversational Markdown text with structured recommendation sections and risk notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final guidance normally contains three career and major directions after collecting sufficient user context.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
