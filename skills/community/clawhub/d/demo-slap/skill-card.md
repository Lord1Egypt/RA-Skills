## Description: <br>
Generate CS2 highlights and fragmovies from demos using the Demo-Slap API, with optional Leetify integration and Demo-Slap match history fallback to select recent matches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Damirikys](https://clawhub.ai/user/Damirikys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
CS2 players, creators, and operators use this skill to find recent matches, analyze demos, select highlights, and render MP4 clips or fragmovies through Demo-Slap, with optional Leetify-backed match discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends match or demo data to Demo-Slap and may use Leetify for match discovery. <br>
Mitigation: Use it only when sharing that match or demo data with those services is acceptable. <br>
Risk: Runtime state can include API-adjacent workflow data such as chat IDs and clip URLs. <br>
Mitigation: Review or clear the skill data directory after use, especially in shared environments. <br>
Risk: The workflow requires a Demo-Slap API key and may optionally use a Leetify API key. <br>
Mitigation: Provide keys through the expected environment variables and avoid storing credentials in shared local configuration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Damirikys/demo-slap) <br>
- [Demo-Slap API documentation](https://api-doc.demo-slap.net/) <br>
- [Demo-Slap API](https://api.demo-slap.net) <br>
- [Leetify public API](https://api-public.cs-prod.leetify.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status or highlight data from helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce external clip URLs after Demo-Slap analysis or rendering completes.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
