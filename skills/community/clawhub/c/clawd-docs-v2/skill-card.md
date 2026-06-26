## Description: <br>
Smart ClawdBot documentation access with local search index, cached snippets, and on-demand fetch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aranej](https://clawhub.ai/user/aranej) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to answer ClawdBot documentation questions efficiently by checking local snippets and cached documentation before fetching live documentation pages when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cached snippets or local documentation pages may be stale or unexpected. <br>
Mitigation: Verify important setup, update, and troubleshooting guidance against the live ClawdBot documentation when freshness is uncertain. <br>
Risk: Local documentation data under ~/clawd/data/ can affect the guidance the skill returns. <br>
Mitigation: Keep the local documentation cache trusted and review cache contents before relying on them for operational changes. <br>


## Reference(s): <br>
- [ClawdBot Documentation](https://docs.clawd.bot/) <br>
- [ClawdBot Documentation Index](https://docs.clawd.bot/llms.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/aranej/clawd-docs-v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prioritizes cached snippets and local documentation indexes before live documentation fetches.] <br>

## Skill Version(s): <br>
2.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
