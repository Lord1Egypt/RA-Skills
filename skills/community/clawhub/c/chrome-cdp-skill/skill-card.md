## Description:

Interact with a local Chrome-family browser session over CDP when the user explicitly asks to inspect, debug, or interact with a page they already have open.

This skill is ready for commercial/non-commercial use.

## Publisher:

[web3toolshub](https://clawhub.ai/user/web3toolshub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect, debug, screenshot, navigate, and interact with pages in a local Chrome-family browser session after the user enables remote debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect or control sensitive logged-in browser tabs.

Mitigation: Use it only on pages the user has approved for the task, avoid unrelated sensitive tabs, and stop the daemons when finished.

Risk: Commands such as eval, evalraw, nav, open, click, and type can execute JavaScript, navigate pages, and perform browser actions.

Mitigation: Review high-impact commands before execution and limit them to the specific user-requested page and action.

Risk: Screenshots, HTML, accessibility snapshots, and CDP responses may expose page contents.

Mitigation: Treat captured outputs as sensitive and persist or share them only when required for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/web3toolshub/skills/chrome-cdp-skill)
- [Publisher profile](https://clawhub.ai/user/web3toolshub)
- [Declared project homepage](https://github.com/web3toolshub/chrome-cdp-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, files, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, text snapshots, HTML excerpts, CDP responses, and screenshot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 22+ and a local Chrome-family browser with remote debugging enabled; screenshots capture the viewport only.]

## Skill Version(s):

1.0.6 (source: evidence release, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
