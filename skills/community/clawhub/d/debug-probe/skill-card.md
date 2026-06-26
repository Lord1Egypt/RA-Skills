## Description: <br>
Debug Probe guides agents through hypothesis-driven runtime debugging with precise instrumentation, reproduction, root-cause convergence, fixes, and cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zelixag](https://clawhub.ai/user/zelixag) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when static code reading is insufficient to debug bugs, crashes, or unexpected behavior. It guides an agent through hypothesis generation, targeted instrumentation, reproduction, log review, root-cause fixes, verification, and cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Temporary diagnostic logging and dump hooks may expose secrets, personal data, or sensitive runtime state if used carelessly. <br>
Mitigation: Require explicit approval before instrumentation, log only minimal non-sensitive key=value pairs, and sanitize exported logs before sharing. <br>
Risk: Temporary instrumentation may be left in the codebase after debugging. <br>
Mitigation: Mark diagnostic code with DIAG cleanup comments, remove diagnostic imports and buffers after verification, and confirm the build passes with only the fix remaining. <br>
Risk: Diagnostic code may affect application behavior or be deployed beyond the intended debugging session. <br>
Mitigation: Use project-level installation on a clean branch, keep instrumentation narrow, and review changes before deployment. <br>


## Reference(s): <br>
- [Debug Probe README](README.md) <br>
- [Diagnostic Buffer Templates](TEMPLATES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown with diagnostic code snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include temporary diagnostic instrumentation that must be removed after verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
