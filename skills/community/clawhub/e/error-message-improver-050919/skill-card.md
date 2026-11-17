## Description:

Helps users and support teams improve vague error messages so they explain what failed, why it failed, and what action to take next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, SaaS operators, and end users use this skill to turn unclear errors into actionable messages, reusable workflows, checklists, or implementation guidance for troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may invoke the skill for general debugging or support prompts beyond explicit error-message rewriting.

Mitigation: Use narrower triggers or invoke the skill explicitly when teams only want it for troubleshooting-copy and error-message improvement tasks.

Risk: Generated guidance can make incorrect assumptions about a failure when the original error context is incomplete.

Mitigation: Ask for missing inputs that materially change the answer and state assumptions, limits, and validation steps in the output.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/error-message-improver-050919)
- [Publisher Profile](https://clawhub.ai/user/kyro-ma)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text guidance with optional code, shell-command, configuration, workflow, or checklist blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should expose assumptions, limits, validation notes, and next steps when helpful.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
