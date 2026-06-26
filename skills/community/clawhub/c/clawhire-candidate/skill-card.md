## Description: <br>
Helps a job seeker use ClawHire to build a candidate profile, search matching jobs, review matches, and communicate with recruiters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[box1d](https://clawhub.ai/user/box1d) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External job seekers use this skill as a ClawHire assistant for profile intake, resume extraction, job search, match review, and recruiter-facing profile activation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends sensitive resume and profile details to a remote ClawHire service. <br>
Mitigation: Use it only when comfortable sharing that data with ClawHire, confirm before uploading a full resume, and avoid sending unnecessary sensitive details. <br>
Risk: Profile activation can make candidate information visible to recruiters. <br>
Mitigation: Require explicit user confirmation before activating recruiter visibility. <br>
Risk: Notification state can be changed by marking notifications as read. <br>
Mitigation: Ask before marking notifications read and only do so after the user explicitly chooses that action. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/box1d/clawhire-candidate) <br>
- [ClawHire API base](https://metalink.cc/clawhire/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Guidance] <br>
**Output Format:** [Markdown conversation guidance with API request descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ClawHire API key and may relay resume or profile details to ClawHire.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
