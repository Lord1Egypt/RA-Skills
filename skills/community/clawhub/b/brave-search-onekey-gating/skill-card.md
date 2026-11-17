## Description:

Auto-generated skill for brave-search tools via OneKey Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Brave web search and local place search through the OneKey Gateway. It supports general web queries, recent information gathering, and local business lookup with JSON payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent through the OneKey Gateway.

Mitigation: Install only when that routing is acceptable for the intended data, and avoid sending sensitive queries unless the gateway is approved for them.

Risk: The scripts automatically fall back to a shared demo gateway key when DEEPNLP_ONEKEY_ROUTER_ACCESS is unset.

Mitigation: Set a dedicated DEEPNLP_ONEKEY_ROUTER_ACCESS key before use and avoid relying on the shared demo key.

Risk: The release relies on unpinned npm, pip, or npx package execution.

Mitigation: Pin and verify dependency versions before installation or execution, and run the skill in a restricted environment where possible.

## Reference(s):

- [OneKey MCP Router Doc](https://www.deepnlp.org/doc/onekey_mcp_router)
- [OneKey Gateway Doc](https://deepnlp.org/doc/onekey_agent_router)
- [AI Agent Marketplace](https://www.deepnlp.org/store/ai-agent)
- [Skills Marketplace](https://www.deepnlp.org/store/skills)
- [GitHub AI Agent Marketplace](https://github.com/aiagenta2z/ai-agent-marketplace)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [JSON search results with Markdown usage guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Web search supports count and offset controls; local search supports count and may fall back to web search when local results are unavailable.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
