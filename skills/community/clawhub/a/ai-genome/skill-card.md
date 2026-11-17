## Description:

Encode your agent's personality into a diploid genome with 27 cognitive primitives, compare against 216 AI agent personalities, simulate breeding, and explore genetic compatibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohmhm1](https://clawhub.ai/user/mohmhm1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to encode SOUL.md personality definitions into genome files, compare them with a community genome library, and generate phenotype or self-knowledge reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that the skill runs unqualified local Python scripts that are not included in the package.

Mitigation: Before use, verify that the installed package provides encoder.py, visualize.py, agent_report.py, and the genome library, and run the intended packaged files.

Risk: Encoding sends SOUL.md content to Claude as disclosed by the artifact and security guidance.

Mitigation: Review or redact SOUL.md content before encoding, and use the mock mode when external API processing is not acceptable.

Risk: The bundled HTML pages contact Google Fonts when opened.

Mitigation: Remove or self-host the fonts when external font requests are not acceptable for the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohmhm1/skills/ai-genome)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Encoding may call Claude; comparison, visualization, and breeding operations are described as local computation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
