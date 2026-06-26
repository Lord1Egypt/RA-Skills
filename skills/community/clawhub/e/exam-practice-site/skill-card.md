## Description: <br>
Generates a data-driven static exam practice website with daily question selection, answer checking, mistake review, weekly reporting, and question-bank management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzjmay123](https://clawhub.ai/user/zzjmay123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators, developers, and exam-prep teams use this skill to build a static single-page practice site for standardized exams. It guides them through creating a JSON question bank, customizing the HTML template, running the daily question update script, and deploying the resulting site. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Question-bank content is rendered from local JSON into the practice site and may contain inaccurate or inappropriate material if not reviewed. <br>
Mitigation: Review and validate all question, answer, and explanation content before publishing or relying on the generated site. <br>
Risk: The daily update script writes today.json and used_ids.json in the project data directory. <br>
Mitigation: Run the script only in the intended project folder and review the generated data files before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zzjmay123/exam-practice-site) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON, HTML, Python, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for a static website and local question-bank files; users supply and review exam content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
