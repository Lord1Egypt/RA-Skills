## Description: <br>
Generate chibi character generator ai images with AI via the Neta AI image generation API (free trial at neta.art/open). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomcarranzaem](https://clawhub.ai/user/tomcarranzaem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate chibi-style character images from text prompts through the Neta/TalesOfAI image API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and the Neta/TalesOfAI API token are sent to api.talesofai.com. <br>
Mitigation: Use a dedicated or low-privilege token and avoid sending confidential prompt content. <br>
Risk: Passing tokens directly on the command line can expose secrets through shell history or CI logs. <br>
Mitigation: Provide tokens through a controlled secret workflow and avoid logging command invocations that include credentials. <br>
Risk: Image generation depends on an external API and may fail, time out, or be moderated by that service. <br>
Mitigation: Handle nonzero exits and timeouts in downstream workflows, and review generated image URLs before reuse. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tomcarranzaem/chibi-gen-skill) <br>
- [Neta API Access](https://www.neta.art/open/) <br>
- [TalesOfAI Image Generation API Endpoint](https://api.talesofai.com/v3/make_image) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Plain text image URL printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta/TalesOfAI API token and accepts a text prompt, size option, and optional reference picture UUID.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
