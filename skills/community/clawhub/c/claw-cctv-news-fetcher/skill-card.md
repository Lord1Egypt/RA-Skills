## Description: <br>
Fetch and parse news highlights from CCTV News Broadcast (Xinwen Lianbo) for a given date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamwang-wh](https://clawhub.ai/user/williamwang-wh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch CCTV News Broadcast items for a requested date and summarize the returned highlights. It is useful for date-specific news retrieval from the CCTV/CNTV pages the bundled crawler targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled crawler makes outbound requests to CCTV/CNTV news pages and sends a hardcoded cookie header. <br>
Mitigation: Install only in environments where those outbound requests are acceptable, and review or constrain network access before deployment. <br>
Risk: Unexpected date values may cause failed fetches or unnecessary requests. <br>
Mitigation: Validate user-provided dates as YYYYMMDD, or resolve relative dates such as today and yesterday before running the crawler. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/williamwang-wh/claw-cctv-news-fetcher) <br>
- [CCTV News Broadcast day archive](https://tv.cctv.com/lm/xwlb/) <br>
- [CNTV Xinwen Lianbo archive](https://cctv.cntv.cn/lm/xinwenlianbo/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain-text summary based on JSON crawler results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The crawler prints progress messages and JSON news items for the requested YYYYMMDD date.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
