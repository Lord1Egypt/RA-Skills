## Description: <br>
Public ClawHub text release for a Windows companion skill that bridges local AI CLIs and controlled workspace file operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archibald80000-ai](https://clawhub.ai/user/archibald80000-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this documentation-first skill to understand how a separate Windows local companion can bridge installed Gemini, Codex, or Claude CLIs and guarded workspace file operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may expect this public package to execute providers or perform filesystem actions by itself. <br>
Mitigation: Treat the ClawHub release as documentation-only and deploy the separate local companion before relying on provider execution or workspace operations. <br>
Risk: Using the separate local companion may send prompts or file contents to locally configured AI provider accounts. <br>
Mitigation: Confirm which Gemini, Codex, or Claude accounts are installed and allowed for the workspace before sending prompts or file contents. <br>
Risk: Write-like filesystem actions in the separate local companion could affect unintended files if the workspace boundary is too broad. <br>
Mitigation: Choose a narrow workspace root and require explicit approval for mkdir, write, and append operations. <br>


## Reference(s): <br>
- [Approval Model Reference](references/auth-model.md) <br>
- [Filesystem Operations Reference](references/fs-operations.md) <br>
- [Provider Commands Reference](references/provider-commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown prose with reference notes and inline command names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [This public release is documentation-only; runtime behavior depends on a separate local companion package and locally installed provider CLIs.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
