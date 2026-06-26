## Description: <br>
Query Apple Developer Documentation, APIs, and WWDC videos (2014-2025). Search SwiftUI, UIKit, Objective-C, Swift frameworks and watch sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheSethRose](https://clawhub.ai/user/TheSethRose) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to search Apple Developer Documentation, inspect API relationships and platform compatibility, browse Apple technology guides and samples, and look up WWDC sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation command can fetch arbitrary web URLs if an agent passes a full URL. <br>
Mitigation: Use Apple Developer documentation paths or trusted Apple Developer URLs, and review agent-proposed full URLs before execution. <br>
Risk: The skill makes outbound network requests during documentation and WWDC lookups. <br>
Mitigation: Run it only in environments where outbound access to the required documentation sources is acceptable. <br>


## Reference(s): <br>
- [Apple Developer Documentation](https://developer.apple.com/documentation/) <br>
- [Apple Developer](https://developer.apple.com/) <br>
- [apple-docs-mcp MCP Server](https://github.com/kimsungwhee/apple-docs-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or terminal text with command examples, documentation excerpts, URLs, and optional JSON-formatted data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Node.js runtime and makes outbound requests to Apple Developer documentation and WWDC data sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
