## Description:

B站视频弹幕舆情与节奏分析。输入B站视频链接，自动提取弹幕数据，通过大模型分析弹幕的舆情倾向、情感演变、节奏热度分布等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[unclecheng-li](https://clawhub.ai/user/unclecheng-li)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to fetch public Bilibili danmaku for a supplied video, summarize time-based comment activity, and prepare sentiment and rhythm analysis artifacts for LLM review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the user-supplied Bilibili video identifier to Bilibili APIs.

Mitigation: Use it only for video identifiers you are comfortable disclosing to Bilibili services.

Risk: Sampled public danmaku text is stored locally and may be included in generated prompts and reports.

Mitigation: Review generated artifacts before sharing them or submitting them to a model with tools or sensitive context.

Risk: Downloaded comments are untrusted user-generated content.

Mitigation: Run downstream LLM analysis without tools or privileged context when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unclecheng-li/skills/bilibili-danmaku-analyzer-v1)
- [Bilibili video information API](https://api.bilibili.com/x/web-interface/view?bvid={bvid})
- [Bilibili danmaku API](https://api.bilibili.com/x/v1/dm/list.so?oid={cid})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [JSON analysis data, plain-text LLM prompt, Markdown report, and command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local files for a supplied Bilibili BV identifier or video URL.]

## Skill Version(s):

1.0.0 (source: server release metadata and _skillhub_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
