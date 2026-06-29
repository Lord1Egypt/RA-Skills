## Description: <br>
Rigorous workflow for producing long-form knowledge content with multi-agent collaboration, independent audit, machine-verifiable quality gates, and versioned errata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christianye](https://clawhub.ai/user/christianye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, researchers, and agent operators use this skill to plan, produce, audit, fix, publish, and maintain long-form knowledge products such as textbooks, knowledge bases, and deep reports. It is intended for projects large enough to benefit from explicit checkpoints, sub-agent coordination, machine checks, and changelog-driven revision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can add planning, audit, sub-agent, and publishing overhead when applied to broad long-form tasks. <br>
Mitigation: Use it for substantial knowledge products where that process is desired, and avoid it for one-off Q&A, short reports, simple documentation, or code projects. <br>
Risk: Machine checks can catch missing citations, duplicate citations, weak safety coverage, heading errors, and all-positive reviews, but they do not prove the final content is factually correct. <br>
Mitigation: Keep the independent audit step, review red and yellow findings before publishing, and re-run the audit after fixes to catch regressions. <br>


## Reference(s): <br>
- [Build Protocol on ClawHub](https://clawhub.ai/christianye/build-protocol) <br>
- [Workflow Checkpoints](artifact/references/workflow-checkpoints.md) <br>
- [Audit Script Template](artifact/references/audit-script-template.sh) <br>
- [Sub-agent Task Spec Examples](artifact/references/subagent-spec-examples.md) <br>
- [Supplements Knowledge Base Case Study](artifact/references/case-study-supplements.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command templates and checklist-style workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended to guide agent behavior and quality checks; generated deliverables may include long-form Markdown, audit reports, changelogs, and publishable documents.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
