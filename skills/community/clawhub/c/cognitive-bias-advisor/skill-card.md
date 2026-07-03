## Description: <br>
Cognitive Bias Advisor is a Chinese-language coaching skill that routes decision-making, learning, action, communication, influence, and management questions into cognitive-bias diagnostics and practical strategy outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jacksu](https://clawhub.ai/user/jacksu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and employees can use this skill to examine choices, learning blocks, procrastination, communication, persuasion, and team-management situations through cognitive-bias prompts. The skill helps surface bias signals and returns structured, actionable strategy guidance without making the final decision for the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases may activate the skill during ordinary decision, communication, or management conversations. <br>
Mitigation: Confirm the user's intended domain before starting the diagnostic flow and allow the user to decline or switch domains. <br>
Risk: Persuasion and influence templates could be used to pressure, mislead, or manipulate people. <br>
Mitigation: Use the templates only in transparent, non-coercive situations and preserve the skill's stated principles of no harm, transparency, and reciprocal self-checking. <br>
Risk: Users may disclose sensitive personal, workplace, financial, or health details while seeking advice. <br>
Mitigation: Ask for only the minimum context needed and avoid collecting unnecessary sensitive details. <br>
Risk: Bias diagnoses and strategy outputs may be mistaken for professional advice or a final decision. <br>
Mitigation: Frame outputs as advisory prompts for user reflection and avoid deciding on the user's behalf. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jacksu/skills/cognitive-bias-advisor) <br>
- [README](artifact/README.md) <br>
- [Skill workflow](artifact/SKILL.md) <br>
- [Decision domain workflow](artifact/references/domain-decision.md) <br>
- [Learning domain workflow](artifact/references/domain-learning.md) <br>
- [Action domain workflow](artifact/references/domain-action.md) <br>
- [Communication domain workflow](artifact/references/domain-communication.md) <br>
- [Influence domain workflow](artifact/references/domain-influence.md) <br>
- [Management domain workflow](artifact/references/domain-management.md) <br>
- [Doubt-avoidance tendency reference](artifact/references/bias-doubt-avoidance.md) <br>
- [Inconsistency-avoidance tendency reference](artifact/references/bias-inconsistency-avoidance.md) <br>
- [Liking/loving tendency reference](artifact/references/bias-liking-tendency.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown coaching responses with structured question cards, diagnostic summaries, and strategy recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language outputs; may use interactive selection cards where supported.] <br>

## Skill Version(s): <br>
2.5.2 (source: ClawHub release metadata; artifact frontmatter reports 2.8.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
