## Description: <br>
Ai Capsule ranks daily AI news by personal relevance, scoring and ordering articles from configured sources while optionally using local X/Twitter session cookies for that source. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[webpudge](https://clawhub.ai/user/webpudge) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use Ai Capsule to produce personalized AI news digests or score pasted articles, URLs, and batches against their role, familiar areas, and reading purpose. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The daily run can read local Chrome x.com session cookies for the X/Twitter source and pass them to twitter-cli without a clear per-run opt-in. <br>
Mitigation: Install only if this cookie access is acceptable, review the X/Twitter source list first, and remove or disable that source if cookie-backed fetching is not desired. <br>
Risk: X/Twitter fetching may use process environment values and auto-detected local proxy settings while accessing x.com. <br>
Mitigation: Review local proxy behavior before enabling the X/Twitter source and run the skill in an environment where passing these values to the subprocess is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/webpudge/skills/ai-capsule) <br>
- [Project homepage declared by the skill](https://github.com/WebPudge/ai-capsule) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and article cards with structured score_json blocks for scored items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local user profile, source configuration, deduplication state, and selected output language to rank articles; daily mode can write report, history, and deduplication files to the configured data directory.] <br>

## Skill Version(s): <br>
1.0.5 (source: evidence release, SKILL.md frontmatter, CHANGELOG released 2026-06-25) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
