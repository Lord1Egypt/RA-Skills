## Description:

Agent Mbti helps agents run a Chinese-language MBTI-style self-assessment, compare it with a user's desired interaction style, and produce an alignment report with behavior recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[torchesfrms](https://clawhub.ai/user/torchesfrms)

### License/Terms of Use:


## Use Case:

External users and agent builders use this skill to characterize an agent's interaction style, collect a user's preferred style, and compare the two across MBTI-inspired dimensions. It is suited for informal behavior tuning discussions, not clinical personality assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat MBTI-style results as clinical or scientifically rigorous personality evaluation.

Mitigation: Present the report as an informal behavioral framing tool and avoid using it for psychological, employment, medical, or eligibility decisions.

Risk: Behavior or configuration recommendations may misalign the agent with task requirements, policy expectations, or user needs.

Mitigation: Review recommendations before applying them to an agent configuration and test any behavior changes in the intended workflow.

## Reference(s):

- [Agent MBTI scoring rules](references/scoring.md)
- [Agent MBTI 26-question free survey](references/survey-free.json)
- [User preference survey](references/user-survey-free.json)
- [Agent personality type reference](references/personality-types.md)
- [ClawHub skill page](https://clawhub.ai/torchesfrms/skills/agent-mbti)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown diagnostic report with MBTI type codes, dimension scores, match analysis, and recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language questionnaire workflow; the free tier uses 26 agent self-test questions and 4 user preference questions.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
