## Description: <br>
Convert PPTX files, screenshots, website URLs, or style keywords into a polished HTML slide deck with user-approved design and content, then export it as a high-quality PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[karinecsy-collab](https://clawhub.ai/user/karinecsy-collab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and presentation authors use this skill to turn design references or style prompts into a structured HTML slide deck and export it as a pixel-accurate 1440x900 PDF after reviewing the design and slide outline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or user-provided HTML is rendered in a browser during PDF export. <br>
Mitigation: Use trusted or agent-generated HTML and review the slide HTML before running the Puppeteer export. <br>
Risk: The workflow may require npm, pip, or system package installation for Puppeteer, Chrome, or python-pptx. <br>
Mitigation: Review dependency installation commands before execution and prefer a controlled or disposable project environment. <br>
Risk: PDF export creates and removes temporary files while producing the final deck output. <br>
Mitigation: Run the skill in a disposable project directory and inspect generated files before sharing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/karinecsy-collab/awesome-deck-pdf-check) <br>
- [Publisher Profile](https://clawhub.ai/user/karinecsy-collab) <br>
- [DESIGN_TEMPLATE.md](references/DESIGN_TEMPLATE.md) <br>
- [export_pdf_guide.md](references/export_pdf_guide.md) <br>
- [install.md](references/install.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline code blocks, generated HTML files, and PDF export commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates a single-file HTML slide deck and uses Puppeteer screenshot-and-compose to produce a 1440x900 PDF.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
