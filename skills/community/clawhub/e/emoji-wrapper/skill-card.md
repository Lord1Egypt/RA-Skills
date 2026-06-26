## Description: <br>
Wrapper skill for local-auto-emoji - intercepts messages with [markers] and sends emoji images <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wdkmail](https://clawhub.ai/user/wdkmail) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to process bracketed emoji markers in chat messages and return the corresponding text and emoji image responses. It is useful when a local-auto-emoji installation and emoji pack should be exposed through a wrapper skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically processes chat message text for bracketed emoji markers. <br>
Mitigation: Install it only when automatic marker replacement is desired for the target OpenClaw environment. <br>
Risk: The wrapper imports and runs the separate local-auto-emoji skill. <br>
Mitigation: Review and trust local-auto-emoji before deployment, and confirm its emoji pack behavior matches the intended use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wdkmail/emoji-wrapper) <br>
- [Publisher Profile](https://clawhub.ai/user/wdkmail) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Media instructions, Configuration] <br>
**Output Format:** [Text responses with MEDIA image instructions and YAML configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local-auto-emoji to be installed and working; uses fallback static emojis when no generated emoji pack is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release evidence, artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
