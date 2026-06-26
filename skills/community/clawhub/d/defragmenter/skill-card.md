## Description: <br>
Defragmenter provides structural knowledge defragmentation for OpenClaw workspaces by finding information, rules, and operational facts spread across the wrong files or embedded in the wrong layer, then rewriting them into proper files without deleting source material. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[balukov](https://clawhub.ai/user/balukov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace maintainers use this skill to find operational facts, preferences, and workflow rules that are scattered across an OpenClaw workspace and propose moving or copying them into the correct source-of-truth files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can copy workspace notes, preferences, or operational facts into persistent files, which could preserve secrets or private personal information if approved carelessly. <br>
Mitigation: Review the dry-run carefully, approve only narrow useful changes, and avoid copying secrets, credentials, or private personal information into long-lived memory files. <br>
Risk: Incorrectly reorganized knowledge could make a workspace source of truth misleading. <br>
Mitigation: Use the required dry-run report and explicit confirmation step to inspect proposed file targets and content before any write occurs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/balukov/defragmenter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Files] <br>
**Output Format:** [Markdown dry-run report followed by confirmation report after approved file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run by default; writes are limited to approved workspace knowledge files after user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
