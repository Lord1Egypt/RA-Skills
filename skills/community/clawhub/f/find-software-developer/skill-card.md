## Description: <br>
Find Software Developer helps agents find, shortlist, vet, and enrich US software development firms through the ServiceGraph pro_services API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nostrband](https://clawhub.ai/user/nostrband) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to locate US software development firms, translate buyer requirements into ServiceGraph filters, compare brief firm cards, and request credit-bearing enrichments after user approval. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The security scan marks the release suspicious and notes high-impact maintainer workflows. <br>
Mitigation: Install only if the publisher is trusted; review the skill before deployment and require explicit confirmation before moderation, publishing, production deploy, or account-impacting actions. <br>
Risk: The skill requires sensitive ServiceGraph credentials and may perform credit-bearing detail unlocks. <br>
Mitigation: Keep API keys out of chat and loaded through the local environment; confirm requested unlocks and expected credit use with the user before calling paid endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nostrband/find-software-developer) <br>
- [ServiceGraph API](https://api.servicegraph.co) <br>
- [Publisher profile](https://clawhub.ai/user/nostrband) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline API calls, filters, and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ServiceGraph bearer token for API access; detail unlocks can consume credits and should be confirmed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
