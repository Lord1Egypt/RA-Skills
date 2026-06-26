## Description: <br>
Generate polished HTML slide decks from a PowerPoint template, design screenshot, website style, or style prompt, then export 1440x900 slides as PDF using Puppeteer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[karinecsy-collab](https://clawhub.ai/user/karinecsy-collab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and business users use this skill to turn design references and source material into reviewed HTML slide decks and exported PDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or supplied HTML may reference external resources during browser rendering. <br>
Mitigation: Export only HTML that the user trusts, review generated HTML before PDF conversion, and run the workflow in a dedicated project folder. <br>
Risk: Dependency installation for Puppeteer or python-pptx can introduce normal package-management risk. <br>
Mitigation: Review npm and pip installation commands before running them and prefer an isolated project environment. <br>
Risk: Private, login-only, or inaccessible website URLs may fail or expose content that should not be fetched automatically. <br>
Mitigation: Prefer user-provided screenshots for private or access-controlled sites and confirm design choices before generating slides. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/karinecsy-collab/awesome-deck-pdf) <br>
- [Installation Guide](references/install.md) <br>
- [Export PDF Guide](references/export_pdf_guide.md) <br>
- [Design Template](references/DESIGN_TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with generated HTML, shell commands, and slide/PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a single-file HTML deck before PDF export; PDF output uses Puppeteer screenshot-and-compose.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
