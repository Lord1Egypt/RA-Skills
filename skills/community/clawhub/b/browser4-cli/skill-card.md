## Description:

Automates browser interactions for web testing, form filling, screenshots, and data extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[platonai](https://clawhub.ai/user/platonai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to drive Chrome or Chromium through browser4-cli for navigation, page interaction, testing, screenshots, and web data extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad browser automation that can access authenticated sessions, cookies, local storage, browser profiles, downloads, and captured page data.

Mitigation: Use a dedicated automation browser profile, avoid importing everyday browser profiles for sensitive accounts, and clean up auth-state files, profile copies, HARs, logs, and caches after use.

Risk: Some workflows can intentionally grant local shell execution through loop --shell.

Mitigation: Use loop --shell only when local command execution is explicitly intended and reviewed.

Risk: Remote browser or service endpoints can expose browser control surfaces if they are reachable without appropriate access controls.

Mitigation: Prefer localhost endpoints or authenticated tunnels for remote access.

Risk: The release references external installer scripts.

Mitigation: Review installer scripts before running them in a trusted environment.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/platonai/Browser4/tree/main/skills/browser4-cli)
- [ClawHub release page](https://clawhub.ai/platonai/skills/browser4-cli)
- [Quick reference](references/quickstart.md)
- [Snapshot and element refs](references/snapshot.md)
- [HTML snapshot extraction](references/htmlsnapshot.md)
- [Extraction decision trees](references/decision-trees.md)
- [X-SQL reference](references/x-sql.md)
- [Crawl command reference](references/crawl.md)
- [Swarm parallel scraping](references/swarm.md)
- [Loop command reference](references/loop.md)
- [Storage management](references/storage-state.md)
- [Browser state import](references/browser-state-import.md)
- [Network inspection, HAR, and routing](references/network.md)
- [Configuration](references/config.md)
- [Shell quoting guidance](references/shell-quoting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline browser4-cli shell commands and references to structured CLI outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may direct agents to produce snapshots, JSON envelopes, screenshots, HAR files, extracted text, or configuration changes through browser4-cli.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
