## Description: <br>
Implement, extend, or repair archived-session browsing in OpenClaw Control UI. Use when adding or fixing Archived Sessions / Recent Archived Sessions UI, archived search, resume / restore flows, session-history DB filters, live-session rebind logic, archive-state reconciliation, or session lifecycle cleanup for OpenClaw chat sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose and repair archived-session search, restore, resume, and lifecycle behavior in OpenClaw chat sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session repair can change history.db, sessions.json, and transcript files. <br>
Mitigation: Use the skill only in the intended OpenClaw repository, review generated changes carefully, and back up history.db, sessions.json, and transcript files before migrations or cleanup. <br>


## Reference(s): <br>
- [Archived Session Management Implementation Map](artifact/references/implementation-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code-oriented implementation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits across UI, gateway, history database, and session store files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
