## Description:

Fetches ClawFeed AI news digests for 4-hour, daily, or weekly intervals and saves them as Markdown files in a configured Obsidian directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adminlove520](https://clawhub.ai/user/adminlove520)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to collect ClawFeed AI news digests and write them into an Obsidian vault for ongoing review or knowledge-base workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring local writes can overwrite or clutter notes in the configured Obsidian output directory.

Mitigation: Use a dedicated output folder, back up the vault, and confirm the output path and overwrite behavior before enabling scheduled runs.

Risk: Optional sync plugins and executable services are third-party components outside the core digest fetcher.

Mitigation: Install optional BRAT, Obsidian plugin, or sync-service components only after independently verifying and trusting their upstream projects.

Risk: Unattended cron execution can repeatedly run file-writing behavior before configuration mistakes are noticed.

Mitigation: Run the fetch command manually first, then enable cron only after paths, dependencies, and generated files have been reviewed.

## Reference(s):

- [ClawFeed](https://clawfeed.kevinhe.io/)
- [Clawfeed Digest on ClawHub](https://clawhub.ai/adminlove520/skills/clawfeed-digest)
- [Fast Note Sync Service](https://github.com/haierkeys/fast-note-sync-service)
- [Obsidian Sync on ClawHub](https://clawhub.ai/AndyBold/obsidian-sync)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files plus concise command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes digest content to a local output directory selected by CLI arguments or the documented default Obsidian path.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
