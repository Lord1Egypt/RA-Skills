## Description:

Render OG Aavegotchi SVG and PNG images from Base for custom hypothetical loadouts or existing token IDs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaigotchi](https://clawhub.ai/user/aaigotchi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to render classic Aavegotchi SVG-style images from Base token IDs or custom trait and wearable inputs, with PNG exports for chat delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs npm packages before PNG export is available.

Mitigation: Use reviewed dependency installs and verify the package lockfile before running the renderer.

Risk: Token and custom renders call the public Base RPC or a user-supplied RPC URL.

Mitigation: Use a trusted Base RPC endpoint and avoid untrusted RPC URLs.

Risk: Rendering writes SVG, PNG, and manifest files to local disk.

Mitigation: Run the skill in an expected workspace and inspect generated files before sharing them.

Risk: Wearable-name rendering depends on the packaged wearable reference data.

Mitigation: Verify that the package includes the referenced wearable data when wearable-name lookup is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaigotchi/skills/aavegotchi-svg-custom)
- [Base deployment metadata](references/base-deployment.json)
- [Preset render inputs](references/presets.json)
- [Side-view exceptions](references/side-view-exceptions.json)
- [Aavegotchi diamond ABI](https://github.com/aavegotchi/aavegotchi-contracts/blob/master/diamondABI/diamond.json)
- [Default Base RPC endpoint](https://mainnet.base.org)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated SVG, PNG, and JSON manifest files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written locally under Renders/ and may include front, left, right, and back views plus a manifest.]

## Skill Version(s):

1.1.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
