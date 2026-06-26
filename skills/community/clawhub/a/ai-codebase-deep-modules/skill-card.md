## Description: <br>
Designs and refactors software codebases to be AI-friendly by aligning files to domain and feature boundaries, creating deep modules with small public interfaces, enforcing import boundaries, and tightening tests and feedback loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to map existing codebases into domain or feature modules, define stable public interfaces, plan incremental refactors, enforce import boundaries, and establish fast feedback checks for safer AI-assisted coding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to inspect and modify repository structure during refactoring. <br>
Mitigation: Use a branch and review proposed move plans, boundary rules, scaffolded files, and test changes before committing. <br>
Risk: Running local scripts from an untrusted repository can expose the agent to unsafe project behavior. <br>
Mitigation: Inspect local scripts before allowing the agent to execute them, and prefer the documented optional scaffolder only after review. <br>


## Reference(s): <br>
- [Architecture Plan Template](assets/architecture-plan-template.md) <br>
- [Boundary Enforcement Patterns](references/boundary-enforcement.md) <br>
- [Module Templates For Deep Modules](references/module-templates.md) <br>
- [Copy-Paste Prompts For Architecture Work](references/prompts.md) <br>
- [Testing And Feedback Guidance](references/testing-and-feedback.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown plans with tables, code snippets, shell commands, and optional scaffolded files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce refactor plans, interface specs, boundary rules, contract test skeletons, and optional TypeScript or Python module scaffolds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
