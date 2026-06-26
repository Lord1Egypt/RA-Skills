## Description: <br>
Remove AI-style code slop from a branch by reviewing diffs, deleting inconsistent defensive noise, and preserving behavior and local style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrennerSpear](https://clawhub.ai/user/BrennerSpear) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to review branch diffs for AI-generated cleanup issues such as inconsistent comments, unnecessary defensive checks, weak casts, debug leftovers, and style drift while preserving behavior and local conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup edits could unintentionally remove valid guards or change behavior. <br>
Mitigation: Review proposed diffs before committing and keep protections at trust boundaries such as user input, authentication, network, database, and file I/O. <br>
Risk: Source changes may introduce regressions even when the security verdict is clean. <br>
Mitigation: Run the normal project test, typecheck, and lint suite after applying edits. <br>


## Reference(s): <br>
- [Deslop Heuristics](references/slop-heuristics.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Code, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown summary with code diffs and shell command results when changes are made] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify source files in the working branch and should be followed by project checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
