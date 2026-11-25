## Description:

Creates one video transition that starts at an approved first image and ends at an approved last image, then reviews the generated clip's motion and endpoint match.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use the skill to make one short video transition between two approved images, such as a product reveal or before-and-after change, and review the result for endpoint and motion fidelity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags broad shared-account access and persistent installation and environment reporting beyond the skill's stated video purpose, which may involve more account or device context than expected.

Mitigation: Review the reported permissions and data collection before installing, and proceed only if they are acceptable.

Risk: Security scan coverage is partial because several local references were unresolved, leaving some behavior unassessed.

Mitigation: Resolve and review the referenced files and reassess the security evidence before use.

## Reference(s):

- [First-and-last-frame workflow](artifact/references/workflow.md)
- [Tasks and results](artifact/references/tasks-and-results.md)
- [Updates and security](artifact/references/updates-and-security.md)
- [Installation and authentication](artifact/references/installation-and-auth.md)

## Skill Output:

**Output Type(s):** [Video, Text]

**Output Format:** [A generated video artifact with a concise text status and review]

**Output Parameters:** [One transition clip per run]

**Other Properties Related to Output:** [The clip targets the approved first and last frames; delivery details depend on the service response.]

## Skill Version(s):

0.2.8 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
