## Description:

Build, debug, package, and document Adobe Illustrator integrations: CEP extension panels, C++ SDK plug-ins (.aip), the coming UXP plugins, MCP servers that drive Illustrator, computer-use automation, and OS scripts (batch, PowerShell, bash, AppleScript) that run ExtendScript in Illustrator. Use when creating or fixing an Illustrator extension or plug-in, choosing between a script, extension, or plug-in, connecting an AI tool to Illustrator, automating Illustrator from the command line, or writing install and usage docs for an Illustrator tool someone will publish. Pairs with adobe-illustrator-scripting for the ExtendScript DOM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose, build, debug, package, automate, and document Illustrator integrations, including CEP panels, native plug-ins, operating-system scripts, and MCP servers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Development-mode settings such as PlayerDebugMode can remain enabled beyond trusted local testing.

Mitigation: Limit development mode to trusted local testing, remove PlayerDebugMode afterward, and distribute signed extensions.

Risk: Extensions, native plug-ins, and MCP servers downloaded or built later are outside the bundled guidance's security assessment.

Mitigation: Review those components separately before use.

## Reference(s):

- [CEP Extensions for Illustrator](artifact/references/cep-extensions.md)
- [C++ Plug-ins for Illustrator](artifact/references/cpp-plugins.md)
- [Automation, MCP Servers, and Computer Use](artifact/references/automation-and-mcp.md)
- [Publishing Documentation for Illustrator Tools](artifact/references/publishing-docs.md)
- [Adobe CEP Resources](https://github.com/Adobe-CEP/CEP-Resources)
- [Adobe CEP Getting Started Guides](https://github.com/Adobe-CEP/Getting-Started-guides)
- [Adobe Creative Cloud Extensibility Timeline](https://blog.developer.adobe.com/en/publish/2026/09/investing-in-the-future-of-creative-cloud-extensibility-uxp-comes-to-our-flagship-applications)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with code examples, tables, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Implementation and publishing guidance for Illustrator integration workflows.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
