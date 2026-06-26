## Description: <br>
Deprecated legacy OpenClaw session cleanup skill that scans for orphan .jsonl files and stale sessions, then guides user-confirmed cleanup while directing users to session-cleanup-pro. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[irideas](https://clawhub.ai/user/irideas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this deprecated compatibility skill to inspect local session storage, identify orphan session files and stale sessions, and prepare a cleanup plan that requires explicit user confirmation before removal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is deprecated and may guide removal of local OpenClaw session files. <br>
Mitigation: Prefer the replacement skill session-cleanup-pro, run scan mode first, and proceed only after reviewing the generated orphan and stale session lists. <br>
Risk: Cleanup actions can remove session data if the user approves the wrong files. <br>
Mitigation: Prefer archive or move before hard delete, keep protected sessions intact, and require explicit confirmation before deletion. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/irideas/bobo-session-cleanup) <br>
- [Publisher Profile](https://clawhub.ai/user/irideas) <br>
- [Cleanup Policy](references/policy.md) <br>
- [Scan Script](scripts/scan_sessions.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON scan summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local bash and node; scan mode reads OpenClaw session state and cleanup requires user confirmation.] <br>

## Skill Version(s): <br>
0.2.1 (source: server evidence release.version and artifact frontmatter metadata.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
