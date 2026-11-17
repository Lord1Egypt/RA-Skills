## Description:

Helps an agent search, browse, and download anime torrents from miobt.com using the AniCatch CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isongxw](https://clawhub.ai/user/isongxw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent find seasonal anime listings, search anime torrent results, and run AniCatch commands to download selected items. Users should apply it only where torrent downloads are legal and allowed by their network policy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Torrent downloads may be illegal in some jurisdictions or disallowed by a user's network policy.

Mitigation: Use the skill only where torrent activity is legal and explicitly permitted by applicable network and organizational policy.

Risk: Torrent activity may expose the user's IP address through public BitTorrent infrastructure.

Mitigation: Review privacy and network exposure before downloading, and avoid use on networks where public peer-to-peer traffic is not approved.

Risk: The skill documents mutable third-party installation and execution commands such as curl-to-sh and unpinned uvx or pipx usage.

Mitigation: Verify the upstream tool and version before execution, and prefer pinned or reviewed installation paths where available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/isongxw/skills/anime-download-skill)
- [AniCatch CLI Repository](https://github.com/isongxw/anicatch)
- [AniCatch on PyPI](https://pypi.org/project/anicatch/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [AgentSkills.io Standard](https://agentskills.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are read from stdout; downloads may write torrent output to a user-selected directory.]

## Skill Version(s):

0.3.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
