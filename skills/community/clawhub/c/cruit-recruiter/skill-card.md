## Description: <br>
Search Cruit for AI-native developers and reach out to them. Use when the user wants to recruit, source, find developers with specific skills or recency, install recruiter search, set up recruiting, reveal candidate contact info, or message a candidate through Cruit. Requires explicit confirmation before any credit-spending reveal or message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nwang783](https://clawhub.ai/user/nwang783) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters and hiring teams use this skill to search Cruit for AI-native developer candidates, translate hiring needs into structured filters, review low-PII candidate cards, and approve any contact reveal or message before spending credits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a local access token for Cruit recruiter access. <br>
Mitigation: Use user-only file permissions, install only if Cruit is trusted, and revoke or delete ~/.cruit/credentials.json when no longer using the service. <br>
Risk: The skill fetches current instructions from cruit.dev and contacts the Cruit API. <br>
Mitigation: Limit network activity to the documented Cruit URLs and avoid custom installer or instruction origins unless controlled by the user. <br>
Risk: Revealing contact information or sending candidate messages can spend contact credits and expose candidate information. <br>
Mitigation: Require explicit approval before each reveal or message, show exact message text before sending, and avoid batch reveal or batch send actions. <br>
Risk: Company context files may contain sensitive or unrelated information. <br>
Mitigation: Read only user-approved text-like company files and avoid secrets, environment files, credentials, customer lists, and unrelated source files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nwang783/cruit-recruiter) <br>
- [Cruit recruiter instructions](https://cruit.dev/skills/recruiter/INSTRUCTIONS.md) <br>
- [Cruit website](https://cruit.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with candidate summaries, setup prompts, shell commands, and JSON configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Cruit API calls, local user-level credentials, and explicit confirmation gates for contact-credit actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
