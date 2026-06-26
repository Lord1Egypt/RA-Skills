## Description: <br>
OpenClaw execution governance skill for approval gates, risk classification, confirmation policy, and action boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dmiyding](https://clawhub.ai/user/dmiyding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to classify execution risk, reduce confirmation noise for routine work, and require explicit confirmation for high-risk or critical actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally changes confirmation behavior for routine and medium-risk OpenClaw work. <br>
Mitigation: Review the MEDIUM examples before deployment and keep runtime approval policy enabled for destructive, credential, shared-routing, external-delivery, and costly actions. <br>
Risk: Installing or storing the skill does not guarantee active governance behavior in OpenClaw. <br>
Mitigation: Activate it through an always-injected entry point such as AGENTS.md or an equivalent standing-order policy and validate activation with the provided prompts. <br>
Risk: Prompt-layer governance cannot provide a non-bypassable block for privileged, destructive, costly, or outbound actions by itself. <br>
Mitigation: Use runtime and policy enforcement for actions that must always be blocked or require guaranteed approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dmiyding/clawgate) <br>
- [Project homepage](https://github.com/DmiyDing/clawgate) <br>
- [Risk Matrix](references/risk-matrix.md) <br>
- [Confirmation Templates](references/confirmation-templates.md) <br>
- [AGENTS Activation Snippet](references/agents-snippet.md) <br>
- [Eval Guide](evals/README.md) <br>
- [OpenClaw Acceptance Prompts](evals/openclaw-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with structured risk and confirmation blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include explicit LOW, MEDIUM, HIGH, or CRITICAL risk posture and activation guidance.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata; artifact frontmatter reports 0.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
