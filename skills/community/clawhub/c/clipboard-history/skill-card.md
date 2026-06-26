## Description: <br>
Manages clipboard history by saving copied content locally so users can view, search, and restore recent clipboard entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retain a local clipboard history, then view, search, and restore recent copied content during everyday work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retain sensitive clipboard contents in a local history file. <br>
Mitigation: Treat the history file as sensitive storage, avoid copying passwords or tokens while it is active, and clear saved history regularly. <br>
Risk: Broad trigger phrases could expose saved clipboard data unexpectedly. <br>
Mitigation: Require explicit user confirmation before showing or restoring clipboard history, and prefer versions with clear opt-in and delete controls. <br>


## Reference(s): <br>
- [Clipboard History on ClawHub](https://clawhub.ai/534422530/clipboard-history) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text responses describing clipboard-history actions and results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May surface locally stored clipboard contents; no network use is claimed by the skill.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
