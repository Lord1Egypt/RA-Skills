## Description:

Fetches real-time Baidu hot-search rankings directly from top.baidu.com/board.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iph0n3](https://clawhub.ai/user/iph0n3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve and summarize current Baidu hot-search topics from the public Baidu board without relying on simulated data or a separate API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ClawHub security summary flags an unnecessary npm python3 dependency in package metadata.

Mitigation: Review the package before installation and prefer documenting Python 3 as a local prerequisite instead of installing a third-party npm dependency.

Risk: The skill depends on public Baidu page structure and network access, so results may fail or degrade if the page changes, the network is unavailable, or requests are rate-limited.

Mitigation: Use reasonable request intervals, keep timeouts in place, and review parser output before relying on retrieved trend data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/iph0n3/skills/baidu-hot-real)
- [Baidu Hot Search Board](https://top.baidu.com/board)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Text or markdown containing ranked Baidu hot-search entries, status messages, and command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can limit output to a requested top-N count or return up to 50 entries.]

## Skill Version(s):

1.3.0 (source: server release metadata, SKILL.md frontmatter, _meta.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
