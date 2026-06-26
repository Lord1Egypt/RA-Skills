## Description: <br>
Fetch and parse news highlights from CCTV News Broadcast (Xinwen Lianbo) for a given date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuhangch](https://clawhub.ai/user/yuhangch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to retrieve CCTV News Broadcast highlights for a requested date and summarize the fetched items for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to CCTV news sites when invoked. <br>
Mitigation: Use it only in environments where those outbound requests are allowed, and review network access expectations before installation. <br>
Risk: Fetched pages can be unavailable or have changed markup, which may produce empty or incomplete summaries. <br>
Mitigation: Check the requested date and source pages when results are empty, unexpectedly sparse, or used for important reporting. <br>
Risk: The skill requires a JavaScript runtime and the node-html-parser dependency. <br>
Mitigation: Install dependencies from the packaged lockfile and run the crawler in a constrained agent environment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/yuhangch/cctv-news-fetcher) <br>
- [CCTV News Broadcast daily pages](https://tv.cctv.com/lm/xwlb/day/) <br>
- [CCTV News Broadcast archive pages](https://cctv.cntv.cn/lm/xinwenlianbo/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [Markdown summary derived from crawler JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a date-based news crawler and summarizes returned title/content records.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
