## Description: <br>
Fetch, analyze, and compare trending posts from Moltbook to inform your content strategy. Generates virality reports with real statistical benchmarks from 36k+ posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smarvr](https://clawhub.ai/user/smarvr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content strategists, and agent operators use this skill to fetch public Moltbook trending data, analyze post velocity and engagement patterns, and generate posting guidance from current snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A custom DELAY_MS value may be evaluated by the fetch script before numeric validation. <br>
Mitigation: Run only with trusted environment variables, keep the default delay when possible, and review any custom DELAY_MS value before execution. <br>
Risk: The skill makes outbound network requests to Moltbook and writes local snapshot and report files. <br>
Mitigation: Use it in an environment where access to the Moltbook public API is allowed and the data/snapshots/ and reports/ directories are expected writable outputs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/smarvr/analyze-moltbook-trending-posts) <br>
- [Moltbook](https://www.moltbook.com) <br>
- [Moltbook public API](https://www.moltbook.com/api/v1) <br>
- [OpenClaw](https://github.com/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON snapshot files, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes timestamped snapshot JSON files under data/snapshots/ and markdown analysis or comparison reports under reports/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
