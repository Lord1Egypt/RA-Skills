## Description: <br>
Generate traditional Chinese ink painting and sumi-e style images from text prompts using the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate Chinese ink painting, sumi-e, and related East Asian brushwork images from short text descriptions. It is suited for creative assets such as wallpapers, prints, decor concepts, meditation art, cultural projects, and traditional aesthetic designs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference IDs, and the Neta API token are sent to api.talesofai.com. <br>
Mitigation: Use a low-privilege or trial token and avoid sending private or confidential material unless the provider is trusted. <br>
Risk: Putting reusable API tokens directly in shell commands can expose them through shell history or process listings. <br>
Mitigation: Prefer expanding a token from a local environment variable at invocation time and rotate tokens if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/chinese-ink-painting-generator) <br>
- [Neta API token setup](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text] <br>
**Output Format:** [Plain text image URL with progress and error messages on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token, a prompt, optional size selection, and optional reference image UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
