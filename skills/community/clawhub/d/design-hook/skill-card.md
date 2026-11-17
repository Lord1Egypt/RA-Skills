## Description:

Design a Uniswap V4 hook architecture without code generation, helping users plan callbacks, state management, gas estimates, security considerations, and architecture decisions before implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to plan Uniswap V4 hook behavior before writing Solidity. It produces a structured design document covering callback selection, hook flags, state management, gas estimates, security considerations, feasibility, and alternatives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install commands may resolve mutable package or source state.

Mitigation: Prefer a pinned ClawHub version or immutable Git commit when installing.

Risk: The skill delegates planning to a broader hook-building subagent.

Mitigation: Review the local hook-builder subagent's permissions and use this skill as a design aid, not as an enforcement boundary.

Risk: The output can include approximate gas estimates and architecture guidance that may be incomplete for a final implementation.

Mitigation: Validate the design with implementation review, testing, and security review before building or deploying a hook.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown design document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Design-only output; no code or files are generated, and gas estimates are approximate.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata, created 2026-02-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
