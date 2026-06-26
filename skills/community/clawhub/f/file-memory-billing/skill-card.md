## Description: <br>
File Memory Copilot helps agents preserve task state in files by creating task archives and updating ops or memory notes instead of relying on chat history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shr860910](https://clawhub.ai/user/shr860910) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to hand off long-running work across context resets by keeping task status, decisions, work logs, next steps, and memory notes in files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill attempts to charge a billing account on each use without a clear per-use confirmation step. <br>
Mitigation: Install only when paid execution is intended, verify who controls the billing endpoint and key, and set spending limits outside the skill where possible. <br>
Risk: Task and memory files can persist sensitive information or stale instructions beyond the current chat. <br>
Mitigation: Review generated ops and memory files before reuse or commit, and do not persist secrets in repository files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shr860910/file-memory-billing) <br>
- [SkillPay billing endpoint](https://skillpay.me/api/v1/billing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files and concise status text; billing helper output is JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and SKILL_BILLING_API_KEY; SKILL_ID is required by the billing helper.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
