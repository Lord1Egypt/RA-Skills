## Description: <br>
Monitor public OpenClaw ecosystem sources with source-quality checks, metadata-only collection, and trust-first reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marsloting](https://clawhub.ai/user/marsloting) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to monitor public OpenClaw ecosystem metadata, check source freshness, and produce source-linked local reports for manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthenticated public requests can encounter rate limits, access denials, robots changes, or platform warnings. <br>
Mitigation: Use official APIs where available, keep collection low-frequency, and pause affected sources on 403, 429, robots disallow, DMCA, abuse, or platform warning signals. <br>
Risk: Reports could accidentally mirror source content or expose unnecessary data. <br>
Mitigation: Store metadata, hashes, timestamps, short summaries, and canonical source URLs only; avoid full issue bodies, README bodies, docs pages, package tarballs, cookies, secrets, and payment data. <br>
Risk: Candidate contribution signals could lead to premature public action. <br>
Mitigation: Treat candidate lists as manual-review inputs and require human review before any public contribution or posting. <br>


## Reference(s): <br>
- [OpenClaw Ecosystem Monitor on ClawHub](https://clawhub.ai/marsloting/claw-ecosystem-monitor) <br>
- [GitHub REST API documentation](https://docs.github.com/en/rest) <br>
- [OpenClaw documentation](https://docs.openclaw.ai/) <br>
- [ClawHub public site](https://clawhub.ai/) <br>
- [npm registry search endpoint](https://registry.npmjs.org/-/v1/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Local JSON snapshots and Markdown reports, with source links and warning summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local files under dated data and reports directories; uses public metadata only.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
