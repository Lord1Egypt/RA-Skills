## Description: <br>
cn-content-remix helps agents transform Chinese source content into platform-native drafts for Xiaohongshu, Douyin, WeChat Official Account, Zhihu, Weibo, and WeChat Video, with platform-rule lookup and advertising-law compliance checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lm203688](https://clawhub.ai/user/lm203688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and agents use this skill to rewrite one Chinese content source into platform-specific drafts for major Chinese social platforms and to check wording against listed advertising-law and platform rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API-assisted checks may send submitted content or lookup details to an undocumented external service. <br>
Mitigation: Do not submit confidential, client, regulated, or unpublished business content unless the publisher documents data handling and the user accepts those terms. <br>
Risk: Generated compliance checks can miss legal or platform-policy issues. <br>
Mitigation: Review drafts and compliance notes before publishing, especially for advertising, medical, financial, education, or other regulated content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lm203688/cn-content-remix) <br>
- [Platform rules API endpoint](https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown sections with platform-specific drafts, compliance notes, hashtags, and distribution guidance; the included shell script returns plain-text platform-rule summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a remote API for platform-rule lookup and compliance assistance.] <br>

## Skill Version(s): <br>
2.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
