## Description:

Google Draco 3D geometry compression library. Compresses and decompresses 3D meshes and point clouds, with glTF, Three.js, and Unity integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for guidance on compressing and decompressing Draco 3D meshes or point clouds, integrating Draco with glTF and Three.js, and applying encoder, decoder, quantization, and memory-management APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned package or CDN use can make installs and decoder behavior less reproducible.

Mitigation: Pin draco3d and the Draco decoder CDN to reviewed exact versions, and use a lockfile or npm ci for installs.

Risk: Draco WASM objects can leak memory if they are not released.

Mitigation: Release module-created decoder, encoder, mesh, point-cloud, and array objects with d.destroy(obj) after use.

## Reference(s):

- [Draco3D API Reference](references/api-reference.md)
- [Draco decoder CDN](https://www.gstatic.com/draco/versioned/decoders/1.5.7/)
- [ClawHub skill page](https://clawhub.ai/openlark/skills/draco3d)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript code blocks, install commands, API notes, and integration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Draco decoder and encoder usage patterns, Three.js loader configuration, quantization defaults, and memory-release guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
