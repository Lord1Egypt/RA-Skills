## Description: <br>
fairygui-tools helps agents analyze FairyGUI projects, create UI mockup images and white-box XML prototypes from screenshots or natural language, and produce package structures that can be imported into the FairyGUI editor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slinkz](https://clawhub.ai/user/slinkz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and UI designers use this skill to analyze FairyGUI UI structures, discuss XML layouts, generate prototype imagery, and produce validated white-box FairyGUI project files for editor import. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated FairyGUI XML or UI mockups may not match the intended design or local project conventions. <br>
Mitigation: Review generated XML and images before importing them into FairyGUI, and run the bundled validator on a dedicated output directory. <br>
Risk: The full workflow may run local file generation, the bundled Python validator, and may require Puppeteer. <br>
Mitigation: Install and use the skill only in an environment where local file creation and validator execution are expected. <br>


## Reference(s): <br>
- [FairyGUI XML Specification](artifact/references/fairygui-xml-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with XML, HTML/CSS, Python command snippets, and generated file-tree descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local HTML/CSS mockups, screenshot images, FairyGUI XML package files, and validator output.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
