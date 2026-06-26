## Description: <br>
Conducts structured AI paper surveys using alphaXiv MCP tools by reading research interests, searching recent papers, classifying innovation tiers, running impact analysis, and producing a Markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haataa](https://clawhub.ai/user/haataa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and technical reviewers use this skill to survey recent AI papers, run literature-review style searches, assess paper impact, and synthesize ranked findings for a research topic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local research keyword files that match configured filename patterns. <br>
Mitigation: Run it only in a workspace where those research-topic files are intended for use. <br>
Risk: The workflow depends on a separate paper-impact-analyzer for impact assessment. <br>
Mitigation: Review and trust the installed paper-impact-analyzer before using this skill. <br>
Risk: The workflow writes a generated Markdown report to the working directory. <br>
Mitigation: Confirm the working directory and expected report destination before running the survey. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haataa/ai-paper-survey) <br>
- [Publisher profile](https://clawhub.ai/user/haataa) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown report with ranked paper recommendations, tiered tables, trend observations, and optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves a topic/date-stamped Markdown report in the working directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
