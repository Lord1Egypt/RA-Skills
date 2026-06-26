## Description: <br>
AS Autoresearch Loop helps agents run measurable iterative improvement loops for reusable artifacts by defining a metric, testing changes, keeping improvements, and stopping on explicit criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[autosolutionsai-didac](https://clawhub.ai/user/autosolutionsai-didac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, prompt engineers, and operations teams use this skill to improve reusable skills, workflows, system prompts, business processes, and other measurable artifacts through controlled experiment loops. It is best suited when the user can define a stable artifact, metric, evaluation set, and budget before iteration begins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes conflicting active instructions, including historical or nested skill files that may encourage long-running file-changing loops. <br>
Mitigation: Review the installed artifact before use, quarantine historical skill drafts, and run only the intended current skill file. <br>
Risk: Iterative improvement loops can modify files beyond the user's intended scope if paths and boundaries are unclear. <br>
Mitigation: Use sandbox copies or isolated branches, confirm writable paths, and define fixed files before starting the loop. <br>
Risk: Unbounded iteration can consume excessive time, tokens, or cost. <br>
Mitigation: Set explicit maximum iterations, time, cost, and stopping criteria before execution. <br>
Risk: Running the loop against live workflows or production prompts can introduce regressions before review. <br>
Mitigation: Avoid live workflows and production prompts; evaluate candidates separately and require human approval before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/autosolutionsai-didac/as-autoresearch-loop) <br>
- [Karpathy autoresearch methodology](https://github.com/karpathy/autoresearch) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with checklists, tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose file edits, evaluation runs, results logging, and versioned artifact backups; users should set explicit limits before starting.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
