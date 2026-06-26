## Description: <br>
Create presentations, documents, social posts, and web pages through the Gamma.app API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[autosolutionsai-didac](https://clawhub.ai/user/autosolutionsai-didac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and content teams use this skill to call Gamma.app from an agent workflow when creating decks, documents, social posts, web pages, or exports from prompts and templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted prompt text can execute local Python before the Gamma API call. <br>
Mitigation: Install only after the script builds JSON from arguments or stdin safely instead of interpolating text into Python source. <br>
Risk: The Gamma API key and prompt content are sent to Gamma's servers. <br>
Mitigation: Use a revocable Gamma API key and avoid sensitive prompts unless Gamma is approved for that data. <br>
Risk: Workspace or external sharing settings can broaden access to generated Gamma content. <br>
Mitigation: Enable workspace or external sharing only when broader access is explicitly intended. <br>


## Reference(s): <br>
- [Gamma homepage](https://gamma.app) <br>
- [Gamma API getting started](https://developers.gamma.app/docs/getting-started) <br>
- [Gamma API reference](references/api-reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/autosolutionsai-didac/gamma-app-api) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown with inline bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GAMMA_API_KEY plus curl and python3; generated Gamma URLs and export links are returned by the Gamma API.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
