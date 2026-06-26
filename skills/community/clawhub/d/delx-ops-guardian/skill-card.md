## Description: <br>
Delx Ops Guardian helps agents handle OpenClaw production incidents with least-privilege recovery steps, Delx safety checks, and concise incident reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidmosiah](https://clawhub.ai/user/davidmosiah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to classify OpenClaw production incidents, collect evidence, apply narrow recovery actions, and publish recovery reports with Delx session continuity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide host-level operations such as service restarts, cron changes, journal review, and access to OpenClaw production artifacts. <br>
Mitigation: Install only where agent-assisted operations management is intended; use scoped sudo, named services, incident-scoped access, and explicit approvals before restarts or cron edits. <br>
Risk: Incident logs and reports may expose secrets or incorrectly present persistent failures as resolved. <br>
Mitigation: Review reports before sharing, redact secrets, require stabilization evidence, and keep unresolved failures marked open or degraded. <br>
Risk: The required Delx plugin may receive production incident context. <br>
Mitigation: Verify the third-party plugin and publisher before granting production access or access to OpenClaw system paths. <br>


## Reference(s): <br>
- [Delx Protocol Documentation](https://delx.ai/docs) <br>
- [Delx Ontology Documentation](https://delx.ai/docs/ontology) <br>
- [OpenClaw Delx Plugin](https://clawhub.ai/davidmosiah/openclaw-delx-plugin) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown incident guidance with inline shell commands and JSON-like tool call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes approval gates, least-privilege scope, stabilization checks, rollback notes, and Delx session identifiers in reports.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence release.version and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
