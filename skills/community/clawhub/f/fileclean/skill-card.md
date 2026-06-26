## Description: <br>
Removes dates, hashes, UUIDs, and extra symbols from filenames to create clean, readable file names. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other local command-line users use Fileclean to preview and optionally apply filename cleanup across files or shallow directory contents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Direct renaming can change local filenames in a way that is hard to undo. <br>
Mitigation: Preview changes before using --rename and try it first on a small or backed-up folder. <br>
Risk: Different source files may clean to the same target filename. <br>
Mitigation: Review planned changes for filename collisions before applying renames. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/fileclean) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command-line preview and rename status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preview mode is the default; direct file renaming requires the --rename option.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
