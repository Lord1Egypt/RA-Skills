## Description:

WebDriver automation CLI for AI-driven browser control. Provides session management, tab control, element interaction, screenshots, batch execution, and an interactive REPL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yorelog](https://clawhub.ai/user/yorelog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use BrowseCTL to drive Chrome or Edge through WebDriver from an agent or terminal workflow, including session setup, navigation, DOM interaction, screenshots, tab management, batch execution, and an interactive REPL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation and release-pipeline trust affect the downloaded browser automation binary.

Mitigation: Install only when the publisher and release pipeline are trusted, and test in an isolated environment before using real accounts.

Risk: Browser sessions can copy cookies, extensions, localStorage, bookmarks, and other profile data into an automation profile.

Mitigation: Prefer an isolated browser profile or test account, and pass --no-copy-data for non-interactive session creation unless copying profile data is intentional.

Risk: Screenshots, REPL history, persisted sessions, copied cookies, and automation profiles can contain sensitive local data.

Mitigation: Treat generated files and profiles as sensitive, store them only as needed, and clean them up after use.

Risk: Batch files can automate browser actions across pages and tabs.

Mitigation: Review batch files before execution and avoid running untrusted batches against authenticated sessions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yorelog/skills/browserctl)
- [npm Package: @yorelog/browsectl](https://www.npmjs.com/package/@yorelog/browsectl)
- [BrowseCTL README](artifact/README.md)
- [Session and Driver Lifecycle](artifact/skills/session.md)
- [Batch Execution](artifact/skills/batch.md)
- [Interactive REPL](artifact/skills/repl.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local screenshots, persisted session files, REPL history, and browser automation profile data.]

## Skill Version(s):

0.1.1 (source: release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
