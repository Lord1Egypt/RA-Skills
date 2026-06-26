## Description: <br>
Guides OpenClaw users through a Day 7 graduation retrospective by comparing journey progress, identifying an agent archetype, celebrating achievements, and planning next steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[calvinxhk](https://clawhub.ai/user/calvinxhk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw learners and agent users use this skill at the end of a 7-day learning journey to generate a personalized graduation report, 4C growth analysis, archetype assessment, and 7/30/90-day growth roadmap. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may review broad OpenClaw memory, session history, configuration history, workspace metadata, and skill usage to create a profile-like graduation report. <br>
Mitigation: Run it only after an explicit Day 7 request, review the data sources before analysis, and avoid saving reports, sharing journey data, or enabling follow-ups unless the user intentionally opts in. <br>
Risk: Personalized roadmap and archetype conclusions can be misleading if based on incomplete or unverified journey data. <br>
Mitigation: Ask the user to confirm the baseline, current state, and data sources before presenting conclusions as final. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/calvinxhk/botlearn-graduate) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Domain knowledge](artifact/knowledge/Domain.md) <br>
- [Graduation strategy](artifact/strategies/Main.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown graduation report with tables, scores, archetype summary, recommendations, and roadmap sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses available Day 1 and Day 7 journey evidence to produce a personalized progress report; no external post-processing is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata, SKILL.md frontmatter, strategies/Main.md, and test files; manifest.json and package.json list 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
