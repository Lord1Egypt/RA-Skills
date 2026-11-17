## Description:

父母的功课 provides Chinese-language parenting psychology dialogue support for structured conversations, emotion recognition, scenario matching, and safety checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yun520-1](https://clawhub.ai/user/yun520-1)

### License/Terms of Use:

MIT-0

## Use Case:

External parents, caregivers, and support-seeking users can use this skill to frame parent-child conflicts, recognize emotional and crisis signals, and draft compassionate next-step guidance. It is educational support and should not be treated as professional mental-health care or emergency response.

### Deployment Geography for Use:

Global, with China-oriented language and crisis-resource examples.

## Known Risks and Mitigations:

Risk: Optional scripts can persist sensitive family or emotional-health data in local storage.

Mitigation: Keep file persistence disabled unless the saved data and storage paths have been reviewed, and avoid entering unnecessary personal or crisis details.

Risk: Release or maintenance flags can commit, push, or publish local files.

Mitigation: Do not enable ALLOW_AUTO_PUSH or ALLOW_AUTO_PUBLISH unless the working tree, destination, and published content have been explicitly reviewed.

Risk: Crisis, self-harm, abuse, or mental-health guidance could be mistaken for professional care.

Mitigation: Use the skill only for educational support and route urgent or high-risk situations to emergency services, crisis hotlines, child-protection resources, or qualified professionals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yun520-1/skills/fu-mu-gong-ke-v2)
- [README](artifact/skills/fu-mu-gong-ke/README.md)
- [Skill definition](artifact/skills/fu-mu-gong-ke/SKILL.md)
- [Decision flow](artifact/skills/fu-mu-gong-ke/DECISION-FLOW.md)
- [Crisis intervention](artifact/skills/fu-mu-gong-ke/theory/crisis-intervention.md)
- [Positive parenting tools](artifact/skills/fu-mu-gong-ke/references/positive-parenting-tools.md)
- [Academic support](artifact/skills/fu-mu-gong-ke/references/academic-support.md)
- [Runnable tools](artifact/skills/fu-mu-gong-ke/tools/runnable-tools.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown text with optional Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primarily Chinese-language dialogue support; optional local scripts may produce assessments, plans, reflections, timers, or scenario-practice output.]

## Skill Version(s):

2.3.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
