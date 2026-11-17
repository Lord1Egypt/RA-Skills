## Description:

Guides developers in choosing, building, packaging, installing, and debugging After Effects extensions, native plugins, and external automation bridges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building After Effects extensions, native plugins, or automation bridges use this skill to choose an integration approach and work through setup, packaging, installation, debugging, and security considerations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review confidence is medium because some reference checks were incomplete; the guidance on enabling CEP debugging settings needs review.

Mitigation: Check the linked Adobe documentation and enable PlayerDebugMode only for trusted development builds; disable it when development ends.

Risk: Enabling PlayerDebugMode allows unsigned CEP extensions to load.

Mitigation: Enable it only for trusted development builds and disable it when development ends; sign packages for distribution.

Risk: An HTTP bridge can expose After Effects actions through a listening socket.

Mitigation: Prefer stdio; if HTTP is needed, bind to 127.0.0.1, require a token, reject browser-originated requests, and expose only specific commands.

## Reference(s):

- [CEP Extensions for After Effects](references/cep.md)
- [C++ SDK reference](references/cpp-sdk.md)
- [Bridges and MCP servers](references/bridges-and-mcp.md)
- [Adobe CEP Resources](https://github.com/Adobe-CEP/CEP-Resources)
- [After Effects UXP documentation](https://developer.adobe.com/after-effects/uxp/)
- [After Effects C++ SDK guide](https://ae-plugins.docsforadobe.dev/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Adobe CEP retirement and UXP announcement](https://blog.developer.adobe.com/en/publish/2026/09/investing-in-the-future-of-creative-cloud-extensibility-uxp-comes-to-our-flagship-applications)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code, shell command, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Version-specific; check compatibility with the installed After Effects, CEP, UXP, and SDK versions.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
