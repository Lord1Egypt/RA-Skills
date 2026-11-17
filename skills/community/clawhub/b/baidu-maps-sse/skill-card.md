## Description:

Auto-generated skill for baidu-maps-sse tools via OneKey Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to access Baidu Maps geocoding, reverse geocoding, place search, place details, distance matrix, elevation, and directions tools through OneKey Gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends unpinned npm and Python package installs, including npx execution paths.

Mitigation: Install in an isolated environment, pin package versions, and avoid latest-resolution npx workflows before operational use.

Risk: Scripts fall back to a shared demo OneKey Gateway access key when DEEPNLP_ONEKEY_ROUTER_ACCESS is unset.

Mitigation: Set an organization-controlled DEEPNLP_ONEKEY_ROUTER_ACCESS key and verify it is present before running gateway calls.

Risk: Map requests may include sensitive home, work, travel, or location history data sent through OneKey Gateway and the downstream map provider.

Mitigation: Avoid submitting sensitive locations unless the user and organization are comfortable with that data path.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ai-hub-admin/skills/baidu-maps-sse)
- [OneKey Gateway Keys](https://www.deepnlp.org/workspace/keys)
- [OneKey MCP Router Doc](https://www.deepnlp.org/doc/onekey_mcp_router)
- [OneKey Gateway Doc](https://deepnlp.org/doc/onekey_agent_router)
- [AI Agent Marketplace](https://www.deepnlp.org/store/ai-agent)
- [Skills Marketplace](https://www.deepnlp.org/store/skills)
- [AI Agent A2Z Deployment](https://www.deepnlp.org/workspace/deploy)
- [GitHub AI Agent Marketplace](https://github.com/aiagenta2z/ai-agent-marketplace)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [JSON responses from gateway calls, plus Markdown usage guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a OneKey Gateway access key; scripts accept JSON via --data or --data-file and print formatted JSON.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
