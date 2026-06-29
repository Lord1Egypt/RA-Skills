## Description: <br>
面向全国所有省份的通用高考志愿填报建议器：用省份快速学习协议现查现学任意省当年规则，出默认保守的冲稳保三档+可直接录入本省志愿系统的草表。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wujiaming88](https://clawhub.ai/user/wujiaming88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, families, and advising agents use this skill to plan Chinese gaokao college applications across provinces, using official admissions data, rank-based forecasting, conservative reach-match-safety tiers, and a draft table that can be checked against the provincial application system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process sensitive education-planning details such as score, rank, province, subject track, and preferences. <br>
Mitigation: Collect only the details needed for advising, avoid unnecessary retention, and let the user review the final plan before using it. <br>
Risk: Admissions recommendations can be wrong if school codes, major codes, province rules, or current-year plans are stale or mismatched. <br>
Mitigation: Verify every school, major, rank, source, and application-system code in the official provincial system before submission. <br>
Risk: The skill provides decision support, not a guarantee of admission. <br>
Mitigation: Present recommendations conservatively, label missing or single-source data, and make final choices user-reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wujiaming88/skills/gaokao-zhiyuan) <br>
- [province-onboarding-protocol.md](references/province-onboarding-protocol.md) <br>
- [methodology-rank-anchor.md](references/methodology-rank-anchor.md) <br>
- [cross-verification-protocol.md](references/cross-verification-protocol.md) <br>
- [data-source-registry.md](references/data-source-registry.md) <br>
- [output-template.md](references/output-template.md) <br>
- [system-entry-format.md](references/system-entry-format.md) <br>
- [湖北省招生数智综合平台](https://zspt.hubzs.com.cn) <br>
- [湖北招生考试网](https://www.hbksw.cn) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Markdown tables and concise advisory text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include school and major recommendations, source-backed rank data, risk labels, and province-specific application draft tables for user review.] <br>

## Skill Version(s): <br>
1.3.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
