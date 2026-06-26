## Description: <br>
Aky Public Opinion helps agents draft Chinese public opinion and sentiment analysis reports with structured risk assessment, communication data analysis, and actionable recommendations for government and enterprise contexts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangfromchu-ai](https://clawhub.ai/user/wangfromchu-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, communications staff, and institutional users can use this skill to prepare formal Chinese reports on social media and news events, including rapid assessments, special reports, research reports, retrospectives, monthly summaries, and sensitive event analyses. The skill is intended to organize supplied event details, gather current context when URLs or background are needed, and produce evidence-based Markdown reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to gather current web context and produce formal public opinion risk analysis, so weak or incomplete source data may lead to misleading conclusions. <br>
Mitigation: Require users to provide event basics, timelines, actors, and communication data, and review all cited facts and recommendations before use. <br>
Risk: Generated reports may influence institutional communication or response decisions. <br>
Mitigation: Have qualified reviewers check tone, factual grounding, legal citations, and operational recommendations before distribution. <br>
Risk: Use in an environment with active account credentials could affect the wrong project or account if external helper commands are run nearby. <br>
Mitigation: Follow the scanner guidance: install only in a trusted development environment and review commands and active GitHub, ClawHub, or Convex credentials before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangfromchu-ai/aky-public-opinion) <br>
- [Report type templates and formatting standards](artifact/references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown reports in Chinese with structured sections, citations, risk assessments, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report length and section structure vary by selected report type.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
