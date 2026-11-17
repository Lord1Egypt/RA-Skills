## Description:

Calculate legal working days in China according to official government holiday schedules, excluding weekends and public holidays while including makeup workdays for date ranges, months, quarters, and full years.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manucode2000-max](https://clawhub.ai/user/manucode2000-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to calculate China legal workday counts for planning, scheduling, reporting, and date-range analysis using bundled State Council holiday schedule data.

### Deployment Geography for Use:

China mainland

## Known Risks and Mitigations:

Risk: Unsupported or future-year calendar results may be presented as official.

Mitigation: Verify the bundled YAML calendar data against State Council notices before using results for compliance, payroll, operations, or customer-facing commitments.

Risk: Missing calendar years can cause the skill to generate and save example holiday schedules.

Mitigation: Use only years with reviewed source YAML files, and reject or manually validate generated schedule files before relying on their outputs.

Risk: Pricing information differs between publish notes and subscription metadata.

Mitigation: Confirm ClawHub billing terms from the product page or publisher before installation or renewal.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/manucode2000-max/skills/chinese-workdays)
- [Publisher profile](https://clawhub.ai/user/manucode2000-max)
- [State Council Gazette](https://www.gov.cn/gongbao/)
- [2007 State Council holiday notice](https://www.gov.cn/zhengce/content/2008-03/28/content_1761.htm)
- [2008 State Council holiday notice](https://www.gov.cn/zhengce/content/2008-03/28/content_1645.htm)
- [2009 State Council holiday notice](https://www.gov.cn/gongbao/content/2008/content_1175823.htm)
- [2010 State Council holiday notice](https://www.gov.cn/gongbao/content/2009/content_1487011.htm)
- [2011 State Council holiday notice](https://www.gov.cn/gongbao/content/2010/content_1765282.htm)
- [2012 State Council holiday notice](https://www.gov.cn/gongbao/content/2011/content_2020918.htm)
- [2013 State Council holiday notice](https://www.gov.cn/gongbao/content/2012/content_2292057.htm)
- [2014 State Council holiday notice](https://www.gov.cn/gongbao/content/2014/content_2561299.htm)
- [2015 State Council holiday notice](https://www.gov.cn/gongbao/content/2015/content_2799019.htm)
- [2016 State Council holiday notice](https://www.gov.cn/gongbao/content/2016/content_2979719.htm)
- [2017 State Council holiday notice](https://www.gov.cn/gongbao/content/2016/content_5148793.htm)
- [2018 State Council holiday notice](https://www.gov.cn/gongbao/content/2017/content_5248221.htm)
- [2019 State Council holiday notice](https://www.gov.cn/gongbao/content/2018/content_5350046.htm)
- [2020 State Council holiday notice](https://www.gov.cn/gongbao/content/2019/content_5459138.htm)
- [2021 State Council holiday notice](https://www.gov.cn/gongbao/content/2020/content_5567750.htm)
- [2022 State Council holiday notice](https://www.gov.cn/gongbao/content/2021/content_5651728.htm)
- [2023 State Council holiday notice](https://www.gov.cn/gongbao/content/2023/content_5736714.htm)
- [2024 State Council holiday notice](https://www.gov.cn/gongbao/2023/issue_10806/202311/content_6913823.html)
- [2025 State Council holiday notice](https://www.gov.cn/gongbao/2024/issue_11726/202411/content_6989767.html)
- [2026 State Council holiday notice](https://www.gov.cn/gongbao/2025/issue_12406/202511/content_7048922.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python and shell examples; CLI output is plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses bundled YAML holiday calendar files for 2007-2027; dates outside bundled data may trigger generated example schedules.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
