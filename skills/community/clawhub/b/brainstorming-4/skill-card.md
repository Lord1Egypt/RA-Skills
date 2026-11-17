## Description:

Guides agents through structured brainstorming, requirements clarification, design approval, and specification review before implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuhe12](https://clawhub.ai/user/liuhe12)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to turn creative or feature requests into scoped designs and reviewed specs before implementation planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill takes broad control over the agent workflow and can slow or override direct implementation requests.

Mitigation: Install it only when a design-first workflow is desired, and confirm that users explicitly approve designs before implementation planning begins.

Risk: The optional browser companion logs selections and can be exposed on the network if configured with a non-loopback host.

Mitigation: Keep the companion bound to localhost unless remote access is intentional, and avoid putting sensitive information in mockups or browser selections.

Risk: Design documents, mockups, click history, and brainstorm session files may be written or committed as part of the workflow.

Mitigation: Review generated files before committing, keep temporary companion artifacts out of source control unless intentionally preserved, and clean sessions that are no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liuhe12/skills/brainstorming-4)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown prose with occasional shell commands and HTML fragments for visual mockups]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create design documents, review prompts, visual mockups, and local companion session artifacts during the workflow.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
