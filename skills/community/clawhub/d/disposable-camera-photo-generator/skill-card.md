## Description: <br>
Generate authentic disposable camera photos with harsh flash, film grain, light leaks, date stamps, and a nostalgic Y2K snapshot aesthetic via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate disposable-camera-style images from text prompts, optionally selecting output size and a reference image UUID for style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference image UUIDs, and API tokens are sent to the external Neta/TalesOfAI service. <br>
Mitigation: Use the skill only when the service is trusted for the prompt content and avoid sending sensitive text or private identifiers. <br>
Risk: Passing the API token with the documented --token flag can expose the secret through shell history or process listings. <br>
Mitigation: Run on a private machine, keep command histories protected, and rotate the token if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/disposable-camera-photo-generator) <br>
- [Publisher profile](https://clawhub.ai/user/blammectrappora) <br>
- [Neta API access](https://www.neta.art/open/) <br>
- [TalesOfAI image generation endpoint](https://api.talesofai.com/v3/make_image) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text] <br>
**Output Format:** [Plain text image URL printed to stdout, with status messages on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Neta API token; supports square, portrait, landscape, and tall image sizes plus an optional reference image UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
