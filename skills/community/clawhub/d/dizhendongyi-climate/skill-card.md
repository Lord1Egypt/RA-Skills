## Description:

地动仪气候模型 Dizhenyi Climate Model helps agents run and explain local Python workflows for orbital-scale climate modeling, near-term RCP scenario exploration, East Asian monsoon analysis, paleoclimate comparison, and extreme-event indicator checks.

This skill is for research and development only.

## Publisher:

[zxfei420](https://clawhub.ai/user/zxfei420)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical reviewers use this skill to run a local climate-analysis toolkit and interpret outputs about orbital forcing, FEBE response, RCP scenarios, East Asian monsoon behavior, paleoclimate comparisons, and extreme-event indicators. Outputs should be treated as illustrative research calculations rather than authoritative climate forecasts, warnings, or policy guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate the reliability of climate forecasts and warning-style outputs.

Mitigation: Treat generated analyses as illustrative research calculations only; require independent domain review before using outputs for decisions, warnings, or policy guidance.

Risk: Some scripts write result JSON files to fixed paths under /tmp.

Mitigation: Run the skill as an unprivileged user in an isolated environment, avoid shared multi-user systems, and update scripts to use caller-controlled or unique output paths before broader deployment.

Risk: Dependency resolution may vary if numpy is installed without pinning.

Mitigation: Use a dedicated virtual environment and pin numpy to a reviewed version for reproducible execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zxfei420/skills/dizhendongyi-climate)
- [Publisher Profile](https://clawhub.ai/user/zxfei420)
- [Core Theory](references/core_theory.md)
- [Orbital Data](references/orbital_data.md)
- [Extreme Events](references/extreme_events.md)
- [Verification](references/verification.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and local script output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may guide agents to run Python scripts that print climate-analysis tables and write JSON result files.]

## Skill Version(s):

3.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
