## Description: <br>
Smart context compaction for OpenClaw agents that scans tool outputs, extracts valuable information into memory files, and generates a pre-compact checklist before /compact. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wavmson](https://clawhub.ai/user/wavmson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agent users use this skill before context compaction to preserve important facts, decisions, errors, preferences, and task progress in local memory notes. It helps generate a transparent pre-compaction checklist and prompts for confirmation before compression. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist broad conversation and tool-output details, including authentication-related information, to local memory files. <br>
Mitigation: Review what gets saved, avoid sessions containing raw secrets or tokens, and delete or redact memory files when needed. <br>
Risk: Unpinned clone or curl installation paths can bypass ClawHub package controls. <br>
Mitigation: Prefer installing the ClawHub package over unpinned GitHub curl or clone installation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wavmson/compact-test-a) <br>
- [Publisher profile](https://clawhub.ai/user/wavmson) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown checklist and appended local memory notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write summaries of conversation and tool-output details to local memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
