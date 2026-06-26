## Description: <br>
Automate your job search with Mokaru by searching listings, tracking applications, tailoring resumes, managing contacts, and maintaining career profile data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vndck](https://clawhub.ai/user/vndck) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External job seekers and career-management agents use this skill to find roles, save and update application records, tailor resumes, manage contacts, and keep career profile data current through the Mokaru API. The artifact states that it prepares application materials and tracking data but does not submit job applications on the user's behalf. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive job-search and career profile data through a Mokaru API key. <br>
Mitigation: Store MOKARU_API_KEY securely, avoid pasting it into chats or committing it to files, and install only when the user trusts Mokaru and the publisher. <br>
Risk: The skill can update, delete, export, or auto-tailor resumes, contacts, applications, profile, education, experience, and skills records. <br>
Mitigation: Require explicit user confirmation before any write, delete, export, or auto-tailoring action. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vndck/auto-apply) <br>
- [Mokaru API documentation](https://docs.mokaru.ai) <br>
- [Mokaru website](https://mokaru.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown responses with curl and jq examples, JSON API payloads, and optional exported resume files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MOKARU_API_KEY plus curl and jq; operations may read, create, update, delete, export, or tailor sensitive career data.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
