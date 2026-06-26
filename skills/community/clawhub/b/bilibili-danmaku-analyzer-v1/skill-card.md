## Description: <br>
Bilibili Danmaku Analyzer extracts public Bilibili video comments, summarizes comment timing and keyword sentiment, and produces analysis files for LLM-assisted review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unclecheng-li](https://clawhub.ai/user/unclecheng-li) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to collect public danmaku from a Bilibili video and prepare structured sentiment, rhythm, and topic-analysis materials for an LLM or local review workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves sampled public comments, video metadata, generated prompts, and reports locally, which may be sensitive depending on the video topic. <br>
Mitigation: Choose an intentional output directory, review generated files before sharing them, and delete outputs when the topic or comments are sensitive. <br>
Risk: The skill fetches data from public Bilibili APIs for user-supplied videos and may encounter access failures or rate limiting. <br>
Mitigation: Use valid Bilibili video identifiers, retry later after access failures, and avoid high-frequency repeated requests. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/unclecheng-li/bilibili-danmaku-analyzer-v1) <br>
- [Bilibili video page](https://www.bilibili.com/) <br>
- [Bilibili video information API](https://api.bilibili.com/x/web-interface/view?bvid={bvid}) <br>
- [Bilibili danmaku API](https://api.bilibili.com/x/v1/dm/list.so?oid={cid}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [JSON analysis data, plain-text LLM prompt, and Markdown report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves sampled comments, video metadata, generated prompts, and reports to the selected local output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _skillhub_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
