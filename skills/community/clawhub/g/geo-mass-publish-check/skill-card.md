## Description: <br>
Checks GEO mass-publish task status, downloads ready fanwen and fangxie ZIP exports, reports local paths, and tells the user when imports are ready for Rongmeibao. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chameleon-nexus](https://clawhub.ai/user/chameleon-nexus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
GEO SaaS operators use this skill to check pending mass-publish exports, download ready ZIP packages to local storage, and receive status and path guidance for manual import into Rongmeibao. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a reusable GEO API key and contacts ai.gaobobo.cn. <br>
Mitigation: Use it only if the GEO SaaS endpoint and publisher are trusted, and store the API key in the documented local key file instead of pasting it into chat. <br>
Risk: The skill can automatically write downloaded ZIP exports to the user's machine and report local path hints back to the service. <br>
Mitigation: Run it only in an environment where writing to ~/.qclaw/geo-exports and sharing those local path hints with the service is acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chameleon-nexus/geo-mass-publish-check) <br>
- [GEO SaaS endpoint](https://ai.gaobobo.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown status summaries with local path hints and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download ZIP exports under ~/.qclaw/geo-exports and report local path hints back to the GEO service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
