## Description:

Generates Chinese-language running training plans based on Jack Daniels-style pacing, VDOT concepts, workout types, periodization, and rest-day scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiminshuixing](https://clawhub.ai/user/yiminshuixing)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and runners use this skill to create personalized 5K, 10K, half-marathon, or marathon training plans from race goals, recent performance, experience level, rest days, and schedule constraints. The generated plan includes workout structure, paces, heart-rate ranges, and TXT/CSV exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may write age, race goals, schedule details, and training plans to fixed desktop filenames.

Mitigation: Review or change the output path before use on shared machines, and avoid overwriting existing running-plan files.

Risk: Generated training guidance may not match a runner's health status, injury history, or real-world conditions.

Mitigation: Treat plans as reference material, adjust based on physical condition, and seek qualified coaching or medical advice when needed.

## Reference(s):

- [Running training core knowledge](artifact/references/knowledge.md)
- [ClawHub skill page](https://clawhub.ai/yiminshuixing/skills/daniels-running-plan)

## Skill Output:

**Output Type(s):** [Text, CSV, Guidance]

**Output Format:** [Chinese-language training plan text and UTF-8 BOM CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default exports are /home/ai/桌面/running-plan.txt and /home/ai/桌面/running-plan.csv.]

## Skill Version(s):

1.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
