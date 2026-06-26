## Description: <br>
Safely write or update large files over 5000 bytes by reading the current state, editing incrementally, verifying after each step, and using backups for recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YKaiXu](https://clawhub.ai/user/YKaiXu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill to plan safer file writes and updates for large files, especially when avoiding truncation through incremental edits, verification, and backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: File mutation guidance could lead to unintended overwrites, corruption, or truncation if used in the wrong workspace or without reviewing changes. <br>
Mitigation: Use the skill only where file modification is allowed, keep version-control or backup practices in place, and verify file contents after each incremental edit. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides step-by-step writing strategies, verification checks, fallback approaches, and error recovery guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
