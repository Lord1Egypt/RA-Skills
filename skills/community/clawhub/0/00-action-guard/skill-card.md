## Description: <br>
Guides an agent to call permission-gate before tools, writes, sensitive queries, cross-platform messages, skill invocation, or other non-casual actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rancho718](https://clawhub.ai/user/rancho718) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent developers and operators use this skill to add a permission-checking step before tool use, file changes, sensitive queries, cross-platform messages, and skill invocation while allowing routine conversation to continue. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: If permission checks are skipped or misconfigured, tools, writes, sensitive queries, or cross-platform actions may run without the intended gate. <br>
Mitigation: Require the agent to wait for permission-gate results and proceed only when allowed=true, as described in the artifact. <br>
Risk: The security guidance notes powerful actions in the release context. <br>
Mitigation: Install and use the skill only in intended ClawHub or Convex maintenance contexts, and review tool, moderation, or PR actions before approving writes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rancho718/00-action-guard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code, shell commands, API calls, or configuration files are produced by the skill itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
