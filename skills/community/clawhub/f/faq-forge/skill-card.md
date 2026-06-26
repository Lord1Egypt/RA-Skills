## Description: <br>
Build, maintain, and publish professional FAQ documentation for customer-facing knowledge bases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, support teams, and documentation maintainers use this skill to create, organize, import, and publish searchable FAQ content for products or services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool creates and changes FAQ data and published output files in the working directory. <br>
Mitigation: Run it in an intended project directory, keep backups or version control for FAQ data, and review generated files before publishing. <br>
Risk: Imported documentation or generated HTML may include inaccurate, private, or unsafe customer-facing content. <br>
Mitigation: Review imported content and generated HTML before publishing, especially when source documents are untrusted or contain private information. <br>
Risk: Adding third-party analytics or A/B testing later may introduce privacy and consent obligations. <br>
Mitigation: Update privacy notices and consent handling before enabling any additional tracking integrations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TheShadowRose/faq-forge) <br>
- [Publisher Profile](https://clawhub.ai/user/TheShadowRose) <br>
- [README](artifact/README.md) <br>
- [Quick Start](artifact/QUICKSTART.md) <br>
- [Limitations](artifact/LIMITATIONS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and generated FAQ files in HTML, Markdown, plain text, and JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Python scripts and local FAQ data files; no external runtime dependencies are documented.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
