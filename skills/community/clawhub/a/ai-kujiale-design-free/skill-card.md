## Description: <br>
Guides an agent through a Kujiale-based basic interior design workflow for text-based floor plan search, style selection, automated layout, and static rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and design-oriented agent operators use this skill to preview home decoration concepts by searching Kujiale floor plans, selecting styles, generating layouts, and producing static render images. It is intended for lightweight inspiration and pre-renovation previews, not advanced floor plan reconstruction or panoramic output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Kujiale access tokens may be exposed through configuration files, logs, or version control. <br>
Mitigation: Keep the access token out of version control and logs, restrict the config file permissions, and rotate the token if it is exposed. <br>
Risk: The skill uses command execution as part of the Kujiale workflow. <br>
Mitigation: Keep command use narrowly scoped to the documented Kujiale design generation commands and avoid unrelated shell commands or unrelated local files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ai-kujiale-design-free) <br>
- [Kujiale skills page](https://www.kujiale.com/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and links to generated static render images] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final output is expected in ./outputs/result.md with render images and design highlights.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
