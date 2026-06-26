## Description: <br>
Finds orphaned files, unused components, and dead code in projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scan front-end TypeScript and JavaScript projects for orphaned files, unused components, dead utility functions, and unregistered routes before cleanup or refactoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Heuristic dead-code findings may be false positives for dynamic imports, convention-based routes, feature flags, public assets, or test-only references. <br>
Mitigation: Review the report manually, prioritize high-confidence items, and run project builds and tests before removing files. <br>
Risk: An optional generated cleanup script can remove files when executed. <br>
Mitigation: Run cleanup on a branch, inspect every command in the script, and use git history to preserve rollback options. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangzhiming1999/find-orphans) <br>
- [Repository](https://github.com/wangzhiming1999/oliver-skill) <br>
- [Skill homepage](https://github.com/wangzhiming1999/oliver-skill/tree/main/skills/find-orphans) <br>
- [Support issues](https://github.com/wangzhiming1999/oliver-skill/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown report with optional bash cleanup script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Heuristic static analysis output that should be reviewed before any cleanup is applied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
