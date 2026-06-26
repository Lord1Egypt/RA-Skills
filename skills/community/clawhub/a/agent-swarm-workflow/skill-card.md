## Description: <br>
Jeffrey Emanuel's multi-agent implementation workflow using NTM, Agent Mail, Beads, and BV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdnw](https://clawhub.ai/user/clawdnw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate a supervised multi-agent coding workflow across task selection, Agent Mail coordination, review loops, and commit prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may autonomously edit, commit, and push project changes without clear human approval or branch safeguards. <br>
Mitigation: Run the workflow on a dedicated branch or worktree and require human review before any commit or push. <br>
Risk: Multi-agent instructions and messages can expose sensitive project details if secrets are included in prompts or mail. <br>
Mitigation: Keep secrets out of project instructions and Agent Mail messages, and use only trusted coordination tooling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawdnw/agent-swarm-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes reusable prompts for agent coordination, review, and commit workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
