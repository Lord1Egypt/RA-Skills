## Description: <br>
Flow Hugo Publisher manages Hugo publishing workflows by checking Hugo and Git setup, managing workspaces, initializing Git repositories, previewing sites, committing changes, and deploying to GitHub Pages with GitHub Actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZampoRen](https://clawhub.ai/user/ZampoRen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content maintainers use this skill to initialize or manage Hugo workspaces, preview site changes, commit updates, and publish to GitHub Pages while preserving per-workspace state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change and publish a Hugo repository as part of its stated purpose. <br>
Mitigation: Before approving publish steps, verify the workspace, Git remote, branch, staged files, generated workflow, and deployment target. <br>
Risk: Saved workspace and deployment history may be reused across later runs. <br>
Mitigation: Review, edit, or remove ~/.openclaw/state/hugo-publisher-state.json if prior workspace state should not be reused. <br>
Risk: Custom Hugo theme repositories and generated GitHub Actions workflows affect the site build and published output. <br>
Mitigation: Review any custom theme repository and generated .github/workflows/hugo-pages.yml before committing or pushing changes. <br>


## Reference(s): <br>
- [Workflow and Command Templates](references/workflow.md) <br>
- [State File Schema](references/state-schema.md) <br>
- [Human Intervention Points](references/interaction-points.md) <br>
- [Validation and Recovery Checklist](references/validation-checklist.md) <br>
- [Hugo Template Catalog](references/template-catalog.md) <br>
- [GitHub Actions Deployment Guide](references/github-actions.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ZampoRen/flow-hugo-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, GitHub Actions YAML, and JSON state guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Hugo project files, Git state, GitHub Actions workflow files, deployment guide Markdown, and local state JSON when the user approves those steps.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
