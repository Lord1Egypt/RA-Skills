## Description: <br>
AI-Interview-Coach helps users prepare for interviews by generating targeted questions, mock interview flows, sprint plans, readiness scores, progress summaries, radar charts, and answer rewrites across junior, mid, and senior difficulty levels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hogozhang](https://clawhub.ai/user/hogozhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users preparing for job interviews use this skill to generate role-specific practice material, run mock interviews, assess readiness, track progress, and improve interview answers. It supports resume-based and job-role-based preparation for technical, product, and behavioral interviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process resume details or job-history information provided by the user. <br>
Mitigation: Provide only the resume details needed for interview preparation and avoid unnecessary sensitive personal information. <br>
Risk: The skill can save local interview practice history at ~/.ai-interview-coach/history.json. <br>
Mitigation: Review, manage, or delete the local history file when practice records should not be retained. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hogozhang/ai-interview-coach) <br>
- [README](artifact/README.md) <br>
- [Examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown interview-preparation content with structured questions, answer spaces, reference answers, scoring summaries, plans, and rewrite suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local interview-history summaries and capability radar chart text when the user requests progress tracking.] <br>

## Skill Version(s): <br>
5.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
