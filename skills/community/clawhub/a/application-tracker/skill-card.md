## Description: <br>
Start and review web form autofill workflow with human approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanghong5233](https://clawhub.ai/user/wanghong5233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Applicants and their agents use this skill to start a preview-first web application form autofill workflow, approve or reject pending fill threads, and review results before manual submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends profile data to a local service at 127.0.0.1:8010 for form preview and filling. <br>
Mitigation: Install only when the local service is trusted and provide the smallest necessary profile data. <br>
Risk: Autofill can place incorrect or stale information into external application forms. <br>
Mitigation: Review the preview before approving, reject stale or unexpected pending threads, and manually inspect the completed form before submitting it yourself. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown summaries with inline curl command templates and local API response details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit human approval before executing fill actions and manual review before form submission.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
