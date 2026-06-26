## Description: <br>
Run a weekly token-optimization audit for durable instruction files in any OpenClaw workspace, generate a markdown report, and propose approval-gated cleanup actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyylin](https://clawhub.ai/user/andyylin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to review durable workspace instruction files for token-heavy content, stale markers, and cleanup candidates while preserving a required approval step before edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads durable workspace instruction files that may contain sensitive project or user context. <br>
Mitigation: Run it only in workspaces where local review of those files is acceptable, and inspect the generated report before sharing it outside the workspace. <br>
Risk: Cleanup proposals may remove useful instructions if accepted without review. <br>
Mitigation: Approve deletions or edits only after checking the specific content proposed for removal, and apply cleanup in explicit batches. <br>
Risk: The generated report records the scanned root path and findings about missing, stale, or large files. <br>
Mitigation: Treat reports as workspace-local review artifacts unless their contents have been checked for sensitive paths or context. <br>


## Reference(s): <br>
- [Publish Safety Notes](references/publish-safety.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/andyylin/durable-files-weekly-review-public) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with concise chat guidance and optional shell command invocation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates a dated local report and an approval queue for proposed removals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and RELEASE.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
