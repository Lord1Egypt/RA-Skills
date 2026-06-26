## Description: <br>
Generates ghost portrait and spectral apparition images from text prompts using the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request ghost portraits, spectral apparition images, gothic horror portraits, and related social media or Halloween imagery from text prompts and optional reference image UUIDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference UUIDs, and the Neta API token are sent to api.talesofai.com. <br>
Mitigation: Avoid sensitive personal or confidential prompts and use a scoped or disposable API token where possible. <br>
Risk: Passing tokens on the command line can expose them through shell history or runtime process inspection. <br>
Mitigation: Treat command-line tokens as sensitive and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/blammectrappora/ghost-portrait-generator) <br>
- [Neta AI Open](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text] <br>
**Output Format:** [Plain text image URL printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token and optionally accepts a size preset and reference image UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
