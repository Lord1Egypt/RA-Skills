## Description: <br>
Find and report dead code in JavaScript/TypeScript projects, including unused exports, unreferenced files, unused dependencies, and dead functions or variables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scan JS/TS codebases for likely unused exports, unreferenced source files, and unused npm dependencies before manual cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dead-code findings may be false positives for dynamic imports, reflection, external library APIs, entry points, CSS imports, or partially supported export patterns. <br>
Mitigation: Review each finding against dynamic imports, configured entry points, public APIs, and tests before removing code or dependencies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/dead-code-finder) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; scanner output is plain text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports candidate findings only; users should verify findings before deleting code.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
