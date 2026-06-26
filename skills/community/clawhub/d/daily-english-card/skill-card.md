## Description: <br>
Daily English Card generates a daily spoken-English scenario card image, sends it to WeChat, and archives it to an IMA knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryaction](https://clawhub.ai/user/jerryaction) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners and personal automation users use this skill to schedule recurring English speaking practice cards, send the generated image to WeChat, and keep an IMA archive of generated cards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence flags recurring WeChat delivery and IMA archival through fixed account details and local credential helpers. <br>
Mitigation: Replace the hard-coded WeChat target, account ID, IMA IDs, and credential helper paths with user-controlled values before enabling the cron job. <br>
Risk: The skill depends on local Python and Node scripts that are referenced but not bundled in the artifact. <br>
Mitigation: Inspect the referenced scripts, confirm what content is uploaded and retained, and verify how to pause or remove the daily cron job before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerryaction/daily-english-card) <br>
- [English card preview image](https://r2.image-upload.app/ptImg/4OOX6Lbi.jpeg) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands, JSON examples, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for generating an image card, sending it through WeChat, and handling IMA archival failures.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
