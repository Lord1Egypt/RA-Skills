## Description: <br>
AI tool that generates structured news digests from Twitter and RSS feeds with summaries available in 4-hour, daily, weekly, or monthly formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ma-star](https://clawhub.ai/user/Ma-star) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and teams use Clawfeed to run or self-host an AI news digest service that curates Twitter, RSS, and other feeds into periodic summaries, feeds, bookmarks, and dashboard views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports real-looking staging credentials and advises review before use. <br>
Mitigation: Rotate any staging key that may be real, set a deployment-specific API_KEY and secrets, and avoid public exposure without access controls. <br>
Risk: Remote or shared test defaults may affect non-isolated data or services. <br>
Mitigation: Run tests only against an isolated local database and API URL. <br>
Risk: Feedback can optionally be forwarded to Lark when FEEDBACK_LARK_WEBHOOK is enabled. <br>
Mitigation: Enable the webhook only when users are clearly informed that feedback details may be sent to Lark. <br>
Risk: Write APIs and authenticated features require correct access-control configuration. <br>
Mitigation: Review API key, OAuth, session secret, CORS, and reverse-proxy settings before enabling write or personal features. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ma-star/clawfeed-3) <br>
- [README](README.md) <br>
- [Skill entry documentation](SKILL.md) <br>
- [Product design](docs/PRODUCT.md) <br>
- [Architecture](docs/ARCHITECTURE.md) <br>
- [Testing guide](docs/TESTING.md) <br>
- [Staging notes](docs/STAGING.md) <br>
- [Digest prompt template](templates/digest-prompt.md) <br>
- [Curation rules template](templates/curation-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration values, API descriptions, and template text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce setup guidance, digest and curation templates, API usage examples, and deployment configuration notes.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact package.json and CHANGELOG report 0.8.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
