## Description:

Manages Ark inference endpoints through the arkcli command line, including listing and maintaining endpoints and explicitly requested raw CRUD creation for scripted workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and manage inference endpoints with arkcli. It supports listing, detail lookup, start and stop, updates, deletion, and explicitly requested script or CI creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this skill suspicious because some endpoint creation instructions may not match the declared purpose and a deletion safeguard can be bypassed.

Mitigation: Follow the supplied Skillspector DO_NOT_INSTALL recommendation and review the suspicious findings before installation. The scan is partial because two referenced paths were missing, so this evidence does not establish that the artifact is safe.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jasonstarlight/skills/arkcli-infer-endpoint)
- [arkcli endpoint creation guide](artifact/references/arkcli-infer-endpoint-create.md)
- [arkcli endpoint list guide](artifact/references/arkcli-infer-endpoint-list.md)
- [arkcli endpoint get guide](artifact/references/arkcli-infer-endpoint-get.md)
- [arkcli endpoint update guide](artifact/references/arkcli-infer-endpoint-update.md)
- [arkcli endpoint start guide](artifact/references/arkcli-infer-endpoint-start.md)
- [arkcli endpoint stop guide](artifact/references/arkcli-infer-endpoint-stop.md)
- [arkcli endpoint delete guide](artifact/references/arkcli-infer-endpoint-delete.md)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text, Markdown, JSON, CSV]

**Output Format:** [Markdown guidance with shell commands and structured endpoint results or tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands for state-changing endpoint operations.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata; artifact frontmatter reports 1.3.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
