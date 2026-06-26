## Description: <br>
Generate dark fantasy artwork, grimdark illustrations, and gothic horror scenes from text prompts via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and creative teams use this skill to generate dark fantasy, gothic horror, and grimdark concept art from short text prompts, with optional image sizing and reference-image style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and the user's Neta API token are sent to api.talesofai.com. <br>
Mitigation: Use an environment variable such as --token "$NETA_TOKEN" instead of typing raw tokens directly, and review the provider's terms, quota, and billing expectations before use. <br>
Risk: Generated image availability and completion depend on the Neta service, including moderation, quota, and polling behavior. <br>
Mitigation: Treat the returned URL as provider-hosted output, handle timeouts or failed tasks, and retry only after checking provider status or quota. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/dark-fantasy-art-generator) <br>
- [Neta API token page](https://www.neta.art/open/) <br>
- [Neta image generation endpoint](https://api.talesofai.com/v3/make_image) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands] <br>
**Output Format:** [Plain text image URL printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The command accepts a text prompt, required Neta API token, optional size preset, and optional reference image UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
