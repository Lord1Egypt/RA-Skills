## Description:

Actuator is presented as an actuator selection and sizing calculator, but the artifact evidence shows a command-line local record manager for adding, listing, searching, removing, exporting, and configuring entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can run the skill as a CLI-style local entry manager for storing, searching, exporting, and deleting user-provided records. Do not rely on it for actuator sizing or operational engineering decisions unless the implementation is corrected to match that advertised purpose.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised actuator sizing purpose does not match the artifact behavior, which operates as a persistent local record manager.

Mitigation: Verify the implementation against the advertised engineering use case before using outputs for actuator selection, sizing, or operational decisions.

Risk: The config command is identified by the security evidence as unsafe with untrusted input and capable of executing injected shell commands.

Mitigation: Avoid untrusted config keys and values, do not run the skill in automated workflows, and require implementation changes before production deployment.

Risk: The skill stores user-provided entries locally and can export or delete them.

Mitigation: Do not store sensitive operational notes, and scope ACTUATOR_DIR to an isolated directory when evaluating the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/actuator)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Plain text CLI output and JSONL/CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores entries under the ACTUATOR_DIR path, defaulting to ~/.actuator/.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
