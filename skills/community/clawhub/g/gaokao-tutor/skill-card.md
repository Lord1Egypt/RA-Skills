## Description:

High school exam (Gaokao) AI tutor for Chinese students that supports all major subjects, Socratic problem solving, knowledge lookup, practice generation, mistake tracking, essay scoring, study planning, and college major recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangwei-frank](https://clawhub.ai/user/fangwei-frank)

### License/Terms of Use:

MIT-0

## Use Case:

External Chinese high-school students and tutoring agents use this skill for Gaokao exam preparation, including guided problem solving, subject review, practice generation, essay feedback, study planning, mistake review, and college admissions reference.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill stores student profile and mistake data across sessions.

Mitigation: Tell users where local memory is stored, what student data is retained, and how to delete it before use.

Risk: The emotional-support guidance is inadequate for explicit self-harm or suicide language.

Mitigation: Update the emotional-support flow so self-harm language triggers immediate crisis-oriented guidance to contact local emergency services or a trusted adult.

Risk: Admissions and score guidance relies on static reference data and can become outdated.

Mitigation: Present admissions output as reference-only and instruct users to verify current requirements with the relevant provincial admissions authority and official university sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fangwei-frank/skills/gaokao-tutor)
- [Province policy reference](references/province-policy.md)
- [Solving guide](references/solving-guide.md)
- [Subject knowledge tree](references/subject-knowledge-tree.md)
- [Question generator](references/question-generator.md)
- [Mistakes guide](references/mistakes-guide.md)
- [Essay rubric](references/essay-rubric.md)
- [Study plan template](references/study-plan-template.md)
- [College guide](references/college-guide.md)
- [Emotional support guide](references/emotional-support.md)
- [Province score data](data/province_scores.json)
- [University score data](data/university_scores.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown tutoring responses with optional JSON from helper scripts and local memory files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update local student profile and mistake data in the OpenClaw workspace memory.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
