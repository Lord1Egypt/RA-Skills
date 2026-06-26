## Description: <br>
Belief systems auditor for OpenClaw agents. Systematically evaluates an agent's loaded context files (SOUL.md, AGENTS.md, USER.md, skills) against the user's stated goals to identify misaligned, stale, conflicting, vague, or redundant beliefs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcroebuck](https://clawhub.ai/user/mcroebuck) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent owners use Clawdit to audit OpenClaw agent context files, skills, and stored user goals against the user's intended agent behavior. The skill produces structured findings about alignment, conflicts, stale instructions, vague beliefs, redundancy, and token efficiency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect selected agent context and skill files that contain private preferences or operational instructions. <br>
Mitigation: Confirm the target workspace before use and install only when that level of context-file inspection is acceptable. <br>
Risk: The skill may update USER.md goal information or generate revised files and changelogs that could affect future agent behavior. <br>
Mitigation: Review USER.md goal updates, generated revisions, and changelogs before approving or applying changes to the target agent. <br>


## Reference(s): <br>
- [Clawdit on ClawHub](https://clawhub.ai/mcroebuck/clawdit) <br>
- [Publisher profile](https://clawhub.ai/user/mcroebuck) <br>
- [Audit framework](artifact/audit-framework.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown audit reports, summaries, proposed revisions, changelogs, and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate review artifacts in the Clawdit workspace after user approval; proposed changes require user review before applying to a target agent.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
