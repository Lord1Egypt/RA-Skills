## Description: <br>
Aios Transfer File helps OpenClaw and AIOS agents move file_input:// objects and local workspace files through an S3-compatible SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kadbbz](https://clawhub.ai/user/kadbbz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AIOS/OpenClaw operators use this skill when an agent needs to download a file_input:// object into the workspace or upload a local file and return a file_output:// URI to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move files through S3-compatible object storage and generate file_output:// URIs that represent data leaving the local workspace. <br>
Mitigation: Use it only with trusted S3 endpoints and buckets in a controlled AIOS/OpenClaw environment, and review uploads before sending sensitive files. <br>
Risk: The security summary notes weak user confirmation and no enforced source-path containment for file movement. <br>
Mitigation: Require explicit operator confirmation for outbound transfers, keep file operations inside the intended workspace, and use least-privilege S3 credentials. <br>
Risk: Runtime dependency installation can add supply-chain exposure if performed ad hoc. <br>
Mitigation: Preinstall dependencies from the bundled lockfile in the deployment image or controlled skill directory before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kadbbz/aios-transfer-file) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; the bundled transfer script emits JSON or file_output:// URI strings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a controlled AIOS/OpenClaw environment, trusted S3 endpoint and buckets, configured AIOS_S3_* environment variables, Node.js, and local npm dependencies.] <br>

## Skill Version(s): <br>
0.1.3 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
