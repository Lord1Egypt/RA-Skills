## Description: <br>
Review AI video production packages for creative consistency, asset provenance, platform metadata, disclosure wording, and publishing readiness before a human-controlled release. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, producers, and release reviewers use this skill to assess whether AI-generated video packages are ready for YouTube, TikTok, or short-form publication. It separates creative notes from release blockers across provenance, metadata, disclosures, copyright risk, audience settings, and public-facing wording. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The review could be mistaken for authorization to publish or operate a creator account. <br>
Mitigation: Keep publishing, scheduling, monetization, account access, credentials, cookies, and private analytics outside the workflow; require a human-controlled publish step. <br>
Risk: Client-facing copy could expose private production notes, local paths, private prompts, account names, or unredacted source-asset links. <br>
Mitigation: Review the public surface separately and remove private operational details before manual release. <br>
Risk: Video metadata may contain unresolved disclosure, attribution, affiliate, copyright, platform-policy, or audience-setting issues. <br>
Mitigation: Treat those issues as release blockers or verification items until a human reviewer confirms the required disclosures, rights, and platform settings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/agentic-video-production-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown readiness review with a release verdict] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Package, Creative, Policy, Public surface, Verification, and Verdict sections; verdict is one of ready, ready_with_notes, blocked, or do_not_publish.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
