## Description: <br>
Count words, characters, sentences, paragraphs, and reading time for any text using AceToolz. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[acetoolz](https://clawhub.ai/user/acetoolz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to send text to the AceToolz word-counter API and receive word, character, sentence, paragraph, and reading-time statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text analyzed by the skill may be sent to the external AceToolz API without clear disclosure of consent, privacy, or retention terms. <br>
Mitigation: Avoid using the skill for secrets, private documents, regulated data, or proprietary material unless the publisher provides explicit upload disclosure, consent, and privacy or retention details. <br>
Risk: The external API can be unreachable or rate limited, which may prevent the skill from returning counts. <br>
Mitigation: Surface the failure to the user and suggest retrying later or using the AceToolz website directly. <br>


## Reference(s): <br>
- [AceToolz Word Counter](https://www.acetoolz.com/text/tools/word-counter) <br>
- [AceToolz Word Counter API](https://www.acetoolz.com/api/openclaw/word-counter) <br>
- [ClawHub AceToolz Word Counter release page](https://clawhub.ai/acetoolz/acetoolz-word-counter) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Markdown, Guidance] <br>
**Output Format:** [Markdown summary with optional shell commands and JSON API response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends submitted text to an external AceToolz API; artifact behavior documents a 100,000-character text limit and a 30-requests-per-minute rate limit.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
