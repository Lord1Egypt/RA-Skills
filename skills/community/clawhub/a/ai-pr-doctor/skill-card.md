## Description: <br>
AI PR Doctor orchestrates GitHub pull request review, automated fixes, test reruns, merge handling, and Feishu repair-report publication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and DevOps teams use this skill to triage GitHub pull requests, run multi-dimensional AI review, attempt routine fixes, rerun tests, and produce traceable repair reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change and merge GitHub pull requests without strong user approval gates. <br>
Mitigation: Install only for tightly controlled repositories, use least-privilege GitHub credentials, protected branches, required checks, and set auto_merge=false unless explicitly needed. <br>
Risk: The skill can publish repair reports to Feishu by default. <br>
Mitigation: Set notify_feishu=false unless publication is required, and confirm the target Feishu folder and sharing permissions before use. <br>
Risk: Scheduled or batch operation can broaden the effect of automated review, repair, merge, and publication actions. <br>
Mitigation: Avoid cron or batch mode until merge and publication controls are clearly bounded and trusted versions of referenced skills are in use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/ai-pr-doctor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, structured JSON workflow outputs, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feishu document URLs, GitHub pull request state, review summaries, issue counts, fixed-file counts, and test or merge results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and workflow.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
