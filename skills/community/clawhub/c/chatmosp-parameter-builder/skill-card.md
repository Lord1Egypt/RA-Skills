## Description:

Chatmosp Parameter Builder helps ChatMOSP agents build, complete, validate, and confirm parameter sets for MSR and KMC workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanyangye](https://clawhub.ai/user/sanyangye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and computational chemistry users use this skill to assemble and review ChatMOSP parameters before MSR or KMC calculations. It supports database-backed completion, gas entropy calculation, interaction-parameter conversion, missing-parameter handling, and a required confirmation step before downstream calculation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bilingual routing labels may cause wrong-language handling.

Mitigation: Match the response language to the latest user message and prefer the ClawHub companion skills named by the release evidence.

Risk: Defaulted or converted scientific parameters may be inaccurate for the target system.

Mitigation: Require the user to review and confirm the displayed parameter set, and ask them to verify literature-derived interaction formats before calculation.

Risk: Missing ChatMOSP companion skills can block parameter lookup or downstream calculation.

Mitigation: Install the companion ChatMOSP skills from ClawHub before using fallback sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sanyangye/skills/chatmosp-parameter-builder)
- [Publisher profile](https://clawhub.ai/user/sanyangye)
- [English skill definition](artifact/SKILL.md)
- [Chinese skill definition](artifact/SKILL_cn.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with parameter templates and JSON configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before downstream MSR or KMC calculations; keeps MSR and KMC parameter sets separate.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
