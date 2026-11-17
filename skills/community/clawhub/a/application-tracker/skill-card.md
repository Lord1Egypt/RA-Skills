## Description:

Start and review web form autofill workflow with human approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanghong5233](https://clawhub.ai/user/wanghong5233)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to start a local web form autofill preview, route an approve or reject decision, and summarize filled or failed fields before manual submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented curl templates can create unsafe command-execution exposure if untrusted form URLs or profile values are interpolated literally.

Mitigation: Use a safe HTTP client or JSON serialization path instead of shell command templates, and only connect to a trusted local service.

Risk: The workflow handles application profile data and may fill incorrect or sensitive fields.

Mitigation: Avoid sensitive profile data until command construction is fixed, require explicit approve or reject decisions, and manually review any filled form before submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanghong5233/skills/application-tracker)
- [ClawHub publisher profile](https://clawhub.ai/user/wanghong5233)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before fill execution; external forms are never submitted automatically.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
