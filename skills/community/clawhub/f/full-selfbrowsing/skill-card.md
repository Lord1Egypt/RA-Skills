## Description:

FSB drives the user's Chrome via the FSB extension and an MCP bridge for live web tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lakshmanturlapati](https://clawhub.ai/user/lakshmanturlapati)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use FSB Skill to let an agent inspect and operate the user's real Chrome session for live web tasks such as clicking, typing, multi-tab flows, auth-gated reads, and dynamic page state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unpinned npm/MCP setup can resolve to changed fsb-mcp-server code after installation.

Mitigation: Pin an exact reviewed fsb-mcp-server version in MCP configs and scripts before using the skill in sensitive environments.

Risk: The skill can drive a logged-in Chrome session where browser actions may affect accounts, payments, or public content.

Mitigation: Supervise browser activity and require explicit user confirmation before purchases, payments, account changes, public posts, or other state-changing actions.

Risk: Trust in the local Chrome extension and MCP package is required for safe operation.

Mitigation: Install only when both components are trusted, keep the extension visible during action sequences, and run the included doctor check when behavior is unexpected.

## Reference(s):

- [FSB homepage](https://full-selfbrowsing.com)
- [ClawHub skill page](https://clawhub.ai/lakshmanturlapati/skills/full-selfbrowsing)
- [Chrome Web Store listing](https://chromewebstore.google.com/detail/badgafnfchcihdfnjneklogedcdkmjfk)
- [fsb-mcp-server npm package](https://www.npmjs.com/package/fsb-mcp-server)
- [Usage guide](USAGE.md)
- [Visual session lifecycle](references/visual-session-lifecycle.md)
- [Tool decision tree](references/tool-decision-tree.md)
- [Multi-agent contract](references/multi-agent-contract.md)
- [Vault boundary](references/vault-boundary.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser-action guidance and local MCP configuration; requires the FSB Chrome extension and fsb-mcp-server.]

## Skill Version(s):

0.9.90 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
