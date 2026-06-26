## Description: <br>
Fetch and parse news highlights from CCTV News Broadcast (Xinwen Lianbo) for a given date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve dated CCTV News Broadcast highlights and have an agent summarize the returned titles and article content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The crawler makes outbound requests to CCTV/CNTV pages and fetched article links. <br>
Mitigation: Install only when this network behavior is expected, and enforce a CCTV/CNTV domain allowlist for fetched article links. <br>
Risk: Date handling may accept malformed values if an agent passes unchecked input to the script. <br>
Mitigation: Validate requested dates strictly as YYYYMMDD before execution. <br>
Risk: The crawler sends a fixed cookie header when requesting article pages. <br>
Mitigation: Review and document the fixed cookie header before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/litiao1224/cctv-news-fetcher-conflict) <br>
- [Publisher profile](https://clawhub.ai/user/litiao1224) <br>
- [CCTV Xinwen Lianbo archive](https://cctv.cntv.cn/lm/xinwenlianbo/) <br>
- [CCTV recent Xinwen Lianbo archive](https://tv.cctv.com/lm/xwlb/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Guidance] <br>
**Output Format:** [JSON fetched by script and summarized as Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a YYYYMMDD date input; defaults to the current date when no date is provided by the script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
