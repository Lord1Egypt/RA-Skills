## Description:

Designs and refactors software codebases to be AI-friendly by aligning filesystem structure with domain or feature boundaries, defining deep module interfaces, enforcing import boundaries, and tightening tests and feedback loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to plan incremental refactors that make existing repositories easier for agents and humans to navigate, change, and test. It is suited to repositories with unclear feature boundaries, cross-domain coupling, weak public interfaces, or slow feedback loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional scaffolding script can write files outside the intended repository or generate unsafe source when supplied untrusted module names or paths.

Mitigation: Use the skill primarily as a planning aid; if running the script, pass simple lowercase kebab-case module names, keep paths repository-relative, and review generated files before running tests or builds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tristanmanchester/skills/ai-codebase-deep-modules)
- [Module templates for deep modules](references/module-templates.md)
- [Boundary enforcement patterns](references/boundary-enforcement.md)
- [Testing and feedback loops for greybox modules](references/testing-and-feedback.md)
- [Copy-paste prompts for architecture work](references/prompts.md)
- [AI-Friendly Refactor Plan template](assets/architecture-plan-template.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown plans with tables, code snippets, shell commands, and optional generated scaffold files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include incremental refactor plans, module maps, interface specifications, boundary rules, contract test skeletons, and optional TypeScript or Python scaffold files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
