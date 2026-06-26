## Description: <br>
Fetch and summarize Medium Daily Digest emails from Gmail. Extracts article URLs, generates Freedium links to bypass paywalls, and provides article summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omnimahui](https://clawhub.ai/user/omnimahui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch the latest Medium Daily Digest from Gmail, extract article metadata, generate Freedium mirror links, and guide article summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Gmail IMAP access through mailbox credentials, which can expose mailbox data if the credential is misused. <br>
Mitigation: Use a revocable Gmail app password, prefer a dedicated or low-risk mailbox, and revoke the app password when the skill is no longer needed. <br>
Risk: Freedium mirror links and article summaries can expose article URLs and reading activity to a third-party mirror and may have terms-of-service implications. <br>
Mitigation: Review organizational policy before using Freedium links and avoid sending sensitive reading activity or private article URLs to the mirror. <br>


## Reference(s): <br>
- [Daily Medium on ClawHub](https://clawhub.ai/omnimahui/daily-medium) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python examples and JSON-like article metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns digest date, digest title, article title, author, original URL, and Freedium URL; defaults to a maximum of 15 articles.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
