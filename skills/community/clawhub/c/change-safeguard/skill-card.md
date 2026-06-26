## Description: <br>
Guides agents through impact analysis, confirmed edits, and post-change verification for workspace file, configuration, and script changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidongkl](https://clawhub.ai/user/weidongkl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when planning file moves, renames, deletions, configuration updates, or broad replacements. It helps the agent search for impact, present a checklist, wait for confirmation, edit item by item, and verify old references are cleared. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace edits can miss references or update the wrong files when impact analysis is skipped. <br>
Mitigation: Search scoped project files before editing, classify each result, and edit only from the confirmed checklist. <br>
Risk: A claimed refactor can appear complete while old references remain. <br>
Mitigation: Run a final search for old and new strings and summarize any residual matches before completion. <br>


## Reference(s): <br>
- [Change Safeguard on ClawHub](https://clawhub.ai/weidongkl/change-safeguard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with checklists, tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes impact analysis, confirmation checklist, edit summary, and grep-based verification guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
