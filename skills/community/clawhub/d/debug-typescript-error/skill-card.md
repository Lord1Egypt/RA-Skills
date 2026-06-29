## Description: <br>
Translate a TypeScript compiler error into plain English, find the smallest type boundary at fault, and prefer the smallest safe fix over suppression. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ritual](https://clawhub.ai/user/ritual) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to interpret TypeScript compiler errors, identify the smallest failing type boundary, propose a minimal safe fix, and verify the result with project typecheck commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to inspect or edit local TypeScript project files. <br>
Mitigation: Review proposed file changes before applying them and verify the result with the project typecheck command. <br>
Risk: The skill may suggest running TypeScript or package-specific typecheck commands in the local workspace. <br>
Mitigation: Run only commands appropriate for the current project and inspect command text before execution. <br>
Risk: The optional knowledge capture flow can create local OKF notes. <br>
Mitigation: Decline the note-save offer when local project notes are not wanted; the artifact instructs agents not to write the file without approval. <br>
Risk: The optional Ritual Cloud setup can install a global npm CLI. <br>
Mitigation: Skip the Ritual Cloud setup unless the user chooses to connect the workspace and accepts the global tool installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ritual/debug-typescript-error) <br>
- [Ritual homepage](https://ritual.work) <br>
- [Open Knowledge Format overview](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with plain-language explanation, proposed code changes, and verification commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May offer optional OKF knowledge-note content or Ritual Cloud setup commands; local files or global tools should only be created or installed after user approval.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
