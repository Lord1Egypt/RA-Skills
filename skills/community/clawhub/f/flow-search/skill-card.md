## Description:

Deep web research using Claude's native search tool for comprehensive research, market analysis, competitor intelligence, and cases where standard search is not enough.

This skill is ready for commercial/non-commercial use.

## Publisher:

[windseeker1111](https://clawhub.ai/user/windseeker1111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use FlowSearch to run Claude CLI-backed web research for market analysis, competitor intelligence, recent-news synthesis, and multi-source research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs the local Claude CLI with relaxed permission checks for non-root users.

Mitigation: Review search.ts before installation and run it only in an environment where this execution posture is acceptable.

Risk: The spawned Claude process inherits the user's shell environment, including CLAUDE_CODE_OAUTH_TOKEN and any other exported variables.

Mitigation: Run the skill in a clean environment that contains only the required Claude token and non-sensitive variables.

Risk: The security evidence marks the release as suspicious because of disabled permission checks and full environment inheritance.

Mitigation: Pin dependencies, keep the reviewed artifact hash for the installed version, and re-review before upgrading.

## Reference(s):

- [FlowSearch ClawHub skill page](https://clawhub.ai/windseeker1111/skills/flow-search)
- [Claude Code CLI](https://claude.ai/code)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown research answers or structured reports with cited source links; TypeScript API calls return SearchResult objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quick searches time out after 2 minutes; deep research runs up to 3 minutes.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
