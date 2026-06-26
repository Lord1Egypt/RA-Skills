## Description: <br>
Use the favicons Node.js library to generate multi-platform website icons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate favicon, PWA, mobile platform, and app icon assets from a source image for website or application releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script writes generated assets into the output directory selected by the user. <br>
Mitigation: Choose a dedicated output directory and review its contents before copying generated assets into an application. <br>
Risk: Generated manifest and HTML tag output may affect how browsers and platforms present the site or app. <br>
Mitigation: Review the generated manifest, browser configuration, and HTML tags before publishing them. <br>
Risk: The workflow depends on the npm favicons package being installed in the project environment. <br>
Mitigation: Install and use the dependency only in environments where that package is acceptable under the project's dependency policy. <br>


## Reference(s): <br>
- [Favicons Configuration Reference](references/config_reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/openlark/favicons) <br>
- [OpenLark Publisher Profile](https://clawhub.ai/user/openlark) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples; generated PNG, ICO, JSON, XML, and HTML tag files when the bundled script is run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a clear source image and a user-selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
