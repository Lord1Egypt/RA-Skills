## Description:

Install, update, and launch GameClaw terminal games. Use when a user asks which GameClaw games exist, wants to download or update a GameClaw game binary, needs the correct macOS/Linux/Windows asset, or hits a GitHub network failure while fetching game bundles. Look up the live game list from the latest GitHub Release and catalog/games.json; this skill does not contain that list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arcobalneo](https://clawhub.ai/user/arcobalneo)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to check the current GameClaw catalog and latest release, then choose the correct platform asset, install or update it while preserving saves, launch a game, or troubleshoot download failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Download troubleshooting may change system-wide hosts settings, while mirrored downloads and bundled checksums do not by themselves establish publisher authenticity.

Mitigation: Keep installation within the user's account; avoid the hosts workaround, preserve existing proxy settings, and verify checksums or signatures through a trusted publisher source before using a mirror. Do not dismiss operating-system warnings solely because a bundled checksum matches.

Risk: Downloaded game binaries and future remote release or catalog content were not audited with the skill text.

Mitigation: Review the selected release and its authenticity information before running a downloaded binary, and treat live catalog or release content as unverified until checked.

## Reference(s):

- [GameClaw repository](https://github.com/Arcobalneo/gameclaw)
- [Latest GameClaw release](https://github.com/Arcobalneo/gameclaw/releases/latest)
- [Live game catalog](https://raw.githubusercontent.com/Arcobalneo/gameclaw/main/catalog/games.json)
- [GameClaw on ClawHub](https://clawhub.ai/arcobalneo/skills/gameclaw)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Bash and PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Platform- and release-dependent; the game list and available assets are looked up live.]

## Skill Version(s):

2.3.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
