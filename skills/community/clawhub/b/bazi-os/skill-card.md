## Description:

八字操作系统V2.0 guides an agent through BaZi chart analysis using nine-layer diagnostics, cross-school validation, classical-source attribution, and confidence labeling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhc2026](https://clawhub.ai/user/yhc2026)

### License/Terms of Use:

MIT

## Use Case:

External users invoke the skill to generate structured BaZi readings from birth date, time, location, and gender. The skill is intended for cultural or entertainment analysis and should not be used as a substitute for professional medical, financial, relationship, or life-planning advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects precise birth date, time, location, gender, and possibly a name, then may save reports under identifying filenames.

Mitigation: Use only with informed consent, avoid real names in saved reports, and keep the output directory private.

Risk: Generated readings may include health, financial, relationship, gendered, or life-planning claims that users could over-rely on.

Mitigation: Present outputs as cultural or entertainment content, include uncertainty, and require professional advice for consequential decisions.

Risk: The security evidence flags the release as suspicious because the guidance is under-bounded for sensitive personal topics.

Mitigation: Review generated reports before sharing, remove overconfident claims, and keep disclaimers visible in downstream public materials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yhc2026/skills/bazi-os)
- [BaZi-OS homepage](https://github.com/bazi-os/bazi-os)
- [Artifact README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Core reasoning framework](artifact/框架/顶级命理师思维框架.md)
- [Analysis template](artifact/框架/排盘分析模板.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report saved as a file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include confidence labels, classical-source references, BaZi chart details, and topic-specific analysis sections.]

## Skill Version(s):

2.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
