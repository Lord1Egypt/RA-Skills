## Description: <br>
CineScope XHS evaluates movie reception by collecting multi-source evidence, applying six-dimensional analysis, and producing dynamically weighted ratings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seeu1688](https://clawhub.ai/user/seeu1688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer movie review, rating, and recommendation questions with source-backed platform score snapshots, six-dimensional analysis, and spoiler-aware guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad movie-review triggers may send movie-related queries to external search providers sooner than a user expects. <br>
Mitigation: Avoid including private personal details in movie questions, use dedicated Tavily or Bocha API keys, and confirm search use in sensitive contexts. <br>
Risk: Generated movie ratings can be misleading when platform data is sparse, very recent, or affected by review manipulation. <br>
Mitigation: Preserve evidence levels, sample-size warnings, and date cutoffs, and recheck sources before relying on a recommendation. <br>
Risk: HTML and JavaScript chart output may be inappropriate in restricted rendering environments. <br>
Mitigation: Prefer Markdown or ASCII chart output when HTML or JavaScript rendering is not desired. <br>


## Reference(s): <br>
- [CineScope XHS ClawHub page](https://clawhub.ai/seeu1688/cinescope-xhs) <br>
- [Tavily](https://tavily.com) <br>
- [Bocha Open Platform](https://open.bochaai.com/) <br>
- [Bocha Web Search API](https://api.bocha.cn/v1/web-search) <br>
- [Chart.js CDN](https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Structured Markdown reports with optional Chart.js HTML, ASCII, or Markdown chart output and inline shell commands for API configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAVILY_API_KEY for primary search and can use BOCHA_API_KEY as a fallback; reports include evidence levels, score snapshots, and spoiler-aware limitations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
