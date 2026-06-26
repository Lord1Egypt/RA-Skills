## Description: <br>
Automatically finds resume-matched jobs, presents candidates for approval, fills approved applications, drafts cover letters, answers screening questions, and logs application status through ResumeX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atharva-badgujar](https://clawhub.ai/user/atharva-badgujar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers use this skill to search for relevant job postings, compare matches against their ResumeX resume, and apply to selected jobs with guided browser automation after approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access ResumeX resume data and store sensitive answers such as salary, work authorization, demographic, or compliance-related fields locally. <br>
Mitigation: Keep RESUMEX_API_KEY in environment variables only, restrict or delete data/user_preferences.json, and avoid saving optional sensitive answers unless needed. <br>
Risk: The skill can submit applications and screening answers under the user's identity. <br>
Mitigation: Review the approval list, job details, cover letters, and screening answers before submission, and limit early runs with MAX_APPLICATIONS. <br>
Risk: Some job-board automation may require login or conflict with site expectations for manual submission. <br>
Mitigation: Treat LinkedIn Easy Apply and external redirects as manual-review flows unless the user explicitly chooses otherwise. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/atharva-badgujar/auto-job-applier) <br>
- [ResumeX Agent API](https://resumex.dev/api/v1/agent) <br>
- [ResumeX Privacy Policy](https://resumex.dev/privacy) <br>
- [Form Field Mappings Reference](references/form_field_mappings.md) <br>
- [Job Boards Reference](references/job_boards.md) <br>
- [Screening Questions Reference](references/screening_questions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, approval tables, command snippets, JSON helper output, and browser-action guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RESUMEX_API_KEY and may create local user preference data during application workflows.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
