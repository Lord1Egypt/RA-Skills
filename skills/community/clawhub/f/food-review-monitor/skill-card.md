## Description: <br>
Monitors food-delivery reviews from Meituan, Ele.me/Taobao Shangou, and JD to detect service anomalies, generate HTML reports, and surface alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Restaurant operators and support teams use this skill to import or retrieve food-delivery reviews, identify changes in taste, ratings, delivery, service, and negative-review volume, and produce reports for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional platform API keys and review history may be stored in local plaintext files. <br>
Mitigation: Use CSV import when possible; if API keys are needed, restrict permissions on ~/.food_review_monitor/config.json and rotate or remove keys that are no longer required. <br>
Risk: Review data and generated reports can contain sensitive business information. <br>
Mitigation: Treat ~/.food_review_monitor/data and ~/.food_review_monitor/reports as sensitive local storage and avoid sharing generated reports outside approved channels. <br>
Risk: Generated HTML reports load ECharts from a public CDN. <br>
Mitigation: Use reports only where external CDN loading is acceptable, or replace the CDN reference with an approved local asset before distribution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bettermen/food-review-monitor) <br>
- [Publisher Profile](https://clawhub.ai/user/bettermen) <br>
- [Artifact README](README.md) <br>
- [Configured Python Package Index](https://pypi.tuna.tsinghua.edu.cn/simple/) <br>
- [ECharts Runtime Asset](https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, HTML files] <br>
**Output Format:** [Markdown guidance with shell commands, CLI text summaries, configuration JSON, and generated HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local review history and report files under ~/.food_review_monitor by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
