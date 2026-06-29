## Description: <br>
Generates an end-to-end enterprise brand asset package from requirements, including logo variants, SVG assets, PNG and ICO conversions, HTML handoff pages, brand guidelines, and validation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, founders, brand teams, and developers use this skill to transform company details and design preferences into a structured brand kit with logo systems, VI assets, favicon files, display pages, and handoff checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill generates and modifies brand asset files in a project directory. <br>
Mitigation: Run it only in the intended workspace and review generated SVG, PNG, ICO, and HTML outputs before use. <br>
Risk: Business contact details may be inserted into generated assets. <br>
Mitigation: Review company and personal contact information before generation and again in the final handoff package. <br>
Risk: Rendering uses an Edge executable selected from the environment. <br>
Mitigation: Use a trusted Edge installation when setting the EDGE environment variable. <br>
Risk: Cleanup commands may remove generated files if pointed at the wrong targets. <br>
Mitigation: Confirm cleanup and rm command targets are limited to generated brand asset files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangjiaocheng/skills/brand-kit) <br>
- [Publisher Profile](https://clawhub.ai/user/wangjiaocheng) <br>
- [Brand Kit Catalog](artifact/references/brand-kit-catalog.md) <br>
- [Brand Kit Requirements](artifact/references/brand-kit-requirements.md) <br>
- [Exemplars Index](artifact/references/exemplars.md) <br>
- [SVG Specification](http://www.w3.org/2000/svg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with SVG, HTML, Python, shell command, and generated asset file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce a full brand asset package of 87 files: 2 HTML, 33 SVG, 51 PNG, and 1 ICO.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
