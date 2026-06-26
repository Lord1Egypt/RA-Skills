## Description: <br>
Creates template-based dress-up playable ads for mobile advertising platforms with customizable character, clothing, background, and CTA assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxnan](https://clawhub.ai/user/lxnan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and ad creative producers use this skill to generate customizable dress-up playable ad bundles from image assets for Mintegral and other mobile advertising platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated playable ads include a hardcoded app-store CTA destination that may not match the intended campaign. <br>
Mitigation: Review and edit window.install() and the DOWNLOAD NOW button destination in the generated index.html before publishing. <br>
Risk: The generator copies user-supplied assets into the output bundle. <br>
Mitigation: Run the generator only on trusted asset folders with normal image filenames, then review the generated bundle before distribution. <br>


## Reference(s): <br>
- [Dressup Playable Maker guide](references/guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/lxnan/dressup-playable-maker) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated HTML/JavaScript files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an output folder containing index.html, mraid.js, and copied assets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
