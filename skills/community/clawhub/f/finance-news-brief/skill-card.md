## Description: <br>
Collects important global financial news from the past 24 hours and generates a Chinese briefing as Markdown and a formal PDF with a cover page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jihefanlan-art](https://clawhub.ai/user/jihefanlan-art) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to gather timely market news across macro policy, commodities, U.S. equities, Hong Kong equities, and A-shares, then produce a structured Chinese finance report. It is intended for briefing generation and includes a non-investment-advice risk notice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local code, install Python packages, and launch unsandboxed Chrome while generating reports. <br>
Mitigation: Run it in an isolated virtual environment or container and review dependency installation before allowing execution. <br>
Risk: Broad market-news prompts can trigger web searches, file writes, and PDF generation when the user may only want a short answer. <br>
Mitigation: Ask explicitly for a short answer when report files, web searches, or PDF output are not desired. <br>
Risk: Financial briefings may contain time-sensitive or incomplete market information. <br>
Mitigation: Review cited sources and keep the included non-investment-advice risk notice in user-facing reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jihefanlan-art/finance-news-brief) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files] <br>
**Output Format:** [Markdown report and PDF file, with source links and generated file paths reported to the user] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create finance_brief_YYYYMMDD.md, finance_brief_YYYYMMDD.pdf, and an intermediate HTML file in the current or user-specified directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
