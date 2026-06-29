## Description: <br>
AI PR Narrative Factory analyzes GitHub pull request changes and produces human-readable changelog entries, technical explanations, and team synchronization reports for Feishu publication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to turn GitHub PR URLs, PR numbers, or release ranges into structured change narratives for code review follow-up, release notes, product communication, and team knowledge capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pull request metadata, diffs, summaries, file lists, and change analysis may be shared through configured GitHub, AI, and Feishu services. <br>
Mitigation: Use the skill only when organization policy permits those services for the target repository, and confirm provider data handling for private or sensitive repositories. <br>
Risk: Automatically published Feishu documents may expose code-derived information to unintended readers. <br>
Mitigation: Review Feishu document permissions and the generated report before sharing links outside the intended audience. <br>


## Reference(s): <br>
- [Keep a Changelog](https://keepachangelog.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured report content, markdown changelog entries, summary text, and a Feishu document URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include executive summaries, technical and non-technical narratives, changelog entries, team communication text, test notes, and migration guidance when breaking changes are detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and workflow.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
