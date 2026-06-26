## Description: <br>
Systematic workspace reorganization for AI agent users. Scans workspace, builds safety-first reorganization plan, executes with zero data loss, and verifies everything works afterward. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI agent operators use this skill to scan, plan, and audit file-based workspace reorganizations before moving files. It is intended for cleanup, recovery, migration, onboarding, and pre-deployment workspace integrity checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill loads user-provided Python configuration files, which can execute code with the user's privileges. <br>
Mitigation: Use only reviewed configuration files from trusted sources and run the skill in a limited, backed-up workspace. <br>
Risk: Configured process checks can run local commands and inspect process output. <br>
Mitigation: Review or hardcode process-check commands before use, and disable process checks where they are not needed. <br>
Risk: Generated reports and manifests may expose workspace structure, secret locations, and process details. <br>
Mitigation: Keep generated outputs out of shared repositories and review them before sharing. <br>
Risk: Workspace reorganization plans can still lead to broken references or data loss if executed without review. <br>
Mitigation: Maintain an independent backup, review the generated plan manually, run the pre-move audit, and verify with the post-move audit after execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TheShadowRose/crucible-forge) <br>
- [Publisher Profile](https://clawhub.ai/user/TheShadowRose) <br>
- [OpenClaw Project](https://github.com/openclaw/openclaw) <br>
- [LIMITATIONS.md](artifact/LIMITATIONS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON reports, Audit manifests] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local filesystem analysis; generated reports may include workspace paths, file structure, secret-location warnings, process details, and rollback guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact SKILL.md frontmatter says 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
