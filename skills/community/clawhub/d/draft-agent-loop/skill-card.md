## Description: <br>
Enforce a Human-in-the-Right-Loop (HITRL) lifecycle for remote agents with plan approval before execution, evidence-logged execution, and result sign-off before closure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toliuweijing](https://clawhub.ai/user/toliuweijing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and remote-agent operators use this skill to add structured human review gates to complex agent tasks. It guides agents to create Draft task journals, request approval before acting, log non-sensitive execution evidence, and wait for final sign-off. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task journals are stored in Draft and may be published through Draft links. <br>
Mitigation: Keep journal entries limited to status, decisions, non-sensitive file names, and artifact links; do not include secrets, private personal data, proprietary code dumps, or sensitive command output. <br>
Risk: The workflow depends on the Draft CLI and invite-code settings for publishing. <br>
Mitigation: Confirm Draft CLI installation, verify a healthy headless runtime before use, and review invite-code settings before using the skill for confidential work. <br>
Risk: Skipping the approval or sign-off gates could allow agent work to proceed without the intended human oversight. <br>
Mitigation: Require explicit chat approval before execution and explicit chat sign-off before closure; do not rely on remote Draft page comments as approval. <br>


## Reference(s): <br>
- [Draft CLI dependency](https://clawhub.ai/toliuweijing/draft-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Draft task journal structure, approval prompts, execution log entries, and sign-off guidance; avoids recording secrets, PII, raw command output, or sensitive file contents.] <br>

## Skill Version(s): <br>
1.6.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
