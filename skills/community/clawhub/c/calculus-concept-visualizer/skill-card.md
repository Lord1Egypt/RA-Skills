## Description: <br>
Helps calculus learners and instructors explain limits, derivatives, integrals, and Taylor approximations with dynamic visualizations, misconception diagnosis, and short quizzes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daigxok](https://clawhub.ai/user/daigxok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners, instructors, and education developers use this skill to create calculus concept explanations, generate GeoGebra or Python visualizations, diagnose student misconceptions, and produce short assessment items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A plotting tool can run user-supplied math text as Python code on the local machine. <br>
Mitigation: Use the skill only in a restricted environment and avoid untrusted function strings until expression handling is replaced with a safe, allowlisted parser. <br>
Risk: Generated visualizations and student interaction data may be retained by auto-save or session modeling behavior. <br>
Mitigation: Check storage locations and deletion procedures before using the skill with real student data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daigxok/calculus-concept-visualizer) <br>
- [Publisher profile](https://clawhub.ai/user/daigxok) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Hermes agent configuration](artifact/hermes.config.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown explanations with GeoGebra configuration, Python visualization code, JSON-style diagnostic reports, and quiz content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local visualization files or base64 image data when plotting tools run.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
