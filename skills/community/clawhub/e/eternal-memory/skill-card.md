## Description: <br>
Eternal Memory provides an offline-first five-layer memory system with local vector search, append-only archiving, L1c verification, topology scoring, and hot/cold separation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yy13507320330](https://clawhub.ai/user/yy13507320330) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to install and operate local OpenClaw memory indexing, retrieval, verification, topology scoring, and maintenance tools for persistent agent memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and writes the local OpenClaw memory workspace. <br>
Mitigation: Review the configured workspace paths and back up important memory data before running archive, wake, migrate, or maintenance commands. <br>
Risk: Suggested recurring jobs can repeatedly scan and modify local memory indexes. <br>
Mitigation: Run maintenance commands manually first and enable cron only after reviewing the scheduled behavior. <br>
Risk: Optional embedding server mode exposes a localhost API. <br>
Mitigation: Avoid --serve unless a local embedding API is required, and keep it bound to localhost. <br>
Risk: Results produced with verification disabled may be less trustworthy. <br>
Mitigation: Treat --no-verify output as untrusted and prefer the default verification path for retrieval results. <br>
Risk: Optional ONNX acceleration may change the offline-only posture. <br>
Mitigation: Use SKIP_ONNX=1 when strict offline operation is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yy13507320330/skills/eternal-memory) <br>
- [Architecture reference](references/architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line text with Python code and YAML configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for local OpenClaw memory workspaces and may include status reports, search results, benchmark output, and maintenance guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
