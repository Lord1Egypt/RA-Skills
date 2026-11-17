## Description:

Build ORBCAFE advanced analytics and voice navigation with CPivotTable/usePivotTable and CAINavProvider/useVoiceInput using official examples patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenruiyang](https://clawhub.ai/user/shenruiyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to implement ORBCAFE pivot analytics and voice navigation workflows with controlled state, persistence, chart controls, ASR wiring, and troubleshooting steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose npm dependency installation for ORBCAFE UI and related frontend packages.

Mitigation: Use an existing lockfile or pin versions, and review dependency changes before applying them.

Risk: Voice navigation examples require ASR endpoint and authentication wiring.

Mitigation: Load ASR URLs and credentials from application configuration, and review generated wiring before deployment.

Risk: Pivot presets can represent personal preferences or business assets.

Mitigation: Scope local persistence to the intended user, and use server-side persistence for shared business data.

## Reference(s):

- [Domain Patterns](references/domain-patterns.md)
- [Pivot + AINav Guardrails](references/guardrails.md)
- [Pivot + AINav Recipes](references/recipes.md)
- [ClawHub Skill Page](https://clawhub.ai/shenruiyang/skills/auto-pivot-table)
- [ClawHub Publisher Profile](https://clawhub.ai/user/shenruiyang)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript/TSX examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes implementation skeletons, operational notes, verification steps, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
