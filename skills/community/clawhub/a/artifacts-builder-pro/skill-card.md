## Description: <br>
Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hsuyungfeng](https://clawhub.ai/user/hsuyungfeng) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agents use this skill to scaffold React, TypeScript, Tailwind CSS, and shadcn/ui artifact projects, then bundle them into single-file HTML artifacts for Claude conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup and bundling scripts install npm and pnpm dependencies in the local environment. <br>
Mitigation: Run the scripts in an intended project directory or disposable workspace and review dependency changes before reuse. <br>
Risk: The initialization script expects and extracts a shadcn-components.tar.gz archive. <br>
Mitigation: Verify the archive source and contents before extraction. <br>
Risk: The bundling script removes existing dist and bundle.html outputs in the project root. <br>
Mitigation: Back up or move existing build outputs before running the bundling script. <br>


## Reference(s): <br>
- [shadcn/ui components](https://ui.shadcn.com/docs/components) <br>
- [Artifacts Builder Pro on ClawHub](https://clawhub.ai/hsuyungfeng/artifacts-builder-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a React project scaffold and a self-contained bundle.html artifact when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
