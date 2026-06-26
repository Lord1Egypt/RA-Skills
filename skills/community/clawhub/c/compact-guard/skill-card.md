## Description: <br>
Compact Guard helps OpenClaw agents prepare for context compaction by scanning tool output, saving important details to memory, and producing a pre-compaction checklist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wavmson](https://clawhub.ai/user/wavmson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to preserve important conversation and tool-output details before context compaction. It is intended for sessions where the user wants a checklist and selected local memory notes before confirming compaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive conversation or tool-output details may be saved into local memory during pre-compaction. <br>
Mitigation: Avoid using the skill in sessions containing secrets, tokens, customer data, or confidential internal details unless the saved content is reviewed and redacted. <br>
Risk: Important or sensitive details may be preserved more broadly than intended. <br>
Mitigation: Review the generated checklist and memory entries before confirming context compaction. <br>


## Reference(s): <br>
- [Compact Guard release page](https://clawhub.ai/wavmson/compact-guard) <br>
- [wavmson publisher profile](https://clawhub.ai/user/wavmson) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown checklist with appended local memory notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts review before compaction and may save selected context details to local memory.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
