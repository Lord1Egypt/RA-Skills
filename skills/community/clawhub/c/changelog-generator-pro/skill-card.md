## Description: <br>
Automatically creates user-facing changelogs from git commits by analyzing commit history, categorizing changes, and transforming technical commits into clear, customer-friendly release notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hsuyungfeng](https://clawhub.ai/user/hsuyungfeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, release managers, and product teams use this skill to turn git commit history into polished changelogs, release notes, app store update copy, and customer-facing product updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reviews repository git history, and commit messages can contain internal details that should not appear in public release notes. <br>
Mitigation: Install only where repository history can be reviewed by the agent, and review generated changelogs before publishing. <br>
Risk: Generated changelogs may be incomplete or misleading when commit messages are ambiguous, overly technical, or unrelated to user-facing changes. <br>
Mitigation: Compare the draft against the release scope and edit the final notes for accuracy, customer relevance, and omitted changes. <br>
Risk: Custom changelog guidelines or commit text can steer wording away from approved brand, legal, or support language. <br>
Mitigation: Use approved changelog guidance when available and have the release owner review public-facing language. <br>


## Reference(s): <br>
- [Changelog Generator Pro on ClawHub](https://clawhub.ai/hsuyungfeng/changelog-generator-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown release notes and concise prose guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May be scoped by date range, version range, or custom changelog guidelines; generated changelogs should be reviewed before publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
