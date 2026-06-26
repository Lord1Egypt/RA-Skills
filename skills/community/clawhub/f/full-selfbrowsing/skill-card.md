## Description: <br>
FSB drives the user's Chrome via the FSB extension and an MCP bridge for live web tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lakshmanturlapati](https://clawhub.ai/user/lakshmanturlapati) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill when a task needs a real browser session for clicking, typing, multi-tab flows, logged-in reads, vault-backed credential entry, or JavaScript-rendered page state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a real logged-in Chrome profile with access to cookies, saved credentials, and payment context. <br>
Mitigation: Install only when browser control is intended, prefer a separate Chrome profile, and keep vault entries minimal. <br>
Risk: Browser automation can perform purchases, account changes, deletions, permission grants, messages, or public posts. <br>
Mitigation: Require explicit user confirmation before the final submission for these sensitive actions. <br>
Risk: Using an unpinned MCP server package can change the browser-control bridge version during later installs. <br>
Mitigation: Pin fsb-mcp-server to a reviewed version when review-before-upgrade is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lakshmanturlapati/full-selfbrowsing) <br>
- [FSB homepage](https://full-selfbrowsing.com) <br>
- [FSB MCP server package](https://www.npmjs.com/package/fsb-mcp-server) <br>
- [Chrome Web Store listing](https://chromewebstore.google.com/detail/badgafnfchcihdfnjneklogedcdkmjfk) <br>
- [Visual session lifecycle](references/visual-session-lifecycle.md) <br>
- [Tool decision tree](references/tool-decision-tree.md) <br>
- [Multi-agent contract](references/multi-agent-contract.md) <br>
- [Vault boundary](references/vault-boundary.md) <br>
- [Restricted tab recovery](references/restricted-tab-recovery.md) <br>
- [Default to FSB](references/default-to-fsb.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to call browser-control MCP tools and run local diagnostic or installer commands.] <br>

## Skill Version(s): <br>
0.9.62 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
