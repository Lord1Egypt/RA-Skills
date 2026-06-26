## Description: <br>
Analyze and safely identify junk, duplicates, storage usage, timeline recaps, and quality scores to help organize and clean Apple Photos libraries on macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[and3rn3t](https://clawhub.ai/user/and3rn3t) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to inspect Apple Photos libraries on macOS, identify cleanup or export candidates, and generate summaries before taking manual or confirmed cleanup actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads sensitive local Apple Photos metadata, including names, faces, places, filenames, dates, and favorites. <br>
Mitigation: Install only when this local metadata access is acceptable, and review generated outputs before sharing them outside the device. <br>
Risk: Cleanup actions can move selected items to Recently Deleted when the cleanup executor is run with --execute. <br>
Mitigation: Run preview or plan-only modes first, inspect the exact candidates, and use --execute only after confirming the intended items. <br>
Risk: Database schema differences, Photos.app state, or AppleScript behavior can make analysis or cleanup results incomplete or unexpected. <br>
Mitigation: Check script output for warnings, keep Photos.app state in mind, and verify important cleanup or export plans in Photos.app before acting. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/and3rn3t/apple-photos-cleaner) <br>
- [README](README.md) <br>
- [Apple Photos database schema reference](references/database-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON or human-readable script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts default to JSON output and can write JSON files when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
