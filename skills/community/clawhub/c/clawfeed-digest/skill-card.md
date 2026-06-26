## Description: <br>
Fetches ClawFeed AI news digests and saves them as Markdown files in a configured Obsidian or local output directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adminlove520](https://clawhub.ai/user/adminlove520) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw or Obsidian users use this skill to collect ClawFeed 4h, daily, or weekly AI news digests and store them as notes in a controlled output folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package promotes broad Obsidian and OpenClaw syncing, third-party plugin or binary installation, background startup, and note deletion workflows without enough safeguards. <br>
Mitigation: Run the digest fetcher against a narrow dedicated output folder, keep backups, avoid whole-vault bidirectional sync or deletion commands unless explicitly intended, and verify any third-party Obsidian plugin or sync-service binary before enabling it. <br>


## Reference(s): <br>
- [ClawFeed](https://clawfeed.kevinhe.io/) <br>
- [Fast Note Sync Service](https://github.com/haierkeys/fast-note-sync-service) <br>
- [Obsidian Sync Skill](https://clawhub.ai/AndyBold/obsidian-sync) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files with command-line and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports 4h, daily, and weekly digest types with limit, offset, and output-directory options.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
