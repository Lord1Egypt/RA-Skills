## Description:

Fetch, analyze, and compare trending posts from Moltbook to inform your content strategy. Generates virality reports with real statistical benchmarks from 36k+ posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smarvr](https://clawhub.ai/user/smarvr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and content strategists use this skill to fetch Moltbook trending-post snapshots, analyze virality and author momentum, and generate markdown briefings for posting decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local shell and Python scripts and its security evidence reports that DELAY_MS can be abused to execute arbitrary local code when the fetch script is invoked.

Mitigation: Run it only in a trusted, disposable workspace; prevent untrusted automation from setting environment variables; keep SNAPSHOT_DIR pointed at an intended output folder; and validate DELAY_MS as a bounded integer before invoking the fetch workflow.

## Reference(s):

- [Moltbook](https://www.moltbook.com)
- [Moltbook API](https://www.moltbook.com/api/v1)
- [ClawHub Skill Page](https://clawhub.ai/smarvr/skills/analyze-moltbook-trending-posts)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, terminal output, JSON snapshots, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates timestamped snapshot files under data/snapshots/ and report files under reports/ when run in a writable skill directory.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
