## Description: <br>
Reviews WeChat public-account articles before publication by checking sensitive words, typos, political and platform compliance, writing quality, AI-flavored prose signals, image markers, and required publishing elements, then outputs an actionable revision list. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiworkskills](https://clawhub.ai/user/aiworkskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External WeChat editors, self-media authors, and compliance reviewers use this skill to review draft articles before publication and receive a prioritized list of required and suggested fixes. It supports content review before formatting and final review before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that the skill under-discloses a finalization-time Python command from a neighboring aws-wechat-article-writing skill that edits draft files. <br>
Mitigation: Install the related skill suite only from a trusted source, review the sibling Python script before use, and run the skill only in the intended local article workspace. <br>
Risk: The skill can write article files and review records during its review and finalization workflow. <br>
Mitigation: Keep drafts under version control or backups, review proposed changes before finalization, and limit execution to the article workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiworkskills/aws-wechat-article-review) <br>
- [Publisher profile](https://clawhub.ai/user/aiworkskills) <br>
- [Declared project homepage](https://aiworkskills.cn) <br>
- [Declared source repository](https://github.com/aiworkskills/wechat-article-skills) <br>
- [Review checklist](references/checklist.md) <br>
- [Review output format](references/output-format.md) <br>
- [AI flavor check methodology](references/ai-flavor-check.md) <br>
- [AI flavor check samples](references/ai-flavor-check-samples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown review results, revision checklists, and local file or command instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write review records and finalized article files in the local article workspace after the required review flow completes.] <br>

## Skill Version(s): <br>
1.0.24 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
