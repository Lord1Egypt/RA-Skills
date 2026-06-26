## Description: <br>
Use this skill when the user wants to extract a webpage's design language into a reusable HTML style reference file, including typography, colors, spacing, surfaces, components, states, themes, motion, code-block styles, background atmosphere, decorative motifs, and art direction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VintLin](https://clawhub.ai/user/VintLin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to analyze a target webpage and turn its visual language into reusable style references for future AI-generated pages. It is intended for style-system extraction rather than page cloning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill loads target webpages through browser automation, which can expose browsing context or page content during extraction. <br>
Mitigation: Run it only against trusted or intended pages, and avoid private authenticated pages unless that exposure is acceptable. <br>
Risk: Generated HTML style specimens may contain remote font imports or reusable page styling that should be reviewed before reuse. <br>
Mitigation: Review generated specimen files before publishing or incorporating them, and localize or remove remote font imports for offline or privacy-sensitive use. <br>
Risk: The skill writes extraction outputs to files, so incorrect paths could create unwanted artifacts. <br>
Mitigation: Keep output paths constrained to the skill's assets/theme directory as directed by the artifact workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/VintLin/extract-design) <br>
- [Extraction checklist](references/extraction-checklist.md) <br>
- [Style specimen template](references/style-specimen.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, HTML, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown extraction summary plus JSON style manifests and HTML style specimen files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are saved as named style manifest and style specimen files under the skill's assets/theme directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
