## Description: <br>
Architecture personal assistant for independent architects working on commercial, retail, F&B, and institutional projects, supporting daily news digests, project tracking, research scouting, design concept exploration, client message drafting, and passive project context capture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hao-tian-xu](https://clawhub.ai/user/hao-tian-xu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Independent architects and architecture teams use this skill to maintain project context, run architecture news and research digests, explore design concepts, and draft client-facing messages for commercial, retail, F&B, and institutional projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Always-on project tracking can persist client, payment, and project details without clear per-update approval. <br>
Mitigation: Review or remove the workspace/AGENTS.md passive-capture directive before enabling the skill, and require explicit approval for sensitive updates. <br>
Risk: Workspace project files and digests may retain confidential or overly sensitive architecture project information. <br>
Mitigation: Avoid storing confidential client or payment details unless appropriate, and periodically audit project files for incorrect or sensitive captured notes. <br>
Risk: Recommended cron entries can run digest, check-in, and research actions proactively. <br>
Mitigation: Review any cron entries before activation and disable scheduled runs when proactive behavior is not desired. <br>


## Reference(s): <br>
- [Architecture Information Sources](references/config/sources.md) <br>
- [Construction Methods Knowledge Reference](references/knowledge/construction.md) <br>
- [Cost & Schedule Knowledge Reference](references/knowledge/cost-schedule.md) <br>
- [Materials Knowledge Reference](references/knowledge/materials.md) <br>
- [Retail & Commercial Design Knowledge Reference](references/knowledge/retail-commercial.md) <br>
- [Sustainability Knowledge Reference](references/knowledge/sustainability.md) <br>
- [Check-in Procedure](references/procedures/checkin.md) <br>
- [Concept Exploration Procedure](references/procedures/concept-explore.md) <br>
- [Digest Procedure](references/procedures/digest.md) <br>
- [Draft Message Procedure](references/procedures/draft-message.md) <br>
- [Research Procedure](references/procedures/research.md) <br>
- [Project Template](references/project-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses and workspace Markdown files, with optional shell commands for cron setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update workspace project files, digests, source configuration, and AGENTS.md directives.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
