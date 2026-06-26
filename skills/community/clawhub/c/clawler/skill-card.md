## Description: <br>
Use when you want current web information through the Clawler OpenClaw plugin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxpetretta](https://clawhub.ai/user/maxpetretta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Clawler to configure an OpenClaw web-search plugin, select a search provider, manage provider credentials, and guide agents on when to call `search_web`. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may be sent to the configured provider and could expose sensitive information if secrets are included. <br>
Mitigation: Choose a trusted provider and avoid sending sensitive secrets in search queries. <br>
Risk: Unnecessary provider credentials can increase credential exposure. <br>
Mitigation: Configure only the API key needed for the selected provider. <br>
Risk: Changing tools.deny can replace the built-in web search behavior for the OpenClaw installation. <br>
Mitigation: Only change tools.deny when the operator intentionally wants Clawler to become the active search surface. <br>


## Reference(s): <br>
- [Clawler GitHub Repository](https://github.com/maxpetretta/clawler) <br>
- [Clawler on ClawHub](https://clawhub.ai/maxpetretta/clawler) <br>
- [Release Changelog](https://github.com/maxpetretta/clawler/compare/v2026.3.11-5...v2026.3.11-6) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JSON and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provider-specific search options may include freshness, locale, topic, and domain filters.] <br>

## Skill Version(s): <br>
2026.3.11-6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
