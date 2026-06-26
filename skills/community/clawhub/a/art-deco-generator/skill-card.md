## Description: <br>
Art Deco Generator helps agents create 1920s-inspired art deco images such as posters, invitations, branding concepts, geometric patterns, and vintage glamour illustrations through the Neta/TalesOfAI image API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, designers, and developers use this skill to generate art deco image concepts from text prompts, with optional size selection and reference-image style inheritance. It is useful for visual ideation around posters, invitations, wall art, branding, and 1920s-inspired design assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference image IDs, and the API token are sent to api.talesofai.com. <br>
Mitigation: Avoid confidential prompts and sensitive internal asset IDs, and use the service only when sharing this data with the external provider is acceptable. <br>
Risk: Passing the API token on the command line can expose it through shell history or process metadata. <br>
Mitigation: Use a low-privilege or temporary token and rotate it if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/blammectrappora/art-deco-generator) <br>
- [Neta API token setup](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text image URL returned by a command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta/TalesOfAI API token; supports portrait, landscape, square, and tall image sizes plus optional reference image UUIDs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
