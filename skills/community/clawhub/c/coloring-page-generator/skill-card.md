## Description: <br>
AI coloring page generator that creates printable black and white coloring pages, adult coloring book pages, kids coloring sheets, mandala pages, animal pages, fantasy pages, and custom line art from text descriptions via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate printable coloring-page image outputs from a prompt, optionally selecting page dimensions or passing a reference image UUID for style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference image UUIDs, and the Neta API token are sent to a third-party Neta/TalesOfAI service. <br>
Mitigation: Avoid sensitive or confidential prompts and use this skill only when sharing that data with the remote service is acceptable. <br>
Risk: Passing the API token directly on the command line can expose it through shell history or local process inspection. <br>
Mitigation: Prefer shell practices that limit token exposure, such as using a temporary environment variable and avoiding persistent command history for token-bearing commands. <br>
Risk: Image generation depends on the availability, moderation behavior, and response format of the remote service. <br>
Mitigation: Review the returned image URL and generated content before using or distributing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/coloring-page-generator) <br>
- [Neta API token setup](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Plain text image URL with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs a direct generated-image URL after polling the remote image-generation task.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
