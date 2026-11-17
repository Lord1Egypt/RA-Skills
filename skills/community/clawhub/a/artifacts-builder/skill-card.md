## Description:

Artifacts Builder helps agents create multi-component Claude HTML artifacts with React 18, TypeScript, Tailwind CSS, shadcn/ui, and bundling tools for single-file sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javotillo](https://clawhub.ai/user/javotillo)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agents use this skill to scaffold richer Claude artifact projects, add modern frontend components, and bundle the finished React application into a self-contained HTML artifact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The initialization and bundling scripts install many npm dependencies and may install pnpm globally.

Mitigation: Run the skill only in an environment where package installation is acceptable, and review dependency changes before reusing the generated project.

Risk: The bundling script removes existing dist and bundle.html paths in the current project.

Mitigation: Run the bundling script from the intended project root and keep important non-build files out of dist and bundle.html.

Risk: The scripts generate and mutate local frontend project files.

Mitigation: Use a clean workspace or version control so generated configuration and source changes can be reviewed.

## Reference(s):

- [shadcn/ui components](https://ui.shadcn.com/docs/components)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with bash commands plus generated React project files and a bundled HTML artifact]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18 or newer; scripts may install npm packages, create or modify project configuration, remove prior dist and bundle.html build outputs, and produce bundle.html.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
