## Description:

Zero‑exposure cross‑device script authorization using MGC Blackbox, with encrypted capsule delivery, p2p and free modes, link authorization, and self-describing capsules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zkeviny](https://clawhub.ai/user/zkeviny)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations teams use this skill to seal, transfer, import, and run scripts across MGC nodes while limiting plaintext exposure. It also explains how to choose between node-bound p2p authorization and public free mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Imported scripts may be unreadable before execution and can run with the caller's account permissions.

Mitigation: Review the script source or obtain an independently authenticated delivery, require approval before execution, and run it in a separate environment with limited permissions and credentials.

Risk: The skill's origin and tamper-resistance claims may be mistaken for proof that a script is trustworthy.

Mitigation: Verify the owner node's public key through a trusted channel; treat public-key comparison and link authorization as limited integrity checks, not proof of safe behavior.

Risk: Sandbox workarounds could weaken execution boundaries.

Mitigation: Preserve sandbox restrictions and do not bypass them to make tool calls work.

## Reference(s):

- [MGC Blackbox repository](https://github.com/zkeviny/MGC-Blackbox)
- [MGC Blackbox issues](https://github.com/zkeviny/MGC-Blackbox/issues)
- [ClawHub skill page](https://clawhub.ai/zkeviny/skills/cross-node-script-auth)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown with Python, JSON, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Procedural guidance and examples for MGC Blackbox 1.5.4 or later; workflows may produce sealed capsule files.]

## Skill Version(s):

1.3.0 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
