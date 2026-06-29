## Description: <br>
Gaokao Admissions helps users estimate provincial rank from score and subject choices, then generate reach, match, and safety university recommendations, major guidance, and a four-year college plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dengjiangit](https://clawhub.ai/user/dengjiangit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External students and families use this skill to support Chinese Gaokao admissions planning by combining province, score, subject choices, family context, rank estimation, university matching, and major selection guidance. The recommendations are advisory and should be checked against official provincial examination authority data before final decisions. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Admissions recommendations can be incorrect or outdated when live sources fail, source data changes, or rank estimates are used. <br>
Mitigation: Treat outputs as advisory and verify final school, major, score line, and rank data against official provincial examination authority sources. <br>
Risk: Live data lookup may send admissions-related queries to external education or search sites. <br>
Mitigation: Use live lookup only when acceptable for the user's privacy context, or rely on local reference files when sensitive details should not be sent externally. <br>
Risk: External education sites may rate-limit, block, or return incomplete data. <br>
Mitigation: Disclose when recommendations use fallback or estimated data, and prefer official provincial examination authority sources for final validation. <br>


## Reference(s): <br>
- [Gaokao Admissions ClawHub page](https://clawhub.ai/dengjiangit/skills/gaokao-admissions) <br>
- [31 Province Gaokao Mode Reference](references/provinces.md) <br>
- [University Classification and Discipline Evaluation](references/universities.md) <br>
- [Reach-Match-Safety Scoring Algorithm](references/scoring-model.md) <br>
- [Major Outlook and Employment Analysis](references/career-outlook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown admissions analysis with optional inline shell commands for data lookup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include estimated rank, reach-match-safety recommendation groups, major recommendations, rationale, and data caveats.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
