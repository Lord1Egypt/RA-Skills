## Description: <br>
Dual-mode Twitter/X writing tool that analyzes an account's writing style, extracts a style DNA document, and composes tweets, threads, or X long-form posts through Felo SuperAgent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze public Twitter/X writing style and generate tweets, threads, or X long-form posts that follow a selected or extracted style. It is intended for Claude Code workflows that can call the required Felo companion skills and use a Felo API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may reuse and persist work into an existing private Felo LiveDoc without clear user confirmation or isolation. <br>
Mitigation: Create or select a dedicated LiveDoc for Twitter Writer work and avoid using the skill with LiveDocs or style-library data that contain sensitive content. <br>
Risk: The skill depends on companion Felo skills and a Felo API key, so generated content and style data may be sent to Felo services. <br>
Mitigation: Use only trusted companion skills, verify the Felo API key configuration, and limit input to data you are comfortable sending to Felo. <br>


## Reference(s): <br>
- [Felo Twitter Writer on ClawHub](https://clawhub.ai/wangzhiming1999/felo-twitter-writer) <br>
- [Felo Open Platform](https://openapi.felo.ai/docs/) <br>
- [Felo SuperAgent API](https://openapi.felo.ai/docs/api-reference/v2/superagent.html) <br>
- [Felo Skills Repository](https://github.com/Felo-Inc/felo-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Felo SuperAgent JSON responses and prints the returned answer text for tweet, thread, long-form post, or style analysis outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
