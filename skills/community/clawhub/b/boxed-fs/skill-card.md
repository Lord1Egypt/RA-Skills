## Description: <br>
WebAssembly sandboxed file system operations for secure file read/write within explicitly declared directories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guyoung](https://clawhub.ai/user/guyoung) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to read, write, append, copy, remove, create, and list files through an OpenClaw WebAssembly sandbox limited to explicitly declared directories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and runs an unpinned remote WASM component. <br>
Mitigation: Use only after reviewing and trusting the downloaded component source, and avoid automatic refreshes without review. <br>
Risk: File write, overwrite, copy, and remove commands can modify or delete files in mapped directories. <br>
Mitigation: Keep workDir and mapDirs narrow, avoid mapping sensitive folders, and review each mutating command before execution. <br>


## Reference(s): <br>
- [boxed-fs Usage Reference](references/USAGE.md) <br>
- [Boxed fs ClawHub page](https://clawhub.ai/guyoung/boxed-fs) <br>
- [boxed-fs WASM component download](https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/boxed-fs/files/boxed-fs-component.wasm) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline JavaScript command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenClaw WebAssembly sandbox plugin and a downloaded WASM component before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
