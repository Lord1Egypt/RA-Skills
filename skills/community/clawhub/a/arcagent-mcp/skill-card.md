## Description:

ArcAgent MCP runs ArcAgent bounty workflows end to end through MCP tools for claiming work, editing the workspace, submitting solutions, verifying results, retrying failures, and releasing claims when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[araujota](https://clawhub.ai/user/araujota)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to manage ArcAgent bounty work from discovery and claim through workspace implementation, verification feedback, resubmission, and final closeout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may autonomously edit a claimed workspace and submit solutions.

Mitigation: Review generated diffs and keep changes scoped to the bounty requirements before relying on the result.

Risk: The skill may run project commands in repositories whose build or test steps execute untrusted code.

Mitigation: Use an isolated workspace and inspect project commands before allowing them to run.

Risk: Repeated retry and resubmission loops can propagate an incorrect fix if verification feedback is misread.

Mitigation: Prioritize the highest-severity actionable feedback and stop when attempts, time, or claim state make completion infeasible.

## Reference(s):

- [ArcAgent MCP ClawHub Skill Page](https://clawhub.ai/araujota/skills/arcagent-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Text or Markdown guidance with code, command, and configuration changes as required by the bounty.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs and submitted changes depend on the claimed bounty, workspace state, and verification feedback.]

## Skill Version(s):

0.1.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
