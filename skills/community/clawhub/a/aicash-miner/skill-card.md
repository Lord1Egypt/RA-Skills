## Description: <br>
AICash Network auto-miner for $CASH tokens on Base L2. Use when setting up automated Proof of Compute mining on the AICash mempool network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Doctor-1017](https://clawhub.ai/user/Doctor-1017) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure and manage automated AICash Proof of Compute mining, including multi-instance Linux services and status controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs persistent root-level mining services. <br>
Mitigation: Install only on a dedicated Linux host where persistent mining is intended, verify the created systemd units, and remove both the unit files and /root/.openclaw/workspace/aicash when uninstalling. <br>
Risk: Supplied API credentials can be stored in generated files. <br>
Mitigation: Use a revocable API key and rotate it if the host or generated files may have been exposed. <br>
Risk: High instance counts can increase host resource use. <br>
Mitigation: Start with a small instance count and monitor service behavior before scaling. <br>


## Reference(s): <br>
- [AICash Network](https://aicash.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/Doctor-1017/aicash-miner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of persistent systemd services and generated miner files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
