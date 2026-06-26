## Description: <br>
Generate ai action figure generator toy packaging images with AI via the Neta AI image generation API (free trial at neta.art/open). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomcarranzaem](https://clawhub.ai/user/tomcarranzaem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate action-figure toy packaging images from text prompts, optionally using size settings and a reference image ID for style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference image IDs, and the API token are sent to the Neta/TalesOfAI service. <br>
Mitigation: Install only if you trust the publisher and service, use a revocable low-privilege API token where possible, and avoid sensitive or proprietary prompt content or reference IDs. <br>
Risk: API tokens passed directly in shell commands can be exposed through shell history or process listings. <br>
Mitigation: Prefer safer secret handling, such as environment variables or a local secret manager, instead of literal command-line tokens. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tomcarranzaem/action-figure-skill) <br>
- [Neta API Access](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text image URL printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token and sends prompts, optional reference IDs, and generation requests to the Neta/TalesOfAI service.] <br>

## Skill Version(s): <br>
2.0.1 (source: server evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
