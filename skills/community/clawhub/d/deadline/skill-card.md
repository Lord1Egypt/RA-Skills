## Description: <br>
Deadline is an offline command-line assistant for tracking, managing, and exporting content creation entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and operators use Deadline to record drafts, edits, schedules, hashtags, hooks, calls to action, rewrites, translations, tone changes, headlines, and outlines from a local command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Drafts, schedules, translations, and other entered text are saved locally in plaintext under ~/.local/share/deadline/. <br>
Mitigation: Avoid entering secrets or confidential material, and review or delete the local data directory when needed. <br>
Risk: A different deadline command on the user's PATH could run instead of the reviewed script. <br>
Mitigation: Verify that the deadline command points to the reviewed script before relying on it. <br>


## Reference(s): <br>
- [ClawHub Deadline Skill Page](https://clawhub.ai/xueyetianya/deadline) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Command-line text with optional JSON, CSV, or plain-text export files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores history and exported files locally under ~/.local/share/deadline/.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
