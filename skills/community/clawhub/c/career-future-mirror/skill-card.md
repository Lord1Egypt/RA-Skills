## Description: <br>
Career Future Mirror collects career background information, generates three differentiated career path options with an HTML career report, role-plays a three-years-later future self, and produces an immersive HTML future letter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaniu001](https://clawhub.ai/user/shaniu001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to explore career uncertainty, compare three possible career paths, and receive Chinese-language career planning artifacts. Agents use it to gather career context, produce a styled career report, conduct a future-self dialogue, and generate a future letter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for sensitive career background, resume-like details, income goals, and future-self dialogue that may be saved locally. <br>
Mitigation: Before use, remove contact details, addresses, IDs, employer-confidential information, and anything the user does not want retained; review or delete output/data/conversation_log.json after generating the letter. <br>
Risk: Generated career paths, salary expectations, and future-self dialogue can influence personal career decisions without guaranteeing accuracy. <br>
Mitigation: Review generated plans against current market information and personal constraints before acting on them, and treat the output as planning support rather than authoritative advice. <br>


## Reference(s): <br>
- [Career survey data schema](artifact/reference/career_survey_data.json) <br>
- [Skill page](https://clawhub.ai/shaniu001/career-future-mirror) <br>
- [Tailwind CSS CDN](https://cdn.tailwindcss.com) <br>
- [Chart.js CDN](https://cdn.jsdelivr.net/npm/chart.js) <br>
- [Alpine.js CDN](https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, HTML files, JSON, Shell commands, Guidance] <br>
**Output Format:** [Chinese conversational text with generated HTML reports, JSON conversation logs, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates output/reports/career_report.html, output/reports/future_letter.html, and output/data/conversation_log.json when run as described.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
