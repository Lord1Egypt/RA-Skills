## Description: <br>
Recommends AI coding models, SaaS products, and developer tools for programming agents, returning product summaries and direct links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iswangheng](https://clawhub.ai/user/iswangheng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to search for AI development tools, coding models, and SaaS products relevant to a user's stated need. Agents can return recommendation text, JSON responses, and product or affiliate links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recommendations may be influenced by affiliate incentives or promotional links. <br>
Mitigation: Treat returned links as promotional, disclose affiliate context to users, and verify product fit independently before purchase or adoption. <br>
Risk: Broad trigger terms may activate the skill for general tool or model recommendation requests. <br>
Mitigation: Use explicit tool calls where possible and narrow activation triggers before installing in shared or sensitive agent environments. <br>
Risk: The documented remote HTTP API uses a hard-coded non-HTTPS endpoint. <br>
Mitigation: Prefer local command or MCP stdio use, and avoid sending sensitive project, business, or user details to the remote endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iswangheng/ai-dev-tools) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style recommendation text and JSON tool responses containing product summaries, match details, and links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include promotional or affiliate links and product commission details when present in the product data.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
