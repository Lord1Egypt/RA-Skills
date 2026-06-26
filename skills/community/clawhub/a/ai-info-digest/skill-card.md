## Description: <br>
Summarizes recent WeChat public-account articles from configured sources into a themed digest with source citations and account-level value notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinntrance](https://clawhub.ai/user/jinntrance) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People monitoring Chinese AI and technology publishers use this skill to collect recent articles from a configured WeChat-account list, read available mirrored sources, and produce a topical digest with citations and account-value assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow browses Zhihu, publisher websites, and search results for configured accounts. <br>
Mitigation: Confirm the source list and date range before running vague reading-summary requests. <br>
Risk: The workflow may save a markdown digest under the user's Documents folder. <br>
Mitigation: Ask the agent to skip saving or provide a different output path when local persistence is not desired. <br>
Risk: Some sources may require login, trigger access restrictions, or present anti-automation checks. <br>
Mitigation: Stop collection for those sources and ask for user guidance or manual intervention instead of bypassing access controls. <br>


## Reference(s): <br>
- [AI Info Digest ClawHub release](https://clawhub.ai/jinntrance/ai-info-digest) <br>
- [Configured WeChat account sources](artifact/wechat-accounts.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown digest shown in chat and saved as a .md file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source links, topic groupings, an account performance table, and notes for unavailable sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
