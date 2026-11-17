## Description:

BT Download helps an agent manage BitTorrent, magnet, and direct URL downloads through aria2 RPC, including download monitoring and seeding controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n0nsense11](https://clawhub.ai/user/n0nsense11)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check or install aria2, start an aria2 RPC download service, add BitTorrent or direct URL downloads, inspect status, and stop seeding when target ratios are reached.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start a persistent aria2 RPC service without authentication.

Mitigation: Review before installation and prefer a version that binds RPC to localhost, uses an RPC secret, and exposes explicit controls to stop the background service.

Risk: The skill can install aria2 through automatic sudo package-manager commands.

Mitigation: Install aria2 manually through an approved system package process before enabling the skill, or use a revised version without automatic sudo installation.

Risk: The skill includes unsafe shell execution paths for service startup and helper commands.

Mitigation: Prefer a revised version that starts aria2 without shell interpolation and review command arguments before execution.

Risk: The skill can read local .torrent files and enable DHT or seeding behavior.

Mitigation: Use only trusted torrent files and configure seeding, DHT, download directory, and stop conditions explicitly.

## Reference(s):

- [BT Download ClawHub page](https://clawhub.ai/n0nsense11/skills/bt-download)
- [aria2 project homepage](https://aria2.github.io)
- [ngosang trackers list](https://raw.githubusercontent.com/ngosang/ngosang-trackerslist/master/trackers_best.txt)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON tool results and human-readable status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires aria2c and may read local .torrent files or control a local aria2 RPC service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
