## Description: <br>
RumorChecker 统一报告标准。确保证据链可追溯、多元交叉验证可视化、误解来源可解释，培养用户辨别能力。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EvianEvans](https://clawhub.ai/user/EvianEvans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and fact-checking agents use this skill to produce Chinese-language information-checking reference reports with traceable evidence, cross-source verification, misunderstanding analysis, and reader-oriented discernment tips. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Readers may treat a generated information-checking report as an authoritative verdict. <br>
Mitigation: Keep the report framed as a reference, preserve the disclaimer that final judgment remains with the user, and use reference opinions rather than definitive verdict language. <br>
Risk: Evidence gathered upstream may be incomplete, outdated, or factually incorrect. <br>
Mitigation: Require complete source URLs, publication dates, source-type labels, credibility reasons, and cross-source verification before presenting the report. <br>
Risk: Users who do not read Chinese may misunderstand the generated report format or cautions. <br>
Mitigation: Use this skill only where Chinese-language output is acceptable, or have a fluent reviewer verify the report before relying on it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/EvianEvans/evidence-report) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Guidance] <br>
**Output Format:** [Chinese-language Markdown report template with JSON intermediate-report schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires traceable source URLs, source credibility ratings, cross-reference analysis, misunderstanding-source analysis, discernment tips, and participant attribution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
