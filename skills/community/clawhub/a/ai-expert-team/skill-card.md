## Description:

Use when a complex problem needs a structured expert team rather than a single general answer. Runs a Single-CEO Expert Council with a Nuwa-style decision lens, Agency-style specialist selection, NEXUS handoffs, evidence-backed expert reports, and a verification layer before final synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wei840222](https://clawhub.ai/user/wei840222)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product leads, and strategy teams use this skill to route complex architecture, product, risk, research, or planning questions through a small evidence-oriented expert council. It is intended for decisions that need scoped specialists, verification, clear assumptions, and a grounded final recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full task details may be stored in a predictable local temp directory.

Mitigation: Avoid secrets or sensitive business data unless the artifact directory is hardened, run IDs are validated, permissions are restricted, and cleanup is planned.

Risk: Optional source asset initialization can rely on current unpinned GitHub content.

Mitigation: Initialize external source assets only when needed and pin repositories to reviewed commits before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wei840222/skills/ai-expert-team)
- [README](README.md)
- [Skill definition](SKILL.md)
- [CEO Profiles](references/ceo-profiles.md)
- [Source Research Snapshot](references/source-research-snapshot.md)
- [Specialist Selection](references/specialist-selection.md)
- [Validation Case Library](references/validation-case-library.md)
- [Validation Cycle Closure](references/validation-cycle-closure.md)
- [Expert Handoff Template](templates/expert-handoff.md)
- [Final Synthesis Template](templates/final-synthesis.md)
- [Agency Agents source asset](https://github.com/msitarzewski/agency-agents.git)
- [Nuwa Skill source asset](https://github.com/alchaincyf/nuwa-skill.git)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports and structured filesystem artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write full run artifacts under /tmp/ai-expert-team/runs/<run_id>/ with PASS, FAIL, or PARTIAL verification verdicts.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata; source frontmatter says 0.1.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
