## Description:

Query CPBL 中華職棒 scores, schedules, live games, standings, player stats, news, and Taiwan baseball history for Taiwan users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ichendong](https://clawhub.ai/user/ichendong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer CPBL questions about scores, schedules, standings, player statistics, advanced Statcast-style data, news, and Taiwan baseball history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags stealth browser automation for protected Taiwan Baseball Wiki pages.

Mitigation: Use the stealth wiki-fetching path only when authorized and when site-policy and operational risks are acceptable; prefer official CPBL sources for routine sports data.

Risk: The security evidence notes unpinned Scrapling/Patchright browser components.

Mitigation: Review dependency resolution before installation and run browser automation in an isolated environment.

Risk: Official CPBL data may lag, return partial results, or require brittle HTML parsing.

Mitigation: State data freshness and parser limitations in user-facing answers and verify important results against official CPBL pages when needed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ichendong/cpbl)
- [ClawHub skill page](https://clawhub.ai/ichendong/skills/cpbl)
- [CPBL API Endpoints](references/api-endpoints.md)
- [CPBL Skill Summary](references/summary.md)
- [CPBL Test Report](references/test-report.md)
- [CPBL official news](https://cpbl.com.tw/news)
- [Taiwan Baseball Wiki CPBL MVP page](https://twbsball.dils.tku.edu.tw/wiki/index.php?title=中華職棒年度最有價值球員)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON from Python CLI scripts, with Markdown guidance for agent responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and python3; some history lookups may require Scrapling/Patchright browser components]

## Skill Version(s):

2.0.0 (source: evidence.release.version and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
