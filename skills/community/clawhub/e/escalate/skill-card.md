## Description: <br>
Self-learn to decide when to act, when to ask, and which actions should always need approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to maintain a durable ask-versus-act policy across sessions. It helps agents decide when to proceed autonomously, when to propose a path, and when explicit approval is required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores local escalation notes under ~/escalate/, which could accidentally include secrets or private third-party data. <br>
Mitigation: Keep secrets out of escalation memory, review ~/escalate/ periodically, and follow the skill guidance to avoid persisting credentials or copied private data. <br>
Risk: Workspace AGENTS or SOUL routing snippets could change how an agent decides when to ask for approval. <br>
Mitigation: Review the exact proposed snippet before any write and only approve small, non-destructive additions. <br>
Risk: Incorrect autonomy rules could let an agent proceed too freely on risky work. <br>
Mitigation: Keep money, deletion, credentials, legal, production, external communication, and other irreversible actions behind explicit approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/escalate) <br>
- [Skill homepage](https://clawic.com/skills/escalate) <br>
- [Setup guide](artifact/setup.md) <br>
- [Hard boundaries](artifact/boundaries.md) <br>
- [Pattern recognition](artifact/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local escalation memory files after user approval.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
