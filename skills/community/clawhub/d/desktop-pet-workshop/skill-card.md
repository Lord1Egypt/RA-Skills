## Description:

Transforms user photos into interactive desktop pets with subject detection, background removal, cute restyling, multiple animated actions, interaction rules, and a ready-to-install Electron desktop application.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haixuma](https://clawhub.ai/user/haixuma)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and creators use this skill to convert a source image into desktop-pet assets, interaction guidance, and an installable Windows or macOS desktop pet package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The build process downloads npm packages and uses an Electron template to create local installers.

Mitigation: Pin dependencies, add a lockfile, prefer npm ci, review the generated template, and run packaging in a disposable least-privilege environment before sharing installers.

Risk: The workflow sends user-provided images to ImageGen for background removal, restyling, and animation asset generation.

Mitigation: Use the skill only with images the user is comfortable processing through ImageGen and avoid sensitive or restricted content.

## Reference(s):

- [Default actions reference](references/default_actions.md)
- [Project homepage](https://github.com/HaixuMa/desktop-pet-workshop)
- [ClawHub skill page](https://clawhub.ai/haixuma/skills/desktop-pet-workshop)
- [Publisher profile](https://clawhub.ai/user/haixuma)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also produce image assets and platform-specific installer files when the required ImageGen, Node.js, Electron, and operating-system build environment are available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
