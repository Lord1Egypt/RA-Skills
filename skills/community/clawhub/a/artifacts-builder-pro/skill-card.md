## Description:

Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui).

This skill is ready for commercial/non-commercial use.

## Publisher:

[hsuyungfeng](https://clawhub.ai/user/hsuyungfeng)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to scaffold React, TypeScript, Tailwind CSS, and shadcn/ui projects for complex Claude HTML artifacts, then bundle the result into a single shareable HTML file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts install packages from the npm ecosystem, may install pnpm globally, and modify files in the active project directory.

Mitigation: Run the skill only in a disposable or intended project directory, review scripts before execution, and avoid shells with unrelated secrets or production credentials.

Risk: Bundling removes existing dist and bundle.html outputs in the project directory.

Mitigation: Run bundling from the intended artifact project root and preserve any needed prior build outputs before execution.

## Reference(s):

- [shadcn/ui Components](https://ui.shadcn.com/docs/components)
- [Artifacts Builder Pro on ClawHub](https://clawhub.ai/hsuyungfeng/skills/artifacts-builder-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce a scaffolded frontend project and a bundled single-file HTML artifact when the scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
