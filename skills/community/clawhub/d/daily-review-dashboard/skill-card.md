## Description: <br>
Manage Steven's daily subjective review dashboard by reading, updating, and displaying daily reviews, issue tracking, sentiment tags, and next-day plans in review_egg/. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j97feng-beep](https://clawhub.ai/user/j97feng-beep) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to maintain a local daily review dashboard for personal trading reflections, including raw review text, issue tags, sentiment tags, holdings snapshots, summaries, and next-day plans. It is intended for subjective review records and should not be mixed with objective trade ledger data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes personal review content and dashboard data under review_egg/, which may include private reflections, holdings, or trading notes. <br>
Mitigation: Keep the review_egg folder private, avoid storing secrets in review text, and review exact file changes before saving new daily reviews. <br>
Risk: The dashboard is a subjective review system and could be mistaken for an objective trading ledger. <br>
Mitigation: Keep review_egg content separate from trade/ records and use the skill only for personal reflection data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/j97feng-beep/daily-review-dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, CSV, HTML data updates, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Updates local review_egg files and may open the local dashboard in a browser.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
