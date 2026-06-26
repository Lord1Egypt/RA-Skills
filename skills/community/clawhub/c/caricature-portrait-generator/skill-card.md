## Description: <br>
Generate caricature, cartoon, comic, or funny face portraits from text descriptions using the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate humorous caricature-style portrait image URLs from text prompts, with optional size selection and reference-image style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference image IDs, and the API token are sent to the Neta/TalesOfAI service. <br>
Mitigation: Avoid confidential or sensitive personal descriptions and use the service only for content appropriate to share with that provider. <br>
Risk: Passing a secret with --token can expose it in shell history or process listings on shared systems. <br>
Mitigation: Prefer a short-lived or rotated token and avoid running the command where other users can inspect command history or processes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/caricature-portrait-generator) <br>
- [Neta API token access](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text image URL and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token; supports portrait, landscape, square, and tall image sizes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
