## Description: <br>
Trust verification for AI output: verify any document or code before you act on it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wmehobbs](https://clawhub.ai/user/wmehobbs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, auditors, and teams use this skill to submit selected documents, code, or URLs to GauntletScore for trust scoring, claim verification, code safety analysis, and certificate verification before acting on AI-generated output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected content or URLs may be sent to GauntletScore's cloud service. <br>
Mitigation: Redact secrets, credentials, personal data, and regulated or proprietary material unless approved, and review the privacy and terms before confidential use. <br>
Risk: The skill depends on an external API key and cloud service availability. <br>
Mitigation: Configure GAUNTLET_API_KEY only in approved environments and treat API results as advisory until reviewed for the intended use case. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wmehobbs/gauntletscore) <br>
- [GauntletScore Homepage](https://gauntletscore.com) <br>
- [GauntletScore API Documentation](https://gauntletscore.com/docs) <br>
- [GauntletScore API Base](https://api.gauntletscore.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP request examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GAUNTLET_API_KEY; selected documents, code, or URLs are sent to GauntletScore's cloud service unless using Sovereign Edition.] <br>

## Skill Version(s): <br>
5.1.5 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
