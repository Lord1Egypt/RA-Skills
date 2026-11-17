## Description:

Resolve Doc Bridge boundaries before changing code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emersonbraun](https://clawhub.ai/user/emersonbraun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill before repository edits to resolve Doc Bridge package or ownership boundaries, read required handoff guidance, keep changes inside declared edit roots, and run the returned checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may run repository-provided checks returned by Doc Bridge.

Mitigation: Use the skill in repositories you trust, inspect returned checks before execution, and keep edits within the resolved editRoots.

Risk: The fallback resolver may execute a downloaded npm package through npx when a local Doc Bridge binary is not configured.

Mitigation: Prefer a reviewed local Doc Bridge binary through DOC_BRIDGE_BIN or a pinned dependency installation before using the fallback path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emersonbraun/skills/doc-bridge-handoff)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with optional JSON resolver output and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The resolver is fail-closed when required handoff fields are missing, unsafe, or target-mismatched.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
