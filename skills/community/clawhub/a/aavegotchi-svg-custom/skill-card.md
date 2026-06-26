## Description: <br>
Render OG Aavegotchi SVG and PNG images from Base for custom hypothetical loadouts or existing token IDs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaigotchi](https://clawhub.ai/user/aaigotchi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to render classic onchain Aavegotchi images from Base token IDs or custom trait and wearable selections. It is intended for OG SVG-style Aavegotchi outputs rather than generic image generation or 3D renders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Node and shell scripts and installs locked npm dependencies. <br>
Mitigation: Install and run it only in an environment where local script execution and the bundled dependency lockfile are acceptable. <br>
Risk: Token IDs and custom loadout details may be sent to the configured Base RPC provider. <br>
Mitigation: Use a trusted RPC endpoint, such as an approved AAVEGOTCHI_RPC_URL override, when render inputs are sensitive. <br>
Risk: Token rendering depends on Base RPC availability and required reference data. <br>
Mitigation: Expect runtime failures when the RPC endpoint is unavailable or required wearable reference data is missing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aaigotchi/aavegotchi-svg-custom) <br>
- [Base Deployment Metadata](references/base-deployment.json) <br>
- [Preset Definitions](references/presets.json) <br>
- [Side-View Exceptions](references/side-view-exceptions.json) <br>
- [Aavegotchi Diamond ABI](https://github.com/aavegotchi/aavegotchi-contracts/blob/master/diamondABI/diamond.json) <br>
- [Default Base RPC Endpoint](https://mainnet.base.org) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [SVG, PNG, JSON manifest, and chat-ready media path text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes front, left, right, and back render files plus a manifest JSON into Renders/ by default.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
