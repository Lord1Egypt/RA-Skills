## Description: <br>
An AI-assisted international news reporting toolkit that guides agents through web-based source collection, multi-source verification, Markdown report drafting, and PDF generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YWWZZsgit](https://clawhub.ai/user/YWWZZsgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and AI agents use this skill to produce daily international news briefings by collecting current public sources, verifying facts across source tiers, drafting analysis in Markdown, and generating a PDF. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Current-news reports can contain stale, incomplete, or unverified information when search results lag or sources disagree. <br>
Mitigation: Use timestamped sources, prioritize Tier 1-2 references, cross-check critical facts, and review the final report before relying on it. <br>
Risk: Local Markdown and PDF generation writes report files and depends on the installed PDF library and runtime environment. <br>
Mitigation: Confirm input and output paths before execution, install reportlab from a trusted source, and inspect the generated PDF. <br>
Risk: The workflow is not intended to replace professional journalism or support real-time trading or other critical decisions by itself. <br>
Mitigation: Keep human review in the loop and treat generated analysis as briefing material rather than a sole source of truth. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Source Directory](references/source_directory.md) <br>
- [Daily Report Template](assets/templates/daily_report_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown reports, generated PDF files, and concise shell commands for PDF conversion.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AI agent with web search capability; final reports should include source tiers, timestamps, attribution, and review.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
