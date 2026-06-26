## Description: <br>
BOSS Zhipin greeting generator that uses boss-cli to fetch target job details, compare role requirements with a user's resume, and draft a personalized greeting under 200 Chinese characters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bifang988](https://clawhub.ai/user/bifang988) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and recruiting assistants use this skill to inspect a BOSS Zhipin job posting, identify the strongest resume-to-role matches, and draft two concise outreach greeting options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The external boss-cli login flow may read browser cookies for a job-site account. <br>
Mitigation: Review and trust the kabi-boss-cli package before installation and prefer QR login over browser-cookie reuse when available. <br>
Risk: Resume content and job-search details may contain personal or sensitive information. <br>
Mitigation: Provide only the resume details needed to draft the greeting and avoid sharing unnecessary personal data. <br>
Risk: The skill could be mistaken for an automated application or messaging tool. <br>
Mitigation: Confirm it is only fetching job details and drafting text, and review any greeting before sending it manually. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bifang988/boss-greeting-message) <br>
- [Publisher profile](https://clawhub.ai/user/bifang988) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with job analysis, two greeting drafts, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Greeting drafts are constrained to two versions, each under 200 Chinese characters with a stated character count.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
