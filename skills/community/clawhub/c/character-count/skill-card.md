## Description: <br>
Count string length deterministically for text with hard limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evandataforge](https://clawhub.ai/user/evandataforge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to verify that final posts, replies, captions, commit messages, or other text fit within a maximum character count before publication or saving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Platform character limits may use URL, Unicode, or token weighting rules that differ from Python string length. <br>
Mitigation: Use this skill as a deterministic local gate and add a platform-specific validator when exact enforcement matters. <br>
Risk: Text can change after counting, making the reported result stale. <br>
Mitigation: Count the exact final text immediately before posting or saving, including spaces, punctuation, hashtags, and URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evandataforge/character-count) <br>
- [Publisher profile](https://clawhub.ai/user/evandataforge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON object or plain text key-value lines, with Markdown guidance and shell command examples for agent use] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Counts Python string length, reports chars, limit, remaining, and ok status, and requires python3.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
