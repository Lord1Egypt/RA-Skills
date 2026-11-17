## Description:

Use Engrm to compare what was asked, what was promised, and what evidence suggests was actually delivered.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dr12hes](https://clawhub.ai/user/dr12hes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to review whether an agent session delivered the requested outcome, identify scope drift or partial delivery, and preserve concise delivery-review history when Engrm is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent may invent Engrm setup steps or CLI commands when Engrm is not connected.

Mitigation: Use Engrm only when it is already connected and available; otherwise disclose that Delivery Review cannot use Engrm on the machine and continue without invented setup or shell instructions.

Risk: Delivery history may become misleading if the agent saves optimistic summaries when evidence is mixed.

Mitigation: Compare the brief, plan, decisions, and delivery evidence, then save the real outcome, the main gap or drift, and the lesson future sessions should know first.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or concise prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include concise review memories about outcomes, gaps, and lessons when Engrm is available.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
