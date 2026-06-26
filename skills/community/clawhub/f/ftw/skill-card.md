## Description: <br>
PIV workflow orchestrator - Plan, Implement, Validate loop for systematic multi-phase software development. Use when building features phase-by-phase with PRPs, automated validation loops, or multi-agent orchestration. Supports PRD creation, PRP generation, codebase analysis, and iterative execution with validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SmokeAlot420](https://clawhub.ai/user/SmokeAlot420) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use Piv to plan, implement, validate, debug, and commit multi-phase software changes with PRDs, PRPs, codebase analysis, and role-specific agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can actively modify repository files and create commits. <br>
Mitigation: Run it only in the intended project, keep a clean git state or backup first, and review file changes before accepting commits. <br>
Risk: Generated PRDs and PRPs may direct agents to run commands or implement changes that do not match user intent. <br>
Mitigation: Review generated PRDs and PRPs before execution, and approve shell commands and commits deliberately. <br>
Risk: External research or helper-agent output may introduce incorrect assumptions into implementation plans. <br>
Mitigation: Treat research and sub-agent summaries as claims to verify during validation, with the validator checking actual code and test results independently. <br>


## Reference(s): <br>
- [Piv ClawHub page](https://clawhub.ai/SmokeAlot420/ftw) <br>
- [Project homepage](https://github.com/SmokeAlot420/ftw) <br>
- [PIV discovery workflow](artifact/references/piv-discovery.md) <br>
- [PRD creation guide](artifact/references/create-prd.md) <br>
- [PRP generation guide](artifact/references/generate-prp.md) <br>
- [Codebase analysis guide](artifact/references/codebase-analysis.md) <br>
- [PIV executor role](artifact/references/piv-executor.md) <br>
- [PIV validator role](artifact/references/piv-validator.md) <br>
- [PIV debugger role](artifact/references/piv-debugger.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, generated PRD/PRP files, code edits, shell command results, workflow updates, and git commit messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify repository files, run validation commands, spawn role-specific helper agents, and create git commits when the workflow passes validation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
