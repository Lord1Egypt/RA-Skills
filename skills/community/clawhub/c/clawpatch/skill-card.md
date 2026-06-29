## Description: <br>
Clawpatch guides an agent through using the Clawpatch CLI to review repositories, read findings, choose fix workflows, and avoid unsafe review or fix patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmchow](https://clawhub.ai/user/tmchow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill when Clawpatch is explicitly requested for repository review, triage, per-finding fixes, or PR handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to run terminal commands and create local .clawpatch review state in a repository. <br>
Mitigation: Use it only in repositories where Clawpatch review state and terminal execution are expected, and review generated state before continuing. <br>
Risk: Provider CLIs or optional API credentials may be needed for review and fix workflows. <br>
Mitigation: Configure credentials outside the skill, avoid interactive login delegation, and limit credential exposure to the intended provider. <br>
Risk: User-directed fixes or PR creation can change code or propose changes based on false-positive findings. <br>
Mitigation: Review findings before allowing fixes, confirm each finding is real, and keep changes within the minimum fix scope. <br>
Risk: Parallel fixing with shared Clawpatch state can create conflicting or misplaced patches. <br>
Mitigation: Use separate worktrees for parallel scanner-only fixes and reserve Clawpatch's own fix loop for sequential workflows. <br>


## Reference(s): <br>
- [Clawpatch Skill Page](https://clawhub.ai/tmchow/clawpatch) <br>
- [tmchow Publisher Profile](https://clawhub.ai/user/tmchow) <br>
- [Clawpatch Homepage](https://clawpatch.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires terminal access and may rely on a configured provider CLI.] <br>

## Skill Version(s): <br>
0.1.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
