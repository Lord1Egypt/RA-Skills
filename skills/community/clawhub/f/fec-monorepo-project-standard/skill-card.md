## Description: <br>
Use when creating, reviewing, or restructuring frontend monorepos with pnpm workspace, Turborepo, Nx, multi-package dependency boundaries, task orchestration, package naming, or package publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to standardize frontend monorepo structure, dependency boundaries, task orchestration, caching, CI validation, and package publishing practices for pnpm workspace, Turborepo, and Nx repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated monorepo guidance could introduce package boundary, dependency, or publishing changes that do not match the repository's policy. <br>
Mitigation: Review proposed changes against the existing dependency graph, package exports, peer dependencies, and release policy before applying them. <br>
Risk: Cache or CI recommendations could expose sensitive artifacts or allow affected-only checks to miss release issues. <br>
Mitigation: Keep secrets out of cache keys and artifacts, separate trusted CI from local cache behavior, and retain full validation on main or release branches. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bovinphang/fec-monorepo-project-standard) <br>
- [Frontend Craft Repository](https://github.com/bovinphang/frontend-craft) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, code, shell commands] <br>
**Output Format:** [Markdown with inline code and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for repository layout, workspace dependencies, task orchestration, CI validation, and publishing checks.] <br>

## Skill Version(s): <br>
2.4.0 (source: evidence release metadata, artifact metadata.json, artifact package.json, and artifact README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
