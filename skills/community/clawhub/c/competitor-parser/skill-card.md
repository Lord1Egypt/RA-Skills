## Description: <br>
Automates collection and analysis of robotics competitor data, then helps summarize competitors, pricing, ratings, locations, and report files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larthe](https://clawhub.ai/user/larthe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business analysts, operators, and developers use this skill to run a competitor-scraping workflow and ask an agent for ranked competitor summaries, pricing comparisons, location analysis, and report delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow includes external sharing to a hardcoded Telegram target. <br>
Mitigation: Replace or remove the Telegram target before sending reports, and review CSV output for confidential notes or business intelligence. <br>
Risk: The setup guidance includes privileged system package installation. <br>
Mitigation: Run any sudo apt-get dependency installation manually only in an environment where those system changes are acceptable. <br>
Risk: The skill references a local competitors_scraper.py file that is not included in the artifact evidence. <br>
Mitigation: Verify that competitors_scraper.py is present and trusted in the workspace before executing the workflow. <br>


## Reference(s): <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/larthe/competitor-parser) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and references to JSON and CSV report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected report artifacts are competitors_data.json and competitors_data.csv when the referenced scraper runs successfully.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
