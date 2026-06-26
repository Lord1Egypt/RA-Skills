## Description: <br>
Designs a Uniswap V4 hook architecture without code generation, producing a structured design document for callbacks, hook flags, state management, gas estimates, security considerations, and architecture choices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and protocol engineers use this skill to plan Uniswap V4 hook behavior before implementation. It helps select callbacks, reason about state and gas tradeoffs, identify security considerations, and document architecture decisions for implementers or reviewers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Design guidance may be incomplete or incorrect for production smart contract implementation. <br>
Mitigation: Review outputs against Uniswap V4 documentation and have qualified smart contract engineers or auditors validate the design before implementation. <br>
Risk: The delegated hook-builder step could exceed the intended no-code, no-write boundary if the runtime does not enforce those constraints. <br>
Mitigation: Run the skill with the documented design-only constraints and review generated plans before using them for development. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/design-hook) <br>
- [Skill specification](artifact/SKILL.md) <br>
- [Skill README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown design document] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Design-only output; no code generation or file writes. Gas estimates are approximate and depend on implementation details.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
