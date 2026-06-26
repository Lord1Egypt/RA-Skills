## Description: <br>
AI-assisted local writing and tracking skill that filters Upwork job listings, drafts personalized proposals, tracks applications, and improves proposal hooks from reported outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DTTNpole-commits](https://clawhub.ai/user/DTTNpole-commits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Freelancers use this skill to evaluate pasted Upwork job listings, prioritize qualified opportunities, draft review-ready proposals, and maintain a local application history. It supports manual submission workflows and does not connect to Upwork or submit proposals automatically. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Upwork profile details, job data, proposal drafts, and outcomes in local files that may contain personal information. <br>
Mitigation: Keep the local skill files private, avoid committing them to public repositories, and do not store secrets in the profile, log, or proposal vault files. <br>
Risk: Generated proposals may contain inaccurate, overstated, or poorly matched claims if the profile, proof points, or job details are incomplete. <br>
Mitigation: Review and edit every proposal before manually submitting it on Upwork, and keep profile proof points and job criteria accurate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/DTTNpole-commits/ai-upwork-proposal-writing-job-tracking-system) <br>
- [README](artifact/README.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Pre-Apply Check Script](artifact/pre-apply-check.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, proposal drafts, job qualification summaries, local log entries, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft proposals are intended for user review and manual submission; application data and proposal history are stored in local skill files.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
