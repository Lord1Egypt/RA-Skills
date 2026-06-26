## Description: <br>
Generates Chinese marketing search terms, industry Q&A topics, GEO-optimized Q&A knowledge base prompts, and structured company information extraction prompts from company names, industries, and Word documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuyingkj-coder](https://clawhub.ai/user/shuyingkj-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, SEO, and business-content teams use this skill to generate Chinese search-term ideas, industry Q&A topics, and prompts for GEO-optimized knowledge bases or company profile extraction from Word documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Company documents or generated prompts may contain confidential business information, personal data, trade secrets, customer details, addresses, phone numbers, or regulated content before being pasted into an external AI service. <br>
Mitigation: Review and redact sensitive or regulated content before copying prompts or source material into Claude or any other external service. <br>
Risk: Generated Word files may overwrite existing files when the user chooses an output path. <br>
Mitigation: Choose output paths deliberately and keep backups or unique filenames for generated .docx files. <br>
Risk: Generated marketing and company-profile content may be inaccurate or overstate claims from the source document. <br>
Mitigation: Have a knowledgeable reviewer check generated Q&A, search terms, company facts, contact details, and claims before publication. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shuyingkj-coder/geo-optimization-cn) <br>
- [README](artifact/README.md) <br>
- [Quick reference](artifact/quickref.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, files] <br>
**Output Format:** [Plain text and Markdown prompts, with optional Word document output through python-docx.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and Q&A commands print text reports; document workflows print prompts for Claude and may convert saved Markdown to .docx files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
