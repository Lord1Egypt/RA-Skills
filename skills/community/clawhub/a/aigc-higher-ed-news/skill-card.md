## Description: <br>
高校AIGC日报每日聚合高校 AIGC 行业资讯、AI 微专业动态、高校招标需求和高校 AI 政策，并输出结构化中文简报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgugeng](https://clawhub.ai/user/lgugeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, education-market analysts, and higher-education teams use this skill to generate a daily Chinese-language digest of AIGC news, AI micro-major updates, relevant procurement activity, and AI policy signals for universities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Daily public-web lookups may retrieve low-quality, stale, or promotional source material. <br>
Mitigation: Review generated digest entries and keep the skill's source filtering rules focused on authoritative sources before using the digest for decisions. <br>
Risk: Saved digest archives may expose collected links, summaries, or institution-specific monitoring interests to users with filesystem access. <br>
Mitigation: Store archives only in an approved location and apply normal workspace access controls and retention practices. <br>
Risk: Optional knowledge-base sync may make generated digests visible beyond the local agent session. <br>
Mitigation: Confirm the destination knowledge base, reader permissions, and whether sync should be enabled before deployment. <br>
Risk: The daily schedule may create recurring network activity. <br>
Mitigation: Confirm that scheduled execution is expected and disable or adjust the schedule where automated daily searches are not appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lgugeng/aigc-higher-ed-news) <br>
- [Sample generated digest](digests/2026-05-09.md) <br>
- [Ministry of Education work updates](http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/) <br>
- [机器之心](https://www.jiqizhixin.com/) <br>
- [智东西](https://www.zhidx.com/) <br>
- [雷锋网 AI 频道](https://www.leiphone.com/category/ai) <br>
- [InfoQ AI topic](https://www.infoq.cn/topic/AI) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Structured Chinese Markdown digest with categorized items, summaries, source links, and a trend observation section.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save daily archive files under skills/aigc-higher-ed-news/digests/YYYY-MM-DD.md and optionally sync to an IMA knowledge base when permission exists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
