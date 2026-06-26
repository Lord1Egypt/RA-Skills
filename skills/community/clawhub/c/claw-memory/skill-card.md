## Description: <br>
Claw Memory helps AI agents store, retrieve, search, and share memories across agent instances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[siddontang](https://clawhub.ai/user/siddontang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to configure a shared memory space, import existing memory notes, and store or search memories through a hosted API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send local memory notes to a third-party hosted memory service. <br>
Mitigation: Install only when external memory storage is intended, and review or redact MEMORY.md, daily notes, and other content before upload. <br>
Risk: Bearer tokens and optional encryption keys can grant access to stored memories if exposed. <br>
Mitigation: Protect tokens and encryption keys, avoid placing secrets in shared logs or notes, and rotate credentials if they are disclosed. <br>
Risk: The install instructions use a raw main-branch download URL. <br>
Mitigation: Prefer a pinned or reviewed install source before deploying the skill in a sensitive environment. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/siddontang/claw-memory) <br>
- [Claw Memory API](https://claw-memory.siddontang.workers.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, API Calls] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include curl commands to create tokens, upload memory content, search memories, or claim the backing database.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
