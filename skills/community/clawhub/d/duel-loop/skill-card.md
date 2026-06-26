## Description: <br>
Duel Loop coordinates isolated execution and QA subagents to draft, score, revise, and either approve or halt changes requested through an explicit QA workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dexzopiclone](https://clawhub.ai/user/dexzopiclone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill when they want an agent to handle rule, plan, protocol, policy, or review-document drafting through a separated execution-and-QA loop, with user review reserved for final acceptance or circuit-break decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow writes draft files and may land approved content into target production files. <br>
Mitigation: Confirm draft and target paths before use, and review the final diff before accepting production-file changes. <br>
Risk: Subagents receive task context and relevant file contents during drafting and QA. <br>
Mitigation: Pass only task-relevant excerpts and avoid sharing full conversation history or unrelated sensitive context. <br>
Risk: The automated revision loop can continue through multiple failed QA rounds. <br>
Mitigation: Use the documented five-round circuit breaker and require a user decision before continuing after repeated QA failures. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dexzopiclone/duel-loop) <br>
- [QA review prompt template](templates/qa-review-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown drafts and QA review reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Drafts are versioned under drafts/<name>-v<n>.md, and the loop halts after five failed QA rounds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
