## Description: <br>
Helps an agent perform controlled Windows C-drive cleanup by scanning only approved temporary, cache, log, and WPS cache directories, asking for user confirmation before deletion, and producing a Markdown cleanup log. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanyvo](https://clawhub.ai/user/wanyvo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Windows users and support agents use this skill when a user explicitly wants to free C-drive space through whitelist-only cleanup with per-directory explanations, confirmations, dry-run support, and auditable Markdown logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup actions can remove unexpected temporary or cache data if the user approves an unexpected path. <br>
Mitigation: Run DryRun first, review each directory prompt, and approve deletion only when the path is expected. <br>
Risk: The referenced PowerShell cleanup script was not included in the submitted artifact evidence. <br>
Mitigation: Inspect the script from the release source before running it, especially before using ExecutionPolicy Bypass. <br>


## Reference(s): <br>
- [Safety boundaries](references/safety.md) <br>
- [ClawHub release page](https://clawhub.ai/wanyvo/c-drive-safe-cleanup-skill) <br>
- [Publisher profile](https://clawhub.ai/user/wanyvo) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown with inline PowerShell commands and cleanup-log structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports DryRun guidance, per-directory confirmation prompts, and a Markdown cleanup log path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
