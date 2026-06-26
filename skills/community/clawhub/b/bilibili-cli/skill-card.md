## Description: <br>
CLI skill for Bilibili with token-efficient YAML output for AI agents to browse videos, users, search, trending content, dynamics, favorites, and interactions from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackwener](https://clawhub.ai/user/jackwener) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and AI agents use this skill to inspect Bilibili videos, users, search results, feeds, favorites, comments, subtitles, and account state from a terminal. Authenticated users can also perform account interactions such as likes, coins, triple actions, dynamic posts, deletes, and unfollows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically uses local Bilibili browser session cookies and can store credentials locally. <br>
Mitigation: Install only when local browser-session access is acceptable, avoid sharing raw credential values, and run `bili logout` to remove saved credentials. <br>
Risk: Authenticated commands can perform real account actions, including posts, deletes, likes, coins, triple actions, unfollows, and file-to-post operations. <br>
Mitigation: Use read-only workflows by default and require explicit user approval before any write or account-changing command. <br>
Risk: Authenticated read commands may expose account-specific data such as favorites, following, watch-later, history, feeds, or posted dynamics. <br>
Mitigation: Check authentication state before use and limit collection with narrow commands, pagination, and result caps. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jackwener/bilibili-cli) <br>
- [Structured Output Schema](SCHEMA.md) <br>
- [PyPI Package](https://pypi.org/project/bilibili-cli/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, YAML, JSON, Text, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI commands emit YAML, JSON, plain text, and optional audio segment files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Machine-readable command output uses a shared ok/schema_version/data/error envelope; YAML is recommended for token-efficient agent use.] <br>

## Skill Version(s): <br>
0.6.0 (source: ClawHub release metadata and pyproject.toml; SKILL.md frontmatter reports 1.0.0 and CHANGELOG top entry reports 0.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
