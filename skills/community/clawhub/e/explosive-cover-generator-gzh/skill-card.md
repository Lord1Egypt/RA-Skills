## Description: <br>
公众号爆款封面AI设计工具。基于全网每日收录的10w+文章数据，获取同赛道爆款封面视觉元素，通过AI分析总结高转化视觉规律，生成贴合文章内容、符合平台流量审美的封面设计方案。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
WeChat Official Account creators, content operators, MCN teams, new media teams, and designers use this skill to analyze recent high-performing cover patterns by keyword, produce a visual HTML report, and generate three cover design proposals with image-generation prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided cover keywords and a REDFOX_API_KEY to RedFoxHub. <br>
Mitigation: Use it only when sharing those keywords with redfox.hk is acceptable, keep REDFOX_API_KEY out of prompts, code, logs, and generated files, and rotate or revoke the key if exposure is suspected. <br>
Risk: Debug output and generated JSON or HTML reports may contain private campaign planning terms, article links, and API response details. <br>
Mitigation: Keep debug mode off except during troubleshooting and delete generated reports when they contain sensitive planning data. <br>
Risk: Cover proposals depend on third-party trend data availability and may be sparse or unavailable for niche keywords. <br>
Mitigation: Tell users when data is insufficient and broaden or change keywords instead of inventing trend evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/explosive-cover-generator-gzh) <br>
- [Publisher profile](https://clawhub.ai/user/yuanyi-github) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [WeChat trend data format](references/gzh_trend_data_format.md) <br>
- [Cover analysis report template](references/report_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON trend data, shell commands, generated HTML report files, image-generation prompts, and optional 2.35:1 cover images after user selection] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY and uses recent WeChat cover data from the RedFoxHub API; generated HTML reports may contain private planning keywords and third-party article links.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
