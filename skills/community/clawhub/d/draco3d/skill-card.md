## Description: <br>
Google Draco 3D geometry compression library. Compresses and decompresses 3D meshes and point clouds, with glTF, Three.js, and Unity integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for guidance on compressing and decompressing 3D meshes and point clouds with Draco3D, including glTF, Three.js, browser, and Node.js integration patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples rely on third-party Draco3D package and CDN decoder dependencies. <br>
Mitigation: Pin package and CDN versions, use trusted sources, and review production dependency policy before adoption. <br>
Risk: WASM objects created by Draco3D can leak memory if not released. <br>
Mitigation: Follow the skill guidance to release module-created objects with d.destroy(obj). <br>


## Reference(s): <br>
- [Draco3D API Reference](references/api-reference.md) <br>
- [Versioned Draco decoder CDN](https://www.gstatic.com/draco/versioned/decoders/1.5.7/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with JavaScript code examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; examples require users to manage third-party Draco3D package and CDN dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
