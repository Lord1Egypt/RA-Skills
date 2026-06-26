## Description: <br>
Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zarazhangrui](https://clawhub.ai/user/zarazhangrui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, presenters, and non-designers use this skill to create distinctive browser-based slide decks, convert PowerPoint files to web presentations, and enhance existing HTML presentations with responsive layout, motion, and style guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated decks and extracted PPTX assets may persist confidential presentation content in local files or browser localStorage when inline editing is enabled. <br>
Mitigation: For confidential presentations, skip inline editing when possible and deliberately preserve or delete generated files, extracted assets, and local browser data after use. <br>
Risk: Generated presentations may load remote font resources, which can disclose network activity and may be unsuitable for restricted environments. <br>
Mitigation: Ask the agent to avoid remote font links or replace them with approved local fonts before opening or distributing the deck. <br>
Risk: Opening generated HTML from untrusted source content can expose users to unwanted browser behavior. <br>
Mitigation: Review generated HTML before opening it when the source content is untrusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zarazhangrui/frontend-presentations) <br>
- [Publisher profile](https://clawhub.ai/user/zarazhangrui) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, JSON extraction data, and shell commands as needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces zero-dependency, self-contained HTML slide files and may extract PPTX assets into local files during conversion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
