## Description: <br>
AI-assisted pull request analysis companion that reviews GitHub PR changes, identifies scope, technical debt, code quality risks, and test coverage gaps, then produces a structured review report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering leads use this skill to analyze GitHub pull requests, focus review attention on risky changes, and generate a structured review report for team collaboration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PR-derived analysis may be published to Feishu and expose private code details beyond the intended audience. <br>
Mitigation: Confirm the Feishu document destination and access controls before publishing reports for private or security-sensitive repositories. <br>
Risk: Reports can include secrets or proprietary details present in PR metadata or diffs. <br>
Mitigation: Review generated reports before sharing and avoid publishing sensitive content outside the intended team. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/ai-pr-analysis-companion) <br>
- [README.md](artifact/README.md) <br>
- [workflow.json](artifact/workflow.json) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Structured Markdown review report with risk ratings and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish PR-derived findings to Feishu when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and workflow.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
