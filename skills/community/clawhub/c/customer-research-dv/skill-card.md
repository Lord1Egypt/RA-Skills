## Description: <br>
Customer Research & Validation helps agents validate product ideas by mining public forums, generating surveys and interview guides, scraping competitor reviews, and analyzing customer sentiment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, founders, and marketing teams use this skill to collect directional customer evidence before product or campaign work. It supports persona validation, pain-point discovery, competitor sentiment review, and interview preparation using public web sources and local research files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public web content and scrapes user-specified URLs, which can create terms-of-service or authorization issues. <br>
Mitigation: Confirm authorization and applicable site terms before scraping, prefer official APIs where available, and limit collection to the research purpose. <br>
Risk: Customer interviews, surveys, and forum research can collect unnecessary personal or financial details. <br>
Mitigation: Avoid collecting sensitive details unless required, revise confidentiality wording before real interviews, and anonymize or delete stored research files on a schedule. <br>
Risk: Local research outputs can persist beyond their useful life. <br>
Mitigation: Periodically delete or archive local research files and keep only data needed for validation decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/clawdiri-ai/customer-research-dv) <br>
- [README](artifact/README.md) <br>
- [Skill Documentation](artifact/SKILL.md) <br>
- [Quick Start](artifact/QUICKSTART.md) <br>
- [Examples](artifact/examples/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON files] <br>
**Output Format:** [Markdown guidance with shell commands plus JSON and Markdown research artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Research outputs are written to user-selected files or local data/research paths; results may include public web excerpts, sentiment summaries, persona validation findings, surveys, and interview scripts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
