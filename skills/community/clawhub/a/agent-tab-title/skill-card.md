## Description: <br>
Patches a local OpenClaw Control UI installation so browser tab titles show the active agent name instead of the static OpenClaw Control title. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[symbolstar](https://clawhub.ai/user/symbolstar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users apply this skill when they run multiple Control UI tabs and need each browser tab to identify the active agent. It provides guidance and a local script for applying, removing, and reapplying the tab-title patch after OpenClaw updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script edits a local OpenClaw Control UI index.html file. <br>
Mitigation: Verify the target index.html path before running the script, review the patch, and keep the generated .bak file for rollback. <br>
Risk: OpenClaw updates may overwrite the patched Control UI files. <br>
Mitigation: Re-run the apply command after OpenClaw updates, or uninstall the patch from the backup if reverting to the static title is preferred. <br>


## Reference(s): <br>
- [ClawHub release: Agent Tab Title](https://clawhub.ai/symbolstar/agent-tab-title) <br>
- [OpenClaw upstream PR 80944](https://github.com/openclaw/openclaw/pull/80944) <br>
- [Agent Tab Title demo screenshot](https://raw.githubusercontent.com/SymbolStar/SymbolStar/main/assets/agent-tab-title-demo.png) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash commands and a bundled shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Applies or removes a local index.html patch and creates a .bak rollback file when applying.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
