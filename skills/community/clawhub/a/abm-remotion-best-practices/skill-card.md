## Description: <br>
Helps users create videos programmatically with React and Remotion by covering project setup, composition structure, animation patterns, and rendering workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariokarras](https://clawhub.ai/user/mariokarras) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold or extend Remotion projects, build React-based video compositions, apply animation best practices, and generate preview and render commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lambda rendering guidance requires AWS credentials and can create cloud resources with associated costs. <br>
Mitigation: Use least-privilege or temporary/profile-based AWS authentication, review resources before creating them, and avoid storing secrets in committed files, logs, or shared shell history. <br>
Risk: Generated project changes and render commands may introduce incorrect video behavior if used without review. <br>
Mitigation: Review generated files and commands, preview the composition locally, and scan the project before deployment. <br>


## Reference(s): <br>
- [Remotion Animation Patterns](references/animations.md) <br>
- [Remotion Lambda Rendering](references/lambda.md) <br>
- [Remotion Rendering Reference](references/rendering.md) <br>
- [Remotion Project Setup](references/setup.md) <br>
- [Remotion Lambda documentation](https://www.remotion.dev/docs/lambda) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript/TSX snippets and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project files or file diffs, scene component code, composition registration, and exact preview/render commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
