## Description: <br>
Generates user-friendly changelogs and release notes from local git commit history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and release managers use this skill to turn technical git commits into polished changelogs, release notes, app store descriptions, update announcements, and internal release summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated changelogs may expose private commit messages or details from style files if published without review. <br>
Mitigation: Run the skill in the intended repository and branch, then review the generated changelog before publishing. <br>
Risk: An incorrect date range or version range can omit relevant commits or include unintended changes. <br>
Mitigation: Specify the release range explicitly and compare the generated summary against the relevant commits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guohongbin-git/changelog-generator-cn) <br>
- [Publisher profile](https://clawhub.ai/user/guohongbin-git) <br>
- [Metadata homepage](https://clawhub.com/skills/changelog-generator-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown changelog or release notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated from the selected local git history and any supplied changelog style guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
