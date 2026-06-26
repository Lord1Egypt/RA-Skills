## Description: <br>
Log bKash, Nagad, Rocket, and cash transactions conversationally in Bengali or English, with weekly spending digests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sabbiramin113008](https://clawhub.ai/user/sabbiramin113008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users who track Bangladesh-focused expenses use this skill to log mobile money and cash transactions from conversational English, Bengali, or mixed-language messages and receive weekly spending summaries. <br>

### Deployment Geography for Use: <br>
Bangladesh and global Bangladeshi diaspora <br>

## Known Risks and Mitigations: <br>
Risk: Transaction messages and weekly spending statistics may be sent to Anthropic for parsing or digest generation. <br>
Mitigation: Use a dedicated limited API key, avoid highly sensitive notes, and only enable automatic weekly digests when the user intentionally wants them. <br>
Risk: The artifact makes local-storage privacy claims while still using external API calls for natural-language parsing and summaries. <br>
Mitigation: Tell users that local JSON storage does not prevent selected transaction content or summary statistics from being sent to Anthropic under their API key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sabbiramin113008/bkash-nagad-tracker) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/sabbiramin113008) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Plain text and Markdown with JSON records and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores transaction records locally as JSON and can generate scheduled weekly digest text.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
